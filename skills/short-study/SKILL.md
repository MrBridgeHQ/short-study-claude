---
name: short-study
description: Use when turning a simple question into a one-pager data study - a clearly reframed question, a light analysis of a dataset (comparison, correlation, or distribution), and an easy-to-read answer grounded in real, computed figures - plus its promotion assets: anchor links to the study page and social posts for X, Bluesky, and LinkedIn. Triggers on "make a short study", "one-pager study", "is X rated higher than Y", "are A and B correlated", "data study", "study plus social posts", "anchors and posts for a study", EN or FR. Every figure is computed by a script, never estimated.
---

# Short Study

This skill owns **one-pager data studies and their promotion assets**. A short study is a single publishable page that takes a vague question, reframes it as a falsifiable claim, backs that claim with computed figures from a real dataset, and presents the answer clearly. Alongside the one-pager, the skill produces anchor links to the study page and social posts for X, Bluesky, and LinkedIn, in EN and FR. Every figure in every output - study or post - is computed by `scripts/analyze.py` or traced to an explicitly cited external source. Nothing is hand-waved.

---

> **Integrity rule (the skill's reason to exist).** Every figure that appears in a study or a promotion post must trace to one of two sources: (a) the JSON output of `scripts/analyze.py` on the supplied dataset, or (b) an explicitly cited external source (URL + retrieval date + the exact quoted number). Hand-computed estimates, approximate figures, and unverifiable statistics are not permitted. If the dataset cannot support a number, the number does not appear.

---

## The pipeline

There is one pipeline: **Frame → Analyze → Write → Promote**. Most requests start at Frame. The only shortcut: "regenerate posts for an existing study" enters at **Promote** directly, reading the study's existing figures from the already-published one-pager.

1. **Frame** - Translate a vague question into a single falsifiable question of type comparison, correlation, or distribution. Identify the dataset (CSV or JSON file, or a dataset export). Document the reframed question, dataset source, n, and date in `analysis.md`. Reference: `references/analysis.md`.

2. **Analyze** - Run `scripts/analyze.py` with the appropriate subcommand (`compare`, `correlate`, or `distribute`) on the dataset file or via stdin (JSON piped in). Capture the full JSON output. All figures used downstream must come from this output. Reference: `references/analysis.md`.

3. **Write** - Produce the one-pager using the fixed structure (reframed question, key finding, chart spec, methodology note, source + date). The chart spec describes axes, series, and type - it is not rendered here. Write EN and FR versions. Reference: `references/one-pager.md`.

4. **Promote** - Produce anchor-text variants for the study URL and social posts (X ≤ 280 chars, Bluesky ≤ 300 chars, LinkedIn long-form), EN and FR. Reference: `references/promotion.md`.

---

## Available references and script

| Resource | Purpose |
|---|---|
| `references/analysis.md` | How to run `scripts/analyze.py`, interpret its JSON output, document n + source + date, flag sample bias, and what to do when figures are unsupported |
| `references/one-pager.md` | Fixed structure for the study page - all mandatory sections, EN/FR templates, chart spec format, methodology note, and validation checklist |
| `references/promotion.md` | Anchor-text variants + social post templates for X / Bluesky / LinkedIn, EN and FR, with character-count rules |
| `scripts/analyze.py` | The numbers engine - `compare`, `correlate`, `distribute` subcommands; file or stdin; JSON output with n and chart series; stdlib only, no network |

---

## Rules

**R1 - No live fetching in the script.** `scripts/analyze.py` reads a local file or stdin only - it never opens a network connection. Data must arrive as a pre-downloaded CSV/JSON file or as dataset JSON piped in. The script never invokes `requests`, `httpx`, `curl`, or any HTTP library.

**R2 - Integrity and honesty.** Every figure must be traceable (see the integrity rule above). Always state n, the dataset source, and the retrieval/export date in the study. Correlation ≠ causation - say so when reporting a correlation. Flag sample bias explicitly if the dataset is non-representative (e.g., only items rated on a single platform, only entries with ≥ 10 reviews).

**R3 - Anchor doctrine.** Anchor-text selection for the study URL follows standard link-building doctrine: branded + naked-URL anchors dominate; partial-match descriptive anchors fill the middle; exact-match anchors are rare. `references/promotion.md` shows how to apply these principles to a specific study.

**R4 - Human-readable prose.** Study prose and all social posts should be reviewed so they read as human-authored before delivery. AI-pattern text in a published study undermines credibility.

---

## What this skill is not

- **Not the anchor-text doctrine itself.** This skill applies common link-building principles; it does not own or re-derive a full off-page SEO strategy.
- **Not a chart renderer.** The skill emits a chart specification (axes, series, type) embedded in the one-pager. Rendering the chart as an image is outside scope.
