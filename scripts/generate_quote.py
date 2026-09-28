import json
from datetime import date
from html import escape
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
q=json.loads((ROOT/"quotes.json").read_text(encoding="utf-8"))
x=q[date.today().isocalendar().week % len(q)]
(ROOT/"quote.svg").write_text(f"""<svg xmlns="http://www.w3.org/2000/svg" width="900" height="260"><rect width="900" height="260" rx="18" fill="#0d1117"/><rect x="1" y="1" width="898" height="258" rx="18" fill="none" stroke="#30363d"/><text x="450" y="60" text-anchor="middle" fill="#8b949e" font-family="Arial" font-size="14" letter-spacing="3">QUOTE OF THE WEEK</text><text x="450" y="122" text-anchor="middle" fill="#f0f6fc" font-family="Georgia" font-size="25">“{escape(x[0])}”</text><text x="450" y="168" text-anchor="middle" fill="#c9d1d9" font-family="Arial" font-size="16">— {escape(x[1])}</text><text x="450" y="211" text-anchor="middle" fill="#6e7681" font-family="Arial" font-size="11">{escape(x[2])}</text></svg>""",encoding="utf-8")
