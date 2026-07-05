# WRITE - one-pager structure + chart-spec doctrine

This reference covers **Step 3 (Write)** of the pipeline: how to assemble the study page from the figures produced in Step 2. Stats operations and the framing move are in `references/analysis.md`; promotion assets (anchors + social posts) are in `references/promotion.md`.

---

## The fixed one-pager structure

A study page has exactly **5 parts**, in this order. No part is optional. No part is repeated. Do not add sections; do not reorder.

```
1. Reframed question
2. TL;DR
3. Facts with figures  (3-5 items)
4. Method & source
5. Micro-conclusion
```

The structure is language-agnostic. Write EN and FR versions of the same page - same figures, same 5 parts, translated prose. A figure that appears in one language version must appear in the other.

---

## Part 1 - Reframed question

**Rule:** The single falsifiable question produced in the Frame step, stated plainly. One sentence. No answer here - the answer is in the TL;DR.

**Why it comes first:** It tells the reader exactly what was tested. Without it, any figure that follows is unanchored.

**Source:** Copied directly from the question documented in `analysis.md` (the Frame step). Do not rephrase to sound more confident; do not add "we found that".

**Mini-example (cafes, EN):**
> In this dataset of 11 cafes, is the mean rating for independent cafes different from the mean rating for chain cafes, and by how much?

**Mini-example (FR):**
> Dans cet ensemble de 11 cafes, la note moyenne des cafes independants differe-t-elle de celle des chaines, et de combien ?

---

## Part 2 - TL;DR

**Rule:** The answer in ONE sentence. The sentence must contain at least one figure from `analyze.py` output. The sentence must be guarded - no causation claim, no superlative, no ranking assertion.

**One sentence only.** If you need two sentences, you are writing a micro-conclusion - move the second sentence there.

**Guarding pattern:** "In this dataset of [n], [group A] scored [X] vs [Y] for [group B] - a [gap]-point gap." Do not write "X is better than Y".

**Mini-example (EN):**
> In this dataset of 11 cafes, independent cafes averaged 3.94 vs 3.85 for chain cafes - a 0.09-point gap.

**Mini-example (FR):**
> Dans cet ensemble de 11 cafes, les cafes independants obtiennent en moyenne 3,94 contre 3,85 pour les chaines - un ecart de 0,09 point.

---

## Part 3 - Facts with figures

**Rule:** 3 to 5 short items. Each item carries at least one number. Every number must trace directly to the JSON output of `scripts/analyze.py` - read it from the output, do not recompute or estimate. Bullet or short-line form; scan-friendly.

**Integrity rule (restated for the page):** If you cannot point to the exact field in the `analyze.py` JSON that produced a figure, remove the figure. The traceability chain is: dataset file -> `analyze.py` run -> JSON output field -> figure on page. One break in that chain and the figure is not permitted. See `references/analysis.md` section 4a for the full statement.

**What to cover:** group means, group n values, the gap, spread if informative, any notable min/max. Do not add facts that require a separate dataset or a figure you did not compute.

**Mini-example (cafes compare, EN) - figures from the `compare` JSON output above:**
- Independent cafes: mean 3.94, n=5 (range 3.7-4.2)
- Chain cafes: mean 3.85, n=6 (range 3.6-4.1)
- Gap: 0.09 points (independent higher)
- Spread: sigma = 0.185 for independent; 0.171 for chain - overlapping ranges

**Mini-example (FR):**
- Cafes independants : moyenne 3,94, n=5 (plage 3,7-4,2)
- Chaines : moyenne 3,85, n=6 (plage 3,6-4,1)
- Ecart : 0,09 point (independants plus eleves)
- Dispersion : sigma = 0,185 pour les independants ; 0,171 pour les chaines - plages qui se chevauchent

---

## Part 4 - Method & source

**Rule:** Always present. Always contains: dataset source, `n` (from the `n` field of the JSON output), retrieval/export date, and at least one limitation caveat.

**Template (EN):**
> Dataset: [source description], n=[value from analyze.py output], exported [date]. [Limitation: small-n caveat and/or sample bias.]

**Template (FR):**
> Donnees : [description de la source], n=[valeur du champ n], exportees le [date]. [Limite : avertissement sur la taille de l'echantillon et/ou biais de l'echantillon.]

**What counts as a limitation:** small per-group n (below 30 for compare, below 20 rows for correlate), platform bias (single-platform data), selection bias (only entries with >= 10 ratings), or any other known constraint on generalizability. If none applies, state "no obvious selection bias identified" - do not silently omit the limitation slot.

**Mini-example (EN):**
> Dataset: ratings export, n=11, exported 2026-06-15. With only 5 independent cafes and 6 chain cafes, this result is illustrative, not statistically robust; a larger and more representative dataset would be needed to confirm the direction of the gap.

**Mini-example (FR):**
> Donnees : export de notes, n=11, exporte le 2026-06-15. Avec seulement 5 cafes independants et 6 chaines, ce resultat est illustratif et non statistiquement robuste ; un ensemble de donnees plus large et plus representatif serait necessaire pour confirmer le sens de l'ecart.

