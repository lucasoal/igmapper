import json
import random
import string
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

    # def get_profile_id(self, username: str) -> str | None:
    #     feed_response = self.get_feed(username)
    #     edges = (
    #         feed_response.get("data", {})
    #         .get("xdt_api__v1__feed__user_timeline_graphql_connection", {})
    #         .get("edges", [])
    #     )
    #     try:
    #         for edge in edges:
    #             user = edge.get("node", {}).get("user", {})
    #             if user.get("username") == username:
    #                 return user.get("id")
    #     except Exception as e:
    #         return e

    def _get_profile_id_anonymous(self, username: str = None) -> str:
        random_csrftoken = "".join(
            random.choice(string.ascii_letters + string.digits) for _ in range(32)
        )
        # fmt:off
        command = [
            "curl", "--url", "https://www.instagram.com/ajax/bulk-route-definitions/",
            "-H", "accept: */*", "-H", "accept-language: pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7", "-H", "content-type: application/x-www-form-urlencoded",
            # "-b", f"csrftoken=hWv1HUEXWJXrjQJ0Y3nI39; datr=H2ihap7UBS1zV2kDiVjHShzu; ig_did=18259CA3-CC0A-46AA-B15E-57D46B9065FB; mid=aqFoIAAEAAGyDFhRNqnbKpwaNnSJ; wd=1077x958",
            "-b", f"csrftoken={random_csrftoken}; datr=H2ihap7UBS1zV2kDiVjHShzu; ig_did=18259CA3-CC0A-46AA-B15E-57D46B9065FB; mid=aqFoIAAEAAGyDFhRNqnbKpwaNnSJ; wd=1077x958",
            "-H", "origin: https://www.instagram.com", "-H", "priority: u=1, i", "-H", f"referer: https://www.instagram.com/{username}/", "-H", "sec-ch-prefers-color-scheme: dark",
            "-H", 'sec-ch-ua: "Not=A?Brand";v="99", "Google Chrome";v="151", "Chromium";v="151"',
            "-H", 'sec-ch-ua-full-version-list: "Not=A?Brand";v="99.0.0.0", "Google Chrome";v="151.0.7922.173", "Chromium";v="151.0.7922.173"',
            "-H", "sec-ch-ua-mobile: ?0", "-H", 'sec-ch-ua-model: ""', "-H", 'sec-ch-ua-platform: "Linux"', "-H", 'sec-ch-ua-platform-version: ""',
            "-H", "sec-fetch-dest: empty", "-H", "sec-fetch-mode: cors", "-H", "sec-fetch-site: same-origin",
            "-H", "user-agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/151.0.0.0 Safari/537.36",
            "-H", "x-asbd-id: 359341", "-H", "x-fb-lsd: AdT9k8PRVpJsQi_dNcZjFumNFSk", "-H", "x-ig-d: www", "-H", "x-ig-max-touch-points: 0", "--data-raw",
            f"route_urls[0]=%2F{username}%2F&routing_namespace=igx_www%24a%2487a091182d5bd65bcb043a2888004e09&__d=www&__user=0&__a=1&__req=3&__hs=20705.HYP%3Ainstagram_web_pkg.2.1...0&dpr=1&__ccg=EXCELLENT&__rev=1047079153&__s=zlpokx%3Ah5wh9a%3A34lli1&__hsi=7683537958032746721&__dyn=7xeUjG1mxu1syaxG4Vp41twpUnwgU7SbzEdF8vyUco2qwJyE1kUhw2nVE4W0qa321Rw8G11wBz81s8hwGxu786a3a1YwBgao6C1uwoE2swlo8od8-U2zxe2GewGw9a361qw8Xxm16wa-0oa2-azo7u3C2u2J0bS1LyUaUbGxK3R08-269wr84-6o5p389oed6goK10xKi2K7E5y4U158KmUhw4rwXyFEaVE461Hwj83KwRzk1jw&__csr=gpR5gniPFlQDftkv_ibJUAR64nhh9iBJzXGpliLVaF4eHZaiAiu699Bnl4DAGh2u9DHWBRZ6ajrXAiTlWmhlPisClJdqlJLvAHHmiuVp4WQuynQdDGrGF7VpXXBVpAXhECQ-maCDBACDgy7E-EqyFoK5ppUO9x6VVFVEhyqGSqdBmfyqxeVFKiiqWwLx2QqFFpoK9BgOeCyEGezUlhoGax-5VbmcyJ1ucGHwLw0x2Aw2kU3yw083-00ReoO2u08Vw2S8ja0fra0f_g9U5fc027C1oN4i5U2YwJwUw8ato0yG09Ww5QwBo-Eb4exV3q8FoK1Zgf446qby80nLBwjC01J8w0BGUiw0xmw2Yo0Oe&__hsdp=l156MT1H4RT1L9664FAAqiioDyk64ezknuh4osK2yMGaGA6UPe26i1cDg8Ae80D8ig2qxRaWmu9AxB48dz9EgK0hObx21LxG2u1cwAg8EcpES1nw_wSwj8S3e18x6322i1dx26E4KU1-bw8C0JE0Z-0cGwfW687-07to5y582iBlwtU0Ne2W0hKi1Nw5rw4cg0VW08Lwto2fwdKubJo6il0&__hblp=0hU5C3S0xo6679ErwXU4u7Elm9Cw-wfSp1CcnDypbwIz9EgKi19x23am1LxebBCK585qUqxq484O2dwyxd1Oqdxa14w_wAx61cCCwPwi8yrwMxe484SfgqwIwloaE6W3G1lg2pK1HxS0JE1lU8U-0BEnwfK1SwNwl80Jm0_EowvU0ghwsE1qU6K0KE5S2a3m58vAyEb8dplo7um0zE2Xw72wKwaW1IAwlUpw5rw4cg0VW2-0C84Hwca2e7UixW1mwEwpE2rw_DyXm1ABg&__sjsp=l156MT1H99ns9MhOhxx0GhF99yu9xGexjpAhxOUbhEng&__comet_req=7&lsd=AdT9k8PRVpJsQi_dNcZjFumNFSk&jazoest=22406&__spin_r=1047079153&__spin_b=trunk&__spin_t=1788963088&__crn=comet.igweb.PolarisLoggedOutDesktopWWWProfileRoute",
        ]
        # fmt:on

        result = subprocess.run(command, capture_output=True, text=True)

        try:
            if result.returncode == 0:
                json_str = result.stdout.replace("for (;;);", "").strip()
                data_json = json.loads(json_str)
                return data_json["payload"]["payloads"][f"/{username}/"]["result"][
                    "exports"
                ]["rootView"]["props"]["id"]
        except Exception as e:
            return e

    def get_profile(self, username: str = None) -> dict | str:

        userid = self._get_profile_id_anonymous(username)

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

        try:
            result = subprocess.run(command, capture_output=True, text=True)
            return json.loads(result.stdout)
        except Exception as e:
            return e

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

        try:
            result = subprocess.run(command, capture_output=True, text=True)
            return json.loads(result.stdout)
        except Exception as e:
            return e
