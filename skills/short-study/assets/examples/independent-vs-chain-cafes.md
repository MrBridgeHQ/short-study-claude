# Worked example — Independent vs chain cafes

> **How to read this file.**
> This document is the canonical end-to-end output of the `short-study` pipeline applied to a single question.
> Every figure originates from one source of truth: the JSON output of `scripts/analyze.py` shown in section 2.
> Nothing is estimated, hand-computed, or paraphrased. The command in section 2 is reproducible verbatim.

---

## Section 1 — Reframed question + classification

**Original question (raw):** "Are independent cafes rated higher than chain cafes?"

**Modelling note:** This question compares two groups (independent vs chain) on one shared numeric metric (rating on a 5-point scale). That is a **comparison** question. The data is in **long format** with a `type` column (`independent` | `chain`) and a `rating` column, one row per cafe.

**Reframed question (EN):**
> In this dataset of 11 cafes, is the mean rating for independent cafes different from the mean rating for chain cafes, and by how much?

**Reframed question (FR):**
> Dans cet ensemble de 11 cafes, la note moyenne des cafes independants differe-t-elle de celle des chaines, et de combien ?

**Question type:** Comparison (two groups on a shared numeric metric)
**Subcommand:** `compare`
**Data format:** Long — one row per cafe; columns: `cafe`, `type`, `rating`

**Fixture file:** `assets/examples/independent-vs-chain-cafes.csv`

---

## Section 2 — Exact command + real JSON output

```bash
python3 scripts/analyze.py compare \
  --input assets/examples/independent-vs-chain-cafes.csv \
  --group-col type \
  --value-col rating
```

**Real JSON output (not fabricated — paste from actual run):**

```json
{"operation": "compare", "n": 11, "value_col": "rating", "group_col": "type", "groups": [{"label": "chain", "n": 6, "mean": 3.85, "median": 3.85, "std": 0.171, "min": 3.6, "max": 4.1}, {"label": "independent", "n": 5, "mean": 3.94, "median": 3.9, "std": 0.185, "min": 3.7, "max": 4.2}], "chart": {"type": "bar", "x": "type", "y": "mean rating", "series": [{"label": "chain", "value": 3.85}, {"label": "independent", "value": 3.94}]}}
```

**Figures extracted from the JSON (single source of truth for everything that follows):**

| Field | Value |
|---|---|
| `n` (total rows) | 11 |
| `groups[chain].n` | 6 |
| `groups[chain].mean` | 3.85 |
| `groups[chain].median` | 3.85 |
| `groups[chain].std` | 0.171 |
| `groups[chain].min` | 3.6 |
| `groups[chain].max` | 4.1 |
| `groups[independent].n` | 5 |
| `groups[independent].mean` | 3.94 |
| `groups[independent].median` | 3.9 |
| `groups[independent].std` | 0.185 |
| `groups[independent].min` | 3.7 |
| `groups[independent].max` | 4.2 |
| gap (independent mean - chain mean) | 3.94 - 3.85 = 0.09 |

> **Reproducibility note:** Run the command above verbatim from the skill root to obtain these exact figures. The fixture file at `assets/examples/independent-vs-chain-cafes.csv` ships with the skill.

---

## Section 3 — One-pager (EN + FR)

### EN version

---

#### 1. Reframed question

In this dataset of 11 cafes, is the mean rating for independent cafes different from the mean rating for chain cafes, and by how much?

---

#### 2. TL;DR

In this dataset of 11 cafes, independent cafes averaged 3.94 vs 3.85 for chain cafes — a 0.09-point gap on a 5-point scale.

---

#### 3. Facts with figures

- **Independent cafes:** mean 3.94, n=5 (range 3.7-4.2, median 3.9)
- **Chain cafes:** mean 3.85, n=6 (range 3.6-4.1, median 3.85)
- **Gap:** 0.09 points (independent higher)
- **Spread:** sigma = 0.185 for independent; 0.171 for chain — overlapping ranges
- **Consistency:** chain ratings are slightly tighter (sigma 0.171) than independent ratings (sigma 0.185)

