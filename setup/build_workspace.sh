#!/usr/bin/env bash
# Builds the exam sandbox next to this folder:
#   workspace/  your working folder (the legacy files you start from)
#   remote/     two empty bare repositories that stand in for GitHub
# Running it again deletes workspace/ and remote/ and builds them afresh.
set -euo pipefail

HERE="$(cd "$(dirname "$0")/.." && pwd)"

rm -rf "$HERE/workspace" "$HERE/remote"
mkdir -p "$HERE/workspace/legacy" "$HERE/remote"

printf 'def set_speed(v):\n    # TODO: clamp the speed\n    return v\n' > "$HERE/workspace/legacy/motor_old.c"
printf 'Old notes from the last shift. Safe to delete.\n' > "$HERE/workspace/legacy/old_notes.txt"
printf 'team=kestrel-1\nrole=trainee\n' > "$HERE/workspace/.ops-config"

git init -q --bare -b main "$HERE/remote/rover-exam.git"
git init -q --bare -b main "$HERE/remote/upstream.git"

echo "Exam sandbox ready: $HERE/workspace"
