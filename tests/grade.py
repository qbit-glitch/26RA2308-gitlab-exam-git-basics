#!/usr/bin/env python3
"""Automatic grader for the Git Basics lab exam (Labs 1-12, 20 subtasks, 1 mark each).

Usage (from inside your lab-exam folder):
    python3 tests/grade.py                        # grade submission/outputs.txt
    python3 tests/grade.py --submission FILE      # grade another pasted-outputs file
    python3 tests/grade.py --no-report            # do not write submission/results.txt

The grader only reads the text you pasted. It never runs anything from your folder.
Exit status: 0 when all 20 subtasks pass, 1 otherwise, 2 when the submission file is missing.
"""
from __future__ import annotations

import argparse
import os
import re
import sys
from dataclasses import dataclass
from datetime import datetime
from typing import Callable, Dict, List, Optional, Tuple

sys.dont_write_bytecode = True  # grading must never leave __pycache__ folders behind

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
DEFAULT_SUBMISSION = os.path.join(ROOT, "submission", "outputs.txt")
DEFAULT_REPORT = os.path.join(ROOT, "submission", "results.txt")
PLACEHOLDER = "(paste output here)"
MAX_SUBMISSION = 1 << 20  # a real submission is a few kilobytes
ERROR_PATTERNS = (r"^fatal:", r"^error:", r"^usage:", r"command not found", r"No such file or directory")

Check = Tuple[str, Callable[[str], bool]]


def has(label: str, pattern: str) -> Check:
    """Pass when the pattern appears anywhere in the pasted output."""
    return (label, lambda text: re.search(pattern, text, re.M) is not None)


def absent(label: str, pattern: str) -> Check:
    """Pass when the pattern does not appear in the pasted output."""
    return (label, lambda text: re.search(pattern, text, re.M) is None)


def at_least(label: str, pattern: str, count: int) -> Check:
    """Pass when the pattern matches on at least `count` lines."""
    return (label, lambda text: len(re.findall(pattern, text, re.M)) >= count)


def before(label: str, first: str, second: str) -> Check:
    """Pass when `first` matches and `second` matches somewhere after it."""
    def ok(text: str) -> bool:
        match = re.search(first, text, re.M)
        return match is not None and re.search(second, text[match.end():], re.M) is not None
    return (label, ok)


@dataclass(frozen=True)
class Subtask:
    """One graded subtask: one command block in ASSIGNMENT.md, worth one mark."""
    sid: str
    title: str
    checks: Tuple[Check, ...]


