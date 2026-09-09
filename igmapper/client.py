import json
import subprocess
import urllib.parse

from .session import InstagramSession


class InstaClient:
    def __init__(
        self,
        csrftoken,
        ds_user_id,
        fbdtsg,
        lsd,
        sessionid,
        datr=None,
        ig_did=None,
        mid=None,
        rur=None,
        av=None,
        proxy=None,
        user_agent=None,
    ):
        self.state = InstagramSession(
            csrftoken=csrftoken,
            ds_user_id=ds_user_id,
            fbdtsg=fbdtsg,
            lsd=lsd,
            sessionid=sessionid,
            datr=datr,
            ig_did=ig_did,
            mid=mid,
            rur=rur,
            av=av,
            proxy=proxy,
            user_agent=user_agent,
        )

    def _get_jazoest(self) -> str:
        if not self.state.fbdtsg:
            return "26033"
        return "2" + str(sum(ord(c) for c in self.state.fbdtsg))

    def get_feed(self, username: str) -> dict:
        vars_dict = {
            "data": {
                "count": 12,
                "include_reel_media_seen_timestamp": True,
                "include_relationship_info": True,
                "latest_besties_reel_media": True,
                "latest_reel_media": True,
            },
            "username": username,
            "__relay_internal__pv__PolarisMultiCaptionCarouselEnabledrelayprovider": True,
            "__relay_internal__pv__PolarisShortDramaEnabledrelayprovider": False,
            "__relay_internal__pv__PolarisReelsRecoDebugOverlayEnabledrelayprovider": False,
        }
        variables = urllib.parse.quote(json.dumps(vars_dict))
        # fmt:off
        payload = f"av={self.state.av}&__d=www&__user=0&__a=1&__req=6&__hs=20703.HYP%3Ainstagram_web_pkg.2.1...0&dpr=1&__ccg=EXCELLENT&__rev=1046936532&__s=4jhz11%3Awaevfz%3A1snom8&__hsi=7682841949103505900&__dyn=7xe6E5q5U5ObxG4Vp41twpUnwgU7SbzEdF8vyUco38w5ux609vCwjE1EE2Cw8G11w6zx61vwoEcE2ygao38woE2swaO4U2zxe2GewGw9a361qw8W1uw2oEGdwtU662O0Lo6-3u2WErwfG1IwjU721IQp1yU426V8aUuwm8jw4kyVrx60hK3KaCwHwi84q2i0jK3mewkU&__csr=hD4MJkaNcRtOAOF5Aail_QX9QFLnIAEzhJuVESdbtrAQqrWjn8iml7m8JqAVKaxG7pozzebHSmT-iWKUXAgrz-V8Wiq9AKJaumWKmicULDCg_UhV9aK_xq7Aczo8ouy88UiKbGi2m3iFAFopwyxKdyECmdz8akuEgxqbwwy8OErxKdxe58bEK4UconzUyu00mxm4809oi3E0bOE0wVwEwEw1vq8wvA1cai8gKWm0jVwzz8Dw3g8x0wBw0UDw0hFm0fDwkUcUO0HQ0IEfk07GE&__hsdp=rNL6ygGpQDF5h4BY95BCVqmgW-QK9x6Fe8F7ggxe8zogKbg52FGF5uE8U2_w6kDU0qSg&__sjsp=rNL6ygGpQKh5h4BY95ze8mgVeQK9x6Fe8Kt124Uy2V0kaCGAlWwzw&__comet_req=7&fb_dtsg={self.state.fbdtsg}&jazoest=26033&lsd={self.state.lsd}&__spin_r=1046936532&__spin_b=trunk&__spin_t=1788801036&fb_api_caller_class=RelayModern&fb_api_req_friendly_name=PolarisProfilePostsQuery&server_timestamps=true&variables={variables}&doc_id=38154989454116081"
        command = ["curl", "--url", "https://www.instagram.com/graphql/query", "-H", "accept: */*", "-H", "accept-language: pt-BR,pt;q=0.9,en-GB;q=0.8,en;q=0.7", "-H", "content-type: application/x-www-form-urlencoded", "-b", self.state.cookies, "-H", "origin: https://www.instagram.com", "-H", "priority: u=1, i", "-H", f"referer: https://www.instagram.com/{username}/", "-H", "sec-ch-prefers-color-scheme: dark", "-H", 'sec-ch-ua: "Not=A?Brand";v="99", "Google Chrome";v="151", "Chromium";v="151"', "-H", 'sec-ch-ua-full-version-list: "Not=A?Brand";v="99.0.0.0", "Google Chrome";v="151.0.7922.173", "Chromium";v="151.0.7922.173"', "-H", "sec-fetch-dest: empty", "-H", "sec-fetch-mode: cors", "-H", "sec-fetch-site: same-origin", "-H", f"user-agent: {self.state.user_agent}", "-H", "x-asbd-id: 359341", "-H", "x-bloks-version-id: 394436feebb82fbc8bf09459d29e98a4182d7d9f4f36777d8278b409536b0803", "-H", f"x-csrftoken: {self.state.csrftoken}", "-H", "x-fb-friendly-name: PolarisProfilePostsQuery", "-H", f"x-fb-lsd: {self.state.lsd}", "-H", "x-ig-app-id: 936619743392459", "-H", "x-ig-max-touch-points: 0", "-H", "x-root-field-name: xdt_api__v1__feed__user_timeline_graphql_connection", "--data-raw", payload]
        # fmt:on

        if self.state.proxy:
            command.extend(["-x", self.state.proxy])

        result = subprocess.run(command, capture_output=True, text=True)
        try:
            return json.loads(result.stdout)
        except json.JSONDecodeError:
            return result.stdout

    def get_profile_id(self, username: str) -> str | None:
        feed_response = self.get_feed(username)
        edges = (
            feed_response.get("data", {})
            .get("xdt_api__v1__feed__user_timeline_graphql_connection", {})
            .get("edges", [])
        )
        for edge in edges:
            user = edge.get("node", {}).get("user", {})
            if user.get("username") == username:
                return user.get("id")
        return None

    def get_profile(self, username: str, userid: str = "") -> dict | str:
        if userid == "":
            userid = self.get_profile_id(username)
        if not userid:
            return {}

        vars_dict = {
            "enable_integrity_filters": True,
            "id": userid,
            "__relay_internal__pv__PolarisCannesGuardianExperienceEnabledrelayprovider": True,
            "__relay_internal__pv__PolarisCASB976ProfileEnabledrelayprovider": False,
            "__relay_internal__pv__PolarisWebSchoolsEnabledrelayprovider": False,
            "__relay_internal__pv__PolarisRepostsConsumptionEnabledrelayprovider": True,
            "__relay_internal__pv__PolarisShortDramaEnabledrelayprovider": False,
        }
        variables = urllib.parse.quote(json.dumps(vars_dict))
        # fmt:off

        payload = f"av={self.state.av}&__d=www&__user=0&__a=1&__req=1&__hs=20703.HYP%3Ainstagram_web_pkg.2.1...0&dpr=1&__ccg=EXCELLENT&__rev=1046936532&__s=4jhz11%3Awaevfz%3A1snom8&__hsi=7682841949103505900&__dyn=7xe6E5q5U5ObxG4Vp41twpUnwgU7SbzEdF8vyUco38w5ux609vCwjE1EE2Cw8G11w6zx61vwoEcE2ygao38woE2swaO4U2zxe2GewGw9a361qw8W1uw2oEGdwtU662O0Lo6-3u2WErwfG1IwjU721IQp1yU426V8aUuwm8jw4kyVrx60hK3KaCwHwi84q2i0jK3mewkU&__csr=hD4MJkaNcRtOAOF5Aail_QX9QFLnIAEzhJuVESdbtrAQqrWjn8iml7m8JqAVKaxG7pozzebHSmT-iWKUXAgrz-V8Wiq9AKJaumWKmicULDCg_UhV9aK_xq7Aczo8ouy88UiKbGi2m3iFAFopwyxKdyECmdz8akuEgxqbwwy8OErxKdxe58bEK4UconzUyu00mxm4809oi3E0bOE0wVwEwEw1vq8wvA1cai8gKWm0jVwzz8Dw3g8x0wBw0UDw0hFm0fDwkUcUO0HQ0IEfk07GE&__hsdp=rNL6ygGpQDF5h4BY95BCVqmgW-QK9x6Fe8F7ggxe8zogKbg52FGF5uE8U2_w6kDU0qSg&__sjsp=rNL6ygGpQKh5h4BY95ze8mgVeQK9x6Fe8Kt124Uy2V0kaCGAlWwzw&__comet_req=7&fb_dtsg={self.state.fbdtsg}&jazoest=26033&lsd={self.state.lsd}&__spin_r=1046936532&__spin_b=trunk&__spin_t=1788801036&fb_api_caller_class=RelayModern&fb_api_req_friendly_name=PolarisProfilePageContentQuery&server_timestamps=true&variables={variables}&doc_id=28036671149327607"
        command = ["curl", "--url", "https://www.instagram.com/api/graphql", "-H", "accept: */*", "-H", "accept-language: pt-BR,pt;q=0.9,en-GB;q=0.8,en;q=0.7", "-H", "content-type: application/x-www-form-urlencoded", "-b", self.state.cookies, "-H", "origin: https://www.instagram.com", "-H", "priority: u=1, i", "-H", "referer: https://www.instagram.com/", "-H", "sec-ch-prefers-color-scheme: dark", "-H", 'sec-ch-ua: "Not=A?Brand";v="99", "Google Chrome";v="151", "Chromium";v="151"', "-H", 'sec-ch-ua-full-version-list: "Not=A?Brand";v="99.0.0.0", "Google Chrome";v="151.0.7922.173", "Chromium";v="151.0.7922.173"', "-H", "sec-fetch-dest: empty", "-H", "sec-fetch-mode: cors", "-H", "sec-fetch-site: same-origin", "-H", f"user-agent: {self.state.user_agent}", "-H", "x-asbd-id: 359341", "-H", f"x-csrftoken: {self.state.csrftoken}", "-H", "x-fb-friendly-name: PolarisProfilePageContentQuery", "-H", f"x-fb-lsd: {self.state.lsd}", "-H", "x-ig-app-id: 936619743392459", "-H", "x-ig-max-touch-points: 0", "--data-raw", payload]
        # fmt:on

        if self.state.proxy:
            command.extend(["-x", self.state.proxy])

        result = subprocess.run(command, capture_output=True, text=True)
        try:
            return json.loads(result.stdout)
        except json.JSONDecodeError:
            return result.stdout

    def get_simple_feed(self, username: str) -> dict | str:
        jazoest = self._get_jazoest()
        vars_dict = {
            "data": {
                "count": 12,
                "include_reel_media_seen_timestamp": True,
                "include_relationship_info": True,
                "latest_besties_reel_media": True,
                "latest_reel_media": True,
            },
            "username": username,
            "__relay_internal__pv__PolarisMultiCaptionCarouselEnabledrelayprovider": True,
            "__relay_internal__pv__PolarisShortDramaEnabledrelayprovider": False,
            "__relay_internal__pv__PolarisReelsRecoDebugOverlayEnabledrelayprovider": False,
        }
        variables = urllib.parse.quote(json.dumps(vars_dict))
        # fmt:off
        payload = f"av={self.state.av}&__d=www&__user=0&__a=1&__req=6&__hs=20704.HYP%3Ainstagram_web_pkg.2.1...0&dpr=1&__ccg=EXCELLENT&__rev=1046968929&__s=g81rky%3Afs19h5%3Amqh4d9&__hsi=7683215160171999843&__dyn=7xe6E5q5U5ObxG4Vp41twpUnwgU7SbzEdF8vyUco38w5ux609vCwjE1EE2Cw8G11w6zx61vwoEcE2ygao38woE2swaO4U2zxe2GewGw9a361qw8W1uw2oEGdwtU662O0Lo6-3u2WErwfG1IwjU721IQp1yU426V8aUuwm8jw4kyVrx60hK3KaCwHwi84q2i0jK3mewkU&__csr=hYQ5Qc8iAAyb4O9OrkXHqkZkdehbABF29Ay5ii9ip5cm_l8xm8lpVpqm8DpagJap1eQ4bK9GO4AF2UHfvAajuPBGkCGGyaYGQFlABXUCiuEymK8CG4miEXghCHBiVqwiXx6u9AJ4x6q2CdwKyFU9t3UOufwUCy899EnG2664bF6zqwOgdEnGaxu4EhzUW6U0x20-U01wZ82Jw0Bwa02Yu08jScwww1qC2O3h3U7Cu3m41m0ktxBw3tC9Aw0UUw0hFC04fU1PoKgE0tVw&__hsdp=mzPn5E9VDimnOnsA9PrWQVLikOAeCVKbIyoCAdhqGhCBy98WbyGxq5izQBHbi4Oa5IXwAIz82m1Vwaum0Ck2-iiaGU27w8O0G82DwhE1EF81w86u3K062o0bZ81n8gw2U80i3w1ji0wU3cw&__hblp=0ay0Bomxu68swaS1cWxK0xUC9Bx60xQ2a4u4bxObwnEtwjUuzo762y2K7US9wgU4qE18U5e6EOi1iw4JKfwkUeU4q0aqw5nw83K0z82XwiUW021q0bWw8u5EdQm2y0LE5C0aSwai0wE6y0bOw2Kk0xU6W0g62O1jw8e1Hwo8&__sjsp=uzPn5E9VDigDozn2oy8QaZ9nKhkjK8yUF2qgR28my85GEgyQmKn8E&__comet_req=7&fb_dtsg={self.state.fbdtsg}&jazoest={jazoest}&lsd={self.state.lsd}&__spin_r=1046968929&__spin_b=trunk&__spin_t=1788887931&fb_api_caller_class=RelayModern&fb_api_req_friendly_name=PolarisProfilePostsQuery&server_timestamps=true&variables={variables}&doc_id=38154989454116081"
        command = ["curl", "--url", "https://www.instagram.com/graphql/query", "-H", "accept: */*", "-H", "accept-language: pt-BR,pt;q=0.9,en-GB;q=0.8,en;q=0.7", "-H", "content-type: application/x-www-form-urlencoded", "-b", self.state.cookies, "-H", "origin: https://www.instagram.com", "-H", "priority: u=1, i", "-H", f"referer: https://www.instagram.com/{username}/", "-H", "sec-ch-prefers-color-scheme: dark", "-H", 'sec-ch-ua: "Not=A?Brand";v="99", "Google Chrome";v="151", "Chromium";v="151"', "-H", 'sec-ch-ua-full-version-list: "Not=A?Brand";v="99.0.0.0", "Google Chrome";v="151.0.7922.173", "Chromium";v="151.0.7922.173"', "-H", "sec-ch-ua-mobile: ?0", "-H", 'sec-ch-ua-model: ""', "-H", 'sec-ch-ua-platform: "Linux"', "-H", 'sec-ch-ua-platform-version: ""', "-H", "sec-fetch-dest: empty", "-H", "sec-fetch-mode: cors", "-H", "sec-fetch-site: same-origin", "-H", f"user-agent: {self.state.user_agent}", "-H", "x-asbd-id: 359341", "-H", "x-bloks-version-id: 394436feebb82fbc8bf09459d29e98a4182d7d9f4f36777d8278b409536b0803", "-H", f"x-csrftoken: {self.state.csrftoken}", "-H", "x-fb-friendly-name: PolarisProfilePostsQuery", "-H", f"x-fb-lsd: {self.state.lsd}", "-H", "x-ig-app-id: 936619743392459", "-H", "x-ig-max-touch-points: 0", "-H", "x-root-field-name: xdt_api__v1__feed__user_timeline_graphql_connection", "--data-raw", payload]
        # fmt:on

        if self.state.proxy:
            command.extend(["-x", self.state.proxy])

        result = subprocess.run(command, capture_output=True, text=True)
        try:
            return json.loads(result.stdout)
        except json.JSONDecodeError:
            return result.stdout
