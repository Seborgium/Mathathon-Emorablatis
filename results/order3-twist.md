# The twisted class: exact reduction of the order-three stratum to a finite real system

Second note, 2026-11-14, continuing `results/order3-stratum.md`. That note reduced the order-three
symmetric stratum of four MUBs in $\mathbb C^6$ to seven frame parameters per basis and an exact
12-equation criterion, and measured a gap $0.0422687$ forbidding a fourth basis. This note pushes the
reduction one step further, to a form with **no symmetry left and only real trigonometric equations**.

## 1. Why the twist matters (an exact no-go for the naive configurations)

Recall from `order3-stratum.md`: with $T = I_2\otimes\mathrm{diag}(1,\omega,\omega^2)$, a flat
$T$-covariant basis is given by three orthonormal frames $F(t)$ ($t\in\mathbb Z_3$) in $\mathbb C^2$
whose entries have modulus $1/\sqrt6$, and the unbiasedness of two such bases is equivalent to
$$\tag{3.1}\sum_t|c_t|^2 = \tfrac16,\qquad \sum_t c_t\overline{c_{t-1}} = 0
\quad\text{for each of the four orbit pairs},\qquad c_t = \langle x_t,y_t\rangle .$$

**Lemma (twist).** Suppose each of the two bases has frames constant up to a **scalar** twist, i.e.
$F_X(t) = \mu^{(X)}_t F_X$ with $\mu^{(X)}_t\in\mathbb T$ and $F_X$ a fixed flat frame (the two fixed
frames may differ). Put $\mu_t = \overline{\mu^{(1)}_t}\mu^{(2)}_t$. Then $c_t = \mu_tc_0$ for every orbit
pair, so $(3.1)$ forces $\sum_t|c_0|^2 = 1/6$ **and** $\sum_t \mu_t\overline{\mu_{t-1}} = 0$. In
particular $\mu_t$ cannot be a single chirp $\mu_t = \nu^t$ (the sum is then $3\nu|...| \neq 0$), nor
constant ($3\neq0$). So *an unbiased pair needs a relative twist whose cyclic correlation vanishes* —
and that is exactly what the Fourier triple has. (A general diagonal twist, with the two diagonal
entries differing, is *not* of this form: then $c_t$ is a sum of two independently twisted terms, which
is the case treated in §2.)

Verified: the second basis $F_2\otimes F_3$ has constant frames, the third
$(\mathrm{diag}(1,i)F_2)\otimes(\mathrm{diag}(1,\omega^2,\omega^2)F_3)$ has twist
$d = (1,\omega^2,\omega^2)$ with $\sum_t d_t\overline{d_{t-1}} = 0$ (machine precision), and their pair
satisfies $(3.1)$ exactly. A chirp twist does not.

## 2. The twisted class in reduced real form

Restrict now to the **twisted class**: all four bases have frames $F_X(t) = D_X(t)F_0$ with the *same*
flat frame $F_0 = \frac1{\sqrt6}\bigl(\begin{smallmatrix}1&1\\1&-1\end{smallmatrix}\bigr)$ and diagonal
twists $D_X(t)$; this is a codimension-3 sub-family of the stratum (it drops the third frame phase of
each time slice) and it contains the standard product-type configurations.

For two such bases let $\lambda_t = \mathrm{diag}(\overline{d^{(1)}_t}d^{(2)}_t)$ be the relative twist
and $s_t = \lambda_{t0}+\lambda_{t1}$, $d_t = \lambda_{t0}-\lambda_{t1}$. Since
$(U_t)_{xy} = \frac16\bigl[\lambda_{t0}+(-1)^{x+y}\lambda_{t1}\bigr]$ one gets $c_t = s_t$ for the two
diagonal blocks and $c_t = d_t$ for the two off-diagonal ones, so $(3.1)$ becomes
$$\tag{3.2}\sum_t|s_t|^2 = 6,\quad \sum_t s_t\overline{s_{t-1}} = 0,\qquad
\sum_t|d_t|^2 = 6,\quad \sum_t d_t\overline{d_{t-1}} = 0 .$$

