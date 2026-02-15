import json
import subprocess
import urllib.parse

from .models import FeedData, ProfileData, CommentsData
from .session import InstagramSession


class InstaClient:
    def __init__(self, csrftoken, ds_user_id, sessionid, proxy=None, use_curl=False):
        """
        :param use_curl: Se True, utiliza chamadas via subprocess CURL em vez de requests.
        """
        self.state = InstagramSession(csrftoken, ds_user_id, sessionid, proxy=proxy)
        self.use_curl = use_curl

    def _execute_request(self, method, url, params=None):
        """Gerencia se a requisição será via Requests ou CURL."""
        if params:
            url = f"{url}?{urllib.parse.urlencode(params)}"

        if not self.use_curl:
            return self.state.request_on_session(method, url)

        return self._curl_request(method, url)

    def _curl_request(self, method, url):
        """Simula o comportamento do requests utilizando o binário curl do sistema."""
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
            "-sS",
        ]

        if self.state.session.proxies.get("https"):
            command.extend(["-x", self.state.session.proxies["https"]])

        result = subprocess.run(command, capture_output=True, text=True)

        class MockResponse:
            def __init__(self, text, status_code):
                self.text = text
                self.status_code = status_code

            def json(self):
                return json.loads(self.text)

        status = 200 if result.returncode == 0 else 500
        return MockResponse(result.stdout, status)

    def get_profile_info(self, username: str, return_raw: bool = False):
        url = f"https://www.instagram.com/api/v1/users/web_profile_info/"
        params = {"username": username}
        response = self._execute_request("GET", url, params=params)

        if response.status_code != 200:
            return None

        data = response.json()
        if return_raw:
            return data

        return ProfileData.parse_instagram_json(data)

    def get_feed(self, username: str, max_id: str = "", return_raw: bool = False):
        url = f"https://www.instagram.com/api/v1/feed/user/{username}/username/"
        params = {"count": 33, "max_id": max_id}

        response = self._execute_request("GET", url, params=params)

        if response.status_code != 200:
            return None

        data = response.json()

        if return_raw:
            return data

        items = data.get("items", [])
        posts = [FeedData.parse_item(item) for item in items]

        return FeedData(
            posts=posts,
            next_max_id=data.get("next_max_id"),
            num_results=data.get("num_results", 0),
            more_available=data.get("more_available", False),
        )

    def get_comments(self, media_id: str, next_min_id: str = None, return_raw: bool = False):
        url = f"https://www.instagram.com/api/v1/media/{media_id}/comments/"

        params = {"can_support_threading": "true"}
        if next_min_id:
            params["min_id"] = next_min_id

        response = self._execute_request("GET", url, params=params)

        if response.status_code != 200:
            return None

        data = response.json()

        if return_raw:
            return data

        comments_data = data.get("comments", [])
        comments = [CommentsData.parse_item(item) for item in comments_data]

        return CommentsData(
            comments=comments,
            next_max_id=data.get("next_min_id"),
            num_results=len(comments),
            more_available=data.get("has_more_comments", False),
        )
