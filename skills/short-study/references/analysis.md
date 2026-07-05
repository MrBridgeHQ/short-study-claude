# FRAME + ANALYZE - doctrine reference

This reference covers the first two steps of the pipeline: **Frame** (turn a vague question into one falsifiable question) and **Analyze** (run `scripts/analyze.py` and capture its JSON output). The one-pager structure is in `references/one-pager.md`; promotion is in `references/promotion.md`.

---

## 1. FRAME - rewrite the question

A vague question ("are indie cafes better?", "do hotel stars matter?") cannot produce a falsifiable answer. Frame it as a single testable claim before touching the data.

### The framing move

One question -> one comparison OR one correlation OR one distribution. If the original question implies two of these, pick the one that best answers what the user actually wants, then note the other as a possible follow-up.

**Mapping table**

| Question type | When to use | `analyze.py` subcommand |
|---|---|---|
| **Comparison** | Two or more groups on a shared numeric metric - "do A and B score differently?" | `compare` |
| **Correlation** | Two numeric variables - "do higher X values come with higher Y?" | `correlate` |
| **Distribution** | Counts or proportions across categories - "how is the sample split, and what is each category's average?" | `distribute` |

### Real-world examples

| Original question | Reframed question | Type | Subcommand |
|---|---|---|---|
| "Are independent cafes rated higher than chain cafes?" | "In this dataset of N cafes, is the mean rating for independent cafes different from the mean rating for chain cafes?" | Comparison (two groups: independent vs chain) on rating | `compare` |
| "Do more stars mean better hotel ratings?" | "In this dataset of N hotels, what is the Spearman correlation between official star count and guest rating?" | Correlation (stars x guest_rating) | `correlate` |
| "How do hotel ratings break down by star level?" | "In this dataset of N hotels, what is the count and mean guest rating for each star level?" | Distribution (by star level, value = guest_rating) | `distribute` |

**FR example of the reframing step:**
> *Question brute :* "Les cafes independants sont-ils mieux notes ?"
> *Question cadree :* "Dans cet ensemble de N cafes, la note moyenne des cafes independants differe-t-elle de celle des chaines, et de combien ?"

Document the reframed question, the question type, and the subcommand choice in a comment at the top of the analysis run before invoking the script.

---

## 2. Hybrid input - data sources and CLI

Data arrives as a **local CSV or JSON file** (pre-downloaded, from a dataset export or manual curation) or as **JSON piped to stdin**. The script accepts both.

**R1 reminder: no live fetching in the script.** `scripts/analyze.py` reads a local file or stdin only - it never opens a network connection. Data must arrive as a pre-downloaded file or as dataset JSON piped in. The script never invokes `requests`, `httpx`, `curl`, `playwright`, or any HTTP library. Fetch data first (through whatever data pipeline you use), then pass it to the script.

### Exact CLI commands

**compare** (file input):
```bash
python3 scripts/analyze.py compare \
  --input data.csv \
  --group-col <group_column> \
  --value-col <value_column>
```

**correlate** (JSON file input):
```bash
python3 scripts/analyze.py correlate \
  --input data.json \
  --x-col <x_column> \
  --y-col <y_column>
```

**distribute** (stdin - JSON piped in):
```bash
cat data.json | python3 scripts/analyze.py distribute \
  --input - \
  --by-col <category_column> \
  [--value-col <value_column>]
```

The `--input -` flag tells the script to read from stdin. The `--value-col` flag is optional for `distribute`: omit it to get counts/proportions only; include it to also get `mean_value` per category.

All flags are `--kebab-case`. There are no other flags. Do not invent flags that are not listed above.

The script writes a single JSON object to stdout and exits 0 on success. On error it writes to stderr and exits non-zero with no JSON on stdout.

---

## 3. The three operations

### 3.1 `compare` - two or more groups on a numeric metric

**When to use:** the question is "does group A score higher than group B?" or any multi-group variant. The groups live in one column (`--group-col`), the numeric values in another (`--value-col`).

**Key output fields (read from actual JSON):**

