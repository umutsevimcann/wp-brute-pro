"""Password mutations — generates dozens of variants from a word"""

LEET = {'a': ['@', '4'], 'e': ['3'], 'i': ['1', '!'], 'o': ['0'], 's': ['$', '5'], 't': ['7']}
SUFFIXES = ['!', '@', '#', '.', '*', '!!', '123', '1234', '1', '12', '321', '!@#']
PREFIXES = ['!', '@', '123', '1']
YEARS = ['2019', '2020', '2021', '2022', '2023', '2024', '2025', '2026']
TR_MAP = {'ğ': 'g', 'ü': 'u', 'ş': 's', 'ı': 'i', 'ö': 'o', 'ç': 'c', 'Ğ': 'G', 'Ü': 'U', 'Ş': 'S', 'İ': 'I', 'Ö': 'O', 'Ç': 'C'}


def tr_normalize(word):
    for k, v in TR_MAP.items():
        word = word.replace(k, v)
    return word


def case_variants(word):
    v = {word, word.lower(), word.upper(), word.capitalize(), word.swapcase()}
    if len(word) > 1:
        v.add(word[0].upper() + word[1:].lower())
    return v


def leet_variants(word):
    results = set()
    w = word.lower()
    for i, ch in enumerate(w):
        if ch in LEET:
            for rep in LEET[ch]:
                results.add(w[:i] + rep + w[i+1:])
    # double leet
    for i, ch in enumerate(w):
        if ch in LEET:
            for rep in LEET[ch]:
                w2 = w[:i] + rep + w[i+1:]
                for j, ch2 in enumerate(w2):
                    if ch2 in LEET and j != i:
                        for rep2 in LEET[ch2]:
                            results.add(w2[:j] + rep2 + w2[j+1:])
    return results


def suffix_variants(word):
    results = set()
    for s in SUFFIXES:
        results.add(f"{word}{s}")
    for y in YEARS:
        results.add(f"{word}{y}")
        results.add(f"{word}{y[-2:]}")
        for s in ['!', '@', '#', '!!', '.']:
            results.add(f"{word}{y}{s}")
            results.add(f"{word}{y[-2:]}{s}")
    return results


def prefix_variants(word):
    results = set()
    for p in PREFIXES:
        results.add(f"{p}{word}")
    return results


def combo_variants(word1, word2):
    results = set()
    for sep in ['', '_', '.', '-', '@']:
        results.add(f"{word1}{sep}{word2}")
        results.add(f"{word2}{sep}{word1}")
        results.add(f"{word1.capitalize()}{sep}{word2.capitalize()}")
    return results


def full_mutate(word):
    """Generate all variants from a word"""
    all_v = set()
    word = tr_normalize(word)
    for cv in case_variants(word):
        all_v.add(cv)
        all_v.update(suffix_variants(cv))
        all_v.update(prefix_variants(cv))
    all_v.update(leet_variants(word))
    for lv in leet_variants(word):
        all_v.update(suffix_variants(lv))
    return all_v
