import json
import subprocess
import urllib.parse

import requests

from .session import InstagramSession


class InstaClient:
    def __init__(self, csrftoken, ds_user_id, sessionid, proxy=None, use_curl=False):
        self.state = InstagramSession(csrftoken, ds_user_id, sessionid, proxy=proxy)
        self.use_curl = use_curl
        self.csrftoken = csrftoken

    def _execute_request(self, method, url, params=None, data=None, extra_headers=None):
        headers = {}
        if extra_headers:
            headers.update(extra_headers)

        if params:
            url = f"{url}?{urllib.parse.urlencode(params)}"

        if not self.use_curl:
            return self.state.request_on_session(
                method, url, data=data, headers=headers if headers else None
            )

        return self._curl_request(method, url, data=data, extra_headers=headers)

    def _curl_request(self, method, url, data=None, extra_headers=None):
        cookie_str = (
            f"csrftoken={self.state.session.cookies.get('csrftoken')}; "
            f"ds_user_id={self.state.session.cookies.get('ds_user_id')}; "
            f"sessionid={self.state.session.cookies.get('sessionid')};"
        )

        command = [
            "curl",
            "-X",
            method,
            url,
            "-H",
            f"cookie: {cookie_str}",
            "-H",
            f"x-ig-app-id: {self.state.xigappid}",
            "-H",
            f"x-csrftoken: {self.state.session.cookies.get('csrftoken')}",
            "-sS",
        ]

        if extra_headers:
            for k, v in extra_headers.items():
                command.extend(["-H", f"{k}: {v}"])

        if data:
            body = urllib.parse.urlencode(data) if isinstance(data, dict) else str(data)
            command.extend(["--data-raw", body])

        if self.state.session.proxies.get("https"):
            command.extend(["-x", self.state.session.proxies["https"]])

        result = subprocess.run(command, capture_output=True, text=True)

        class MockResponse:
            def __init__(self, text, status_code):
                self.text = text
                self.status_code = status_code

            def json(self):
                try:
                    return json.loads(self.text)
                except Exception:
                    return {}

        status = 200 if result.returncode == 0 else 500
        return MockResponse(result.stdout, status)

    def get_profile_info(self, username: str, lsd=None, doc_id=None):
        # 1º - FUNCIONA COM TODOS PERFIS, MENOS BUSINESS
        url = "https://www.instagram.com/api/v1/users/web_profile_info/"
        res = self._execute_request("GET", url, params={"username": username})

        if res.status_code == 200:
            data = res.json()
            if data.get("status") != "fail" and data.get("data", {}).get("user"):
                return data

        # 2º - USANDO GRAPHQL (caso o 1 dê errado, pode ser perfil business)
        user_id = self.get_feed(username)["user"].get("pk", None)
        url = "https://www.instagram.com/api/graphql"
        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "x-csrftoken": self.csrftoken,
            "x-fb-lsd": lsd,
        }
        payload_vars = {
            "enable_integrity_filters": True,
            "id": user_id,
            "__relay_internal__pv__PolarisCASB976ProfileEnabledrelayprovider": False,
            "__relay_internal__pv__PolarisCannesGuardianExperienceEnabledrelayprovider": True,
            "__relay_internal__pv__PolarisLongformEnabledrelayprovider": False,
            "__relay_internal__pv__PolarisRepostsConsumptionEnabledrelayprovider": True,
            "__relay_internal__pv__PolarisShortDramaEnabledrelayprovider": False,
            "__relay_internal__pv__PolarisWebSchoolsEnabledrelayprovider": False,
        }
        payload = urllib.parse.urlencode(
            {"doc_id": doc_id, "lsd": lsd, "variables": json.dumps(payload_vars)}
        )

        res = requests.post(url, headers=headers, data=payload)

        if res.status_code == 200:
            data = res.json()
            if data.get("status") != "fail":
                return data

        return None

    def get_feed(self, username: str, max_id: str = ""):
        url = f"https://www.instagram.com/api/v1/feed/user/{username}/username/"
        params = {"count": 33, "max_id": max_id}

        res = self._execute_request("GET", url, params=params)

        if res.status_code == 200:
            data = res.json()
            if data.get("status") != "fail":
                return data

        return None

    def get_comments(self, media_id: str, next_min_id: str = None):
        url = f"https://www.instagram.com/api/v1/media/{media_id}/comments/"

        params = {"can_support_threading": "true"}
        if next_min_id:
            params["min_id"] = next_min_id

        res = self._execute_request("GET", url, params=params)

        if res.status_code == 200:
            data = res.json()
            if data.get("status") != "fail":
                return data

        return None
