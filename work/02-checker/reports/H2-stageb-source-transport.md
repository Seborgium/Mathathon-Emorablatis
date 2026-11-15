# Source-directed Stage-B transport for `bad10#0` (lead)

## Outcome and exact scope

The complete local cover already emitted in
`certdata/runs/h2-stageb/parent-bad10-0.json` is compatible with the producer's
parent-preloading direction. It is **one parent, Root-conditional**, not a full
refinement chain or a proof of `N(6)=3`.

The witness writes a relation from parent `P` to transformed child `Phi Q`.
Applying `Phi^{-1}` to both centres gives the source form from parent
`Phi^{-1}P` to child `Q`. The source permits a transformed parent on the same
grid (preprint (5.25)), and child spheres are covered up to the permitted
equivalences. Signed permutation maps are generally **not** involutions.

For all **902** edges in that witness, the two exact relations agree on

```
eta, sq, nq, total, nu0, lam, e, beta, sigma, D_at_ell
```

with exact rational values. Both reproduce the recorded `dq` and `dhat`.
Inverse and transpose-inverse applications on the actual phase/tangent data
are checked exactly. The 12 maps present in the witness happen not to use
transpose; one synthetic transpose map is tested only as an implementation
control, not as an additional covering edge.

Of these, 303 edges are used. Reclassifying the witness's 3,161 covered boxes
against freshly derived values gives again

```
14,641 = 11,480 outside + 3,161 covered + 0 open.
```

The **chosen-witness** minimum over all 3,161 closure inequalities is
`ell^2 - t_B^2 = 1.0513979010476847e-9`, stored as an exact numerator and
denominator in the machine object. The older value 1.968e-9 is the measured
minimum over the 1,452 boxes initially left open by the identity-only grid;
it is not the minimum over all 3,161 chosen cover boxes.

The proof object is
`certdata/runs/h2-stageb/parent-bad10-0-source-transport.json`
(SHA-256 `f487a4bfe6684bc0b1acd4d96123c2346998de81b78571c98612561955f562fb`,
268,131 bytes). Runtime is deliberately excluded from the hashed object.
The linked earlier witness's outside classification is retained; this bridge
re-checks the transported relations and all of its closed-box values, rather
than claiming a new independent full-stage execution.

## Controls that mattered

An initial test incorrectly used `Phi P` rather than `Phi^{-1}P` and failed at
edge 3. A map with an involutive row/column permutation was not enough:
non-involutive maps really change the relation. This example is retained as a
negative control (wrong direction does not reproduce the same `eta`). Replacing
the child's radius by a smaller value also fails the stated `D_at_ell` bound.
No failing test is converted into a covering conclusion.

## What is *not* discharged

- The transport preserves the mathematical Root obligations but does not supply
  the unresolved original Root/U, HV/LV or sufficient-`C` evidence.
- `Phi Q` is an admissible equivalence centre, **not a new stored fb1 record**.
  A separate invented 'Phi Q's own ledger' is not a hypothesis of Proposition
  5.7: its required argument concerns certified child spheres up to equivalence.
  Connecting this local cover to a later exclusion still requires the later
  child/root and graph evidence, not merely the map.
- The other two tested parents retain their earlier 48 and 175 residuals over
  the tested fb1 child set. The other 160 parents were not examined.
- No Stage-A cell tree, Stage-C exclusion matrix, terminal driver verdict, or
  complete input/upstream cover follows.

## Reproduce

```sh
python3 work/02-checker/src/stageb_transport/source_transport.py
sha256sum certdata/runs/h2-stageb/parent-bad10-0-source-transport.json
```

Measured after the swarm finished: 30.35 s wall, 30.48 s user, 0.02 s sys.
Treat this as one four-CPU VM's measurement, not an extrapolated overall cost.
