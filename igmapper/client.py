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

    def get_feed(self, username: str, after: str = None) -> dict:
        data_payload = {
            "count": 32,
            "include_reel_media_seen_timestamp": True,
            "include_relationship_info": True,
            "latest_besties_reel_media": True,
            "latest_reel_media": True,
        }

        if after:
            doc_id = "39535953862670189"
            friendly_name = "PolarisProfilePostsTabContentQuery_connection"
            vars_dict = {
                "after": after,
                "before": None,
                "data": data_payload,
                "first": 12,
                "include_multi_captions": True,
                "last": None,
                "username": username,
                "__relay_internal__pv__PolarisMultiCaptionCarouselEnabledrelayprovider": True,
                "__relay_internal__pv__PolarisShortDramaEnabledrelayprovider": False,
                "__relay_internal__pv__PolarisReelsRecoDebugOverlayEnabledrelayprovider": False,
            }
        else:
            doc_id = "38154989454116081"
            friendly_name = "PolarisProfilePostsQuery"
            vars_dict = {
                "data": data_payload,
                "username": username,
                "__relay_internal__pv__PolarisMultiCaptionCarouselEnabledrelayprovider": True,
                "__relay_internal__pv__PolarisShortDramaEnabledrelayprovider": False,
                "__relay_internal__pv__PolarisReelsRecoDebugOverlayEnabledrelayprovider": False,
            }

        variables = urllib.parse.quote(json.dumps(vars_dict))

        # fmt:off
        payload = f"av={self.state.av}&__d=www&__user=0&__a=1&__req=p&__hs=20705.HYP%3Ainstagram_web_pkg.2.1...0&dpr=1&__ccg=EXCELLENT&__rev=1047087785&__s=bvefq6%3A27wtxx%3A3we0wk&__hsi=7683573197772336830&__dyn=7xeUjG1mxu1syaxG4Vp41twpUnwgU7SbzEdF8vyUco2qwJyEiw50x609vCwjE1EEc87m0yE462mcw5Mx62G5UswoEcE7O2l0Fwqo5W1yw9O1lwxwQzXwae4UaEW2G0AEco5G0zK5o4q0HU1wEbUGdwtUeo9UaQ0Lo6-bwHwKG6Ufk0zU8oC1IwjUpwlAcwBwUQp1yU426V8aUuwm8jxK0-8KmUhw4rwXyFEaVE4616wAwj83KwRyrg5e&__csr=hA8gP1xMEOP8lNdqh1pRpQBZ7XLfeiGpfmBCtQIAJTV5QihpaHGVt9k9Apy9HXSyoSKaiylh4yaGWKgxjFZIy_Q_5qriTsBqb8AGeiy4OnUy8CmXhDzaFpGiKjVWjGAp4QbCGul9x2l5AALwFh9YwugOaxh5zrzVpo99GGQmeCUhGfJKqK4WUjAxirQ8zFGGmiVArCzeUPzkUycG5ECbxyilu9xt3VHU8poLKuFFAbAw0BeCw6UwkE2xwsUW01-Sw0dgO5Ugw2gE0HhG58980YQE0_Z3o40yxh00yVwR4UB2Xc0hK8yU20yEO8w2bE0BC0n62C7k22vAxR8QwS0JF44k4qChGw1rCi1Xo06RC02pmU4e0c4wtk0bRw6Aw2g8&__hsdp=g9Y7JkMnmx_oVWt5fEj4dOGgMrBmAAkFAfQAlFR1JzKUu88afzF8iwXGcUsgg819w851-U6dyeV8Obzt1xswKcBG48fU2AUa8Ki32U3cxK7Uaoco4OEiAwsoqwRx6u1PzUhwzwSw-xBa12wjU11u08Ew8C0Do0i-w_w5Jw1kC0aewqo8U2fCO0FwiU0Lm320hGE6K0ot054w2jo0Pi2q0x838lU7C0FFk&__hblp=1C6EhwnEeo98jwgFFHzECaqgC11wh8PzGLwyhVV5z89p9-i364bwd62KFK4peVk8GdQczEXUGmEgCUdEkDxO4U4iaBm2yVV9A5UgK19xG6EO3-6Uiz8at0Kwjaxai1fwxxG4U8qy9pU6WQm9x62eUcEfk7k3u9wjawYwSwSwmK0Sku0km0yo521cw4iyU4q320y83pw74w_wpE6m1WwBw3Ro1sU18U660L84K3m3eu6UvBwqpIwG5VFE4i1EwNwLw2aEc82DwsGz85ym0ot0em1uw2jo38g2owhK0W84S10x22q3e1gw9y2ZnwsFE2CBg&__sjsp=g9Y6kllc9MRq7Z3S8hjW4N3sGAc6VlF968p3Z95qpMixW0FU&__comet_req=7&fb_dtsg={self.state.fbdtsg}&jazoest=26543&lsd={self.state.lsd}&__spin_r=1047087785&__spin_b=trunk&__spin_t=1788971293&__crn=comet.igweb.PolarisProfilePostsTabRoute&fb_api_caller_class=RelayModern&fb_api_req_friendly_name={friendly_name}&server_timestamps=true&variables={variables}&doc_id={doc_id}"
        command = ["curl", "--url", "https://www.instagram.com/graphql/query", "-H", "accept: */*", "-H", "accept-language: pt-BR,pt;q=0.9,en-GB;q=0.8,en;q=0.7", "-H", "content-type: application/x-www-form-urlencoded", "-b", self.state.cookies, "-H", "origin: https://www.instagram.com", "-H", "priority: u=1, i", "-H", f"referer: https://www.instagram.com/{username}/", "-H", "sec-ch-prefers-color-scheme: dark", "-H", 'sec-ch-ua: "Not=A?Brand";v="99", "Google Chrome";v="151", "Chromium";v="151"', "-H", 'sec-ch-ua-full-version-list: "Not=A?Brand";v="99.0.0.0", "Google Chrome";v="151.0.7922.173", "Chromium";v="151.0.7922.173"', "-H", "sec-fetch-dest: empty", "-H", "sec-fetch-mode: cors", "-H", "sec-fetch-site: same-origin", "-H", f"user-agent: {self.state.user_agent}", "-H", "x-asbd-id: 359341", "-H", "x-bloks-version-id: 394436feebb82fbc8bf09459d29e98a4182d7d9f4f36777d8278b409536b0803", "-H", f"x-csrftoken: {self.state.csrftoken}", "-H", f"x-fb-friendly-name: {friendly_name}", "-H", f"x-fb-lsd: {self.state.lsd}", "-H", "x-ig-app-id: 936619743392459", "-H", "x-ig-max-touch-points: 0", "-H", "x-root-field-name: xdt_api__v1__feed__user_timeline_graphql_connection", "--data-raw", payload]
        # fmt:on

        if self.state.proxy:
            command.extend(["-x", self.state.proxy])

        try:
            result = subprocess.run(command, capture_output=True, text=True)
            return json.loads(result.stdout)
        except Exception as e:
            return e
