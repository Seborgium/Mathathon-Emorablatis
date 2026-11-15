"""Schema v1-draft composition (cover) block.

The Stage-C argument needs a many-to-many *covering* relation: each unresolved record of a pass
is covered by several records of the next pass, and 90.5 % of those incidences are inherited from
records created for a *different* parent (measured by m2 in
`.ultramath/smwgx104w/m2/H0-stageC-coverage.md` and exported in `composition-cover-map.json`:
163 parents, 1,127 children, 11,838 incidences, 10,711 inherited).  A single creation parent per
record cannot express that, so v1 carries the relation as its own canonical block and keeps
Stage-B provenance (the fine.bin record a fallback record was created from) out of Stage C.

Layout (little-endian, 28-byte header):
    0   8  magic 'SCV1COMP'
    8   2  version major (1)      10  2  version minor (0)
   12   4  parent pass_id         16  4  n_parents          20  4  n_children
   24   4  n_links                (there is no reserved header word after these counts)
  parents  n_parents  x 32 B: u32 global (position in the parent pass's input stream,
                              not ordinal within bad*.bin), u32 base, u32 inside, u32 relation_marks,
                              u32 snap_closed_cells, u32 fail,
                              u16 created, u16 inherited, u16 degree, u16 reserved
  children n_children x  4 B: u32 global
  links    n_links    x  4 B: u16 child_local, u16 parent_local
Counter identities (the point of the two separate u32s): `inside = relation_marks +
snap_closed_cells` for every parent.  `snap_closed_cells` counts cells inside the parent box that
were closed only after a Hadamard snap (7 in this pass); it is **not** the refiner's `snaps`
counter, which counts *snap attempts* over the whole search (17,207 here, `stageB.cpp:175`), nor
`live` (`:170`, cells visited).  Those are operation counts, not per-parent cell classifications,
and v1 deliberately does not encode them: a checker cannot verify them from cells.
Canonical order: parents and children strictly increasing by global; links strictly increasing by
(child_local, parent_local), duplicate-free.  The cover *metric* (w, E(ort,R), cells, criterion)
is a string-valued object in the manifest (`composition_metric`), because it is exact arithmetic,
not data.
"""
import struct, math, json
import stagec_schema as S

MAGIC = b'SCV1COMP'
VERSION = (1, 0)
HDR = 28
PARENT_FMT = '<IIIIIIHHHH'
CHILD_FMT = '<I'
LINK_FMT = '<HH'
assert struct.calcsize(PARENT_FMT) == 32 and struct.calcsize(LINK_FMT) == 4

