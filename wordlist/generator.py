"""Smart password generator — targeted and layered"""
import os
import re
import requests
from wordlist.mutator import full_mutate, combo_variants, tr_normalize, case_variants, suffix_variants

COMMON_FILE = os.path.join(os.path.dirname(__file__), "common.txt")

KEYBOARD_WALKS = [
    "qwerty", "qwertyuiop", "asdfghjkl", "zxcvbnm",
    "1qaz2wsx", "2wsx3edc", "qazwsxedc", "1234qwer",
    "qwer1234", "q1w2e3r4", "1q2w3e4r", "1q2w3e4r5t",
    "zaq1@WSX", "!QAZ2wsx", "qazwsx",
]


def crawl_site(url):
    """Crawl site for keywords"""
    words = set()
    try:
        resp = requests.get(url, timeout=10, verify=False,
                            headers={"User-Agent": "Mozilla/5.0"})
        text = re.sub(r'<[^>]+>', ' ', resp.text)
        text = re.sub(r'[^\w\s]', ' ', text)
        for w in text.split():
            w = w.strip()
            if 4 <= len(w) <= 20 and not w.isdigit():
                words.add(tr_normalize(w.lower()))
    except Exception:
        pass
    return list(words)[:200]


def generate(usernames, company=None, keywords=None, crawl_url=None, extra_wordlist=None):
    """Layered password generation — by priority"""

    layer1 = set()  # High probability
    layer2 = set()  # Medium probability
    layer3 = set()  # Low probability

    # ===== LAYER 1: Company + username =====
    base_words = list(usernames)
    if company:
        parts = company.lower().replace('-', ' ').replace('_', ' ').split()
        base_words.extend(parts)
        base_words.append(company.lower().replace(' ', ''))
        base_words.append(company.lower().replace(' ', '_'))

    for word in base_words:
        for cv in case_variants(word):
            layer1.add(cv)
            layer1.update(suffix_variants(cv))

    # Username + company combo
    for u in usernames:
        for w in (base_words):
            if u != w:
                layer1.update(combo_variants(u, w))

    # ===== KATMAN 2: Anahtar kelimeler + site crawl =====
    extra_words = []
    if keywords:
        extra_words.extend([k.strip() for k in keywords.split(',')])

    if crawl_url:
        crawled = crawl_site(crawl_url)
        extra_words.extend(crawled)

    for word in extra_words:
        if len(word) >= 3:
            for cv in case_variants(word):
                layer2.add(cv)
                layer2.update(suffix_variants(cv))

    # ===== LAYER 3: Common weak passwords =====
    if os.path.exists(COMMON_FILE):
        with open(COMMON_FILE, "r", encoding="utf-8") as f:
            for line in f:
                pwd = line.strip()
                if pwd:
                    layer3.add(pwd)

    layer3.update(KEYBOARD_WALKS)
    layer3.update([
        "123456", "12345678", "123456789", "1234567890",
        "password", "Password1", "Password123", "P@ssw0rd",
        "P@ssw0rd!", "admin", "Admin123!", "Admin@123",
        "qwerty", "qwerty123", "abc123", "letmein",
        "welcome", "Welcome1", "Welcome1!", "Changeme1",
        "Test1234", "Passw0rd", "pass1234", "master",
        "dragon", "monkey", "shadow", "sunshine", "trustno1",
    ])

    # ===== KATMAN 4: Mutasyonlar =====
    layer4 = set()
    priority_words = list(base_words) + list(usernames)
    for word in priority_words[:20]:
        layer4.update(full_mutate(word))

    # ===== KATMAN 5: Ek wordlist =====
    layer5 = set()
    if extra_wordlist and os.path.exists(extra_wordlist):
        with open(extra_wordlist, "r", encoding="utf-8", errors="ignore") as f:
            for line in f:
                pwd = line.strip()
                if pwd and len(pwd) >= 4:
                    layer5.add(pwd)

    # Merge — by priority order
    all_passwords = []
    seen = set()

    for layer_name, layer in [("L1-firma", layer1), ("L2-keywords", layer2),
                               ("L3-common", layer3), ("L4-mutate", layer4),
                               ("L5-extra", layer5)]:
        count = 0
        for pwd in layer:
            if pwd not in seen and 3 <= len(pwd) <= 64:
                seen.add(pwd)
                all_passwords.append(pwd)
                count += 1

    return all_passwords
