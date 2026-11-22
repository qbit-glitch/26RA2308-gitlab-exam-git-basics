# Lab Exam: Git Basics, Labs 1 to 12 (Kestrel-1 Shift Check)

**Course:** 26RA2308 Git for Software Development and Collaboration

**Based on:** Experiments 1 to 12 (terminal, files, Git setup, repositories, commits, undo, branches, merging, push and pull, forks, pull requests, CI and tags)

**Time allowed:** 1 hour. **Marks:** 20 (20 subtasks, 1 mark each)

---

## The story

It is the last shift before the Kestrel-1 rover demo. **Asha** has left the team workstation to you for one shift and
asked for a clean project: a `rover-exam` folder that holds the motor controller, with its history, a feature branch,
a remote copy, a release tag and a review branch. Every command you need is in this handout. You do not have to think
of any command yourself. Your job is to run each block in order, look at what it prints, and paste that output into
your answer file.

## What you need

A terminal on Ubuntu or Debian, macOS Terminal, or Git Bash on Windows, with `python3` and `git` **version 2.28 or
newer**. Check with `python3 --version && git --version`. No internet and no GitHub account are needed: the exam uses
folders on your own computer as the "remote".

## Before you start

Clone the exam into your **home directory**. The folder must be called `lab-exam`, because every command in this
handout uses `~/lab-exam`. Then run the setup block once. It builds the exam sandbox (`workspace` and `remote`) and is
not graded.

```bash
cd ~ && git clone https://github.com/qbit-glitch/26RA2308-gitlab-exam-git-basics.git lab-exam
cd ~/lab-exam && bash setup/build_workspace.sh
```

If you ever need to start again from the beginning, run the same block again. It deletes `workspace` and `remote` and
builds them afresh, so the tasks must then be repeated in order.

## Rules

1. Copy each command block **exactly as printed** and paste it into your terminal. Do not retype or edit the commands.
   Every block that works on the exam files starts with a `cd`, so it works from any folder.
2. One block is one subtask, and one subtask is one mark. A subtask scores only when everything it prints is right.
3. Do the tasks **in order**. Later tasks use the folders and commits that earlier tasks create.
4. Do not change files inside `workspace` by hand. Only the blocks in this handout change it.
5. Dates, sizes, owners, permission letters and commit hashes differ on every computer, so they are never marked.
6. If a block prints `fatal:`, `error:`, `command not found` or `No such file or directory`, read the message, fix it
   and run the block again. If you cannot fix it, run the setup block and redo the tasks in order.

## How you hand in your work

1. Copy the answer template and write your name and registration number at the top:

   ```bash
   cd ~/lab-exam && cp submission/outputs.template.txt submission/outputs.txt
   ```

   Open `submission/outputs.txt` in any editor, write your name after `Name   :` and your registration number after
   `Reg No :`, then save.
2. After each subtask, paste what the terminal printed **under the matching `--- N.M` line** of
   `submission/outputs.txt`, replacing `(paste output here)`. Do not edit or delete the `=== TASK` and `--- N.M` lines.
3. Check your score at any time:

   ```bash
   cd ~/lab-exam && python3 tests/grade.py
   ```

   It prints **PASS** or **FAIL** for every subtask, says which check failed, and shows your total out of 20. The
   report is also saved in `submission/results.txt`. You may fix a mistake and run the grader again as often as you
   like.
4. When you are done, show the final grader output to your instructor and submit `submission/outputs.txt`.

## Time plan

| Task | Lab | Topic | Subtasks | Marks | Suggested time |
|---|---|---|---|---|---|
| 1 | 1 | Terminal navigation | 1.1 to 1.3 | 3 | 5 min |
| 2 | 2 | File operations | 2.1 to 2.3 | 3 | 5 min |
| 3 | 3 | Git setup | 3.1 | 1 | 3 min |
| 4 | 4 | Repository creation | 4.1 | 1 | 3 min |
| 5 | 5 | Commit operations | 5.1 to 5.2 | 2 | 6 min |
| 6 | 6 | History and undo | 6.1 to 6.2 | 2 | 6 min |
| 7 | 7 | Branching | 7.1 | 1 | 5 min |
| 8 | 8 | Merging | 8.1 | 1 | 4 min |
| 9 | 9 | Push and pull | 9.1 | 1 | 4 min |
| 10 | 10 | Forks and the upstream remote | 10.1 | 1 | 4 min |
| 11 | 11 | Pull requests (branch and push) | 11.1 to 11.2 | 2 | 6 min |
| 12 | 12 | CI workflow and release tags | 12.1 to 12.2 | 2 | 6 min |
| | | Buffer for the grader and for fixing mistakes | | | 3 min |

