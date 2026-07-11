# short-study - Claude Code Agent Skill

Turn a vague question into a one-pager data study backed by real, computed figures, then generate its promotion assets. An Agent Skill **for Claude Code**. It reframes the question as a falsifiable claim, computes the answer from an actual dataset, writes a clean one-pager (EN and FR), and produces anchor links plus social posts for X, Bluesky, and LinkedIn.

## The integrity rule (its reason to exist)

Every figure in every output, study or post, traces to one of two sources: the JSON output of `scripts/analyze.py` on the supplied dataset, or an explicitly cited external source (URL, retrieval date, exact quoted number). Hand-computed estimates and unverifiable statistics are not permitted. If the dataset cannot support a number, the number does not appear.

## The pipeline

Frame -> Analyze -> Write -> Promote.

1. **Frame:** turn a vague question into a single falsifiable question (comparison, correlation, or distribution); identify the dataset; record the reframed question, source, n, and date.
2. **Analyze:** run `scripts/analyze.py` (`compare`, `correlate`, or `distribute`) on a local file or stdin; every downstream figure comes from its JSON output.
3. **Write:** produce the one-pager with a fixed structure (reframed question, key finding, chart spec, methodology note, source and date), in EN and FR.
4. **Promote:** anchor-text variants for the study URL and social posts (X up to 280 characters, Bluesky up to 300, LinkedIn long-form), EN and FR.

## The numbers engine

`scripts/analyze.py` is standard-library only and never touches the network (it reads a local CSV or JSON file, or stdin). Subcommands: `compare`, `correlate`, `distribute`. The JSON output includes n and the chart series, so every figure downstream is traceable.

## Rules it enforces

- **No live fetching in the script:** data arrives as a pre-downloaded file or piped JSON; the script never calls requests, httpx, curl, or any HTTP library.
- **Integrity and honesty:** always state n, the dataset source, and the retrieval date; correlation is not causation, and sample bias is flagged explicitly.
- **Human-readable prose:** the study and the posts are reviewed to read as human-authored before delivery.

## Installation

### Claude Code, project level

```bash
cp -r skills/short-study /path/to/your-project/.claude/skills/
```

### Claude Code, global level

```bash
cp -r skills/short-study ~/.claude/skills/
```

## Use it

- "Is X rated higher than Y? Make a short study from this CSV."
- "Are these two variables correlated? A one-pager with the figures."
- "Turn this dataset into a distribution study and give me the chart spec."
- "Write the X, Bluesky, and LinkedIn posts for this study, in EN and FR."
- "Regenerate the promotion posts for my existing study."

## What is inside

The skill lives in [`skills/short-study/`](skills/short-study/): a `SKILL.md`, a `references/` library (analysis, one-pager structure, promotion templates), and `scripts/analyze.py` (the stdlib-only, no-network numbers engine).

## License

See `LICENSE`.

---

Part of the **[mr-bridge.com](https://mr-bridge.com)** toolkit for scraping, data, and content automation:
[Scrapers](https://mr-bridge.com/scrapers) · [MCP servers](https://mr-bridge.com/mcp-servers) · [AI workflows](https://mr-bridge.com/ai-workflows) · [Studies](https://mr-bridge.com/studies) · [Articles](https://mr-bridge.com/articles) · [Solutions](https://mr-bridge.com/solutions)

---

*Part of the [MrBridge Agent Skills catalog](https://github.com/MrBridgeHQ/skills). Browse them all at [mr-bridge.com/skills](https://mr-bridge.com/skills).*
