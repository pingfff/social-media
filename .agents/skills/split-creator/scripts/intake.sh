#!/usr/bin/env bash
# Interactive intake questionnaire for the split-creator skill.
#
# Terminal form (interactive):
#   bash .agents/skills/split-creator/scripts/intake.sh
#
# Batch form (non-interactive; used by the agent when it interviews the
# user in-chat via AskUserQuestion and then writes the profile through
# this same script so validation/marking is identical):
#   bash .agents/skills/split-creator/scripts/intake.sh --batch name=ping q1=d q4="chest and back" ...
# Keys: name, q1..q20. Missing keys fall back to the question default
# (each fallback is printed; defaults are disclosed in the program's
# Assumptions section). Answer syntax per question is the same as the
# terminal form: option letter (+ optional note), ns, !free text.
#
# Both modes write a SELF-CONTAINED lifter profile to
# programs/profiles/<name>.md: option answers are validated against the
# option set and resolved to their meanings, so the profile is readable
# without the questionnaire.
#
# NOTE: written for bash 3.2 (stock macOS) — no assoc arrays, no ${var,,}.

set -euo pipefail
cd "$(dirname "$0")/../../../.."   # repo root

MODE=interactive
BATCH_TMP=""
if [[ "${1:-}" == "--batch" ]]; then
  MODE=batch
  shift
  BATCH_TMP="$(mktemp -t intake_batch)"
  trap 'rm -f "$BATCH_TMP"' EXIT
  for a in "$@"; do
    k="$(printf '%s' "${a%%=*}" | tr '[:upper:]' '[:lower:]' | sed 's/^[[:space:]]*//;s/[[:space:]]*$//')"
    v="${a#*=}"
    [[ "$a" == *=* ]] || { printf 'error: --batch items must be key=value, got "%s"\n' "$a" >&2; exit 2; }
    [[ "$k" =~ ^(name|q([1-9]|1[0-9])|q20)$ ]] || { printf 'error: unknown batch key "%s"\n' "$k" >&2; exit 2; }
    printf '%s=%s\n' "$k" "$v" >> "$BATCH_TMP"
  done
fi

batch_lookup() { # $1=key -> value or empty
  grep "^$1=" "$BATCH_TMP" | head -n 1 | cut -d= -f2- || true
}

trim() { printf '%s' "$1" | sed 's/^[[:space:]]*//;s/[[:space:]]*$//'; }

RAW=""
obtain() { # $1=key $2=prompt $3=default -> sets $RAW (default applied)
  local key=$1 prompt=$2 default=$3
  if [[ "$MODE" == batch ]]; then
    RAW="$(batch_lookup "$key")"
    if [[ -z "$RAW" ]]; then
      printf '  - %s: not provided -> default "%s"\n' "$key" "$default"
      RAW="$default"
    fi
  else
    read -rp "$prompt [$default]: " RAW || true
    RAW="$(trim "${RAW:-$default}")"
  fi
}

bad() { # invalid answer: re-prompts in interactive, aborts in batch
  printf '  !! %s\n' "$1" >&2
  if [[ "$MODE" == batch ]]; then
    printf 'error: batch intake aborted — fix the answer and re-run\n' >&2
    exit 2
  fi
}

ask_free() { # $1=var/key  $2=prompt  $3=default
  local var=$1 prompt=$2 default=$3
  while :; do
    obtain "$var" "$prompt" "$default"
    RAW="$(trim "$RAW")"
    if [[ "$RAW" == "ns" ]]; then
      printf -v "$var" '%s [ns: defaulted]' "$default"
      return
    fi
    if [[ -n "$RAW" ]]; then
      printf -v "$var" '%s' "$RAW"
      return
    fi
    bad 'empty answer not allowed here (use ns if unsure)'
  done
}

ask_opt() { # $1=var/key  $2=prompt  $3=default-letter  then letter=meaning pairs
  local var=$1 prompt=$2 default=$3; shift 3
  local -a keys=() vals=()
  local pair i valid="" re letter note resolved
  for pair in "$@"; do
    keys+=("${pair%%=*}")
    vals+=("${pair#*=}")
    valid="${valid}${pair%%=*}"
  done
  re="^([${valid}])( .*)?$"
  while :; do
    obtain "$var" "$prompt" "$default"
    RAW="$(printf '%s' "$RAW" | sed 's/^[[:space:]]*//;s/[[:space:]]*$//')"
    RAW="$(printf '%s' "$RAW" | tr '[:upper:]' '[:lower:]')"
    case "$RAW" in
      ns)
        resolved=""
        for i in "${!keys[@]}"; do
          if [[ "${keys[$i]}" == "$default" ]]; then resolved="${vals[$i]}"; fi
        done
        printf -v "$var" '%s [ns: defaulted]' "$resolved"
        return
        ;;
      \!*)
        printf -v "$var" '%s [free text]' "${RAW#!}"
        return
        ;;
    esac
    if [[ "$RAW" =~ $re ]]; then
      letter="${BASH_REMATCH[1]}"
      note="${BASH_REMATCH[2]}"
      note="${note# }"
      resolved=""
      for i in "${!keys[@]}"; do
        if [[ "${keys[$i]}" == "$letter" ]]; then resolved="${vals[$i]}"; fi
      done
      if [[ -n "$note" ]]; then
        printf -v "$var" '%s (%s)' "$resolved" "$note"
      else
        printf -v "$var" '%s' "$resolved"
      fi
      return
    fi
    bad "\"$RAW\" matches no option. Use one of [$valid] (a note may follow the letter, e.g. \"b any days\"), ns, or !free-text."
  done
}