SUBTASKS: Tuple[Subtask, ...] = (
    Subtask("1.1", "Move around and print the path", (
        at_least("two absolute paths printed (cd ~ and cd workspace)", r"^/.+$", 2),
        has("last path ends in lab-exam/workspace", r"^/.*lab-exam/workspace$"),
    )),
    Subtask("1.2", "List everything, including hidden files", (
        has("hidden file .ops-config listed", r"\.ops-config\b"),
    )),
    Subtask("1.3", "Build the project folders", (
        has("notes.txt listed", r"\bnotes\.txt\b"),
        has("motor folder listed", r"\bmotor\b"),
    )),
    Subtask("2.1", "Copy a legacy file into the project", (
        has("pid.c listed in src/motor", r"\bpid\.c\b"),
    )),
    Subtask("2.2", "Search the project for a word", (
        has("grep found the TODO on line 2 of pid.c", r"pid\.c:2:.*TODO: clamp the speed"),
    )),
    Subtask("2.3", "Rename a file and delete an old one", (
        has("README.txt listed (renamed from notes.txt)", r"\bREADME\.txt\b"),
        absent("old_notes.txt is gone", r"old_notes\.txt"),
        has("motor_old.c still in legacy", r"\bmotor_old\.c\b"),
    )),
    Subtask("3.1", "Check your Git identity", (
        has("user.name is set", r"^user\.name\s+\S"),
        has("user.email is set", r"^user\.email\s+\S+@\S+"),
    )),
    Subtask("4.1", "Create the repository and check its status", (
        has("repository initialised", r"Initialized empty Git repository"),
        has("no commits yet", r"No commits yet"),
        has("README.txt untracked", r"^\s+README\.txt$"),
        has("src/ untracked", r"^\s+src/$"),
    )),
    Subtask("5.1", "Stage everything and make the first commit", (
        has("root commit created", r"\(root-commit\)"),
        has("commit message shown", r"Add motor PID skeleton"),
    )),
    Subtask("5.2", "Change a file, read the diff, commit, and read the log", (
        has("diff shows the added line", r"^\+PID_GAIN = 1\.5$"),
        before("log lists 'Tune PID gain' above the first commit",
               r"^Tune PID gain$", r"^Add motor PID skeleton$"),
    )),
    Subtask("6.1", "Throw away an unwanted change", (
        has("working tree clean", r"nothing to commit, working tree clean"),
    )),
    Subtask("6.2", "Undo a commit safely with revert", (
        before("log lists the revert commit above 'Tune PID gain'",
               r'^Revert "Tune PID gain"$', r"^Tune PID gain$"),
    )),
    Subtask("7.1", "Create a feature branch, commit on it, and list the branches", (
        has("branch switched", r"Switched to a new branch 'feature/sensor-filter'"),
        has("feature branch marked with *", r"^\*\s+feature/sensor-filter$"),
        has("main listed", r"^\s+main$"),
    )),
    Subtask("8.1", "Merge the feature branch into main", (
        has("fast-forward merge", r"Fast-forward"),
        has("feature commit now on main", r"^Add sensor filter$"),
    )),
    Subtask("9.1", "Connect to the remote, push main, pull, and check the sync status", (
        has("push published main", r"set up to track 'origin/main'|main -> main"),
        has("pull reports nothing new", r"Already up to date"),
        has("main tracks origin/main, nothing behind", r"^## main\.\.\.origin/main$"),
    )),
    Subtask("10.1", "Add the upstream remote and list the remotes", (
        has("origin listed", r"^origin\s"),
        has("upstream listed", r"^upstream\s"),
    )),
    Subtask("11.1", "Make a review branch and publish it", (
        has("review branch published",
            r"set up to track 'origin/feature/ci-tests'|feature/ci-tests -> feature/ci-tests"),
    )),
    Subtask("11.2", "Make a review change on the branch, commit it, and push it", (
        has("review commit created", r"Tune filter for review"),
        has("branch matches origin/feature/ci-tests", r"^## feature/ci-tests\.\.\.origin/feature/ci-tests$"),
    )),
    Subtask("12.1", "Create the CI workflow file, commit it, and read it back", (
        has("commit created", r"Add CI workflow"),
        has("git tracks the workflow file", r"^\.github/workflows/ci\.yml$"),
        has("workflow file content", r"runs-on: ubuntu-latest"),
    )),
    Subtask("12.2", "Tag a release and push the tag", (
        has("tag pushed", r"\[new tag\]\s+v1\.0\s+->\s+v1\.0"),
        has("tag listed", r"^v1\.0$"),
    )),
)

LAB_TITLES: Dict[str, str] = {
    "1": "Lab 1 - Terminal navigation", "2": "Lab 2 - File operations", "3": "Lab 3 - Git setup",
    "4": "Lab 4 - Repository creation", "5": "Lab 5 - Commit operations", "6": "Lab 6 - History and undo",
    "7": "Lab 7 - Branching", "8": "Lab 8 - Merging", "9": "Lab 9 - Push and pull",
    "10": "Lab 10 - Forks", "11": "Lab 11 - Pull requests", "12": "Lab 12 - CI and tags",
}


