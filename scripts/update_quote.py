#!/usr/bin/env python3
"""Update the "Quote of the Day" block in README.md.

Usage:
    python3 scripts/update_quote.py              # quote for today (WIB, UTC+7)
    python3 scripts/update_quote.py 2026-10-01   # quote for a specific date (testing)

How it picks a quote:
    Every quote in quotes.json is shown exactly once per cycle, in a shuffled
    order that changes each cycle. The pick depends only on the date, so
    running the script twice on the same day gives the same result.
"""
import json
import random
import re
import sys
from datetime import date, datetime, timedelta, timezone
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
README = ROOT / "README.md"
QUOTES = ROOT / "quotes.json"

WIB = timezone(timedelta(hours=7))  # Jakarta time
START, END = "<!--QUOTE_START-->", "<!--QUOTE_END-->"


def cycle_order(n, cycle):
    order = list(range(n))
    random.Random(cycle).shuffle(order)
    return order


def pick(quotes, day):
    n = len(quotes)
    cycle, pos = divmod(day.toordinal(), n)
    order = cycle_order(n, cycle)
    # avoid showing the same quote two days in a row at a cycle boundary
    if n > 1 and cycle_order(n, cycle - 1)[-1] == order[0]:
        order[0], order[1] = order[1], order[0]
    return quotes[order[pos]]


def render(q):
    text = escape(q["text"], quote=False)
    author = escape(q["author"], quote=False)
    return (
        '<p align="center">\n'
        f"  <i>“{text}”</i><br/>\n"
        f"  — <b>{author}</b>\n"
        "</p>"
    )


def main():
    day = date.fromisoformat(sys.argv[1]) if len(sys.argv) > 1 else datetime.now(WIB).date()

    quotes = json.loads(QUOTES.read_text(encoding="utf-8"))
    if not quotes:
        sys.exit("quotes.json is empty")

    content = README.read_text(encoding="utf-8")
    pattern = re.compile(re.escape(START) + r".*?" + re.escape(END), re.S)
    if not pattern.search(content):
        sys.exit(f"Markers {START} ... {END} not found in README.md")

    block = f"{START}\n{render(pick(quotes, day))}\n{END}"
    updated = pattern.sub(lambda _m: block, content)

    if updated != content:
        README.write_text(updated, encoding="utf-8")
        print(f"README updated for {day}")
    else:
        print(f"README already up to date for {day}")


if __name__ == "__main__":
    main()