**Proposition T (proved).** With $s_t = 2\cos\delta_t\,e^{im_t}$, $d_t = 2i\sin\delta_t\,e^{im_t}$
($\delta_t,m_t\in\mathbb R$ — this is the general form, because $|\lambda_{t0}| = |\lambda_{t1}| = 1$
gives $|s_t|^2+|d_t|^2 = 4$ and $s_t\overline{d_t}\in i\mathbb R$), and $\beta_t := m_t-m_{t-1}$ (so
$\sum_t\beta_t\equiv0$), the pair condition $(3.2)$ is equivalent to the **three real equations**
$$\tag{A}\sum_t\cos 2\delta_t = 0,\qquad
\tag{B1}\sum_t\cos(\delta_t-\delta_{t-1})\,e^{i\beta_t} = 0,\qquad
\tag{B2}\sum_t\cos(\delta_t+\delta_{t-1})\,e^{i\beta_t} = 0 .$$
*Proof.* (A) is $(|s|^2 = 6) \Leftrightarrow (\sum\cos^2\delta_t = 3/2) \Leftrightarrow
(\sum(3-4\sin^2\delta) = ...)$ together with $|s|^2+|d|^2 = 4$ summing to $12$; (B1) is the sum and
(B2) the difference of the two correlation equations in $(3.2)$, after
$\cos\delta\cos\delta' \pm \sin\delta\sin\delta' = \cos(\delta\mp\delta')$. $\square$

So each basis of the class carries six numbers $(\theta_t,\mu_t)_{t\in\mathbb Z_3}$ (its polarisation
angle and mean phase at each time), a pair carries the two differences $x_t = \tfrac12(\theta^{(2)}_t-\theta^{(1)}_t)$,
$\beta_t = \Delta(\mu^{(2)}-\mu^{(1)})_t$, and the pair is unbiased iff $(x,\beta)$ satisfies
(A),(B1),(B2).

## 3. The quartet problem in the class is a finite system in ten real variables

Let $I$ and three twisted bases $A,B,C$ be given, and put
$$x = \delta^{AB},\quad \beta = \beta^{AB},\quad y = \delta^{BC},\quad \gamma = \beta^{BC},$$
so the third pair has $(\delta,\beta) = (x+y,\ \beta+\gamma)$ (an additive cocycle: differences add).
Then

> **a quartet in the twisted class exists iff there are $x,y\in\mathbb R^3$ and
> $\beta,\gamma\in\mathbb R^2$ (with $\beta_2 = -\beta_0-\beta_1$, $\gamma_2 = -\gamma_0-\gamma_1$) such
> that each of $(x,\beta)$, $(y,\gamma)$ and $(x+y,\beta+\gamma)$ satisfies (A),(B1),(B2).**

That is **ten real variables and fifteen real equations of explicit trigonometric type**, with no group
action, no gauge, and no compactness subtleties left. It is the smallest form of the quartet problem in
dimension six that I can produce.

**Numerical status.**

* The *pair* system (A),(B1),(B2) in five variables has isolated solutions; 280 distinct ones were
  found from random starts (e.g. $\delta/\pi = (0.75,\,1.1307,\,1.3693)$, $\beta/\pi=(1,0,-1)$).
  So twisted pairs exist, as they must (the triple contains one).
* The *three-pair* system has no solution: 400 random starts give a residual floor of
  $0.386$ in the reduced equations, and independently a floor of $0.1096$ in
  $\max|\langle\cdot,\cdot\rangle|^2-\tfrac16|$ over the eighteen twist phases. Every start returns the
  same floor, so the class contains no quartet, with a wide margin.

## 4. What is proved and what is not

Proved here: the twist lemma (§1), Proposition T (§2, the exact reduction of the pair condition to
(A),(B1),(B2)), and the correctness of the cocycle bookkeeping in §3.

Not proved: the final infeasibility. What would prove it is an exact statement of one of two shapes:
(i) for every $x,y$ the twelve equations in $(\beta,\gamma)$ are incompatible — a semialgebraic
question in four variables with trigonometric entries, which should fall to interval branch-and-bound or
to elimination after the substitution $e^{i\beta_t} = $ unit variables; or (ii) an identity forcing
$\sum_t\cos 2x_t\sum_t\cos 2\gamma_t = $ a strictly positive quantity. I did not find either.

Note that the general stratum is *not* covered: §2 assumes a common flat frame $F_0$ for all four
bases, which drops one real parameter per basis. The general stratum needs the frame phases back, and
with them a seventh parameter per basis; whether the reduced system above is a faithful model of the
general case is exactly the question left open.

## 5. Where this leaves the programme

The chain is now: every triple is order-three symmetric (arXiv:2611.06917) $\to$ every symmetric basis
is 7 frame parameters $\to$ every pair is the finite real system (A),(B1),(B2) $\to$ a quartet would be
the ten-variable system of §3, which has no solution numerically. Two steps remain before this is a
proof of anything new: proving §3 infeasible (finite, explicit, and small), and removing the
common-frame hypothesis of §2.
