"""Target reconnaissance — WordPress version, login URL, XML-RPC, WAF detection
Single session, SSL verify=False, retry, direct POST for XML-RPC detection"""
import re
import requests
import time
import urllib3
urllib3.disable_warnings()

from evasion.useragent import get_headers

HIDDEN_LOGIN_PATHS = [
    "/giris", "/login", "/admin-login", "/gizli-giris", "/yonetim",
    "/panel", "/signin", "/log-in", "/oturum-ac", "/hesap",
    "/kullanici-girisi", "/my-account", "/hesabim", "/manage",
    "/wp-yonetim", "/dashboard", "/admin", "/giris",
]


class Scanner:
    def __init__(self, url, timeout=15, proxies=None):
        self.url = url.rstrip('/')
        self.timeout = timeout
        self.session = requests.Session()
        self.session.verify = False
        self.session.headers.update(get_headers())
        if proxies:
            self.session.proxies.update(proxies)
        self.info = {
            "wp_version": None,
            "login_url": None,
            "xmlrpc_active": False,
            "xmlrpc_methods": 0,
            "has_captcha": False,
            "has_waf": None,
            "waf_name": None,
            "users": [],
            "plugins": [],
            "plugin_versions": {},
        }

    def scan(self, log_fn=None):
        """Run full scan"""
        self._detect_waf()
        self._detect_wp_version()
        self._find_login_url()
        self._check_xmlrpc()
        self._enumerate_users()
        self._detect_plugins()
        return self.info

    def _get(self, path="", retries=2, **kwargs):
        for attempt in range(retries):
            try:
                return self.session.get(f"{self.url}{path}", timeout=self.timeout, **kwargs)
            except Exception:
                if attempt < retries - 1:
                    time.sleep(2)
        return None

    def _post(self, path="", retries=2, **kwargs):
        for attempt in range(retries):
            try:
                return self.session.post(f"{self.url}{path}", timeout=self.timeout, **kwargs)
            except Exception:
                if attempt < retries - 1:
                    time.sleep(2)
        return None

    def _detect_waf(self):
        resp = self._get("/")
        if resp is None:
            return
        headers = {k.lower(): v.lower() for k, v in resp.headers.items()}
        server = headers.get("server", "")
        if "cloudflare" in server:
            self.info["has_waf"], self.info["waf_name"] = True, "Cloudflare"
        elif "sucuri" in server or any("sucuri" in v for v in headers.values()):
            self.info["has_waf"], self.info["waf_name"] = True, "Sucuri"
        elif "wordfence" in (resp.text[:5000]).lower():
            self.info["has_waf"], self.info["waf_name"] = True, "Wordfence"
        else:
            self.info["has_waf"] = False

    def _detect_wp_version(self):
        resp = self._get("/")
        if resp is None:
            return
        match = re.search(r'<meta name="generator" content="WordPress ([0-9.]+)"', resp.text)
        if match:
            self.info["wp_version"] = match.group(1)
            return
        resp2 = self._get("/feed/")
        if resp2:
            match2 = re.search(r'generator>https://wordpress\.org/\?v=([0-9.]+)', resp2.text)
            if match2:
                self.info["wp_version"] = match2.group(1)

    def _find_login_url(self):
        resp = self._get("/wp-login.php", allow_redirects=False)
        if resp and resp.status_code == 200 and 'name="log"' in resp.text:
            self.info["login_url"] = f"{self.url}/wp-login.php"
            self._check_captcha(resp.text)
            return
        if resp and resp.status_code in [301, 302]:
            location = resp.headers.get("Location", "")
            if location:
                try:
                    resp2 = self.session.get(location, timeout=self.timeout, allow_redirects=True)
                    if resp2 and resp2.status_code == 200 and 'name="log"' in resp2.text:
                        self.info["login_url"] = resp2.url
                        self._check_captcha(resp2.text)
                        return
                except Exception:
                    pass
        for path in HIDDEN_LOGIN_PATHS:
            resp = self._get(f"{path}/", allow_redirects=True)
            if resp and resp.status_code == 200:
                if 'name="log"' in resp.text and 'name="pwd"' in resp.text:
                    self.info["login_url"] = resp.url
                    self._check_captcha(resp.text)
                    return
            time.sleep(0.5)

    def _check_captcha(self, html):
        for sign in ["recaptcha", "captcha", "turnstile", "hcaptcha", "g-recaptcha"]:
            if sign in html.lower():
                self.info["has_captcha"] = True
                return

    def _check_xmlrpc(self):
        xml = '<?xml version="1.0"?><methodCall><methodName>system.listMethods</methodName></methodCall>'
        resp = self._post("/xmlrpc.php", data=xml.encode('utf-8'),
                          headers={"Content-Type": "text/xml"}, retries=3)
        if resp and resp.status_code == 200 and "system.multicall" in resp.text:
            self.info["xmlrpc_active"] = True
            methods = re.findall(r'<string>([^<]+)</string>', resp.text)
            self.info["xmlrpc_methods"] = len(methods)
            return
        resp2 = self._get("/xmlrpc.php")
        if resp2 and resp2.status_code == 405:
            resp3 = self._post("/xmlrpc.php", data=xml.encode('utf-8'),
                               headers={"Content-Type": "text/xml"})
            if resp3 and "system.multicall" in resp3.text:
                self.info["xmlrpc_active"] = True
                methods = re.findall(r'<string>([^<]+)</string>', resp3.text)
                self.info["xmlrpc_methods"] = len(methods)

    def _enumerate_users(self):
        resp = self._get("/wp-json/wp/v2/users?per_page=50")
        if resp and resp.status_code == 200:
            try:
                users = resp.json()
                if isinstance(users, list) and users:
                    for u in users:
                        self.info["users"].append({"id": u.get("id"), "name": u.get("name"), "slug": u.get("slug")})
                    return
            except Exception:
                pass
        resp = self._get("/?rest_route=/wp/v2/users")
        if resp and resp.status_code == 200:
            try:
                users = resp.json()
                if isinstance(users, list) and users:
                    for u in users:
                        self.info["users"].append({"id": u.get("id"), "name": u.get("name"), "slug": u.get("slug")})
                    return
            except Exception:
                pass
        for n in range(1, 6):
            resp = self._get(f"/?author={n}", allow_redirects=False)
            if resp and resp.status_code in [301, 302]:
                location = resp.headers.get("Location", "")
                match = re.search(r'/author/([^/]+)', location)
                if match:
                    self.info["users"].append({"id": n, "name": match.group(1), "slug": match.group(1)})
            time.sleep(0.3)

    def _detect_plugins(self):
        resp = self._get("/")
        if resp:
            plugins = set(re.findall(r'wp-content/plugins/([^/"\']+)', resp.text))
            self.info["plugins"] = sorted(plugins)
            versions = re.findall(r'wp-content/plugins/([^/"\']+)[^"\']*\?ver=([0-9.]+)', resp.text)
            for name, ver in versions:
                self.info["plugin_versions"][name] = ver
