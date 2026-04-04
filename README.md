# wordlist-generator
Generates wordlists from keywords, dates, and patterns. I made this as a learning project - it's one of the classic beginner Python exercises in the security/CTF space.

It takes things you know about a target (name, birthday, common words) and spits out a bunch of variations: different casings, leet speak, date formats, combinations, etc.

## Requirements
Python 3.10+, nothing to install.

## How to use
```bash
python wordlist_generator.py -k alice -d 1990-07-14 -o alice.txt
```

```bash
# with patterns and csv export
python wordlist_generator.py -k admin root -p '{w}123' '{w}!!' --csv
```

```bash
# stricter filter — only keep words 8+ chars with a digit
python wordlist_generator.py -k john -d 15081988 --min-length 8 --require-digit
```

## Options
```
-k / --keywords       base words (required)
-d / --dates          dates in YYYY-MM-DD, DD/MM/YYYY, or DDMMYYYY
-p / --patterns       patterns using {w} as placeholder, e.g. '{w}123'
--max-combo           max number of keywords to combine (default: 2)
-o / --output         output file (default: wordlist.txt)
--csv                 also export a .csv with index and word length
--min-length          drop anything shorter than this (default: 4)
--require-digit       only keep entries that have at least one number
--require-upper       only keep entries that have at least one uppercase
```

## What it generates

For each keyword it makes variants like:
- original, lowercase, uppercase, capitalized
- reversed (`alice` → `ecila`)
- leet speak (`alice` → `4l1c3`)
- combinations with other keywords (`alicebob`, `bobalice`)

For dates it outputs formats like `14071990`, `19900714`, `1990`, `071990`, etc.

Patterns let you add common suffixes/prefixes: `{w}123` becomes `alice123`, `bob123`, and so on.

## Notes
This is for CTF challenges, security labs, and learning purposes only. Only use it on systems you own or have explicit permission to test.

First real Python project I'm putting on GitHub - feedback welcome.