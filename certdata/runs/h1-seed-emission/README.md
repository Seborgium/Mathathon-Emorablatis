# Seed witness emission run

Command: `src/emit/covrun-emit certdata/runs/h1-seed-emission/centers.txt certdata/runs/h1-seed-emission/seed.wit`

Binary stream layout is documented at the top of `src/emit/covout.cpp`. Prefix test:
2 X tuples, 158 pairs, 9 fresh centres, 136 cheap reuses, 13 dual reuses. Prefix
centre lines are preserved byte for byte; exact cheap reuse and previous-centre checks pass.
Full-run acceptance requires archived centres byte identity, 151,744,086 checked pairs,
249,878 fresh centres and independent evaluation of all dual witnesses.
This run alone is not an exact certificate.
