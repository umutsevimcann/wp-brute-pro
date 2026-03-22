"""False positive prevention — verifies found password with multiple methods"""
import requests
import base64
from evasion.useragent import get_headers


class Validator:
    def __init__(self, url, timeout=15):
        self.url = url.rstrip('/')
        self.timeout = timeout

    def verify(self, username, password):
        """Verify with multiple methods — at least 1 success = real password"""
        results = []
        results.append(self._verify_xmlrpc(username, password))
        results.append(self._verify_restapi(username, password))
        return any(results)

    def _verify_xmlrpc(self, username, password):
        """wp.getUsersBlogs single call"""
        pwd_safe = password.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
        xml = f"""<?xml version="1.0"?>
<methodCall>
  <methodName>wp.getUsersBlogs</methodName>
  <params>
    <param><value><string>{username}</string></value></param>
    <param><value><string>{pwd_safe}</string></value></param>
  </params>
</methodCall>"""
        try:
            resp = requests.post(
                f"{self.url}/xmlrpc.php",
                data=xml.encode('utf-8'),
                headers=get_headers({"Content-Type": "text/xml"}),
                timeout=self.timeout, verify=False
            )
            if resp.status_code == 200:
                if 'faultCode' in resp.text:
                    return False
                if any(k in resp.text for k in ['isAdmin', 'blogid', 'blogName']):
                    return True
        except Exception:
            pass
        return False

    def _verify_restapi(self, username, password):
        """REST API Basic Auth"""
        creds = base64.b64encode(f"{username}:{password}".encode()).decode()
        try:
            resp = requests.get(
                f"{self.url}/wp-json/wp/v2/users/me?context=edit",
                headers=get_headers({"Authorization": f"Basic {creds}"}),
                timeout=self.timeout, verify=False
            )
            if resp.status_code == 200:
                data = resp.json()
                if data.get('id'):
                    return True
        except Exception:
            pass
        return False