---

## Task 1: Terminal navigation, Lab 1 (3 marks)

**Needs:** the setup block only.

> **Asha:** Before anything else, look. A path that starts with `/` is absolute and works from anywhere. `cd ~` goes
> to your home folder.

**1.1** Go home, print the path, then go to the workspace and print it again.

```bash
cd ~ && pwd && cd ~/lab-exam/workspace && pwd
```

**1.2** List everything in the workspace, including the hidden names (they start with a dot).

```bash
cd ~/lab-exam/workspace && ls -la
```

**1.3** Build the project folders for the rover controller. `mkdir -p` makes every folder on the way, and `touch`
creates an empty file.

```bash
cd ~/lab-exam/workspace && mkdir -p rover-exam/src/motor && \
    touch rover-exam/notes.txt && ls -l rover-exam rover-exam/src
```

## Task 2: File operations, Lab 2 (3 marks)

**Needs:** Task 1 (the folders `rover-exam/src/motor` and the file `rover-exam/notes.txt`).

> **Chitra:** Start from the old motor file. Copy it into the project, search for what is still to do, then tidy up.

**2.1** Copy the legacy motor file into the project as `pid.c`, then list the folder.

```bash
cd ~/lab-exam/workspace && cp legacy/motor_old.c rover-exam/src/motor/pid.c && \
    ls rover-exam/src/motor
```

**2.2** Search every file in the project for the word `TODO`. `grep -rn` prints the file, the line number and the line.

```bash
cd ~/lab-exam/workspace && grep -rn "TODO" rover-exam
```

**2.3** Rename `notes.txt` to `README.txt`, delete the old notes in `legacy`, and list both folders.

```bash
cd ~/lab-exam/workspace && mv rover-exam/notes.txt rover-exam/README.txt && \
    rm legacy/old_notes.txt && ls rover-exam legacy
```

## Task 3: Git setup, Lab 3 (1 mark)

**Needs:** nothing.

**3.1** Print your Git identity. The name and email are the ones Git writes into every commit.

```bash
git config --global --get-regexp '^user\.'
```

*Fix-it (only if 3.1 prints nothing):* run the line below **once**, with your own name and email in the quotes,
then run 3.1 again and paste that output.

```bash
git config --global user.name "Your Full Name" && \
    git config --global user.email "you@example.com"
```

## Task 4: Repository creation, Lab 4 (1 mark)

**Needs:** Task 2.3 (the folder `rover-exam` with `README.txt` and `src`).

**4.1** Turn `rover-exam` into a Git repository whose first branch is called `main`, then check its status.

```bash
cd ~/lab-exam/workspace/rover-exam && git init -b main && git status
```

## Task 5: Commit operations, Lab 5 (2 marks)

**Needs:** Task 4.

**5.1** Stage every file in the folder and make the first commit.

```bash
cd ~/lab-exam/workspace/rover-exam && git add . && \
    git commit -m "Add motor PID skeleton"
```

**5.2** Add one line to `pid.c`, read the change with `git diff`, stage and commit it, then read the history.

```bash
cd ~/lab-exam/workspace/rover-exam && echo "PID_GAIN = 1.5" >> src/motor/pid.c && \
    git diff && git add src/motor/pid.c && git commit -m "Tune PID gain" && \
    git log --format=%s
```

## Task 6: History and undo, Lab 6 (2 marks)

**Needs:** Task 5.

**6.1** Make a mistake in `pid.c`, then throw the change away with `git restore` and check that the tree is clean.

```bash
cd ~/lab-exam/workspace/rover-exam && echo "DEBUG = True" >> src/motor/pid.c && \
    git restore src/motor/pid.c && git status
```

**6.2** The commit "Tune PID gain" was wrong. Undo it safely: `git revert` makes a new commit that cancels it, so the
history is kept. Then read the history.

