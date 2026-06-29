# PROMOTE — anchor variants + social posts doctrine

This reference covers **Step 4 (Promote)** of the pipeline: producing anchor-text variants for the study URL and social posts for X, Bluesky, and LinkedIn. The framing + analysis steps are in `references/analysis.md`; the one-pager structure is in `references/one-pager.md`.

The examples below publish to a study page on `mr-bridge.com/studies`. Substitute your own study domain and slug throughout.

---

## Overview

The Promote step produces two assets for a published study:

1. **Anchor variants** — a tight set of varied link labels pointing to `https://mr-bridge.com/studies/<slug>`, ready to drop into backlink placements. This reference shows how to apply standard anchor-text principles to produce study-specific variants.
2. **Social posts** — per-platform copy (X, Bluesky, LinkedIn) in EN and FR, each grounded in figures from the study's `analyze.py` output.

---

## Part 1 — Anchor variants

### Anchor principles

A safe anchor profile for a study page leans on **branded** and **naked-URL** anchors, fills the middle with **descriptive (partial-match)** anchors, and uses **exact-match** anchors rarely (at most once across placements). Over-optimized exact-match anchors are a well-known spam signal, so keep them scarce. Before adding any exact-match anchor, check the page's existing anchor profile so you do not over-optimize.

### What this reference provides

A **tight, varied set of study-specific anchor variants** — 5 to 7 labels per study — covering the three mix types: **branded**, **descriptive (partial-match)**, and **naked URL**. One or two in FR if the study has FR placement targets.

The mix rule: branded + naked URL anchors dominate; partial-match descriptive anchors fill the middle; exact-match money anchors appear once at most, if at all.

### How to produce anchor variants for a study

1. Read the study slug, topic, and key finding from the one-pager (do not invent or paraphrase the finding — use the TL;DR figure).
2. Produce 5-7 variants across the three types: 2 branded, 2 descriptive, 1-2 naked URL, 0-1 exact-match.
3. Keep labels short (under 8 words). Do not include the figure itself in the anchor text.
4. EN first, then FR (translate the descriptive variants; branded and naked URL are language-independent).

### Worked example — cafes study

**Study:** "Are independent cafes rated higher? We looked at 11 cafes."
**Slug:** `independent-vs-chain-cafe-ratings`
**Study URL:** `https://mr-bridge.com/studies/independent-vs-chain-cafe-ratings`

| Type | Anchor text (EN) |
|---|---|
| Branded | Mr Bridge data study |
| Branded | Mr Bridge cafe study |
| Descriptive (partial-match) | independent cafe rating study |
| Descriptive (partial-match) | independent vs chain cafe ratings |
| Exact-match (use sparingly, once) | are independent cafes rated higher |
| Naked URL | https://mr-bridge.com/studies/independent-vs-chain-cafe-ratings |
| Naked URL (shortened) | mr-bridge.com/studies/independent-vs-chain-cafe-ratings |

**FR descriptive variants** (for FR-market placements):

| Type | Anchor text (FR) |
|---|---|
| Descriptive | etude notes cafes independants |
| Descriptive | cafes independants vs chaines notation |

Branded and naked-URL anchors need no FR translation.

**Reminder:** the exact-match row ("are independent cafes rated higher") should appear at most once across all placements. If the domain already has exact-match anchors from earlier campaigns, skip it this cycle. Re-verify the anchor profile before adding more exact-match.

---

## Part 2 — Social posts

### Platform doctrine

Each platform has distinct norms. Posts are **net-new per platform** — they are not copies of each other. The same headline figure may appear on all three, but the framing, length, and tone must differ.

#### X (formerly Twitter)

- **Length:** ~280 characters (hard platform limit). Hit 240-270 for breathing room.
- **Format:** hook (why this is interesting) + ONE headline figure + study link. That is all.
- **Hashtags:** 0-2 maximum. Prioritize native reach over discoverability — hashtag stuffing kills engagement on X.
- **Tone:** direct, factual, slightly opinionated. The hook can be a light provocation ("Everyone says indie cafes are better. The data says...").
- **Do not:** thread the study, paste the methodology, explain the rating source, add multiple figures.

#### Bluesky

- **Length:** ~300 characters (platform limit is 300). Aim for 250-280.
- **Format:** link + figure + one-line context. More conversational than X — less corporate, less data-journalist. It reads like something a person with a real opinion would say, not a press release.
- **Hashtags:** minimal (1 at most, or none). Bluesky culture is anti-hashtag-spam.
- **Tone:** relaxed, curious, first-person friendly. Can open with a genuine observation rather than a provocative hook.

#### LinkedIn

- **Length:** 3-6 short lines. Each line is a punchy idea. No walls of text.
- **Format:** professional "why it matters" framing -> headline figure -> one-line takeaway -> call to action (read the study) -> link -> 3-5 hashtags.
- **Hashtags:** 3-5 is the sweet spot for LinkedIn reach. Topic-relevant, not brand-spam.
- **Tone:** professional but not dry. The "why it matters" opener should be about the domain (ratings, data quality, consumer trust) — not "I ran a cool study today."
- **Do not:** open with "I" (LinkedIn algorithm penalty), paste long methodology blocks, use more than 5 hashtags.

---