class Composition(object):
    def __init__(self, pass_id, parents, children, links):
        self.pass_id = pass_id          # the *parent* pass; children live in pass_id + 1
        self.parents = parents          # list of dicts(global, base, inside, snaps, fail, created, inherited)
        self.children = children        # list of global indices in the child pass
        self.links = links              # list of (child_local, parent_local)

    def degrees(self):
        d = [0] * len(self.parents)
        for (c, p) in self.links:
            d[p] += 1
        return d

    def to_bytes(self):
        body = bytearray()
        for p in self.parents:
            body += struct.pack(PARENT_FMT, p['g'], p['base'], p['inside'], p['relation_marks'],
                                p['snap_closed_cells'], p['fail'], p['created'], p['inherited'],
                                p['degree'], 0)
        for c in self.children:
            body += struct.pack(CHILD_FMT, c)
        for (c, p) in self.links:
            body += struct.pack(LINK_FMT, c, p)
        return struct.pack('<8sHHIIII', MAGIC, VERSION[0], VERSION[1], self.pass_id,
                           len(self.parents), len(self.children), len(self.links)) + bytes(body)

    @staticmethod
    def from_bytes(buf):
        if len(buf) < HDR: S.fail('E_TRUNC', 'composition header')
        magic, vmaj, vmin, pid, np_, nc, nl = struct.unpack_from('<8sHHIIII', buf, 0)
        if magic != MAGIC: S.fail('E_MAGIC', repr(magic))
        if (vmaj, vmin) != VERSION: S.fail('E_VERSION', 'composition')
        if len(buf) != HDR + 32 * np_ + 4 * nc + 4 * nl: S.fail('E_LEN', 'composition body')
        off = HDR
        parents = []
        for t in range(np_):
            g, base, inside, marks, snapclosed, fail, created, inherited, degree, rsv = \
                struct.unpack_from(PARENT_FMT, buf, off)
            off += 32
            if rsv: S.fail('E_RESERVED', 'composition parent %d' % t)
            parents.append(dict(g=g, base=base, inside=inside, relation_marks=marks,
                                snap_closed_cells=snapclosed, fail=fail,
                                created=created, inherited=inherited, degree=degree))
        children = [struct.unpack_from(CHILD_FMT, buf, off + 4 * t)[0] for t in range(nc)]
        off += 4 * nc
        links = [struct.unpack_from(LINK_FMT, buf, off + 4 * t) for t in range(nl)]
        return Composition(pid, parents, children, links)

    def text(self):
        out = ['SCV1-COMP %d.%d' % VERSION, 'COMP pass=%d parents=%d children=%d links=%d'
               % (self.pass_id, len(self.parents), len(self.children), len(self.links))]
        for p in self.parents:
            out.append('P %d %d %d %d %d %d %d %d %d' % (p['g'], p['base'], p['inside'],
                                                        p['relation_marks'], p['snap_closed_cells'],
                                                        p['fail'], p['created'], p['inherited'],
                                                        p['degree']))
        for c in self.children:
            out.append('C %d' % c)
        for (c, p) in self.links:
            out.append('L %d %d' % (c, p))
        out.append('END')
        return '\n'.join(out) + '\n'

    @staticmethod
    def parse_text(txt):
        L = txt.splitlines()
        if not L or L[0] != 'SCV1-COMP %d.%d' % VERSION: S.fail('E_TEXT_HDR', 'composition')
        kv = dict(t.split('=') for t in L[1].split()[1:])
        parents, children, links = [], [], []
        for line in L[2:]:
            if line == 'END': break
            t = line.split()
            if t[0] == 'P':
                v = [int(x) for x in t[1:10]]
                parents.append(dict(g=v[0], base=v[1], inside=v[2], relation_marks=v[3],
                                    snap_closed_cells=v[4], fail=v[5], created=v[6],
                                    inherited=v[7], degree=v[8]))
            elif t[0] == 'C':
                children.append(int(t[1]))
            elif t[0] == 'L':
                links.append((int(t[1]), int(t[2])))
            else:
                S.fail('E_TEXT_LINE', line[:40])
        return Composition(int(kv['pass']), parents, children, links)


def record_positions(passes, shards):
    """(pass_id, pass-level global index) -> Record, rebuilt from the coverage walk."""
    pos = {}
    for pid, p in enumerate(passes):
        filebase = {}
        b = 0
        for t, f in enumerate(p['inputs']):
            filebase[t] = b; b += S._frec(f)
        for sh in shards:
            if sh.pass_id != pid: continue
            cmd = None
            for c in p['commands']:
                if c['part'] == sh.part: cmd = c
            if cmd is None: continue
            off = [0]
            for t in cmd['inputs']:
                off.append(off[-1] + S._frec(p['inputs'][t]))
            for r in sh.records:
                g = filebase[cmd['inputs'][r.input_file]] + r.input_index
                pos[(pid, g)] = r
    return pos


