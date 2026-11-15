# harness/lib/common.sh -- shared helpers for the V harness.  Sourced, never executed.
#
# Sets, from this file's own location (<repo>/work/10-recreate/harness/lib/common.sh):
#   HARNESS  <repo>/work/10-recreate/harness
#   REPO     the project root
# and defines the check/fact plumbing every harness script uses to write one
# machine-readable JSON log.  Callers must run under `set -euo pipefail` and with
# LANG=C LC_ALL=C; callers own $FACTS (the TSV) and choose the output path.

HARNESS=$(CDPATH= cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)
REPO=$(CDPATH= cd -- "$HARNESS/../../.." && pwd)

FAILS=0
CHECKS=0

die() { printf 'FAIL %s\n' "$*" >&2; exit 2; }
need() { command -v -- "$1" >/dev/null 2>&1 || die "missing required tool: $1"; }

# json_escape <string> -- escape for a JSON string body (no surrounding quotes added).
json_escape() {
    local s=$1
    s=${s//\\/\\\\}
    s=${s//\"/\\\"}
    s=${s//$'\t'/\\t}
    s=${s//$'\r'/\\r}
    s=${s//$'\n'/\\n}
    printf '%s' "$s"
}

# fact <dotted.key> <json literal>     -- e.g. fact checks.gcc.status '"pass"'
fact() { printf '%s\t%s\n' "$1" "$2" >>"$FACTS"; }
# fact_s <dotted.key> <string>         -- string value, escaped
fact_s() { fact "$1" "\"$(json_escape "$2")\""; }
# fact_f <dotted.key> <file>           -- a path, plus its sha256/size siblings
fact_file() {
    local key=$1 path=$2
    fact_s "$key.path" "$path"
    if [[ -f $path ]]; then
        fact_s "$key.sha256" "$(sha256_of "$path")"
        fact "$key.bytes" "$(size_of "$path")"
    else
        fact "$key.missing" true
    fi
}

pass_check() { CHECKS=$((CHECKS + 1)); fact_s "checks.$1" "pass"; }
# fail_check <name> <detail> -- record a failure; it does not abort by itself.
fail_check() {
    CHECKS=$((CHECKS + 1))
    FAILS=$((FAILS + 1))
    fact_s "checks.$1" "fail"
    fact_s "failures.$1" "$2"
    printf 'CHECK-FAIL %s: %s\n' "$1" "$2" >&2
}

now_utc() { date -u +%Y-%m-%dT%H:%M:%SZ; }
stamp() { date -u +%Y%m%dT%H%M%SZ; }
# microseconds since epoch, as an integer (bash's EPOCHREALTIME has a '.' in it)
now_us() { local t=${EPOCHREALTIME//[!0-9]/}; printf '%s' "$t"; }
ms_since() { printf '%s' $(( ($(now_us) - $1) / 1000 )); }

sha256_of() { sha256sum -- "$1" | cut -d' ' -f1; }
size_of() { stat -c %s -- "$1"; }

# emit_json <facts-tsv> <log-path> -- atomically write the JSON log.
emit_json() {
    local facts=$1 out=$2
    mkdir -p -- "$(dirname -- "$out")"
    python3 -- "$HARNESS/lib/facts.py" "$facts" >"$out.tmp" || {
        printf 'FAIL facts.py rejected a fact; partial JSON left at %s\n' "$out.tmp" >&2
        return 1
    }
    mv -f -- "$out.tmp" "$out"
}

# head_of_file <path> <bytes> -- first bytes of a text file, as a string fact body
head_of_file() { head -c "$2" -- "$1" 2>/dev/null || true; }

# unique_log_path <wanted-path> -- never overwrite a log: logs/ is append-only, and
# three members share it.  Returns <path>, or <path-with-.2>/.3/... if it exists.
unique_log_path() {
    local want=$1 n=2 cand=$1
    if [[ -e $want ]]; then
        while [[ -e ${want%.json}.$n.json ]]; do n=$((n + 1)); done
        cand=${want%.json}.$n.json
    fi
    printf '%s' "$cand"
}
