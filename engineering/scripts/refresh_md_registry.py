#!/usr/bin/env python3
"""Generate the durable Markdown registry for the fork engineering layer."""
from pathlib import Path
from datetime import datetime, timezone

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "engineering" / "MASTER_MD_REGISTRY.md"
rows = []
for path in sorted(ROOT.rglob("*.md")):
    if ".git" in path.parts:
        continue
    rel = path.relative_to(ROOT).as_posix()
    text = path.read_text(errors="replace")
    heading = next((line.lstrip("# ").strip() for line in text.splitlines() if line.startswith("#")), "(no heading)")
    rows.append((rel, heading, len(text.splitlines())))
lines = ["# Markdown Registry", "", f"Generated: {datetime.now(timezone.utc).isoformat()}", "", "This index is generated; edit source Markdown files, then rerun the script.", "", "| File | First heading | Lines |", "|---|---|---:|"]
lines += [f"| `{p}` | {h.replace('|', '\\|')} | {n} |" for p, h, n in rows]
OUT.write_text("\n".join(lines) + "\n")
print(f"registered {len(rows)} Markdown files -> {OUT}")
