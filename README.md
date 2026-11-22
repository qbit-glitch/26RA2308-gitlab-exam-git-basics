# Git Basics Lab Exam: Labs 1 to 12 (Kestrel-1 Shift Check)

Final exam for 26RA2308, Git for Software Development and Collaboration. It covers the basic and most used commands
of Experiments 1 to 12: the terminal, file operations, Git setup, creating and committing a repository, undo,
branches, merging, push and pull, forks, pull requests, CI workflow files and release tags. Twenty subtasks, one
mark each, 20 marks in total. Every command is given in `ASSIGNMENT.md`: you copy and paste it, and the grader checks
what the terminal printed. The exam runs entirely on your computer: no GitHub account or internet is needed after
the clone.

## Get started

Clone the exam into your home directory. The folder must be called `lab-exam`.

```bash
cd ~ && git clone https://github.com/qbit-glitch/26RA2308-gitlab-exam-git-basics.git lab-exam
cd ~/lab-exam && bash setup/build_workspace.sh
cd ~/lab-exam && cp submission/outputs.template.txt submission/outputs.txt
```

1. Read `ASSIGNMENT.md` (the handout) and run the blocks in order.
2. Paste each block's output into `submission/outputs.txt`, under the matching `--- N.M` line.
3. Check your score any time with:

```bash
cd ~/lab-exam && python3 tests/grade.py
```

The grader only reads text files. It never runs anything from your folder. It needs `python3` and `git` 2.28 or newer.
