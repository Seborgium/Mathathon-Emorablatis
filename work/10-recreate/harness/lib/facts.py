#!/usr/bin/env python3
"""facts.py -- turn a TSV of dotted-key / JSON-literal pairs into one nested JSON object.

usage: facts.py FACTS.tsv > log.json

Rules:
  * each line is  <dotted.key>\t<json literal>  ('#' comment lines and blanks are ignored);
  * a dotted key nests:  a.b.c  ->  {"a": {"b": {"c": ...}}};
  * a repeated leaf becomes a JSON array (in file order);
  * a leaf key ending in '+' always appends, so it is a list even with one element.

Exit 1 (having written the JSON anyway) if any line failed to parse, so that a
harness log is never silently missing a fact.
"""
import json
import sys


def put(root, dotted, value):
    parts = dotted.split('.')
    cur = root
    for part in parts[:-1]:
        nxt = cur.get(part)
        if not isinstance(nxt, dict):
            nxt = {}
            cur[part] = nxt
        cur = nxt
    leaf = parts[-1]
    append = leaf.endswith('+')
    if append:
        leaf = leaf[:-1]
    if append:
        cur.setdefault(leaf, [])
        if not isinstance(cur[leaf], list):
            cur[leaf] = [cur[leaf]]
        cur[leaf].append(value)
    elif leaf in cur:
        old = cur[leaf]
        cur[leaf] = old + [value] if isinstance(old, list) else [old, value]
    else:
        cur[leaf] = value


def main(argv):
    if len(argv) != 2:
        sys.stderr.write(__doc__)
        return 2
    root = {}
    bad = 0
    with open(argv[1], encoding='utf-8') as handle:
        for lineno, line in enumerate(handle, 1):
            line = line.rstrip('\n')
            if not line.strip() or line.lstrip().startswith('#'):
                continue
            key, sep, raw = line.partition('\t')
            if not sep:
                sys.stderr.write('facts.py: line %d: missing tab\n' % lineno)
                bad += 1
                continue
            try:
                value = json.loads(raw)
            except json.JSONDecodeError as exc:
                sys.stderr.write('facts.py: line %d: %r: %s\n' % (lineno, key, exc))
                bad += 1
                continue
            put(root, key.strip(), value)
    json.dump(root, sys.stdout, indent=2, sort_keys=True)
    sys.stdout.write('\n')
    return 1 if bad else 0


if __name__ == '__main__':
    sys.exit(main(sys.argv))
