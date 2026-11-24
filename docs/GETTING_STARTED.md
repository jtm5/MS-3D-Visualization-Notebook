# Getting Started

*Delete this file once your project is up and running. It is onboarding, not project content.*

This guide is for HamSCI participants who are new to Claude Code, new to AI governance
requirements, or both. If you are already running AI-assisted projects under a governance
policy, the README's checklist is all you need.

---

## What this template is for

HamSCI work is done by professional researchers, students, and volunteer amateur radio
operators, often on the same project. When any of that work is done with AI assistance, three
things have to be true:

1. **A human reviewed it and stands behind it.** AI output that nobody checked is not a result.
2. **There is a record of what AI did.** That record is `ai/ai_usage_log.md`, and it is written
   as the work happens.
3. **Published outputs say so.** Papers, posters, and software releases disclose AI use.

This template makes all three the default rather than something you have to remember.

---

## Day one

### 1. Create your project from the template

```bash
gh repo create HamSCI/my-project --template HamSCI/ai_project_template --private --clone
cd my-project
```

Use `--private` while the work is unpublished. Research repositories that hold unpublished
manuscripts, pre-acceptance figures, or unreleased data stay private until publication.

### 2. Install Claude Code, if you have not

See https://docs.claude.com/en/docs/claude-code for installation. Then run `claude` in the
project directory.

### 3. Fill in the placeholders

Every placeholder in the template is wrapped in double curly braces. Find them all:

```bash
grep -rn '{{' --exclude-dir=.git .
```

Work through `CLAUDE.md` first, then `.claude/rules/ai-governance.md`, `ai/ai_usage_log.md`, and
`CITATION.cff`. Claude can do this for you if you tell it about the project; the point of
`CLAUDE.md` is that it is the thing Claude reads first in every future session, so it is worth
getting right.

### 4. Prune what does not apply

```bash
rm .claude/rules/latex-writing.md    # no LaTeX in this project
rm .claude/rules/python-code.md      # no Python in this project
```

Remove the matching lines from `CLAUDE.md` when you delete a rule file.

In `.claude/rules/ai-governance.md`, delete **Tier 2** if no institutional policy governs your
work, and **Tier 3** if the project is unfunded. Leaving a tier in place unread is worse than
deleting it: it makes the file look like it was reviewed when it was not.

### 5. Make your first commit

Run `/commit` inside Claude Code. It will ask what the session was for, draft a log entry, show
it to you for confirmation, append it to `ai/ai_usage_log.md`, and commit. This first commit seeds
`main`, so it will ask before pushing it. Every commit after that goes on a feature branch:
`/commit` pushes the branch and opens a pull request for review.

---

## The log, in practice

The log entry is short. This is a complete one:

```
## [2026-09-22 16:05 EDT]
- **Tool**: Claude (Anthropic), claude-opus-5
- **Session Purpose**: Draft the data-loading module for Grape 1 receiver files and write tests
  against three sample days.
- **Sections/Files Affected**: `src/grape/io.py`, `tests/test_io.py`
- **Nature of Contribution**: Code generation
- **Human Review Status**: Reviewed and verified
- **Git Hash**: a3f91c2
```

**What counts as substantive?** If AI output changed what ends up in a commit, it is substantive.
Asking Claude to explain how a library works and then writing the code yourself is not. Having
Claude write the code is, even if you rewrote half of it afterward.

**"Pending review" is an honest answer.** Use it when you committed something you have not fully
checked, and come back to it. An entry that claims verification that did not happen is worse
than no entry at all.

**Fill in the git hash.** The whole point of the field is that it ties the log to the diff. The
`/commit` workflow prompts for it.

---

## Things that catch people out

**Callsigns are people.** A callsign in a dataset identifies a licensed human being who
volunteered their observation. Never let an AI invent one, and never let it invent the link
between a callsign and a measurement. Check `.claude/rules/hamsci-data.md` before you publish
anything that names contributors or shows station locations.

**Station coordinates are often home addresses.** Publish grid squares at the coarsest precision
your science supports.

**Students: check with your advisor.** Your institution's academic integrity policy applies to
thesis and coursework-adjacent research, and it may be stricter than anything in this template.

**Nothing lands on `main` by itself.** Every change goes through a pull request, and a human
merges it. Once you approve a commit, Claude pushes its feature branch and opens the PR; it will
not push anything else without you saying so, and will not merge, force-push, or hard-reset. If
you ever see it about to, stop it.

**Do not commit data.** The `.gitignore` blocks the common formats. Bulk data belongs in an
archive, fetched by a script that is committed, so that anyone can regenerate your inputs.

---

## Where to ask

- HamSCI community: https://hamsci.org
- Claude Code documentation: https://docs.claude.com/en/docs/claude-code
- Problems with this template: open an issue on
  https://github.com/HamSCI/ai_project_template
