"""Proxy rotation — switch to next proxy on ban"""
import os
import random


class ProxyRotator:
    def __init__(self, proxy_file=None, proxies=None):
        self.proxies = []
        self.current_index = 0
        self.banned = set()
        self.no_proxy = {"http": None, "https": None}

        if proxy_file and os.path.exists(proxy_file):
            with open(proxy_file, "r") as f:
                for line in f:
                    p = line.strip()
                    if p and not p.startswith("#"):
                        self.proxies.append(self._normalize(p))
        if proxies:
            for p in proxies:
                self.proxies.append(self._normalize(p))

    def _normalize(self, proxy):
        proxy = proxy.strip()
        if not proxy.startswith(("http://", "https://", "socks4://", "socks5://")):
            proxy = f"http://{proxy}"
        return proxy

    def has_proxies(self):
        return len(self.proxies) > 0

    def get_current(self):
        if not self.proxies:
            return None
        available = [p for p in self.proxies if p not in self.banned]
        if not available:
            return None
        idx = self.current_index % len(available)
        proxy = available[idx]
        return {"http": proxy, "https": proxy}

    def rotate(self):
        self.current_index += 1
        current = self.get_current()
        return current

    def mark_banned(self, proxy_dict):
        if proxy_dict:
            url = proxy_dict.get("http") or proxy_dict.get("https")
            if url:
                self.banned.add(url)

    def get_random(self):
        available = [p for p in self.proxies if p not in self.banned]
        if not available:
            return None
        proxy = random.choice(available)
        return {"http": proxy, "https": proxy}

    def available_count(self):
        return len([p for p in self.proxies if p not in self.banned])

    def stats(self):
        return {
            "total": len(self.proxies),
            "banned": len(self.banned),
            "available": self.available_count(),
        }
