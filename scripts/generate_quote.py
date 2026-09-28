import json
from datetime import date
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
quotes = json.loads((ROOT / "quotes.json").read_text(encoding="utf-8"))

week = date.today().isocalendar().week
item = quotes[week % len(quotes)]

quote = escape(item["quote"])
author = escape(item["author"])
source = escape(item["source"])

svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="900" height="260" viewBox="0 0 900 260">
  <rect width="900" height="260" rx="18" fill="#0d1117"/>
  <rect x="1" y="1" width="898" height="258" rx="18" fill="none" stroke="#30363d"/>
  <text x="450" y="62" text-anchor="middle" fill="#8b949e" font-family="Arial, Helvetica, sans-serif" font-size="14" letter-spacing="3">QUOTE OF THE WEEK</text>
  <text x="450" y="122" text-anchor="middle" fill="#f0f6fc" font-family="Georgia, Times New Roman, serif" font-size="25">“{quote}”</text>
  <text x="450" y="168" text-anchor="middle" fill="#c9d1d9" font-family="Arial, Helvetica, sans-serif" font-size="16">— {author}</text>
  <text x="450" y="210" text-anchor="middle" fill="#6e7681" font-family="Arial, Helvetica, sans-serif" font-size="11">{source}</text>
</svg>'''

(ROOT / "quote.svg").write_text(svg, encoding="utf-8")
