# AI Usage Log: Meteor Scatter 3D Explorer

This log records every substantive AI-assisted session on the project "Meteor Scatter 3D Explorer".

Required by the HamSCI Generative AI Use Agreement, and by any institutional or funder policy
that applies to this project (see `.claude/rules/ai-governance.md`).

**This log is the source of truth for what AI did on this project.** A disclosure paragraph in a
manuscript, poster, or software release summarizes this log truthfully. Keep it current: an
entry written from memory weeks later is not a record.

## Entry format

```
## [YYYY-MM-DD HH:MM TZ]
- **Tool**: Claude (Anthropic), <exact-model-id>
- **Session Purpose**: What the session set out to accomplish
- **Sections/Files Affected**: Specific files, sections, or documents touched
- **Nature of Contribution**: Draft / Edit / Analysis / Code generation / Research / Scaffolding
- **Human Review Status**: Reviewed and verified / Partially reviewed / Pending review
- **Git Hash**: <filled in after committing>
```

The date and time come from the system clock via `date`, never from an estimate. The `/commit`
command produces this format and appends it in the right order.

---

<!-- Append new entries below this line, newest at the bottom. -->

## [2026-11-24 17:18 UTC]
- **Tool**: Claude (Anthropic), claude-opus-5-5
- **Session Purpose**: Adopt the HamSCI `ai_project_template` (commit a09f960) into this
  repository: AI governance rules, `/commit` and `/template-sync` workflows, session-start
  template check, AI usage log, issue templates, CITATION.cff, and getting-started guide. Fill in
  project placeholders derivable from the README; leave lead, institution and funder fields for
  the maintainer.
- **Sections/Files Affected**: `.claude/` (new), `.github/ISSUE_TEMPLATE/` (new), `CLAUDE.md`,
  `CITATION.cff`, `ai/ai_usage_log.md`, `docs/GETTING_STARTED.md` (all new), `.gitignore`
  (the original four entries kept first, in their original order, after review feedback that
  the reordered diff looked like a deletion; the template's entries follow). Template `README.md`, `LICENSE` and
  `.claude/rules/latex-writing.md` not adopted.
- **Nature of Contribution**: Scaffolding
- **Human Review Status**: Pending review
- **Git Hash**: see the commit adding this entry on branch `adopt-ai-project-template`
