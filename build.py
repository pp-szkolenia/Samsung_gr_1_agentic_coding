#!/usr/bin/env python3
"""Generuje cheatsheet.html na podstawie commands.json.

Użycie: python3 build.py [wejście.json] [wyjście.html]
"""
import json
import sys
from pathlib import Path

HERE = Path(__file__).parent
src = Path(sys.argv[1]) if len(sys.argv) > 1 else HERE / "commands.json"
dst = Path(sys.argv[2]) if len(sys.argv) > 2 else HERE / "cheatsheet.html"

data = json.loads(src.read_text(encoding="utf-8"))
template = (HERE / "template.html").read_text(encoding="utf-8")

# "</" jest escapowane, żeby dane nie mogły zamknąć tagu <script>
payload = json.dumps(data, ensure_ascii=False).replace("</", "<\\/")
html = template.replace("/*__DATA__*/null", payload).replace("__TITLE__", data.get("title", "Cheatsheet"))

dst.write_text(html, encoding="utf-8")
count = sum(len(c["commands"]) for c in data["categories"])
print(f"Zapisano {dst} ({len(data['categories'])} kategorii, {count} komend)")
