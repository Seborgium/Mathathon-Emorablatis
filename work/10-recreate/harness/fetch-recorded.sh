#!/usr/bin/env bash
# Fetch the recorded saved-run execution directory (data/, results/, commands.json,
# check_records.py) that the published preprint ships under
#   preprints/The-maximum-number-of-mutually-unbiased-bases-in-dimension-six-*
#    /verification/saved-run/execution
# It is NOT in this repository: only data/centers.txt is cached in .scratch/gh/data.
# A blobless, sparse, depth-1 clone fetches exactly those blobs (about 80 MB).
#
#   bash work/10-recreate/harness/fetch-recorded.sh [destination]   # default .scratch/m1/gh
#
# Afterwards:  bash work/10-recreate/harness/v2-check.sh
set -euo pipefail
here=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
root=$(CDPATH= cd -- "$here/../../.." && pwd)
dest=${1:-$root/.scratch/m1/gh}
preprint='preprints/The-maximum-number-of-mutually-unbiased-bases-in-dimension-six-September-24-2026/verification/saved-run/execution'
[[ -d $dest/.git ]] || git clone --depth 1 --filter=blob:none --no-checkout --sparse \
    https://github.com/openai/math.git "$dest"
cd "$dest"
git sparse-checkout set "$preprint/data" "$preprint/results"
git checkout -- .
exec_dir=$dest/$preprint
[[ -f $exec_dir/commands.json ]] || { printf 'commands.json missing in %s\n' "$exec_dir" >&2; exit 1; }
printf '%s\n' "$exec_dir"
du -sh "$exec_dir/data" "$exec_dir/results"
