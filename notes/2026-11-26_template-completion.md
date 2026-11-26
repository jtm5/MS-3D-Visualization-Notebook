# 2026-11-26: Finishing the HamSCI template setup, and a map-tile problem

## Context
HamSCI applied its `ai_project_template` to this repo (PRs #1 and #2, merged). Some fields were
left for Tom (K1FR) to finish. This session reviewed what remained and Tom made the edits.
A first run of the notebook on a new Windows user account also exposed a problem with the map.

## Decided
- **CITATION.cff:** author name changed to the informal "Tom McMahan" (matching how he is known).
  Tom corrected the name W2NAF had entered and added his ORCID. The DOI placeholder line was
  removed (no release planned yet). The name does not have to match
  the legal name on the ORCID record. Suggested adding the informal name to ORCID "Also known as".
- **AI usage log:** Tom updated the Human Review Status on the two template-adoption entries
  after reading what those sessions changed.
- **README:** added an "AI disclosure" section. Claude (Anthropic) helped write all of the code,
  and `claude-opus-5-5` added the scaffolding. The code-writing sessions are not in the AI log, so
  the exact models and dates for the code are unknown and the README does not name them.
- **notes/ folder:** created, as CLAUDE.md asks. One dated file per working session.

## Windows firewall prompt
First run on the new account triggered a Windows Firewall prompt. Cancelling it created inbound
block rules for Visual Studio Code on the Public profile. This does not affect the notebook:
it opens no listening socket and only makes outbound connections. No change needed.

## Open: map does not draw on this machine
- The ground map is missing; the notebook runs otherwise. Binder shows the map correctly.
- The map needs ~100 tiles from `server.arcgisonline.com`. curl fetches a tile every time.
  Python (`urllib`) gets connection resets (error 10054) on about 70% of attempts, whatever the
  User-Agent. No outbound firewall block exists. The cause is probably intermittent network
  trouble on this connection (Tom's download speed was also reduced during storms); it was not
  identified.
- `_tile` in `meteor_core.py` has no retry, so one failed tile abandons the whole map ("map tiles
  unavailable ... drawing plain ground"). Re-running the cell did not fill the cache.
- **Proposed, not done:** add a short retry loop (3 to 4 attempts with a brief pause) to `_tile`,
  through a feature branch and PR. Waiting to see whether the problem clears with the weather.
- Idea: try the same code on the old machine (its D drive was unplugged when tried).

## Still open
- DOI in `CITATION.cff` (Zenodo release, or remove the line if no release is planned).
- Delete `docs/GETTING_STARTED.md` (CLAUDE.md says to once the project runs).
- Decide whether to add an AI log entry for the earlier code-writing sessions (no dates or
  models recorded; say so rather than estimating).
- Uncommitted changes to `meteor_3d_interactive_form.html` and `meteor_scatter_3d_form.ipynb`
  look like output from running the notebook; discard or commit deliberately.
- Update the collaborators line in CLAUDE.md when others join.
