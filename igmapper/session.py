class InstagramSession:
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
        self.csrftoken = csrftoken
        self.ds_user_id = ds_user_id
        self.fbdtsg = fbdtsg
        self.lsd = lsd
        self.sessionid = sessionid
        self.datr = datr
        self.ig_did = ig_did
        self.mid = mid
        self.rur = rur
        self.av = av or ds_user_id
        self.proxy = proxy
        self.user_agent = user_agent or (
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/151.0.0.0 Safari/537.36"
        )

        cookies = [
            f"csrftoken={self.csrftoken}",
            f"ds_user_id={self.ds_user_id}",
            f"sessionid={self.sessionid}",
            "ig_nrcb=1",
            "ps_l=1",
            "ps_n=1",
            "wd=1108x958",
        ]
        if self.datr:
            cookies.append(f"datr={self.datr}")
        if self.ig_did:
            cookies.append(f"ig_did={self.ig_did}")
        if self.mid:
            cookies.append(f"mid={self.mid}")
        if self.rur:
            cookies.append(f"rur={self.rur}")

        self.cookies = "; ".join(cookies)