---

## Part 5 - Micro-conclusion

**Rule:** 1 to 2 sentences. States what the finding means in practical terms without overclaiming. No new figures. No causation. No superlative. Ends the page.

**Guarding pattern:** "This suggests [weak directional claim], but [scope limitation]. [Optional: what a stronger study would need]."

**Mini-example (EN):**
> This sample suggests independent cafes may trend slightly higher in ratings, but with n=11 the gap is not conclusive. A dataset of 200+ cafes across multiple cities would be needed to say more.

**Mini-example (FR):**
> Cet echantillon suggere que les cafes independants pourraient tendre vers des notes legerement plus elevees, mais avec n=11 l'ecart n'est pas concluant. Un ensemble de 200+ cafes issus de plusieurs villes serait necessaire pour aller plus loin.

---

## Chart spec section

The one-pager embeds **one visual**, described as a `chart` object. This object is taken directly from the JSON output of `analyze.py` - it is NOT invented or reshaped for display purposes. The `chart` object is the single source of truth: whatever `analyze.py` emitted is what the page spec contains.

**The skill does NOT render an image.** The `chart` object is a spec consumed downstream (by the site's charting library or by a human implementing the visual). Treat it as a JSON block in the one-pager.

### Chart shapes by operation

| `analyze.py` subcommand | `chart.type` | Key fields |
|---|---|---|
| `compare` | `"bar"` | `x` (group col), `y` ("mean \<value col\>"), `series` (label + mean per group) |
| `correlate` | `"scatter"` | `x` (x col), `y` (y col), `points` (list of [x, y] pairs) |
| `distribute` | `"bar"` | `x` (by col), `y` ("mean \<value col\>" or "count"), `series` (label + value per category) |

### Real chart object - cafes compare example

This is the exact `chart` object from the `compare` JSON output for the cafes dataset:

```json
{
  "type": "bar",
  "x": "type",
  "y": "mean rating",
  "series": [
    {"label": "chain", "value": 3.85},
    {"label": "independent", "value": 3.94}
  ]
}
```

Place this block verbatim in the one-pager, labeled **Chart spec** or **Specification du graphique**. Do not modify field names, do not rename `series` to `data`, do not change `value` to `mean`. The downstream consumer reads the exact field names `analyze.py` emits.

### Real chart object - hotel-stars correlate example

For a `correlate` study, the `chart` type is `"scatter"` and `series` is replaced by `points` - a list of `[x, y]` pairs. Example shape:

```json
{
  "type": "scatter",
  "x": "stars",
  "y": "guest_rating",
  "points": [[3, 3.9], [4, 4.05], [5, 4.2]]
}
```

Each element of `points` is a two-element numeric array `[x_value, y_value]` in input order. There is no `series` key on a scatter chart. This is the canonical verbatim shape for any `correlate` study.

### One chart per study

A one-pager contains exactly one chart spec. If the analysis produced both a `compare` and a `distribute` subcommand run (e.g., you ran the script twice), choose the one that best answers the reframed question and embed only that `chart` object. Note the other run in the Method & source section if relevant.

---

## EN + FR - what to translate, what to keep

| Element | Translate? |
|---|---|
| All prose (question, TL;DR, facts labels, method text, conclusion) | Yes |
| Figure values (means, n, gap, std, date) | No - identical in both versions |
| The `chart` object (JSON block) | No - identical in both versions; field names are code, not prose |
| The dataset source description | Yes (translate the label; keep the run ID or URL verbatim) |

Write EN first, then FR. The FR version is a full translation of all 5 parts - not a summary. Both versions live on the same study page (e.g., as tabs or as parallel sections).

---

## Validation checklist

Run this before marking a one-pager done. Every item must pass.

- [ ] **Figures traceable** - every number in every part can be pointed to a specific field in the `analyze.py` JSON output, or to an explicitly cited external source (URL + date + quoted number). No estimated or hand-computed figures anywhere.
- [ ] **n + source + date present** - Part 4 (Method & source) states the `n` field value from the JSON, the dataset source, and the retrieval/export date. No exceptions.
- [ ] **Guarded language** - no causation claim, no ranking assertion, no superlative. TL;DR says "gap" or "association", not "better" or "proves". Micro-conclusion ends with a scope limitation.
- [ ] **TL;DR is one sentence with a figure** - single sentence, contains at least one number from the JSON output.
- [ ] **Chart object present and matches analyze.py output** - the `chart` block in the one-pager is copied verbatim from the JSON output. Field names match exactly: `type`, `x`, `y`, `series` (bar) or `points` (scatter). No invented fields.
- [ ] **EN + FR both complete** - both language versions have all 5 parts with the same figures. No section omitted in the FR version.
- [ ] **No promotion content here** - no anchor links, no social posts in the one-pager. Those belong in `references/promotion.md`.