ask_num() { # $1=var/key  $2=prompt  $3=default  $4=valid-regex (unanchored)
  local var=$1 prompt=$2 default=$3 spec=$4 full
  full="^(${spec})$"
  while :; do
    obtain "$var" "$prompt" "$default"
    RAW="$(trim "$RAW")"
    if [[ "$RAW" == "ns" ]]; then
      printf -v "$var" '%s [ns: defaulted]' "$default"
      return
    fi
    if [[ "$RAW" =~ $full ]]; then
      printf -v "$var" '%s' "$RAW"
      return
    fi
    bad "\"$RAW\" is not valid here (expected: $spec). Try again or use ns."
  done
}

if [[ "$MODE" == interactive ]]; then
  echo "=== Workout Split Creator — Lifter Intake ==="
  printf 'Enter accepts the [default]. ns = not sure (default used, marked).\n'
  printf 'Option questions take a letter (+ optional note, e.g. "b any days"),\n'
  printf 'or !free-text when no option fits. Invalid input re-prompts.\n\n'
else
  echo "=== Workout Split Creator — Batch Intake ==="
fi

ask_free name "Profile name (single word)" "me"
ask_opt  q1 "Q1*  Training age: a)none b)<1yr c)1-3yr d)3-10yr e)10+yr" "c" \
  "a=none" "b=under 1 yr" "c=1-3 yrs" "d=3-10 yrs" "e=10+ yrs"
ask_free q2 "Q2   Age" "30"
ask_opt  q3 "Q3*  Goal: a)hypertrophy b)strength c)recomp d)general fitness" "a" \
  "a=hypertrophy" "b=strength" "c=recomp" "d=general fitness"
ask_free q4 "Q4   Priority/lagging muscles (or 'none')" "none"
ask_num  q5 "Q5*  Days per week (2/3/4/5/6)" "4" "[2-6]"
ask_num  q6 "Q6*  Max session length (45/60/75/90 min)" "60" "45|60|75|90"
ask_opt  q7 "Q7   Schedule: a)fixed weekdays b)flexible/rolling (+ day notes OK after letter)" "a" \
  "a=fixed weekdays" "b=flexible/rolling"
ask_free q8 "Q8   Current split + months on it (or 'none')" "none"
ask_free q9 "Q9   Weekly hard sets per muscle (or 'unknown')" "unknown"
ask_free q10 "Q10  Last 3 mo: progressed / stalled" "-"
ask_opt  q11 "Q11  End-of-session: a)fresh b)drained c)overruns 1-1.5h" "a" \
  "a=fresh" "b=drained" "c=sessions overrun 1-1.5 h"
ask_opt  q12 "Q12  Near-failure habits: a)0-3 RIR regularly b)stop short c)never" "a" \
  "a=regularly reaches ~0-3 RIR" "b=usually stops well short" "c=never near failure"
ask_opt  q13 "Q13  Recovery budget: a)good b)average c)poor" "b" \
  "a=good (7h+ sleep, low stress)" "b=average" "c=poor (short/poor sleep or high stress)"
ask_opt  q14 "Q14  Calories: a)surplus b)maintenance c)deficit" "b" \
  "a=surplus" "b=maintenance" "c=deficit"
ask_opt  q15 "Q15* Equipment: a)full gym b)basic gym c)home d)minimal (+ machines OK after letter)" "a" \
  "a=full commercial gym" "b=basic gym (barbells/DBs/few machines)" "c=home setup" "d=minimal (DBs/bands)"
ask_free q16 "Q16* Injuries/mobility limits (or 'none')" "none"
ask_free q17 "Q17  Exercise likes/dislikes (disliked: ... / favorites: ...)" "no strong feelings"
ask_opt  q18 "Q18  Frequency preference: a)often b)rare+focused" "a" \
  "a=enjoys hitting muscles often" "b=prefers rare and focused"
ask_opt  q19 "Q19  Deload preference: a)scheduled b)by feel c)spread-week" "a" \
  "a=scheduled" "b=by feel" "c=spread-week (frequency deload)"
ask_free q20 "Q20  Anything else to respect" "-"

mkdir -p programs/profiles
out="programs/profiles/${name}.md"

{
  cat <<EOF
# Lifter Profile: $name

Filled via ${MODE} intake on $(date +%Y-%m-%d). Option answers are resolved to
their meanings; entries marked \`[ns: defaulted]\` or \`[free text]\` deviate
from the option schema and must be disclosed in the generated program's
Assumptions section.

## A. Who
- Training age: $q1 | Age: $q2

## B. Goal
- Primary goal: $q3
- Priority muscles: $q4

## C. Schedule
- Days/week: $q5 | Max session: $q6 min
- Schedule type / day notes: $q7

## D. Current training
- Current split: $q8
- Weekly sets/muscle: $q9
- Progressed/stalled (3 mo): $q10
- Session-end state: $q11 | RIR habits: $q12

## E. Recovery & calories
- Recovery budget: $q13 | Calories: $q14

## F. Equipment
- Access + machines: $q15

## G. Constraints & tastes
- Injuries/mobility: $q16
- Exercise likes/dislikes: $q17

## H. Preferences
- Frequency: $q18 | Deload: $q19
- Notes: $q20
EOF
} > "$out"

printf '\nProfile written to %s\n' "$out"
if [[ "$MODE" == interactive ]]; then
  echo "Next: start pi and say 'design my split using profile $name'"
fi
