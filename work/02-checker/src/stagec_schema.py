"""Stage-C certificate schema v1-draft: canonical binary + canonical text + validator.

Reconciles the two accepted designs --
  A = work/02-checker/reports/H0-stageC-criterion.md sec.5  (per-record text, evidence list)
  B = work/02-checker/reports/H0-stageC-search-controls.md sec.3 (one archive, manifest,
      binary record stream, ball layer, adjacency bitsets, six-value verdict)
into one format whose authority order is: manifest (global pinning) > per-record facts >
optional caches.  Money quotes for every decision are in H0-stageC-schema.md.

Units and conventions (fixed by this module, not by the producer):
  * every integer and double is little-endian; doubles are IEEE-754 binary64 bit patterns;
  * -0.0 is canonicalised to +0.0 and NaN is forbidden in every double field;
  * a ball list is sorted by the IEEE totalOrder key of (v0..v5, s) and must be duplicate-free;
  * exclusions are addressed by ball index in that order and are stored as a per-pair bitmap
    (2 bits: relation O then U) followed by one 4-bit rule code per set bit, pairs ascending,
    O before U;
  * adjacency (if present) is indexed by the same ball order, row i word w bit b = ball 64w+b,
    diagonal zero, symmetric, every bit >= n_balls zero.
"""
import json, struct, hashlib, math

MAGIC = b'SCV1STAG'
VERSION = (1, 0)
SHARD_HDR = 80
REC_HDR = 64
MAXK = 10          # stageC.cpp readRecords: r.k>maxK aborts
BALL_CAP = 2048    # cluster() ball cap and BS::L*64
BIN_CAP = 2000000  # Layer::binCap
CAP_MIN, CAP_MAX = 100, 1000000000   # stageC.cpp main() argument validation

# verdict codes -----------------------------------------------------------------
V_NEG, V_EMPTY, V_POS, V_CAP, V_OVER, V_CLUSTER, V_INTERNAL = range(1, 8)
VERDICT_NAME = {V_NEG: 'NEG', V_EMPTY: 'EMPTY_BINS', V_POS: 'POS', V_CAP: 'CAP',
                V_OVER: 'OVERFLOW', V_CLUSTER: 'CLUSTER_FAIL', V_INTERNAL: 'INTERNAL'}
EXCLUDED = frozenset((V_NEG, V_EMPTY))
UNRESOLVED = frozenset((V_POS, V_CAP, V_OVER, V_CLUSTER, V_INTERNAL))

# separation-rule codes (4 bits) ------------------------------------------------
R_O_616, R_U_616, R_O_620, R_U_621, R_O_623, R_U_623 = range(6)
RULE_NAME = {0: '6.16/O', 1: '6.16/U', 2: '6.20/O', 3: '6.21/U', 4: '6.23/O', 5: '6.23/U'}
RULE_REL = {0: 'O', 1: 'U', 2: 'O', 3: 'U', 4: 'O', 5: 'U'}
N_RULES = 6

M_RECOMPUTE, M_WITNESS = 0, 1        # evidence mode
K_BODY, K_REF = 1, 2                 # stage-B record: inline or by reference
C_RECLUSTER, C_BINSET, C_BOXCERT = 0, 1, 2   # cover mode; only 0 and 1 defined in v1

FLAG_ADJ = 1                         # adjacency block present
FLAG_BALLS = 2                       # ball list present in mode RECOMPUTE (a hint)
FLAG_Y = 4                           # reserved: stored joint-test y; must be 0 in v1
NO_PARENT = 0xFFFFFFFF

class SchemaError(Exception):
    def __init__(self, code, detail=''):
        Exception.__init__(self, '%s: %s' % (code, detail))
        self.code = code
        self.detail = detail

def fail(code, detail=''):
    raise SchemaError(code, detail)

# ---------------------------------------------------------------- double handling
_MASK = (1 << 64) - 1
def tot_key(x):
    """Monotone unsigned key of a finite double's bit pattern (IEEE totalOrder order)."""
    if not math.isfinite(x):
        fail('E_NONFINITE', repr(x))
    b = struct.unpack('<Q', struct.pack('<d', x))[0]
    return (~b) & _MASK if (b >> 63) else (b | (1 << 63))

def enc_d(x):
    if not math.isfinite(x):
        fail('E_NONFINITE', repr(x))
    if x == 0.0:
        x = 0.0                      # kills -0.0
    return struct.pack('<d', x)

def dec_d(buf, off):
    x = struct.unpack_from('<d', buf, off)[0]
    if not math.isfinite(x):
        fail('E_NONFINITE', 'offset %d' % off)
    return x

def canon_d(x):
    """canonicalise a double for struct packing: +0.0 for zero, refuse non-finite."""
    if not math.isfinite(x):
        fail('E_NONFINITE', repr(x))
    return 0.0 if x == 0.0 else x

def hx(x):
    return float.hex(x)              # exact, round-trips through float.fromhex