```json
{
  "operation": "compare",
  "n": 11,
  "value_col": "rating",
  "group_col": "type",
  "groups": [
    {
      "label": "chain",
      "n": 6,
      "mean": 3.85,
      "median": 3.85,
      "std": 0.171,
      "min": 3.6,
      "max": 4.1
    },
    {
      "label": "independent",
      "n": 5,
      "mean": 3.94,
      "median": 3.9,
      "std": 0.185,
      "min": 3.7,
      "max": 4.2
    }
  ],
  "chart": {
    "type": "bar",
    "x": "type",
    "y": "mean rating",
    "series": [
      {"label": "chain", "value": 3.85},
      {"label": "independent", "value": 3.94}
    ]
  }
}
```

Groups are sorted alphabetically by label. Each group object contains: `label`, `n`, `mean`, `median`, `std` (population sigma - see section 4e), `min`, `max`.

The `chart` object is the single source of truth for the visual: type `"bar"`, x axis = `group_col`, y axis = `"mean <value_col>"`, series = one entry per group with its mean.

**Headline figure for the study:** the gap between group means. Example: `3.94 - 3.85 = 0.09` points - not "independent cafes are better".

---

### 3.2 `correlate` - two numeric variables

**When to use:** the question is "do higher values of X come with higher values of Y?" Both variables must be numeric.

**Key output fields:**

```json
{
  "operation": "correlate",
  "n": 8,
  "x_col": "stars",
  "y_col": "guest_rating",
  "pearson": 0.932,
  "spearman": 0.945,
  "chart": {
    "type": "scatter",
    "x": "stars",
    "y": "guest_rating",
    "points": [[3, 7.5], [4, 8.0], [5, 9.0]]
  }
}
```

Two coefficients: `pearson` (linear, sensitive to outliers) and `spearman` (rank-based, robust to outliers and appropriate for ordinal data like ratings). **Spearman is the headline coefficient** when the variables are ordinal rating scales; Pearson is the supplementary figure.

The `chart` object is type `"scatter"`, with `x`, `y`, and `points` (a list of `[x, y]` pairs in input order).

**Constant-column guard:** if either column is constant across all rows, the script exits non-zero with an error on stderr - correlation is undefined. Check your data before running.

---

### 3.3 `distribute` - counts and proportions across categories

**When to use:** the question is "how is the dataset split across categories?" - optionally with a per-category average. Use this when the user wants to understand the shape of the sample or compare averages across more than two groups without framing it as a head-to-head comparison.

**Key output fields (with `--value-col`):**

```json
{
  "operation": "distribute",
  "n": 8,
  "by_col": "stars",
  "value_col": "guest_rating",
  "categories": [
    {"label": "3", "count": 3, "proportion": 0.375, "mean_value": 7.433},
    {"label": "4", "count": 3, "proportion": 0.375, "mean_value": 8.233},
    {"label": "5", "count": 2, "proportion": 0.25,  "mean_value": 9.25}
  ],
  "chart": {
    "type": "bar",
    "x": "stars",
    "y": "mean guest_rating",
    "series": [
      {"label": "3", "value": 7.433},
      {"label": "4", "value": 8.233},
      {"label": "5", "value": 9.25}
    ]
  }
}
```

**Without `--value-col`:** `value_col` is absent from the root, `mean_value` is absent from each category, and `chart.y` is `"count"`. Use this form for a pure frequency/proportion breakdown.

The `chart` object is type `"bar"`, x axis = `by_col`, y axis = `"mean <value_col>"` (or `"count"` if no value col), series = one entry per category. The proportions across all categories sum to 1.0 (subject to rounding at 3 decimal places).

---

## 4. Honesty and integrity doctrine

This section is the heart of the reference. The three baseline failure modes that this skill is designed to prevent:

1. **Overclaiming** - a conclusion stated as a universal truth ("Independent cafes are ALWAYS better") from a tiny sample.
2. **Missing n, source, date** - numbers floating without context.
3. **Hand-computed or estimated figures** - bypassing the script and inventing or eyeballing values.

### 4a. The integrity rule (non-negotiable)

Every figure that appears in the study or in a promotion post must trace to exactly one of two sources:

- **(a)** the JSON output of `scripts/analyze.py` on the supplied dataset, OR
- **(b)** an explicitly cited external source - URL + retrieval date + the exact quoted number.

**Hand-computed estimates, approximate figures, and unverifiable statistics are not permitted.** If the dataset cannot support a number, the number does not appear. If you find yourself writing a figure that you did not read directly from `analyze.py` output or a cited URL, stop - either run the script, or remove the figure.

