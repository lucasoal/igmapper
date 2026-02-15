import requests


class InstagramSession:
    def __init__(self, csrftoken, ds_user_id, sessionid, xigappid="936619743392459", proxy=None):
        self.session = requests.Session()
        self.xigappid = xigappid
        self.proxy = proxy

        self.session.cookies.set("csrftoken", csrftoken)
        self.session.cookies.set("ds_user_id", ds_user_id)
        self.session.cookies.set("sessionid", sessionid)

        self.default_headers = {
            "x-ig-app-id": self.xigappid,
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
            "accept": "*/*",
            "accept-language": "en-US,en;q=0.9",
        }
        self.session.headers.update(self.default_headers)

        if proxy:
            self.session.proxies = {"http": proxy, "https": proxy}

    def get_cookie_string(self):
        """Retorna os cookies formatados para o cabeçalho do CURL."""
        c = self.session.cookies.get_dict()
        return "; ".join([f"{k}={v}" for k, v in c.items()])

    def request_on_session(self, method, url, **kwargs):
        """Método para requisições via Requests (Python)."""
        return self.session.request(method, url, timeout=10, **kwargs)