---

#### 4. Method & source

Dataset: hand-curated fixture of 11 cafes with a single rating each, in long format (one row per cafe), n=11, created 2026-06-22. With only 5 independent cafes and 6 chain cafes, this result is illustrative, not statistically robust — the gap is directionally suggestive but would need a substantially larger and more representative sample (ideally 200+ cafes across multiple cities) to support a generalizable claim.

---

#### 5. Micro-conclusion

This sample suggests independent cafes may trend slightly higher in ratings than chains, with a 0.09-point gap in this dataset. However, the ranges overlap and with n=11 the finding is an illustration of the pipeline, not evidence of a market-wide pattern.

---

### FR version

---

#### 1. Question recadree

Dans cet ensemble de 11 cafes, la note moyenne des cafes independants differe-t-elle de celle des chaines, et de combien ?

---

#### 2. TL;DR

Dans cet ensemble de 11 cafes, les cafes independants obtiennent une note moyenne de 3,94 contre 3,85 pour les chaines — un ecart de 0,09 point sur une echelle de 5.

---

#### 3. Faits et chiffres

- **Cafes independants :** moyenne 3,94, n=5 (plage 3,7-4,2, mediane 3,9)
- **Chaines :** moyenne 3,85, n=6 (plage 3,6-4,1, mediane 3,85)
- **Ecart :** 0,09 point (independants plus eleves)
- **Dispersion :** sigma = 0,185 pour les independants ; 0,171 pour les chaines — plages qui se chevauchent
- **Coherence :** les notes des chaines sont legerement plus resserrees (sigma 0,171) que celles des independants (sigma 0,185)

---

#### 4. Methode et source

Donnees : fichier de reference de 11 cafes avec une note chacun, en format long (une ligne par cafe), n=11, constitue le 22 juin 2026. Avec seulement 5 cafes independants et 6 chaines, ce resultat est illustratif et non statistiquement robuste — l'ecart est directionnellement suggestif, mais necessiterait un echantillon nettement plus large et plus representatif (idealement 200+ cafes dans plusieurs villes) pour appuyer une generalisation.

---

#### 5. Micro-conclusion

Cet echantillon suggere que les cafes independants pourraient tendre vers des notes legerement plus elevees que les chaines, avec un ecart de 0,09 point dans ce jeu de donnees. Cependant, les plages se chevauchent et, avec n=11, le resultat illustre le fonctionnement du pipeline — ce n'est pas une preuve d'une tendance de marche generalisable.

---

## Section 4 — Chart spec (verbatim from analyze.py output)

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

> This `chart` object is copied verbatim from the `chart` field of the `analyze.py` JSON output above. Field names (`type`, `x`, `y`, `series`, `label`, `value`) match exactly what the script emits — do not rename them for display purposes. The downstream charting library reads these exact field names.

---

## Section 5 — Promotion assets

### Anchor variants

**Study slug:** `independent-vs-chain-cafe-ratings`
**Study URL:** `https://mr-bridge.com/studies/independent-vs-chain-cafe-ratings`

| Type | Anchor text (EN) |
|---|---|
| Branded | Mr Bridge data study |
| Branded | Mr Bridge cafe study |
| Descriptive (partial-match) | independent vs chain cafe ratings |
| Descriptive (partial-match) | how independent and chain cafes rate |
| Exact-match (use sparingly — once at most) | are independent cafes rated higher |
| Naked URL | https://mr-bridge.com/studies/independent-vs-chain-cafe-ratings |
| Naked URL (shortened) | mr-bridge.com/studies/independent-vs-chain-cafe-ratings |

**FR descriptive variants** (for FR-market placements):

| Type | Anchor text (FR) |
|---|---|
| Descriptive | etude notes cafes independants vs chaines |
| Descriptive | cafes independants et chaines, qui note le mieux ? |