```bash
cd ~/lab-exam/workspace/rover-exam && git revert HEAD --no-edit && git log --format=%s
```

## Task 7: Branching, Lab 7 (1 mark)

**Needs:** Task 6.

**7.1** Create a feature branch called `feature/sensor-filter`, add a file and commit it on that branch, then list the
branches. The branch with a `*` in front is the one you are on.

```bash
cd ~/lab-exam/workspace/rover-exam && git switch -c feature/sensor-filter && \
    mkdir -p src/sensor && echo "FILTER_ALPHA = 0.8" > src/sensor/filter.py && \
    git add . && git commit -m "Add sensor filter" && git branch
```

## Task 8: Merging, Lab 8 (1 mark)

**Needs:** Task 7.

**8.1** Switch back to `main` and merge the feature branch into it. Then read the history. Because `main` has not moved
since the branch was made, Git only moves the pointer forward (a *fast-forward* merge).

```bash
cd ~/lab-exam/workspace/rover-exam && git switch main && \
    git merge feature/sensor-filter && git log --format=%s
```

## Task 9: Push and pull, Lab 9 (1 mark)

**Needs:** Task 8.

> **Ben:** The team's shared copy is the remote, here a folder called `remote/rover-exam.git`. Its address is written
> relative to your repository, with `../../`.

**9.1** Add the remote called `origin`, push `main` to it (`-u` remembers the link), pull to bring the two copies
together, then check that your `main` matches `origin/main`.

```bash
cd ~/lab-exam/workspace/rover-exam && \
    git remote add origin ../../remote/rover-exam.git && \
    git push -u origin main && git pull && git status -sb
```

## Task 10: Forks and the upstream remote, Lab 10 (1 mark)

**Needs:** Task 9.

> **Asha:** When you work on a fork, you keep two remotes. `origin` is your copy. `upstream` is the original project
> you copied from, and you pull new work from it.

**10.1** Add the remote called `upstream` and list all the remotes.

```bash
cd ~/lab-exam/workspace/rover-exam && \
    git remote add upstream ../../remote/upstream.git && git remote -v
```

## Task 11: Pull requests, Lab 11 (2 marks)

**Needs:** Task 10.

> **Chitra:** A pull request starts with a branch of its own. Make a branch for the CI tests and publish it. The
> review then continues on that same branch: each new commit you push is added to the pull request.

**11.1** Create the branch `feature/ci-tests` and publish it to `origin`.

```bash
cd ~/lab-exam/workspace/rover-exam && git switch -c feature/ci-tests && \
    git push -u origin feature/ci-tests
```

**11.2** Make a review change on the same branch, commit it, and push it. Then check that the branch matches
`origin/feature/ci-tests`.

```bash
cd ~/lab-exam/workspace/rover-exam && \
    echo "FILTER_WINDOW = 5" >> src/sensor/filter.py && git add . && \
    git commit -m "Tune filter for review" && git push && git status -sb
```

## Task 12: CI workflow and release tags, Lab 12 (2 marks)

**Needs:** Task 11.

> **Ben:** The CI workflow is a file in `.github/workflows`. It tells the server what to check on every push. Add it
> to the project first, then tag the release, push the tag, and list the tags.

**12.1** Create the CI workflow file `.github/workflows/ci.yml`, commit it, then check that Git tracks it and read it
back.

```bash
cd ~/lab-exam/workspace/rover-exam && mkdir -p .github/workflows && \
    printf 'name: CI\non: push\njobs:\n  test:\n' > .github/workflows/ci.yml && \
    printf '    runs-on: ubuntu-latest\n    steps:\n' >> .github/workflows/ci.yml && \
    printf '      - run: python3 -m pytest\n' >> .github/workflows/ci.yml && \
    git add .github && git commit -m "Add CI workflow" && \
    git ls-files .github && cat .github/workflows/ci.yml
```

**12.2** Create an annotated tag called `v1.0` with a message, push it to `origin`, then list the tags.

```bash
cd ~/lab-exam/workspace/rover-exam && git tag -a v1.0 -m "First rover release" && \
    git push origin v1.0 && git tag
```

---

**End of exam.** Run `cd ~/lab-exam && python3 tests/grade.py`, check your score, and submit
`submission/outputs.txt`.