**Simple arithmetic derived from two fields of the same JSON object is permitted** (for example, the gap = group-A mean - group-B mean, both fields from the same `compare` JSON output), provided the derivation is shown explicitly as `field_A - field_B = result` wherever the derived figure is used (e.g., `90.25 - 87.125 = 3.125`). No rounding or approximation is allowed even in derived figures.

This rule applies to social posts too: a post that says "700+ ratings" when the study has 11 rows is an integrity failure (fabricated n).

### 4b. Always state n, source, and date

Every study and every analysis block must include:

- **n** - total number of rows processed (from the `n` field in the JSON output)
- **Dataset source** - where the data came from (a platform export, a dataset run ID, a manually curated CSV, etc.)
- **Retrieval / export date** - when the data was captured

Template:
> *Dataset: [source description], n=[value from analyze.py output], exported [date].*

FR variant:
> *Donnees : [description de la source], n=[valeur du champ n], exportees le [date].*

Without these three, the study cannot be reproduced or challenged - which makes it worthless as a data study.

### 4c. Correlation != causation; comparison != ranking

**For `correlate`:** report the association. Do not claim direction of cause.

- Correct: "In this dataset of 8 hotels, there is a strong positive Spearman correlation (rho = 0.945) between star count and guest rating - higher-star hotels tend to have higher guest ratings in this sample."
- Wrong: "More stars cause better guest experiences."

**For `compare`:** report the gap. Do not claim one group is objectively superior.

- Correct: "Independent cafes scored 0.09 points higher on average than chain cafes in this dataset (3.94 vs 3.85)."
- Wrong: "Independent cafes are better rated." / "Everyone prefers indie cafes."

The guarded phrasing template (cafes running example):

> "In this dataset of 11 cafes, independent cafes scored on average 3.94 vs 3.85 for chain cafes - a 0.09-point gap. This is an association in a specific sample, not evidence that being independent causes higher scores or that the gap is representative of the broader market."

FR variant:
> "Dans cet ensemble de 11 cafes, les cafes independants obtiennent en moyenne 3,94 contre 3,85 pour les chaines - un ecart de 0,09 point. Il s'agit d'une association observee sur un echantillon precis, et non d'une preuve que l'independance cause des notes plus elevees."

### 4d. Flag sample bias and small n

A small or non-representative sample cannot support a strong claim. If the per-group n is small (rule of thumb: fewer than 30 per group for a comparison; fewer than 20 rows for a correlation), add an explicit caveat in the methodology note.

Examples:
- n=5 per group (cafes dataset): "With only 5 independent cafes and 6 chain cafes, this result is illustrative, not statistically robust. A larger and more representative dataset would be needed to confirm the direction of the gap."
- Single-platform dataset: "This dataset covers only entries with ratings on one platform and may over-represent venues with active online communities."

The script does not block small-n runs - that judgment is yours. But if you run it on n=3 per group and state a strong claim, you are producing the baseline failure.

### 4e. std is population sigma - a spread figure, not inferential

`analyze.py` uses `statistics.pstdev` (population standard deviation, dividing by N, not N-1). This is intentional: the dataset is treated as the complete population of interest for the study, not as a sample drawn to estimate a population parameter. Report `std` as a spread/context figure:

- Correct: "The spread of independent-cafe ratings in this dataset is sigma = 0.185."
- Wrong: "The standard error is 0.185, so the difference is statistically significant."

Do not use `std` from this script for hypothesis testing, confidence intervals, or p-values. It is a description of dispersion, nothing more.

---

## 5. Summary checklist before passing to Write

Before moving to `references/one-pager.md`, confirm:

- [ ] Question is reframed as one falsifiable question of type comparison / correlation / distribution
- [ ] Subcommand chosen matches the question type (see mapping table)
- [ ] `analyze.py` was run and the full JSON output is captured
- [ ] Every figure to be used in the study is read from that JSON output (or from a cited external source)
- [ ] n, dataset source, and retrieval date are documented
- [ ] Guarded phrasing drafted for the headline finding (no overclaiming)
- [ ] Sample bias and small-n caveats added where needed
- [ ] No hand-computed or estimated numbers anywhere