> **Note:** Keep exact-match anchors rare — at most once across placements. Verify the existing anchor profile before placing the exact-match row. Branded and naked-URL anchors are safe at any volume.

---

### Social posts

All figures below trace to the `analyze.py` JSON output in section 2. No figure is estimated or invented.

---

#### X — EN

```
Independent or chain — which rates higher? On 11 cafes: independent 3.94 vs chain 3.85 — a 0.09-point gap on a 5-point scale. Ranges overlap, so it's a direction, not a verdict.

https://mr-bridge.com/studies/independent-vs-chain-cafe-ratings

#cafe #data
```

*(~250 chars — within 280-char limit)*

---

#### X — FR

```
Independants ou chaines — qui note le plus haut ? Sur 11 cafes : independants 3,94 vs chaines 3,85 — ecart de 0,09 point sur 5. Les plages se chevauchent : une tendance, pas un verdict.

https://mr-bridge.com/studies/independent-vs-chain-cafe-ratings

#cafe #data
```

*(~255 chars — within 280-char limit)*

---

#### Bluesky — EN

```
Ran a compare on 11 cafe ratings: independent cafes averaged 3.94, chains 3.85 — 0.09 points apart on a 5-point scale. The ranges overlap. Interesting direction; not a verdict with n=11.

https://mr-bridge.com/studies/independent-vs-chain-cafe-ratings
```

*(~260 chars — within 300-char limit)*

---

#### Bluesky — FR

```
11 notes de cafes comparees : les independants a 3,94 en moyenne, les chaines a 3,85 — 0,09 point d'ecart sur 5. Les plages se chevauchent. Une tendance a suivre, pas encore une conclusion avec n=11.

https://mr-bridge.com/studies/independent-vs-chain-cafe-ratings
```

*(~270 chars — within 300-char limit)*

---

#### LinkedIn — EN

```
Independent cafe fans and chain regulars rarely agree on which is better.

We compared 11 cafe ratings on a 5-point scale — 5 independent venues, 6 chains.

Independent cafes averaged 3.94. Chains averaged 3.85. That's a 0.09-point gap, with overlapping ranges.

Small dataset. Not a verdict. But a direction worth watching at scale.

Full figures and methodology: https://mr-bridge.com/studies/independent-vs-chain-cafe-ratings

#CafeData #IndependentCafe #DataStudy #Ratings #ConsumerInsights
```

*(5 lines + link + 5 hashtags — within LinkedIn format)*

---

#### LinkedIn — FR

```
Amateurs de cafes independants et habitues des chaines sont rarement d'accord sur le meilleur.

On a compare 11 notes de cafes sur une echelle de 5 — 5 etablissements independants, 6 chaines.

Cafes independants : 3,94 en moyenne. Chaines : 3,85. Soit un ecart de 0,09 point, avec des plages qui se chevauchent.

Petit echantillon. Pas un verdict. Mais une direction a explorer a plus grande echelle.

Chiffres complets et methodologie : https://mr-bridge.com/studies/independent-vs-chain-cafe-ratings

#CafeIndependant #DataCafe #Etude #Notation #ConsommateurCafe
```

*(5 lignes + lien + 5 hashtags — dans le format LinkedIn)*

---

> **Human-voice note:** All social post copy above should be reviewed so it reads as human-authored before publishing, to reduce AI-pattern language. The pipeline produces the structure and figures; the prose still needs a human-readability pass.

---

## Section 6 — Closing notes

**Reproducibility:** Every figure in this document is produced by the command in section 2. Run it verbatim from the skill root to verify. The fixture `assets/examples/independent-vs-chain-cafes.csv` ships with the skill and will not change.

**Nothing auto-published:** This document is an illustrative pipeline walkthrough. No page has been published. Publication requires a real dataset, full data provenance, and a separate deployment step.

**Scale caveat (R2):** This example uses a small curated fixture (n=11). A real study on this question would require a dataset of 200+ cafes drawn from multiple cities before drawing any publishable conclusion. The `analyze.py` command and the one-pager structure would remain identical; only the input file would change.
