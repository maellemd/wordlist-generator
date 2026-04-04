import itertools
import csv
import argparse
import sys
from datetime import datetime

def get_variants(word):
    leet = str.maketrans("aeiost", "4310$7")

    variants = []
    variants.append(word)
    variants.append(word.lower())
    variants.append(word.upper())
    variants.append(word.capitalize())
    variants.append(word.lower() + word.capitalize())
    variants.append(word[::-1])  # reversed string
    variants.append(word.lower().translate(leet))

    # remove duplicates but keep the order (set() doesn't keep order)
    seen = []
    for v in variants:
        if v not in seen:
            seen.append(v)
    return seen


def date_to_formats(date_str):
    # try a few common formats because people write dates differently
    fmts = ["%Y-%m-%d", "%d/%m/%Y", "%d%m%Y"]
    dt = None

    for f in fmts:
        try:
            dt = datetime.strptime(date_str, f)
            break
        except ValueError:
            pass

    if dt is None:
        print(f"  couldn't parse date: {date_str}, skipping")
        return []

    return [
        dt.strftime("%d%m%Y"),
        dt.strftime("%Y%m%d"),
        dt.strftime("%m%Y"),
        dt.strftime("%Y"),
        dt.strftime("%d%m%y"),
        dt.strftime("%m%d%Y"),
    ]

def apply_patterns(words, patterns):
    result = []
    for p in patterns:
        for w in words:
            result.append(p.replace("{w}", w))
    return result


def make_combos(words, max_n):
    result = []
    for r in range(2, max_n + 1):
        for combo in itertools.permutations(words, r):
            result.append("".join(combo))
    return result


def passes_filter(word, min_len, need_digit, need_upper):
    if len(word) < min_len:
        return False
    if need_digit:
        has_digit = False
        for c in word:
            if c.isdigit():
                has_digit = True
                break
        if not has_digit:
            return False
    if need_upper:
        has_upper = False
        for c in word:
            if c.isupper():
                has_upper = True
                break
        if not has_upper:
            return False
    return True


def main():
    parser = argparse.ArgumentParser(description="generate wordlists from keywords and dates")

    parser.add_argument("-k", "--keywords", nargs="+", required=True, help="words to use as base")
    parser.add_argument("-d", "--dates", nargs="*", default=[], help="dates (YYYY-MM-DD or DD/MM/YYYY or DDMMYYYY)")
    parser.add_argument("-p", "--patterns", nargs="*", default=[], help="patterns like '{w}123'")
    parser.add_argument("--max-combo", type=int, default=2, help="how many keywords to combine together (default 2)")
    parser.add_argument("-o", "--output", default="wordlist.txt", help="output filename")
    parser.add_argument("--csv", action="store_true", help="also save a csv file")
    parser.add_argument("--min-length", type=int, default=4, help="minimum word length to keep")
    parser.add_argument("--require-digit", action="store_true", help="only keep words with at least one number")
    parser.add_argument("--require-upper", action="store_true", help="only keep words with at least one uppercase")

    args = parser.parse_args()

    print("\ngenerating wordlist...")
    print(f"keywords: {args.keywords}")

    all_words = []

    # variants for each keyword
    for kw in args.keywords:
        v = get_variants(kw)
        all_words.extend(v)
        print(f"  {kw} -> {len(v)} variants")

    # date formats
    if args.dates:
        for d in args.dates:
            all_words.extend(date_to_formats(d))

    # combinations of keywords
    if len(args.keywords) >= 2:
        combos = make_combos(args.keywords, args.max_combo)
        all_words.extend(combos)
        print(f"  {len(combos)} keyword combinations")

    # apply patterns
    if args.patterns:
        base = [kw.lower() for kw in args.keywords]
        patterned = apply_patterns(base, args.patterns)
        all_words.extend(patterned)

    # deduplicate
    unique = []
    for w in all_words:
        if w not in unique:
            unique.append(w)
    all_words = unique

    # filter
    before = len(all_words)
    all_words = [w for w in all_words if passes_filter(w, args.min_length, args.require_digit, args.require_upper)]
    print(f"  filtered out {before - len(all_words)} words, {len(all_words)} remaining")

    if not all_words:
        print("nothing left after filtering, try loosening the options")
        sys.exit(1)

    # save txt
    with open(args.output, "w", encoding="utf-8") as f:
        f.write("\n".join(all_words))
    print(f"\nsaved {len(all_words)} words to {args.output}")

    # save csv if asked
    if args.csv:
        csv_path = args.output.replace(".txt", ".csv")
        with open(csv_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["index", "word", "length"])
            for i, word in enumerate(all_words, 1):
                writer.writerow([i, word, len(word)])
        print(f"saved csv to {csv_path}")


if __name__ == "__main__":
    main()