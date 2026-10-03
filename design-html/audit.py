"""Audit generated pages and prepare a manual review queue."""

from __future__ import annotations

import json
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parent
pages = json.loads((ROOT / "manifest.json").read_text(encoding="utf-8"))
assert len(pages) == 114, f"Expected 114 pages, got {len(pages)}"
problems = []
queue = []
for page in pages:
    page_id = page["id"]
    for path in [ROOT / "pages" / f"{page_id}.html", ROOT / "assets" / f"{page_id}-source.webp", ROOT / "assets" / f"{page_id}-art.webp"]:
        if not path.is_file() or path.stat().st_size == 0:
            problems.append(f"Missing or empty: {path}")
    layers = page["layers"]
    low = [item for item in layers if item["confidence"] < 0.75]
    queue.append({"id": page_id, "module": page["module"], "title": page["title"], "text_layers": len(layers), "low_confidence": len(low), "status": "needs-manual-review"})
if problems:
    raise SystemExit("\n".join(problems))
(ROOT / "review-queue.json").write_text(json.dumps(queue, ensure_ascii=False, indent=2), encoding="utf-8")
print(f"Pages: {len(pages)}")
print(f"Modules: {dict(Counter(item['module'] for item in pages))}")
print(f"Text layers: {sum(item['text_layers'] for item in queue)}")
print(f"Low confidence layers: {sum(item['low_confidence'] for item in queue)}")
print("All generated HTML and image assets exist. Manual review remains open for every page.")