# ---------------------------------------------------------------- ball / exclusion
class Ball(object):
    __slots__ = ('v', 's', 'n')
    def __init__(self, v, s, n=0):
        self.v = tuple(float(t) for t in v); self.s = float(s); self.n = int(n)
    def key(self):
        return tuple(tot_key(t) for t in self.v) + (tot_key(self.s),)
    def __eq__(self, o): return self.v == o.v and self.s == o.s
    def __repr__(self): return 'Ball(%s,%r)' % (list(self.v), self.s)

def _bit(buf, k):
    return (buf[k >> 3] >> (k & 7)) & 1

def _pack_bits(bits):
    out = bytearray((len(bits) + 7) // 8)
    for i, b in enumerate(bits):
        if b:
            out[i >> 3] |= 1 << (i & 7)
    return bytes(out)

def enc_exclusions(n_balls, excl):
    """excl: sorted list of (i, j, code) with i<j.  -> (bytes, bitmap_bytes, code_bytes)"""
    P = n_balls * (n_balls - 1) // 2
    bitmap = bytearray((2 * P + 7) // 8)
    codes = []
    for (i, j, c) in excl:
        if not 0 <= i < j < n_balls:
            fail('E_EXCL_RANGE', '%d,%d,%d' % (i, j, c))
        p = i * n_balls - i * (i + 1) // 2 + (j - i - 1)   # index of pair (i,j) in lexicographic order
        bit = 2 * p + (0 if RULE_REL[c] == 'O' else 1)
        if _bit(bitmap, bit):
            fail('E_EXCL_DUP', '%d,%d,%d' % (i, j, c))
        bitmap[bit >> 3] |= 1 << (bit & 7)
        codes.append(c)
    packed = bytearray((4 * len(codes) + 7) // 8)
    for t, c in enumerate(codes):
        packed[(4 * t) >> 3] |= (c & 0xF) << ((4 * t) & 7)
    return bytes(bitmap) + bytes(packed), bytes(bitmap), bytes(packed), len(codes)

def pair_of_index(p, n):
    """Inverse of the lexicographic pair index used by enc_exclusions."""
    i = 0
    while p >= n - 1 - i:
        p -= n - 1 - i
        i += 1
    return i, i + 1 + p

def dec_exclusions(n_balls, n_excl, blob):
    P = n_balls * (n_balls - 1) // 2
    nb = (2 * P + 7) // 8
    nc = (4 * n_excl + 7) // 8
    if len(blob) != nb + nc:
        fail('E_EXCL_LEN', 'want %d got %d' % (nb + nc, len(blob)))
    bitmap = blob[:nb]
    packed = blob[nb:]
    if sum(bin(b).count('1') for b in bitmap) != n_excl:
        fail('E_EXCL_COUNT', 'bitmap popcount != n_excl')
    out = []
    t = 0
    k = 0
    for p in range(P):
        for rel in (0, 1):
            if _bit(bitmap, 2 * p + rel):
                c = (packed[k >> 1] >> (4 * (k & 1))) & 0xF
                if k >= n_excl:
                    fail('E_EXCL_COUNT', 'code stream overrun')
                if c >= N_RULES or (RULE_REL[c] == 'O') != (rel == 0):
                    fail('E_EXCL_REL', 'code %d in relation slot %d' % (c, rel))
                i, j = pair_of_index(p, n_balls)
                out.append((i, j, c))
                k += 1
    if k != n_excl:
        fail('E_EXCL_COUNT', '%d codes decoded, %d declared' % (k, n_excl))
    return out

# ---------------------------------------------------------------- stage-B payload
STAGEB_BOUNDS = dict(kmax=MAXK, p_abs=4.0, t_abs=1.01, r_max=0.03)

def dec_stageb(buf, off, kdecl):
    """Upstream layout, byte-for-byte (atlas.cpp saveRecords): int32 k, 36 doubles P,
    k*36 doubles T, 8 doubles (C, n0, id, ort, hor, mnorm, froot, radius)."""
    need = 4 + 288 + 288 * kdecl + 64
    if off + need > len(buf):
        fail('E_TRUNC', 'stageB needs %d bytes' % need)
    k = struct.unpack_from('<i', buf, off)[0]
    if k != kdecl:
        fail('E_K_MISMATCH', 'header k=%d, stageB k=%d' % (kdecl, k))
    if not 0 <= k <= MAXK:
        fail('E_K_BOUNDS', str(k))
    P = [dec_d(buf, off + 4 + 8 * t) for t in range(36)]
    T = [[dec_d(buf, off + 4 + 288 + 8 * (36 * a + t)) for t in range(36)] for a in range(k)]
    vals = [dec_d(buf, off + 4 + 288 + 288 * k + 8 * t) for t in range(8)]
    if any(abs(t) > STAGEB_BOUNDS['p_abs'] for t in P):
        fail('E_P_BOUNDS')
    if any(abs(t) > STAGEB_BOUNDS['t_abs'] for a in T for t in a):
        fail('E_T_BOUNDS')
    r = vals[7]
    if not (0.0 <= r <= STAGEB_BOUNDS['r_max']):
        fail('E_RADIUS', 'radius %r not in [0,.03]' % r)
    return dict(k=k, P=P, T=T, values=vals)

def enc_stageb(sb):
    out = bytearray()
    out += struct.pack('<i', sb['k'])
    for t in sb['P']:
        out += enc_d(t)
    for a in sb['T']:
        for t in a:
            out += enc_d(t)
    for t in sb['values']:
        out += enc_d(t)
    return bytes(out)

def stageb_bytes(k):
    return 4 + 288 + 288 * k + 64

# ---------------------------------------------------------------- record
REC_FMT = '<IBBBBHHHHIIIIBBBBdIQQ'
assert struct.calcsize(REC_FMT) == REC_HDR, struct.calcsize(REC_FMT)

class Record(object):
    def __init__(self, **kw):
        self.kind = kw.get('kind', K_BODY)
        self.evidence = kw.get('evidence', M_WITNESS)
        self.verdict = kw.get('verdict', V_NEG)
        self.cover_mode = kw.get('cover_mode', C_RECLUSTER)
        self.flags = kw.get('flags', 0)
        self.input_file = kw.get('input_file', 0)
        self.input_index = kw.get('input_index', 0)
        self.atlas_radius = kw.get('atlas_radius', 0.0)
        self.n_balls = kw.get('n_balls', 0)
        self.n_bins_last = kw.get('n_bins_last', 0)
        self.empty_at_layer = kw.get('empty_at_layer', 0)
        self.detail = kw.get('detail', 1)
        self.search_mode = kw.get('search_mode', 1)
        self.k = kw.get('k', 0)
        self.steps_used = kw.get('steps_used', 0)
        self.cap_steps = kw.get('cap_steps', 5000000)
        self.stageb = kw.get('stageb')
        self.balls = kw.get('balls')
        self.excl = kw.get('excl', [])
        self.adj = kw.get('adj')            # (O_words, U_words) row-major lists of ints, or None
        self.pos = kw.get('pos')
        self._svals = []
        if self.balls is not None:
            self.n_balls = len(self.balls)
        self.n_excl = len(self.excl)

    # -- derived helpers
    def words(self):
        return (self.n_balls + 63) // 64

    def ball_key_sorted(self):
        return all(self.balls[t].key() < self.balls[t+1].key() for t in range(len(self.balls)-1))

    def to_bytes(self):
        payload = bytearray()
        if self.kind == K_BODY:
            if self.stageb is None:
                fail('E_STAGEB_MISSING')
            payload += enc_stageb(self.stageb)
        if self.evidence == M_WITNESS and self.balls is None:
            fail('E_BALLS_MISSING', 'mode W needs the ball family')
        if self.balls is not None and self.evidence == M_RECOMPUTE and not (self.flags & FLAG_BALLS):
            fail('E_BALLS_FLAG', 'a ball hint in mode RECOMPUTE must set FLAG_BALLS')
        if self.balls is not None and (self.evidence == M_WITNESS or (self.flags & FLAG_BALLS)):
            if len(self.balls) != self.n_balls:
                fail('E_BALLS_COUNT')
            for b in self.balls:
                for t in b.v:
                    payload += enc_d(t)
                payload += enc_d(b.s)
        if self.evidence == M_WITNESS:
            blob, _, _, n = enc_exclusions(self.n_balls, self.excl)
            payload += blob
            self.n_excl = n
        if self.flags & FLAG_Y:
            fail('E_Y_RESERVED')
        if self.flags & FLAG_ADJ:
            if self.adj is None:
                fail('E_ADJ_MISSING')
            W = self.words()
            for A in self.adj:
                if len(A) != self.n_balls * W:
                    fail('E_ADJ_SIZE')
                for w in A:
                    payload += struct.pack('<Q', w)
        if self.verdict == V_POS:
            if self.pos is None or len(self.pos) != 12:
                fail('E_POS_LABELS')
            for l in self.pos:
                payload += struct.pack('<I', l)
        hdr = struct.pack(REC_FMT, REC_HDR + len(payload), self.kind, self.evidence, self.verdict,
                          self.cover_mode, self.flags, 0, self.input_file, 0,
                          self.input_index, self.n_balls, self.n_excl, self.n_bins_last,
                          self.empty_at_layer, self.detail, self.search_mode, 0,
                          canon_d(self.atlas_radius),
                          self.k, self.steps_used, self.cap_steps)
        return hdr + bytes(payload)

    @staticmethod
    def from_bytes(buf, off=0):
        if off + REC_HDR > len(buf):
            fail('E_TRUNC', 'record header')
        (ln, kind, evidence, verdict, cover, flags, r0, ifile, r1, iidx, n_balls, n_excl,
         n_bins, empty, detail, smode, r2, atlas, k, steps, cap) = struct.unpack_from(REC_FMT, buf, off)
        r3 = 0
        if r0 or r1 or r2:
            fail('E_RESERVED', 'record reserved fields must be zero')
        if not math.isfinite(atlas):
            fail('E_NONFINITE', 'atlas_radius')
        if ln < REC_HDR or off + ln > len(buf):
            fail('E_LEN', 'record length %d' % ln)
        rec = Record(kind=kind, evidence=evidence, verdict=verdict, cover_mode=cover, flags=flags,
                     atlas_radius=atlas, input_file=ifile, input_index=iidx, n_balls=n_balls,
                     n_bins_last=n_bins, empty_at_layer=empty, detail=detail, search_mode=smode,
                     k=k, steps_used=steps, cap_steps=cap)
        rec.n_excl = n_excl
        p = off + REC_HDR
        end = off + ln
        if kind not in (K_BODY, K_REF):
            fail('E_KIND', str(kind))
        if kind == K_BODY:
            sb = dec_stageb(buf[:end], p, k)
            rec.stageb = sb
            p += stageb_bytes(k)
        if evidence == M_WITNESS or (flags & FLAG_BALLS):
            need = 56 * n_balls
            if p + need > end:
                fail('E_TRUNC', 'balls')
            rec.balls = []
            for t in range(n_balls):
                v = [dec_d(buf, p + 56 * t + 8 * j) for j in range(6)]
                s = dec_d(buf, p + 56 * t + 48)
                rec.balls.append(Ball(v, s))
            p += need
        if evidence == M_WITNESS:
            P = n_balls * (n_balls - 1) // 2
            nb = (2 * P + 7) // 8
            nc = (4 * n_excl + 7) // 8
            if p + nb + nc > end:
                fail('E_TRUNC', 'exclusions')
            rec.excl = dec_exclusions(n_balls, n_excl, bytes(buf[p:p + nb + nc]))
            p += nb + nc
        if flags & FLAG_Y:
            fail('E_Y_RESERVED')
        if flags & FLAG_ADJ:
            W = (n_balls + 63) // 64
            need = 2 * n_balls * W * 8
            if p + need > end:
                fail('E_TRUNC', 'adjacency')
            rows = []
            for g in range(2):
                A = []
                for t in range(n_balls):
                    for w in range(W):
                        A.append(struct.unpack_from('<Q', buf, p + 8 * (t * W + w))[0])
                rows.append(A)
                p += n_balls * W * 8
            rec.adj = tuple(rows)
        if verdict == V_POS:
            if p + 48 > end:
                fail('E_TRUNC', 'pos')
            rec.pos = [struct.unpack_from('<I', buf, p + 4 * t)[0] for t in range(12)]
            p += 48
        if p != end:
            fail('E_LEN', 'record has %d trailing bytes' % (end - p))
        return rec, end

# ---------------------------------------------------------------- validator
def _bits(A, i, W):
    return A[i * W:(i + 1) * W]

def adj_bit(rec, g, i, j):
    W = rec.words()
    return (rec.adj[g][i * W + (j >> 6)] >> (j & 63)) & 1

def validate_record(rec, n_records=None):
    """Structural obligations only: everything a checker can decide without re-deriving the
    predicates or the search.  Returns a list of (code, detail)."""
    E = []
    def bad(c, d=''): E.append((c, d))

    if rec.kind not in (K_BODY, K_REF): bad('E_KIND', str(rec.kind))
    if rec.evidence not in (M_RECOMPUTE, M_WITNESS): bad('E_EVIDENCE', str(rec.evidence))
    if rec.verdict not in VERDICT_NAME: bad('E_VERDICT', str(rec.verdict))
    if rec.cover_mode not in (C_RECLUSTER, C_BINSET): bad('E_COVER', str(rec.cover_mode))
    if rec.flags & ~(FLAG_ADJ | FLAG_BALLS): bad('E_FLAGS', hex(rec.flags))
    if not 0 <= rec.k <= MAXK: bad('E_K_BOUNDS', str(rec.k))
    if not (0 <= rec.detail <= 10): bad('E_DETAIL', str(rec.detail))
    if rec.search_mode not in (0, 1, 2): bad('E_SEARCH_MODE', str(rec.search_mode))
    if not (CAP_MIN <= rec.cap_steps <= CAP_MAX): bad('E_CAP_BOUNDS', str(rec.cap_steps))
    if not (0 <= rec.n_bins_last <= BIN_CAP): bad('E_BINS_BOUNDS', str(rec.n_bins_last))
    if rec.n_balls > BALL_CAP: bad('E_BALL_CAP', str(rec.n_balls))
    if rec.n_balls < 0: bad('E_BALL_CAP', str(rec.n_balls))
    if rec.kind == K_BODY and rec.stageb is None: bad('E_STAGEB_MISSING')
    if rec.stageb is not None and rec.stageb['k'] != rec.k: bad('E_K_MISMATCH')
    if not (0.0 <= rec.atlas_radius <= 0.03): bad('E_RADIUS', 'atlas_radius %r' % rec.atlas_radius)
    if rec.stageb is not None:
        pr = rec.stageb['values'][7]
        if not (rec.atlas_radius <= pr):
            bad('E_RADIUS_ORDER', 'atlas_radius %r > pass_radius %r' % (rec.atlas_radius, pr))

    if rec.balls is not None:
        if len(rec.balls) != rec.n_balls: bad('E_BALLS_COUNT')
        for t, b in enumerate(rec.balls):
            if any(abs(x) > 2.0 for x in b.v): bad('E_V_BOUNDS', 'ball %d' % t)
            if not (0.0 <= b.s < 0.1): bad('E_S_BOUNDS', 'ball %d s=%r' % (t, b.s))
            if t and not (rec.balls[t - 1].key() < b.key()):
                bad('E_BALL_ORDER', 'ball %d not strictly after %d' % (t, t - 1))
        if any(b.key() == c.key() for b in rec.balls for c in rec.balls if b is not c):
            pass  # equality is caught by the order test above
    elif rec.evidence == M_WITNESS:
        bad('E_BALLS_MISSING')

    if rec.evidence == M_WITNESS:
        if rec.n_excl == 0: bad('E_EXCL_EMPTY', 'mode W with no exclusions')
        prev = None
        for (i, j, c) in rec.excl:
            if not 0 <= i < j < max(rec.n_balls, 1): bad('E_EXCL_RANGE', '%d,%d' % (i, j)); break
            if not 0 <= c < N_RULES: bad('E_EXCL_CODE', str(c)); break
            key = (i, j, 0 if RULE_REL[c] == 'O' else 1)
            if prev is not None and key <= prev: bad('E_EXCL_ORDER', str((i, j, c)))
            prev = key
    elif rec.n_excl:
        bad('E_EXCL_EMPTY', 'mode R must not carry exclusions')

    if rec.flags & FLAG_ADJ:
        if rec.adj is None: bad('E_ADJ_MISSING')
        else:
            W = rec.words()
            if any(len(A) != rec.n_balls * W for A in rec.adj): bad('E_ADJ_SIZE')
            else:
                for g, nm in ((0, 'O'), (1, 'U')):
                    A = rec.adj[g]
                    for i in range(rec.n_balls):
                        if (A[i * W + (i >> 6)] >> (i & 63)) & 1:
                            bad('E_DIAG', '%s row %d' % (nm, i)); break
                        for j in range(i):
                            if ((A[i * W + (j >> 6)] >> (j & 63)) & 1) != \
                               ((A[j * W + (i >> 6)] >> (i & 63)) & 1):
                                bad('E_ASYM', '%s %d,%d' % (nm, i, j)); break
                        for w in range(W):
                            hi = (1 << 64) - 1
                            if w == W - 1 and rec.n_balls % 64:
                                hi = (1 << (rec.n_balls % 64)) - 1
                            if A[i * W + w] & ~hi:
                                bad('E_HIGHBIT', '%s row %d word %d' % (nm, i, w)); break
            if rec.evidence == M_WITNESS and rec.adj is not None and not E:
                # O edge <=> pair not excluded with rel O ; same for U
                ex = {(i, j, RULE_REL[c]) for (i, j, c) in rec.excl}
                W = rec.words()
                for i in range(rec.n_balls):
                    for j in range(i):
                        for g, rel in ((0, 'O'), (1, 'U')):
                            e = ((rec.adj[g][i * W + (j >> 6)] >> (j & 63)) & 1)
                            lo, hi = (j, i) if j < i else (i, j)
                            if e == ((lo, hi, rel) in ex):
                                bad('E_ADJ_EXCL', '%s %d,%d' % (rel, i, j)); break
                        else:
                            continue
                        break

    v = rec.verdict
    if v == V_NEG:
        if rec.n_balls < 1: bad('E_NEG_NEEDS', 'no balls')
        if rec.steps_used < 1: bad('E_NEG_NEEDS', 'steps_used=0')
        if rec.steps_used > rec.cap_steps: bad('E_CAP', '%d>%d' % (rec.steps_used, rec.cap_steps))
        if rec.empty_at_layer: bad('E_EMPTY', 'NEG with empty_at_layer')
    elif v == V_EMPTY:
        if not 1 <= rec.empty_at_layer <= 6: bad('E_EMPTY', 'empty_at_layer=%d' % rec.empty_at_layer)
        if rec.n_balls != 0 or rec.n_excl != 0: bad('E_EMPTY', 'EMPTY_BINS with balls/exclusions')
        if rec.steps_used != 0: bad('E_EMPTY', 'EMPTY_BINS with steps')
    elif v == V_POS:
        if rec.pos is None or len(rec.pos) != 12: bad('E_POS_LABELS')
        else:
            if len(set(rec.pos)) != 12: bad('E_POS_LABELS', 'repeated label')
            if any(not (0 <= l < rec.n_balls) for l in rec.pos): bad('E_POS_LABELS', 'out of range')
            if not (rec.flags & FLAG_ADJ): bad('E_ADJ_NEEDED', 'POS needs the declared graph')
            else:
                A, B = rec.pos[:6], rec.pos[6:]
                for X in (A, B):
                    for a in range(6):
                        for b in range(a + 1, 6):
                            if not adj_bit(rec, 0, X[a], X[b]): bad('E_POS_EDGE', 'O %d,%d' % (X[a], X[b]))
                for a in A:
                    for b in B:
                        if not adj_bit(rec, 1, a, b): bad('E_POS_EDGE', 'U %d,%d' % (a, b))
    elif v == V_CAP:
        if rec.steps_used <= rec.cap_steps: bad('E_CAP', 'CAP without exceeding cap_steps')
    return E

def _finish(r):
    if r._svals:
        n = len(r._svals)
        want = 36 + 36 * r.k + 8
        if n != want: fail('E_TEXT_SVALS', '%d != %d' % (n, want))
        r.stageb = dict(k=r.k, P=r._svals[:36],
                        T=[r._svals[36 + 36 * a:36 + 36 * (a + 1)] for a in range(r.k)],
                        values=r._svals[36 + 36 * r.k:])
    return r

# ---------------------------------------------------------------- shard container
SHARD_FMT = '<8sHHIIIQQ32sQ'
assert struct.calcsize(SHARD_FMT) == SHARD_HDR, struct.calcsize(SHARD_FMT)

class Shard(object):
    def __init__(self, pass_id, part, parts, records):
        self.pass_id = pass_id; self.part = part; self.parts = parts
        self.records = list(records)

    def body(self):
        return b''.join(r.to_bytes() for r in self.records)

    def encode(self):
        body = self.body()
        hdr = struct.pack(SHARD_FMT, MAGIC, VERSION[0], VERSION[1], self.pass_id, self.part,
                          self.parts, len(self.records), len(body), hashlib.sha256(body).digest(), 0)
        return hdr + body

    @staticmethod
    def decode(buf):
        if len(buf) < SHARD_HDR: fail('E_TRUNC', 'shard header')
        (magic, vmaj, vmin, pid, part, parts, n, blen, sha, rsv) = struct.unpack_from(SHARD_FMT, buf, 0)
        if magic != MAGIC: fail('E_MAGIC', repr(magic))
        if (vmaj, vmin) != VERSION: fail('E_VERSION', '%d.%d' % (vmaj, vmin))
        if rsv: fail('E_RESERVED', 'shard header')
        if parts < 1 or not 0 <= part < parts: fail('E_PART', '%d/%d' % (part, parts))
        if len(buf) != SHARD_HDR + blen: fail('E_LEN', 'shard body %d vs %d' % (len(buf) - SHARD_HDR, blen))
        body = buf[SHARD_HDR:]
        if hashlib.sha256(body).digest() != sha: fail('E_BODY_HASH')
        recs = []; off = 0
        for t in range(n):
            r, off = Record.from_bytes(body, off)
            recs.append(r)
        if off != len(body): fail('E_LEN', 'trailing bytes')
        sh = Shard(pid, part, parts, recs)
        return sh

    # -- canonical text rendering (authority stays with the binary form)
    def text(self):
        out = ['SCV1-TEXT %d.%d' % VERSION,
               'SHARD pass=%d part=%d parts=%d n_records=%d' % (self.pass_id, self.part, self.parts,
                                                              len(self.records))]
        for r in self.records:
            out.append('REC input_file=%d input_index=%d kind=%d evidence=%d verdict=%s cover=%d '
                       'atlas=%s k=%d steps=%d cap=%d n_bins=%d empty=%d detail=%d mode=%d '
                       'n_balls=%d n_excl=%d flags=%d'
                       % (r.input_file, r.input_index, r.kind, r.evidence,
                          VERDICT_NAME[r.verdict], r.cover_mode, hx(r.atlas_radius), r.k,
                          r.steps_used, r.cap_steps, r.n_bins_last, r.empty_at_layer, r.detail,
                          r.search_mode, r.n_balls, r.n_excl, r.flags))
            if r.stageb is not None:
                out.append('S ' + ' '.join(hx(t) for t in r.stageb['P']))
                for a in r.stageb['T']:
                    out.append('S ' + ' '.join(hx(t) for t in a))
                out.append('S ' + ' '.join(hx(t) for t in r.stageb['values']))
            if r.balls is not None:
                for b in r.balls:
                    out.append('B ' + ' '.join(hx(t) for t in b.v) + ' ' + hx(b.s))
            for (i, j, c) in r.excl:
                out.append('X %d %d %d' % (i, j, c))
            if r.adj is not None:
                W = r.words()
                for i in range(r.n_balls):
                    out.append('A ' + ''.join('%016x' % w for w in r.adj[0][i * W:(i + 1) * W]) +
                               ' ' + ''.join('%016x' % w for w in r.adj[1][i * W:(i + 1) * W]))
            if r.pos is not None:
                out.append('POS ' + ' '.join(str(l) for l in r.pos))
        out.append('END')
        return '\n'.join(out) + '\n'

    @staticmethod
    def parse_text(txt):
        lines = txt.splitlines()
        if not lines or lines[0] != 'SCV1-TEXT %d.%d' % VERSION: fail('E_TEXT_HDR')
        if not lines[1].startswith('SHARD '): fail('E_TEXT_HDR')
        kv = dict(t.split('=') for t in lines[1].split()[1:])
        recs = []; cur = None
        for line in lines[2:]:
            if line == 'END': break
            t = line.split()
            if t[0] == 'REC':
                if cur is not None: recs.append(_finish(cur))
                d = dict(x.split('=') for x in t[1:])
                cur = Record(input_file=int(d['input_file']), input_index=int(d['input_index']),
                             kind=int(d['kind']), evidence=int(d['evidence']),
                             verdict=int([k for k, v in VERDICT_NAME.items() if v == d['verdict']][0]),
                             cover_mode=int(d['cover']),
                             atlas_radius=float.fromhex(d['atlas']),
                             k=int(d['k']), steps_used=int(d['steps']), cap_steps=int(d['cap']),
                             n_bins_last=int(d['n_bins']), empty_at_layer=int(d['empty']),
                             detail=int(d['detail']), search_mode=int(d['mode']),
                             n_balls=int(d['n_balls']), flags=int(d['flags']))
            elif t[0] == 'S':
                cur._svals.extend(float.fromhex(x) for x in t[1:])
            elif t[0] == 'B':
                cur.balls = cur.balls or []
                cur.balls.append(Ball([float.fromhex(x) for x in t[1:7]], float.fromhex(t[7])))
            elif t[0] == 'X':
                cur.excl.append((int(t[1]), int(t[2]), int(t[3])))
            elif t[0] == 'A':
                W = (cur.n_balls + 63) // 64
                if cur.adj is None: cur.adj = ([], [])
                cur.adj[0].extend(int(t[1][16 * w:16 * w + 16], 16) for w in range(W))
                cur.adj[1].extend(int(t[2][16 * w:16 * w + 16], 16) for w in range(W))
            elif t[0] == 'POS':
                cur.pos = [int(x) for x in t[1:]]
            else:
                fail('E_TEXT_LINE', line[:40])
        if cur is not None: recs.append(_finish(cur))
        sh = Shard(int(kv['pass']), int(kv['part']), int(kv['parts']), recs)
        for r in sh.records: r.n_excl = len(r.excl)
        return sh

# ---------------------------------------------------------------- manifest
def _num_ok(x):
    return isinstance(x, int) and not isinstance(x, bool) and abs(x) <= 2 ** 53

def _check_json_types(o, path='$'):
    if isinstance(o, dict):
        for k, v in o.items():
            if not isinstance(k, str): fail('E_MANIFEST_TYPE', '%s: non-string key' % path)
            _check_json_types(v, path + '.' + k)
    elif isinstance(o, list):
        for t, v in enumerate(o): _check_json_types(v, '%s[%d]' % (path, t))
    elif isinstance(o, bool) or o is None or isinstance(o, str):
        return
    elif isinstance(o, float):
        fail('E_MANIFEST_FLOAT', '%s: JSON number with a fractional part is not portable; '
             'use a hex-float string' % path)
    elif isinstance(o, int):
        if not _num_ok(o):
            fail('E_MANIFEST_INT53', '%s: integer beyond 2^53 must be a decimal string' % path)
    else:
        fail('E_MANIFEST_TYPE', '%s: %r' % (path, type(o)))

def canonical_json(obj):
    _check_json_types(obj)
    return json.dumps(obj, sort_keys=True, separators=(',', ':'), ensure_ascii=True) + '\n'

def parse_manifest(buf):
    if isinstance(buf, bytes):
        try:
            buf = buf.decode('ascii')
        except UnicodeDecodeError:
            fail('E_MANIFEST_ASCII')
    seen = []
    def hook(pairs):
        keys = [k for k, _ in pairs]
        if len(set(keys)) != len(keys): fail('E_MANIFEST_DUP', str(keys))
        seen.append(keys)
        return dict(pairs)
    obj = json.loads(buf, object_pairs_hook=hook)
    if canonical_json(obj) != buf:
        fail('E_MANIFEST_CANON', 'manifest is not in canonical form')
    return obj

REQUIRED = ('format', 'preprint_sha256', 'sources', 'params', 'arithmetic', 'passes', 'trust')

def check_manifest(m):
    E = []
    def bad(c, d=''): E.append((c, d))
    for k in REQUIRED:
        if k not in m: bad('E_MANIFEST_KEY', k)
    if m.get('format') != 'stagec-v1': bad('E_MANIFEST_KEY', 'format')
    for i, p in enumerate(m.get('params', [])):
        for k in ('M', 'layers', 'linear', 'RB', 'detail', 'search_mode', 'cap_steps', 'lloyd'):
            if k not in p: bad('E_MANIFEST_KEY', 'params[%d].%s' % (i, k))
        if not (6 <= p.get('M', 0) <= 24): bad('E_PARAM', 'params[%d].M' % i)
        if not (1 <= p.get('layers', 0) <= 6): bad('E_PARAM', 'params[%d].layers' % i)
        if not (0.012 <= float(p.get('RB', 0)) <= 0.09): bad('E_PARAM', 'params[%d].RB' % i)
        if not (0 <= p.get('detail', -1) <= 10): bad('E_PARAM', 'params[%d].detail' % i)
    return E

# ---------------------------------------------------------------- coverage and outcome
def _frec(f):
    """A pass-level input file entry: {'path','sha256','records'} (a dict), position = the
    file index used by records and by commands."""
    return int(f['records'])

def command_offsets(pcmd):
    off = [0]
    for t in pcmd['inputs']:
        off.append(off[-1] + 0)   # filled in by the caller, which knows the pass
    return off

def check_coverage(passes, shards):
    """passes: manifest['passes']; shards: list of Shard.

    A pass models one *logical* batch (the initial Stage-C pass, or the fallback pass).
    Shape:
        pass   = {name, inputs: [ {path, sha256, records}, ... ], commands: [cmd, ...]}
        cmd    = {inputs: [file_index, ...], parts: int, part: int}    # argv order
    `inputs` is the pass-level index space: the concatenation of its files in order, exactly
    the `offset += v.size()` space of stageC.cpp's main().  A command is one upstream
    invocation: a group of input files, a (part, parts) split, and the single shard file it
    wrote (identified by the shard header's pass_id/part).

    Coverage has three parts, all checked here:
      (i)   inside a command, the shard holds exactly {g : g % parts == part} over that
            command's own local index space, each index once;
      (ii)  across the commands of a pass, every pass-level global index occurs exactly
            once (a dropped or duplicated input record is an error, never a silent gap);
      (iii) across passes, every UNRESOLVED record has >= 1 child in the next pass, every
            child's parent is an UNRESOLVED record of the previous pass, and no child hangs
            off a resolved one.
    The shard header carries `part` only, so a pass's commands are numbered by `part`; that
    is why the recorded run is 88 initial commands of one shard each (parts=1) and 4
    fallback commands (parts=4) over one shared input file.
    """
    E = []
    def bad(c, d=''): E.append((c, d))
    seen = {}
    for pid, p in enumerate(passes):
        file_base = {}
        base = 0
        for t, f in enumerate(p['inputs']):
            file_base[t] = base
            base += _frec(f)
        N = base
        got = {}
        for sh in shards:
            if sh.pass_id == pid:
                got.setdefault(sh.part, []).append(sh)
        if len(got) != len(p['commands']):
            bad('E_COV_PARTS', 'pass %d: %d distinct shard indices for %d commands'
                % (pid, len(got), len(p['commands'])))
        for ci, cmd in enumerate(p['commands']):
            ins = cmd['inputs']
            off = [0]
            for t in ins:
                off.append(off[-1] + _frec(p['inputs'][t]))
            parts, part = int(cmd['parts']), int(cmd['part'])
            if part != ci:
                bad('E_COV_PARTS', 'pass %d command %d declares shard index %d (must equal command index)'
                    % (pid, ci, part))
            shs = [sh for sh in shards if sh.pass_id == pid and sh.part == part]
            if len(shs) != 1:
                bad('E_COV_PARTS', 'pass %d command %d: %d shards' % (pid, ci, len(shs)))
                continue
            sh = shs[0]
            if sh.parts != parts:
                bad('E_COV_PARTS', 'pass %d command %d declares parts=%d, shard says %d'
                    % (pid, ci, parts, sh.parts))
            for r in sh.records:
                if not (0 <= r.input_file < len(ins)):
                    bad('E_COV_FILE', 'pass %d command %d: input slot %d' % (pid, ci, r.input_file))
                    continue
                if not (0 <= r.input_index < off[r.input_file + 1] - off[r.input_file]):
                    bad('E_COV_INDEX', 'pass %d command %d: slot %d index %d'
                        % (pid, ci, r.input_file, r.input_index))
                    continue
                g = off[r.input_file] + r.input_index
                if g % parts != part:
                    bad('E_COV_PART', 'pass %d command %d: local index %d in part %d' % (pid, ci, g, part))
                gf = file_base[ins[r.input_file]] + r.input_index
                if (pid, gf) in seen:
                    bad('E_COV_DUP', 'pass %d global %d' % (pid, gf))
                seen[(pid, gf)] = r
        miss = [g for g in range(N) if (pid, g) not in seen]
        if miss:
            bad('E_COV_MISSING', 'pass %d: %d records absent, first %s' % (pid, len(miss), miss[:5]))
    return E

def certificate_outcome(passes, shards):
    """accept | unresolved | reject, plus the error list.  A structural error is a reject: an
    invalid record may never be downgraded to 'unresolved' (that would let a certificate fill
    itself with garbage and still report zero unresolved)."""
    E = check_coverage(passes, shards)
    for sh in shards:
        for r in sh.records:
            E.extend(validate_record(r))
    if E:
        return 'reject', E
    n_unres = sum(1 for sh in shards for r in sh.records if r.verdict in UNRESOLVED)
    return ('unresolved' if n_unres else 'accept'), E
