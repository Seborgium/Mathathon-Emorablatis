"""Does the stored C need the tensor (Lemma 4.4, second constant) branch?

patchx.cpp: C = pi*sqrt(8)*mnorm + 1e-7 first; only when that exceeds 4.35 is the tensor bound
attempted, and then C = min(C, pi*sqrt(6*(row+.0002)/(1-beta)) + .00001).
A checker that wants to accept the stored C must reproduce one of the two branches.
This script measures, per saved record, which branch the stored C is consistent with, using a
freshly derived (numpy) eigenbasis U of the 30x30 signed Gram A: the "derive then verify" route.
Numbers here are float64 and are NOT certificates; they fix which obligations bind.
"""
import math
import numpy as np
import records as R
from derive import derive

EI, EJ = [], []
for _i in range(6):
    for _j in range(_i):
        EI += [_i, _i]; EJ += [_j, _j]
EI = np.array(EI); EJ = np.array(EJ)
SIGN = ((EI[:, None] == EI[None, :]).astype(int) + (EJ[:, None] == EJ[None, :]).astype(int)
        - (EI[:, None] == EJ[None, :]).astype(int) - (EJ[:, None] == EI[None, :]).astype(int)).astype(float)


def tensor_C(M):
    A = SIGN * (M.T @ M)
    w, U = np.linalg.eigh(A)
    beta = np.linalg.norm(U.T @ U - np.eye(30)) + 1e-8          # A.5's bump
    row = np.abs(U.T @ (A @ U)).sum(axis=1).max()
    C = math.pi * math.sqrt(6 * (row + 0.0002) / (1 - beta)) + 0.00001
    return C, beta, row


def main(paths):
    print("file             n    simple-pass  needs-tensor  tensor-derive-ok  rejected  worst deficit")
    tot = [0, 0, 0, 0]
    for p in paths:
        v = R.read(p)
        simple = tensor = tok = rej = 0
        worst = []
        for r in v:
            Cs = math.pi * math.sqrt(8.0) * r.mnorm + 1e-7
            if r.C >= Cs:
                simple += 1
                continue
            tensor += 1
            d = derive(r)
            Ct, beta, row = tensor_C(d["M"])
            if r.C >= Ct - 1e-7:
                tok += 1
            else:
                rej += 1
                worst.append((r.C - Ct, r.C, Ct))
        print("%-14s %5d      %5d        %5d            %5d       %d   %+.2e"
              % (p.split("/")[-1], len(v), simple, tensor, tok, rej, min(worst)[0] if worst else 0.0))
        tot = [tot[0] + simple, tot[1] + tensor, tot[2] + tok, tot[3] + rej]
    print("TOTAL simple %d, tensor-needed %d, tensor-ok(derive) %d, rejected %d" % tuple(tot))


if __name__ == "__main__":
    main([R.DATA + x for x in ("coarse0.bin", "mid.bin", "fb1.bin")])
