#!/usr/bin/env bash
# One command to run the recorded MUB run through the replay harness.
#
#   bash work/10-recreate/harness/replay.sh selftest
#   bash work/10-recreate/harness/replay.sh control
#   bash work/10-recreate/harness/replay.sh replay <build-dir> [--only REGEX] [--timeout S]
#
# selftest  replays the recorded artefacts against themselves; must PASS.
# control   seeded corruptions of the recorded set; every one must be caught.
# replay    executes the 100 recorded argv against <build-dir>/{arun,brun,crun,covrun}
#           chaining each command's own outputs into the next command's inputs.  The
#           full 100 are hours of CPU; use --only to select a subset (see budget).
#
# Exit status = the driver's.  The last line printed is the machine-readable verdict
# with the summary log path.
set -euo pipefail
here="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
repo="$(cd "$here/../../.." && pwd)"
cache="${V_CACHE:-$repo/work/10-recreate/crew/m3/saved-run}"
logs="${V_LOGS:-$repo/work/10-recreate/logs}"
export LANG=C LC_ALL=C

if [ "${1:-}" = "" ]; then sed -n '2,16p' "$0"; exit 2; fi
mode="$1"; shift

# The recorded artefact set is the definition of the expected outputs: make sure the
# cache is present and untouched before replaying anything.
if [ -f "$here/saved-run.manifest.json" ]; then
  python3 "$here/fetch_saved_run.py" --cache "$cache" --check >/dev/null \
    || { echo "FAIL: recorded artefact cache does not match saved-run.manifest.json" >&2
         python3 "$here/fetch_saved_run.py" --cache "$cache" --check >&2 || true
         echo "re-run: python3 $here/fetch_saved_run.py --cache $cache" >&2; exit 2; }
else
  echo "no manifest; fetching the published saved-run first" >&2
  python3 "$here/fetch_saved_run.py" --cache "$cache" >/dev/null
fi

case "$mode" in
  replay)
    bin="${1:-}"; [ -n "$bin" ] || { echo "replay needs a build directory" >&2; exit 2; }
    shift ;;
  selftest|control) bin="" ;;
  *) echo "unknown mode $mode" >&2; exit 2 ;;
esac

args=(python3 "$here/replay.py" "$mode" --cache "$cache" --logs "$logs")
[ "$mode" = replay ] && args+=(--bin "$bin")
exec "${args[@]}" "$@"