def parse_sections(text: str) -> Dict[str, str]:
    """Map each '--- N.M' header to the text pasted under it (placeholder removed).

    Only the template's own headers end a section. Pasted output may contain lines such as
    '--- a/src/motor/pid.c' (from git diff), so a generic '--- ' prefix must not count.
    """
    sections: Dict[str, str] = {}
    current: Optional[str] = None
    buffer: List[str] = []
    for line in text.splitlines():
        header = re.match(r"^--- (\d+\.\d+)(\s|$)", line)
        if header or line.startswith("=== "):
            if current is not None:
                sections[current] = "\n".join(buffer).replace(PLACEHOLDER, "").strip()
            current = header.group(1) if header else None
            buffer = []
        elif current is not None:
            buffer.append(line)
    if current is not None:
        sections[current] = "\n".join(buffer).replace(PLACEHOLDER, "").strip()
    return sections


def grade_subtask(subtask: Subtask, sections: Dict[str, str]) -> List[str]:
    """Return the reasons a subtask failed; an empty list means it earns its mark."""
    if subtask.sid not in sections:
        return ["the '--- " + subtask.sid + "' line is missing from outputs.txt"]
    body = sections[subtask.sid]
    if not body:
        return ["nothing pasted under this line"]
    reasons = [f"error text in the output (matched {p!r})" for p in ERROR_PATTERNS
               if re.search(p, body, re.M)]
    reasons += [f"expected: {label}" for label, ok in subtask.checks if not ok(body)]
    return reasons


def build_report(sections: Dict[str, str], name: str) -> Tuple[str, int]:
    """Build the printable report and return it with the total score."""
    lines = [
        "Git Basics Lab Exam - automatic grader",
        f"Student : {name}",
        f"Graded  : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        "",
    ]
    total = 0
    current_lab = None
    for subtask in SUBTASKS:
        lab = subtask.sid.split(".")[0]
        if lab != current_lab:
            current_lab = lab
            lines.append(f"{LAB_TITLES[lab]}")
        reasons = grade_subtask(subtask, sections)
        mark = "PASS" if not reasons else "FAIL"
        total += 1 if not reasons else 0
        lines.append(f"  [{mark}] {subtask.sid}  {subtask.title}")
        lines.extend(f"         - {reason}" for reason in reasons)
    lines.extend(["", f"TOTAL: {total} / {len(SUBTASKS)}"])
    return "\n".join(lines), total


def parse_args(argv: Optional[List[str]] = None) -> argparse.Namespace:
    """Read the command-line options."""
    parser = argparse.ArgumentParser(description="Grade the Git Basics lab exam.")
    parser.add_argument("--submission", default=DEFAULT_SUBMISSION, help="pasted-outputs file")
    parser.add_argument("--no-report", action="store_true", help="do not write submission/results.txt")
    return parser.parse_args(argv)


def main(argv: Optional[List[str]] = None) -> int:
    """Grade the submission, print the report, and save it next to the submission."""
    args = parse_args(argv)
    if not os.path.isfile(args.submission):
        print(f"Submission file not found: {args.submission}\n"
              "Create it with:  cp submission/outputs.template.txt submission/outputs.txt")
        return 2
    with open(args.submission, encoding="utf-8", errors="replace") as handle:
        raw = handle.read(MAX_SUBMISSION)
    text = raw.replace("\r\n", "\n")
    name_match = re.search(r"^Name\s*:\s*(.*)$", text, re.M)
    name = name_match.group(1).strip() if name_match and name_match.group(1).strip() else "(name not filled in)"
    report, total = build_report(parse_sections(text), name)
    print(report)
    default = os.path.abspath(args.submission) == os.path.abspath(DEFAULT_SUBMISSION)
    if default and not args.no_report:
        with open(DEFAULT_REPORT, "w", encoding="utf-8") as handle:
            handle.write(report + "\n")
    return 0 if total == len(SUBTASKS) else 1


if __name__ == "__main__":
    sys.exit(main())
