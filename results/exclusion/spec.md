# Cell exclusion certificates for Stage A: exact specification

Source: *The maximum number of mutually unbiased bases in dimension six*, 24 Sep 2026.
Sections 3.1-3.6 (printed pp. 12-20), Lemma 3.9, Corollary 3.10, Appendix A.
Text extract with layout: `.scratch/rt/paper.txt` (Section 3.5 begins at line 944,
Lemma 3.9 and (3.29) at lines 1071-1090, Corollary 3.10 at 1103).

Everything below is a restatement of the paper's own definitions, made explicit so that a
certificate can be recomputed from scratch. Nothing here is new mathematics.

## 1. Cell data

A *cell* consists of a seed centre and a unitary-cell midpoint.

Seed centre: nine unit-modulus complex numbers `a, b0..b3, c0..c3` (the entries at row-major
phase positions (7,8,9,10,11,13,19,25,31) of the 36-phase array), taken as exact reals.
Seed radius in cycles `rs = .0320001`, radians `Rs = 2*pi*rs = 0.2010619...`.
Unitary-cell midpoint `U in U(2)`; angular half-width `h = pi/Nu` with `Nu` the bin count
(`Nu` in {16,32,64,...,512} in the run of Section 3.7).

```
E0 = [[1,1],[1,a]]                       (2x2)
B0 = [[1,1,1,1],[b0,b1,b2,b3]]           (2x4)
C0 = [[1,c0],[1,c1],[1,c2],[1,c3]]       (4x2, row i = (1,ci))
GB = B0^* (B0 B0^*)^-1                   (4x2)
GC = C0 (C0^* C0)^-1                     (4x2)
KB : 4x2, orthonormal columns, ran KB = ker B0
KC : 4x2, orthonormal columns, ran KC = ker C0^*
PK = KB KB^*,  PB = I-PK,  PC = I - KC KC^*
mB = sigma_min(B0), mC = sigma_min(C0), m = min(mB,mC)
A0 = sqrt(2 + |1+a|),  A* = min(2, A0+Rs)
D  = -C0 E0^* GB^* + sqrt(6) KC U KB^*   (4x4)     [the comparison block, (3.15)]
q  = Rs^2 (1 + (A*^2+6)/mC^2)                      [= (3.10)]
p  = sqrt(q) / (sqrt(6) + sqrt(6-q))               [= (3.11), needs q<6]
z  = sqrt( (Rs (sqrt6 + A*)/m)^2 + (6h+p)^2 )      [= (3.19)]
L  = max(sqrt6, ||C0||op * sqrt(1+(A0/mB)^2))      [= (3.20)]
eoff = Rs^2 (L+A0+1)/(2m) + z Rs/m                 [= (3.25)]
Er = sqrt( eoff^2 + ((sqrt6*42/2) h^2 + p)^2 )     [= (3.24)]
```

## 2. The twenty equations

Seed first variations: `E1` has zero entries except `[1,1] = i*a*sa`; `B1` has zero entries
except `[1,j] = i*bj*s_bj`; `C1` has zero entries except `[i,1] = i*ci*s_ci`.
`dU[theta]` is the four-dimensional angular differential of U at midpoint U (definition in
(3.12)-(3.13) and the paragraph after Lemma 3.4): alpha-derivative `iU`; beta-derivative
`diag(i U00, -i U11)`; gamma-derivative off-diagonal `(i U01, -i U10)`, zero diagonal;
t-derivative differentiates the sine and cosine factors of (3.12).
`theta = (theta_alpha, theta_t, theta_beta, theta_gamma)` in radians, `|theta_j| <= h`.

```
J(s,theta) = (-C1 E0^* - C0 E1^* - D B1^*) GB^*
             + GC (-E0^* B1 - C1^* D) PK
             + sqrt(6) KC dU[theta] KB^*                    (3.23)  [4x4, linear in (s,theta)]
```

Flatness rows (16), for 0<=i,j<4:
```
c_ij  = (|D_ij|^2 - 1)/2
Jbar_ij(s,theta) = Re( conj(D_ij) * J_ij(s,theta) )
exact:  0 = c_ij + Jbar_ij + Re(conj(D_ij) R_ij) + |Z_ij|^2/2 ,   Z = J(s,theta)+R, ||R||_F <= Er
```
Seed-sum rows (2 complex, i.e. 4 real), with `s = (sa,s_b0..s_b3,s_c0..s_c3)`:
```
cX = (1 + a + sum_j b_j)/i ,        JX s = a sa + sum_j b_j s_bj
cY = (1 + a + sum_i c_i)/i ,        JY s = a sa + sum_i c_i s_ci
exact:  cX + JX s + rhoX = 0 ,  cY + JY s + rhoY = 0 ,  |rhoX|,|rhoY| <= Rs^2/2    (3.27)
```
`c_all in R^20` = (c_00..c_33 row-major, Re cX, Im cX, Re cY, Im cY);
`Jall in R^20x13` = rows 1-16: the real linear forms `Jbar_ij` in (s,theta);
rows 17-20: Re and Im of `JX`,`JY` (zero theta block).

## 3. The certificate (Lemma 3.9)

For any `y in R^20`, split as `yX,yY in R^2` and `yD in R^16` (4x4 matrix, row-major), and put
`g = Jall^T y = (gs, gtheta) in R^9 x R^4`. Then every feasible completion in the cell satisfies

```
y . c_all  <=  Rs*||gs||  +  h*||gtheta||_1  +  Er*||D o yD||_F
             + (1/2) z^2 max(0, max_ij(-yD_ij))  +  (1/2) Rs^2 (||yX||+||yY||)          (3.29)
```

Write the right-hand side as `B(y)`. A cell is excluded if `y.c_all > B(y)` for some y
(Corollary 3.10); all terms are positively homogeneous in y, so only the direction matters.
Independently, the norm test (3.26) `sum_ij (|D_ij|-1)^2 <= z^2` also excludes.

## 4. What is wanted

1. **Structure of the direction problem.** `y |-> y.c_all - B(y)` is a difference of a linear
   functional and a sum of five (semi)norms of linear images of y. Determine the resulting
   optimization problem, its dual, the optimal direction, and the geometry of the set of
   excluding directions.
2. **A stronger inequality.** (3.29) bounds `Re(conj(D)R)` and `|Z_ij|^2` separately. Use the
   exact identity `|D_ij+Z_ij| = 1` for the feasible set instead, and derive a certificate whose
   right-hand side is strictly smaller on a positively described class of directions.
3. **Scaling.** How does the maximal margin scale with `h` and `Rs`, i.e. which cell level `Nu`
   suffices? This decides the number of subdivisions.
4. **Transported certificates.** Symmetries of the construction (rephasing gauge, `Z_6` or
   other discrete symmetries, unitarity of the U(2) parametrisation) and continuity of the
   margin in the cell data: which families of cells does one certificate exclude?

## 5. Verification standard

A candidate direction `y` is a *certificate* only when `y.c_all > B(y)` has been checked in
rigorous arithmetic (outward-rounded interval arithmetic at 60+ decimal digits, or exact
rational arithmetic). Discovery may be heuristic; the final inequality may not.
The authors' proposing routine (`trial::pass`: regularised linear solves plus weight updates)
and their verifier (`trial::certificate`) are described in the paper but their source is not
used here; any reimplementation must be labelled as such.
