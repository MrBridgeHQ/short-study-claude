# Installation — short-study skill

This skill is designed to be installed at the **user level** in Claude Code, so it's available across all your projects without copying it into each repo.

## Prerequisites

- Claude Code installed and working
- Python 3.10+ available on your system (required for the analyzer script — it uses `from __future__ import annotations` and PEP 604 union syntax `int | None`)

No third-party Python packages are required. `scripts/analyze.py` uses the standard library only (`argparse`, `csv`, `json`, `statistics`).

## Installation

### macOS / Linux

```bash
# 1. Create the user-level skills directory if it doesn't exist
mkdir -p ~/.claude/skills

# 2. Copy or unzip the skill into that directory
cp -r short-study ~/.claude/skills/
# or: unzip short-study.zip -d ~/.claude/skills/

# 3. Verify the structure
ls ~/.claude/skills/short-study/
# Expected: SKILL.md  INSTALL.md  references/  scripts/  assets/

# 4. Make the analyzer script executable (optional, for convenience)
chmod +x ~/.claude/skills/short-study/scripts/analyze.py
```

### Windows (PowerShell)

```powershell
# 1. Create the user-level skills directory if it doesn't exist
New-Item -ItemType Directory -Force -Path "$env:USERPROFILE\.claude\skills"

# 2. Unzip the skill into that directory
Expand-Archive -Path .\short-study.zip -DestinationPath "$env:USERPROFILE\.claude\skills\"

# 3. Verify the structure
Get-ChildItem "$env:USERPROFILE\.claude\skills\short-study\"
```

## Verification

Open Claude Code and ask:

> "What skills do you have access to?"

You should see `short-study` in the list. If not, check that the SKILL.md file is at the path:

- macOS / Linux: `~/.claude/skills/short-study/SKILL.md`
- Windows: `%USERPROFILE%\.claude\skills\short-study\SKILL.md`

## First test

### Test the skill's auto-activation

In any Claude Code session, ask:

> "Make a short data study: are independent cafes rated higher than chains? Use the example dataset shipped with the skill."

The skill should activate, frame the question as a comparison, run `scripts/analyze.py compare`, and produce a one-pager grounded in the computed figures.

### Test the analyzer directly

The analyzer is a standalone, offline CLI. Run the shipped worked example to confirm it works:

```bash
cd ~/.claude/skills/short-study

python3 scripts/analyze.py compare \
  --input assets/examples/independent-vs-chain-cafes.csv \
  --group-col type \
  --value-col rating
```

Expected output: a single JSON object on stdout with `"n": 11`, an `independent` group at `mean 3.94`, and a `chain` group at `mean 3.85`. No network call is made.

## Updating the skill

To install a newer version, replace the directory:

```bash
# macOS / Linux
rm -rf ~/.claude/skills/short-study
cp -r short-study ~/.claude/skills/
```

## Uninstalling

```bash
# macOS / Linux
rm -rf ~/.claude/skills/short-study

# Windows (PowerShell)
Remove-Item -Recurse -Force "$env:USERPROFILE\.claude\skills\short-study"
```

## Troubleshooting

**Skill doesn't activate when expected.**
The skill's auto-activation depends on the description in `SKILL.md`'s frontmatter. Triggers include: "make a short study", "one-pager study", "is X rated higher than Y", "are A and B correlated", "data study". If your phrasing doesn't match, force activation: "Use the `short-study` skill to..."

**Python 3.10+ syntax errors.**
`analyze.py` uses `from __future__ import annotations` and PEP 604 union syntax (`int | None`). On Python 3.8 or 3.9 this will fail. Upgrade Python.
