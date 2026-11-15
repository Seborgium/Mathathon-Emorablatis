#!/bin/sh
# Recompute every number used in mub-step{2,3,4,5}-example.tex.
# Each script prints a table of key/value rows; the documents quote those rows.
set -e
cd "$(dirname "$0")"
python3 mubexact.py        | tee out/step0-selftest.txt
python3 step2_example.py   | tee out/step2.txt
python3 step3_example.py   | tee out/step3.txt
python3 step4_example.py   | tee out/step4.txt
python3 step5_example.py   | tee out/step5.txt