### Integrity rule for posts (non-negotiable)

**Every figure in every post must trace to the `analyze.py` JSON output for that study.** If a number does not appear in the JSON, it does not appear in the post.

**Fabricated n is an integrity failure.** Writing "700+ ratings" when the study has n=11 is not an acceptable approximation — it is a false claim. State the actual `n` from the JSON. If the sample is small and you feel exposed saying "11 cafes", that discomfort is a signal: either gather more data before publishing, or own the small-n honestly in the post (the methodology caveat in the one-pager already flags it).

**Never invent a sample size or number.** Restate the figure you read from the JSON. If you do not have it in front of you, go read the `analyze.py` output before writing the post.

**When a post exceeds a platform's character limit, trim prose — never round or drop a figure.** Shorten introductory phrases, caveats, or hashtags; the numeric figures must remain exact.

The same traceability chain applies here as in `analysis.md` section 4a:
> dataset file -> `analyze.py` run -> JSON output field -> figure in post

---

### Review prose for a human voice before publishing

All social post copy should be reviewed so it reads as human-authored before delivery. AI-pattern language in a published post undermines credibility. Do this for both the EN and FR copy — do not skip it.

---

### Worked example — cafes study (6 posts)

**Study figures (from `analyze.py compare` JSON output):**
- n = 11 cafes total (independent: n=5, chain: n=6)
- independent mean: 3.94 | chain mean: 3.85
- gap: 0.09 points (independent higher)
- sigma independent: 0.185 | sigma chain: 0.171
- ranges overlap (independent 3.7-4.2; chain 3.6-4.1)

**Study URL:** `https://mr-bridge.com/studies/independent-vs-chain-cafe-ratings`

All figures below trace directly to the JSON output above. No figure is estimated or invented.

---

#### X — EN

```
Everyone says indie cafes are better. On 11 ratings: independent 3.94 vs chain 3.85 — a 0.09-point gap. The ranges overlap. Make of that what you will.

https://mr-bridge.com/studies/independent-vs-chain-cafe-ratings

#cafe #data
```

*(~225 chars — within limit)*

---

#### X — FR

```
"Les cafes independants sont meilleurs." Sur 11 notes : independants 3,94 vs chaines 3,85 — ecart de 0,09 point. Les plages se chevauchent. A vous de juger.

https://mr-bridge.com/studies/independent-vs-chain-cafe-ratings

#cafe #data
```

*(~230 chars — within limit)*

---

#### Bluesky — EN

```
Ran a quick look at 11 cafe ratings: independent cafes averaged 3.94, chains 3.85 — 0.09 points apart with overlapping ranges. A direction, not a verdict. Full numbers:

https://mr-bridge.com/studies/independent-vs-chain-cafe-ratings
```

*(~245 chars — within limit)*

---

#### Bluesky — FR

```
11 notes de cafes : les independants a 3,94 en moyenne, les chaines a 3,85 — 0,09 point d'ecart, plages qui se recoupent. Une tendance, pas une conclusion. Les chiffres complets :

https://mr-bridge.com/studies/independent-vs-chain-cafe-ratings
```

*(~250 chars — within limit)*

---

#### LinkedIn — EN

```
Independent cafe fans and skeptics both claim the data is on their side.

We checked 11 cafe ratings: independent cafes averaged 3.94, chains 3.85 — a 0.09-point gap, with overlapping ranges.

Small sample. Not a verdict. But an interesting direction worth tracking at scale.

Full methodology and figures: https://mr-bridge.com/studies/independent-vs-chain-cafe-ratings

#CafeData #IndependentCafe #DataStudy #Ratings
```

*(4 lines + link + hashtags — within format)*

---

#### LinkedIn — FR

```
Amateurs de cafes independants et sceptiques se reclament tous les deux des donnees.

On a regarde 11 notes de cafes : independants a 3,94 en moyenne, chaines a 3,85 — un ecart de 0,09 point, plages qui se chevauchent.

Petit echantillon. Pas un verdict. Mais une direction interessante a suivre a plus grande echelle.

Chiffres complets et methodologie : https://mr-bridge.com/studies/independent-vs-chain-cafe-ratings

#CafeIndependant #DataCafe #Notation #Etude
```

*(4 lines + link + hashtags — within format)*

---

## Validation checklist

Run this before marking the Promote step done. Every item must pass.

- [ ] **Figures traceable** — every number in every post is read directly from the `analyze.py` JSON output for this study. No estimated or invented figures anywhere.
- [ ] **n is correct** — the post states the actual `n` from the JSON, not an approximation, rounded figure, or invented sample size.
- [ ] **Posts are distinct** — each platform post has a different hook, length, and tone. X and Bluesky are not copies of each other; LinkedIn is not a copy of either.
- [ ] **EN + FR both complete** — 6 posts total (3 platforms x 2 languages). No language version omitted.
- [ ] **Guarded language** — posts do not claim one group is objectively better; gap and ranges are stated, not a ranking.
- [ ] **Human voice reviewed** — post copy has been reviewed to read as human-authored before publishing.
- [ ] **Anchor variants produced** — 5-7 anchor variants covering branded, descriptive, naked-URL, at most one exact-match. FR descriptive variants included if FR-market placements are planned.
