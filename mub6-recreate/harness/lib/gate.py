#!/usr/bin/env python3
"""gate.py -- condense a detailed harness log into a gate record.

usage: gate.py UNIT DETAILED_LOG OUT_JSON CRITERION

The gate record names the unit, the criterion it tests, pass/fail, the evidence
(the detailed log), the toolchain that produced it, and the artefact hashes, so
that gates.md can point at one small file per rung.  Exits 0 iff pass is true.
"""
import json
import sys


def dig(obj, *path, default=None):
    for key in path:
        if not isinstance(obj, dict) or key not in obj:
            return default
        obj = obj[key]
    return obj


def main(argv):
    if len(argv) != 5:
        sys.stderr.write(__doc__)
        return 2
    unit, detailed, out, criterion = argv[1:]
    with open(detailed, encoding='utf-8') as handle:
        log = json.load(handle)
    artefacts = {}
    for name, entry in (dig(log, 'artefacts', default={}) or {}).items():
        if isinstance(entry, dict) and 'sha256' in entry:
            artefacts[name] = {'sha256': entry['sha256'], 'bytes': entry.get('bytes')}
    checks = dig(log, 'checks', default={}) or {}
    failed = sorted(k for k, v in checks.items() if v == 'fail')
    record = {
        'unit': unit,
        'criterion': criterion,
        'pass': bool(log.get('pass')) and not failed,
        'evidence': {'detailed_log': detailed, 'out_dir': log.get('out', {}).get('dir')
                     or log.get('out_dir')},
        'toolchain': {
            'compiler': dig(log, 'toolchain', 'compiler', default={}),
            'cpu': dig(log, 'toolchain', 'cpu', default={}),
            'glibc': dig(log, 'toolchain', 'glibc'),
            'flags': dig(log, 'toolchain', 'flags', default={}),
        },
        'checks': checks,
        'failed_checks': failed,
        'failures': dig(log, 'failures', default={}) or {},
        'artefacts': artefacts,
        'probe': dig(log, 'probe', default={}),
        'finished_utc': log.get('finished_utc'),
    }
    with open(out, 'w', encoding='utf-8') as handle:
        json.dump(record, handle, indent=2, sort_keys=True)
        handle.write('\n')
    return 0 if record['pass'] else 1


if __name__ == '__main__':
    sys.exit(main(sys.argv))