def check_composition(comps, metric=None, pos=None):
    """comps: list of Composition.  Internal consistency is always checked; the record-level
    cross-checks run when `pos` (from record_positions) is given.  The *cover criterion* itself
    (that the listed child balls really cover the parent's box under E(ort,R)) is an external
    arithmetic obligation, priced in H0-stageC-schema.md §5, not a format property."""
    E = []
    def bad(c, d=''): E.append((c, d))
    for comp in comps:
        pid = comp.pass_id
        if pos is not None:
            sub = {g: r for (q, g), r in pos.items() if q == pid}
            un = sorted(g for g, r in sub.items() if r.verdict in S.UNRESOLVED)
            declared = [p['g'] for p in comp.parents]
            miss = [g for g in un if g not in set(declared)]
            extra = [g for g in declared if g not in set(un)]
            if miss or extra:
                bad('E_COVER_MISSING', 'pass %d: %d unresolved, %d declared, missing %s, extra %s'
                    % (pid, len(un), len(declared), miss[:3], extra[:3]))
            for t, g in enumerate(comp.children):
                rc = pos.get((pid + 1, g))
                if rc is None:
                    bad('E_COVER_CHILD', 'pass %d child %d absent' % (pid + 1, g))
                elif rc.verdict not in S.EXCLUDED:
                    bad('E_COVER_CHILD_STATE', 'pass %d child %d is %s'
                        % (pid + 1, g, S.VERDICT_NAME.get(rc.verdict)))
        declared = [p['g'] for p in comp.parents]
        if declared != sorted(set(declared)):
            bad('E_COVER_ORDER', 'pass %d parents not strictly increasing' % pid)
        if comp.children != sorted(set(comp.children)):
            bad('E_COVER_ORDER', 'children not strictly increasing')
        prev = None
        ok_order = True
        for (c, p) in comp.links:
            if not (0 <= c < len(comp.children)) or not (0 <= p < len(comp.parents)):
                bad('E_COVER_LINK', '%d,%d out of range' % (c, p)); ok_order = False; continue
            if prev is not None and (c, p) <= prev:
                bad('E_COVER_ORDER', 'links not strictly increasing'); ok_order = False
            prev = (c, p)
        deg = comp.degrees()
        for t, p in enumerate(comp.parents):
            if p['degree'] != deg[t]:
                bad('E_COVER_DEGREE', 'parent %d degree %d != %d' % (t, p['degree'], deg[t]))
            if p['created'] + p['inherited'] != p['degree']:
                bad('E_COVER_DEGREE', 'parent %d created+inherited != degree' % t)
            if deg[t] == 0:
                bad('E_COVER_EMPTY_PARENT', 'parent %d has no covering child' % t)
            if p['fail']:
                bad('E_COVER_COUNTERS', 'parent %d fail=%d' % (t, p['fail']))
            if p['relation_marks'] > p['inside'] or p['snap_closed_cells'] > p['inside'] or \
                    p['inside'] != p['relation_marks'] + p['snap_closed_cells']:
                bad('E_COVER_COUNTERS', 'parent %d inside != relation_marks + snap_closed_cells' % t)
            if metric:
                cells = int(metric['cells_total_per_parent'])
                if p['inside'] > cells:
                    bad('E_COVER_COUNTERS', 'parent %d inside>cells' % t)
                if 'inside_cells_per_parent' in metric and \
                        p['inside'] != int(metric['inside_cells_per_parent']):
                    bad('E_COVER_COUNTERS', 'parent %d inside=%d' % (t, p['inside']))
        if sum(p['created'] for p in comp.parents) != len(comp.children):
            bad('E_COVER_CREATION', 'sum(created)=%d != %d children'
                % (sum(p['created'] for p in comp.parents), len(comp.children)))
        if sum(p['inherited'] for p in comp.parents) != len(comp.links) - len(comp.children):
            bad('E_COVER_CREATION', 'sum(inherited)=%d != links-children=%d'
                % (sum(p['inherited'] for p in comp.parents), len(comp.links) - len(comp.children)))
    if pos is not None:
        claimed = {c.pass_id for c in comps}
        for pid in range(len({q for (q, g) in pos}) ):
            un = [g for (q, g), r in pos.items() if q == pid and r.verdict in S.UNRESOLVED]
            if un and pid not in claimed:
                bad('E_COVER_MISSING', 'pass %d has %d unresolved records and no composition block'
                    % (pid, len(un)))
    return E
