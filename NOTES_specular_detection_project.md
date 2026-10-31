# Notes: possible new project, "can this meteor produce a bistatic detection?"

Status: DRAFT for team discussion. Nothing built yet. Not committed.
Written 2026-10-29 after the Jupyter / Binder notebook release (see README.md).

## Idea

Take the vector of one meteor (position, heading, descent, speed), work out where its trail is tangent to the
TX/RX ellipsoid (the surface of constant TX -> point -> RX path length, foci at TX and RX), and say whether a
bistatic detection is **possible**. Later, repeat for many meteors (a shower).

## Decisions so far (from the project owner)

- It is a **new project**, not an addition to this notebook.
- Scope of "valid detection": **the specular point only**. Show it is *possible*; do not say how probable
  and do not model echo strength (no link budget, no meteor mass or electron line density).
- Start with **one meteor at a time**, then grow to a **shower** (many meteors).
- Make `meteor_core.py` an **installable package**, shared by this notebook and the new project.
- **Configuration control** still has to be worked out. To be discussed with the team before committing anything.

## Physics summary (proposed, to be checked by the team)

- A trail is a line. It reflects specularly where the line is tangent to a confocal ellipsoid (foci TX, RX).
- That tangent point is the point on the line that minimises |P - TX| + |P - RX|. A 1-D convex minimisation,
  so there is always one answer per line.
- "Possible" (for a trail echo) would mean, at least: the specular point lies on the part of the trail that is
  actually ionised (roughly 70-120 km altitude, depending on speed), and the trail is within the agreed
  tolerance of exact tangency (see "Head echo vs trail echo" below). The earlier idea of a Doppler window as
  the pass/fail rule is **superseded** by that section.
- Open point: "ellipsoid" here means the TX/RX path-length ellipsoid. If the Earth's WGS-84 ellipsoid (meteor
  entry point) is also wanted, that is a separate, easier step.

## Head echo vs trail echo (added 2026-10-29, after team discussion started)

The actual specular reflection comes from the ionised **trail**, which is mostly stationary relative to the
meteor's own velocity. That is different from the **head echo** from the moving plasma around the meteor.

| | Head echo | Trail echo |
|---|---|---|
| Source | plasma around the moving meteor | ionised column left behind |
| Doppler | large: f_D = -(v/lambda) vhat . (uT + uR) | near zero: only wind drift and diffusion, a few Hz to tens of Hz |
| Needs specular geometry | no | yes |

Consequences for the existing notebook and for this project:

- The trail is specular where it is tangent to the TX/RX ellipsoid. That is the same condition as
  vhat . (uT + uR) = 0, so the existing tool's "0 Hz" line is the geometric specular condition, evaluated with
  the head-velocity formula as a convenient test. It is not the Doppler of the trail echo.
- The tool's green/red colour (|f_D| <= the form's Doppler limit, default 100 Hz) therefore acts as an
  **angular tolerance around specular**, not as a real Doppler window. At 54.3 MHz and 20 km/s, 100 Hz is about
  +-0.5 degrees on the trail direction for the WDPN to Washington DC example. The Summary tab prints the exact
  angle for the current settings.
- The physical tolerance for a trail echo is the first Fresnel zone: a stretch of trail a few km long that
  reflects in phase around the exact tangent point.
- Time matters: the trail forms behind the head, so the tangent point can only echo after the meteor has passed
  it, and only while the column lasts (fractions of a second to seconds for underdense trails).
  Proposed for the one-meteor tool: report only whether the tangent point lies within the ionised segment
  (begin height to end height), not how long the echo lasts.

### Open questions added by this

1. Target: trail echoes only, head echoes only, or both? (Head echoes would keep the current Doppler formula as
   the main output and need no specular test.)
2. For trail echoes, how is the tolerance defined: an angle, a Fresnel-zone length, or exact tangency only?
3. Is the ionised height band fixed at 70-120 km, or does it depend on meteor speed?

## Proposed plan (not yet agreed)

1. Tangent-point solver and a yes/no verdict for one meteor, as a small tested library plus a notebook front end.
   Validate against the existing 3D tool: same inputs must give the same reflection point and Doppler.
2. Shower mode: sample many meteors from assumed radiant and speed distributions and report which fraction
   have a possible specular point. This is still "possible", not "how likely", but the answer depends on the
   assumed distribution.
3. Out of scope for now: echo power, link budget, underdense/overdense trails.

## Open questions for the team

- Exact pass/fail rules for "possible" (altitude band, tolerance around specular, trail length, any angle limits). See the head vs trail section.
- Packaging `meteor_core.py`:
  - Where should the shared package live (its own repo, or a folder in one of the two)?
  - Name, and how should it be versioned (semantic versions with git tags is the usual choice)?
  - How do the notebook, Binder and the new project pin to a version (`requirements.txt` pointing at a tag)?
  - A changelog, and a regression test that checks results against the current 3D tool, so a change to the
    maths is noticed.
  - Who is allowed to change the shared maths, and how is a change reviewed?
- Shower inputs: where do radiant and speed distributions come from (published data, or user-entered)?
- Front end: notebook again (Binder-friendly), or something else?

## Reuse

`meteor_core.py` already has the ECEF/ENU conversions, baseline and bearing helpers, and the Doppler
calculation. The new work is mainly the tangent-point solver, the verdict rules and the shower sampling.
