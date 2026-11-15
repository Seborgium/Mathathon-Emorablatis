#!/usr/bin/env bash
# One command for work unit 10 (independent record checker, team V wave W1).
#
#   bash work/10-recreate/harness/v2-check.sh [--published PATH] [--execution DIR]
#
# Defaults: the recorded saved-run execution directory is expected at
#   $MUB_EXECUTION (or .scratch/m1/gh/<preprint>/verification/saved-run/execution,
#   which harness/fetch-recorded.sh creates), and the published checker is taken
#   from .scratch/gh/upstream/check_records.py when present (black-box oracle).
set -euo pipefail
here=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
root=$(CDPATH= cd -- "$here/../../.." && pwd)
cd "$root"

execution=${MUB_EXECUTION:-}
published=""
sandbox=".scratch/m1/cases"
while [[ $# -gt 0 ]]; do
  case $1 in
    --execution) execution=$2; shift 2;;
    --published) published=$2; shift 2;;
    --sandbox) sandbox=$2; shift 2;;
    *) printf 'unknown argument: %s\n' "$1" >&2; exit 2;;
  esac
done

if [[ -z $execution ]]; then
  execution=$(find .scratch -maxdepth 8 -type d -path '*saved-run/execution' 2>/dev/null | head -1)
fi
[[ -n $execution && -d $execution ]] || { printf 'no recorded execution directory; run harness/fetch-recorded.sh\n' >&2; exit 2; }
if [[ -z $published && -f .scratch/gh/upstream/check_records.py ]]; then
  published=.scratch/gh/upstream/check_records.py
fi

args=(--execution "$execution" --sandbox "$sandbox" --logdir "$root/work/10-recreate/logs")
[[ -n $published ]] && args+=(--published "$published")
printf 'execution: %s\npublished: %s\n' "$execution" "${published:-<none>}"
python3 "$here/v2_check.py" "${args[@]}"
