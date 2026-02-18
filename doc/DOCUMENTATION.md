# User Guide

<h3>Table of Contents</h3>

- [**`InstaClient`**](#instaclient): Initializes the session and handles transport selection (Requests or CURL)
  - [**`get_profile_info()`**](#get_profile_info): Scrapes profile metadata and returns a structured ProfileData object.
  - [**`get_feed()`**](#get_feed): Retrieves user timeline posts with built-in pagination support.
  - [**`get_comments()`**](#get_comments): Fetches media comments and automates cursor-based pagination.
- [**Raw Responses Examples**](#-raw-responses-examples)

<hr>

### `InstaClient`
This **class** provides the core engine for authentication and request transport.

> [!IMPORTANT]
> You will need to fill in the parameters for the request. See here how to get them:
> - [**❗How to obtain the parameters to make the request**](https://github.com/lucasoal/igmapper/blob/main/doc/HOT_TO.md)

```py
from igmapper import InstaClient

client = InstaClient(
    csrftoken="0zzZzzzzzz0ZZZZzZZZZzzzz0Zz0ZZzz",
    ds_user_id="00000000000",
    sessionid="00000000000%3AzzzzZZZZzZZ0ZZ%3A00%3AZZzZz00ZZZzzzZ0ZzzZzzZzzZzZ0_zZz0ZzZZ0zZZZ",
    proxy=None, # optional
    use_curl=True, # optional
)
```

_For public information, use only the `csrftoken` obtained without needing to log in, leaving the other fields as "`None`". For information that requires login (such as on the website/app), fill in all authentication fields. <br>_
- _`proxy`: Use this option to make the request through a specific proxy._
- _`use_curl`: Set to True or False to choose whether the request will be made with `CURL` or via `Requests`._

<hr>

### `get_profile_info()`
This **method** scrapes profile metadata and returns a structured ProfileData object.

```py
prof = client.get_profile_info("leomessi") # return Class Object

print(prof.username)       # leomessi
print(prof.follower_count) # 511525283
print(prof.business_email) # None
```

```py
# OR
client.get_profile_info("leomessi", return_raw=True) # return JSON
```

| Section | Fields |
|---------|--------|
| 🔎 Basic Infos | `id`, `username`, `full_name`, `biography`, `profile_pic_url` |
| 🔐 Account Status | `is_private`, `is_verified`, `is_business_account`, `is_professional_account` |
| 📊 Metrics | `follower_count`, `following_count`, `total_posts`, `highlight_reel_count`, `mutual_followers` |
| 🏷 Category | `category_name`, `business_category_name`, `should_show_category` |
| 🎬 Features | `has_clips`, `has_guides`, `has_channel` |
| 🔗 Links | `external_url`, `bio_links` |
| 📍 Business Address | `business_address` |
| 📞 Public Contacts | `should_show_public_contacts`, `business_email`, `business_phone_number` |

<hr>

### `get_feed()`
This **method** retrieves user timeline posts with built-in pagination support.

```py
feed = client.get_feed("leomessi")

for i in feed.posts:
    print(i.post_id)   # 3762701545612571046_427553890
    print(i.caption)   # Anoche volví a un ...
    print(i.media_url) # https://instagram.fp...
```

```py
# OR
client.get_feed("leomessi", return_raw=True) # return JSON
```

| Section | Fields |
|---------|--------|
| 📌 Identification | `post_id`, `pk`, `shortcode` |
| 🕒 Date | `created_at` |
| 📝 Content | `caption`, `media_url`, `media_type`, `carousel_media_count` |
| 📊 Engagement | `like_count`, `comment_count`, `view_count` |
| 📦 Complete Feed Structure | `posts`, `next_max_id`, `num_results`, `more_available` |

<hr>

### `get_comments()`
This **method** fetches media comments and automates cursor-based pagination.

```py
comms = client.get_comments(media_id="3762701545612571046")

for i in comms.comments:
    print(i.username)   # 256312688045976769
    print(i.comment_id) # the_uusername123
    print(i.text)       # BUENAS NOCHES, SOY...
```

```py
# OR
client.get_comments(media_id="3762701545612571046", return_raw=True) # return JSON
```

| Section | Fields |
|---------|--------|
| 📝 Comment Details | `comment_id`, `media_id`, `text`, `created_at`, `like_count`, `content_type`, `status`, `is_ranked_comment`, `is_edited` |
| 👤 Author Details | `user_id`, `username`, `full_name`, `profile_pic_url`, `is_private`, `is_verified` |

<br>
<hr>
<hr>
<hr>

### **</>** Raw Responses Examples

<details>
<summary><strong>get_profile_info()</strong></summary>

```py
# ProfileData CLASS
In [1]: client.get_profile_info("leomessi")
Out[1]:
ProfileData(id='<REDACTED_ID>', username='<REDACTED_USERNAME>', full_name='<REDACTED_NAME>', biography='<REDACTED_BIO>', profile_pic_url=HttpUrl('https://instagram.fpoo3-1.fna.fbcdn.net/<REDACTED>'), is_private=False, is_verified=True, is_business_account=True, follower_count=511487329, following_count=356, total_posts=1460, highlight_reel_count=3, mutual_followers=2, category_name='Athlete', external_url=HttpUrl('<REDACTED_URL>'), bio_links=[{'title':'<REDACTED_TITLE>', 'url':'<REDACTED_URL>'}, {'title':'<REDACTED_TITLE>', 'url':'<REDACTED_URL>'}, {'title':'<REDACTED_TITLE>', 'url':'<REDACTED_URL>'}, {'title':'<REDACTED_TITLE>', 'url':'<REDACTED_URL>'}], business_address={'city_name':'<REDACTED_CITY>', 'latitude':25.77481, 'longitude':-80.19773})...
```

```py
# JSON
In [2]: client.get_profile_info("leomessi", return_raw=True)
Out[2]:
{
    "id": "<REDACTED_ID>",
    "username": "<REDACTED_USERNAME>",
    "full_name": "<REDACTED_NAME>",
    "biography": "<REDACTED_BIO>",
    "profile_pic_url": "https://instagram.fpoo3-1.fna.fbcdn.net/<REDACTED>",
    "is_private": False,
    "is_verified": True,
    "is_business_account": True,
    "follower_count": 511487329,
    "following_count": 356,
    "total_posts": 1460,
    "highlight_reel_count": 3,
    "mutual_followers": 2,
    "category_name": "Athlete",
    "external_url": "<REDACTED_URL>",
    "bio_links": [
        {
            "title": "<REDACTED_TITLE>",
            "url": "<REDACTED_URL>"
        }
    ],
    "business_address": {
        "city_name": "<REDACTED_CITY>",
        "latitude": 25.77481,
        "longitude": -80.19773
    }
...
}
```
</details>

<details>
<summary><strong>get_feed()</strong></summary>

```py
# FeedData CLASS
In [1]: client.get_feed("leomessi")
Out[1]:
FeedData(post_id=None, pk=None, shortcode=None, created_at=None, caption=None, media_url=None, media_type=None, like_count=0, comment_count=0, view_count=None, carousel_media_count=0, posts=[FeedData(post_id='<REDACTED_POST_ID>', pk='<REDACTED_PK>', shortcode='<REDACTED_SHORTCODE>', created_at=datetime.datetime(2025, 11, 10, 7, 3, 19), caption='<REDACTED_CAPTION>', media_url=HttpUrl('https://instagram.fpoo3-1.fna.fbcdn.net/<REDACTED>'), media_type=8, like_count=35433328, comment_count=1085526, carousel_media_count=6), FeedData(post_id='<REDACTED_POST_ID>', pk='<REDACTED_PK>', shortcode='<REDACTED_SHORTCODE>', created_at=datetime.datetime(2025, 10, 23, 12, 0, 2), caption='<REDACTED_CAPTION>', media_url=HttpUrl('https://instagram.fpoo3-1.fna.fbcdn.net/<REDACTED>'), media_type=2, like_count=1696841, comment_count=57660), FeedData(post_id='<REDACTED_POST_ID>', pk='<REDACTED_PK>', shortcode='<REDACTED_SHORTCODE>', created_at=datetime.datetime(2026, 2, 13, 17, 50, 37), caption='<REDACTED_CAPTION>', media_url=HttpUrl('https://instagram.fpoo3-1.fna.fbcdn.net/<REDACTED>'), media_type=8, like_count=10418116, comment_count=70107, carousel_media_count=3), FeedData(post_id='<REDACTED_POST_ID>', pk='<REDACTED_PK>', shortcode='<REDACTED_SHORTCODE>', created_at=datetime.datetime(2026, 1, 1, 13, 14, 38), caption='<REDACTED_CAPTION>', media_url=HttpUrl('https://instagram.fpoo3-1.fna.fbcdn.net/<REDACTED>'), media_type=8, like_count=7150174, comment_count=45125, carousel_media_count=2)], next_max_id='<REDACTED_NEXT_MAX_ID>', num_results=12, more_available=True)...
```

```py
# JSON
In [2]: client.get_feed("leomessi", return_raw=True)
Out[2]:
{
    "post_id": None,
    "pk": None,
    "shortcode": None,
    "created_at": None,
    "caption": None,
    "media_url": None,
    "media_type": None,
    "like_count": 0,
    "comment_count": 0,
    "view_count": None,
    "carousel_media_count": 0,
    "posts": [
        {
            "post_id": "<REDACTED_POST_ID>",
            "pk": "<REDACTED_PK>",
            "shortcode": "<REDACTED_SHORTCODE>",
            "created_at": "2025-11-10T07:03:19",
            "caption": "<REDACTED_CAPTION>",
            "media_url": "https://instagram.fpoo3-1.fna.fbcdn.net/<REDACTED>",
            "media_type": 8,
            "like_count": 35433328,
            "comment_count": 1085526,
            "view_count": None,
            "carousel_media_count": 6
        },
        ...
    ],
    "next_max_id": "<REDACTED_NEXT_MAX_ID>",
    "num_results": 12,
    "more_available": True
}
```
</details>

<details>
<summary><strong>get_comments()</strong></summary>


**get_comments()**
```py
# CommentsData CLASS
In [1]: client.get_comments(media_id="3762701545612571046")
Out[1]:
CommentsData(comment_id=None, media_id=None, text=None, created_at=None, like_count=0, content_type=None, status=None, is_ranked_comment=None, is_edited=None, user_id=None, username=None, full_name=None, profile_pic_url=None, is_private=None, is_verified=None, comments=[CommentsData(comment_id='<REDACTED_COMMENT_ID>', media_id='<REDACTED_MEDIA_ID>', text='<REDACTED_TEXT>', created_at=datetime.datetime(2026, 2, 8, 16, 24, 31), like_count=765, content_type='comment', status='Active', is_ranked_comment=True, is_edited=False, user_id='<REDACTED_USER_ID>', username='<REDACTED_USERNAME>', full_name='<REDACTED_NAME>', profile_pic_url=HttpUrl('https://scontent.cdninstagram.com/<REDACTED>'), is_private=False, is_verified=False), CommentsData(comment_id='<REDACTED_COMMENT_ID>', media_id='<REDACTED_MEDIA_ID>', text='<REDACTED_TEXT>', created_at=datetime.datetime(2026, 2, 5, 23, 25, 47), like_count=36, content_type='comment', status='Active', is_ranked_comment=True, is_edited=False, user_id='<REDACTED_USER_ID>', username='<REDACTED_USERNAME>', full_name='<REDACTED_NAME>', profile_pic_url=HttpUrl('https://scontent.cdninstagram.com/<REDACTED>'), is_private=False, is_verified=False), CommentsData(comment_id='<REDACTED_COMMENT_ID>', media_id='<REDACTED_MEDIA_ID>', text='<REDACTED_TEXT>', created_at=datetime.datetime(2026, 2, 14, 21, 42, 56), like_count=1, content_type='comment', status='Active', is_ranked_comment=True, is_edited=False, user_id='<REDACTED_USER_ID>', username='<REDACTED_USERNAME>', full_name='<REDACTED_NAME>', profile_pic_url=HttpUrl('https://scontent.cdninstagram.com/<REDACTED>'), is_private=False, is_verified=False)], next_max_id='<REDACTED_NEXT_MAX_ID>', num_results=15, more_available=False)...
```
```py
# JSON
In [2]: client.get_comments(media_id="3762701545612571046", return_raw=True)
Out[2]:
{
    "comment_id": None,
    "media_id": None,
    "text": None,
    "created_at": None,
    "like_count": 0,
    "content_type": None,
    "status": None,
    "is_ranked_comment": None,
    "is_edited": None,
    "user_id": None,
    "username": None,
    "full_name": None,
    "profile_pic_url": None,
    "is_private": None,
    "is_verified": None,
    "comments": [
        {
            "comment_id": "<REDACTED_COMMENT_ID>",
            "media_id": "<REDACTED_MEDIA_ID>",
            "text": "<REDACTED_TEXT>",
            "created_at": "2026-02-08T16:24:31",
            "like_count": 765,
            "content_type": "comment",
            "status": "Active",
            "is_ranked_comment": True,
            "is_edited": False,
            "user_id": "<REDACTED_USER_ID>",
            "username": "<REDACTED_USERNAME>",
            "full_name": "<REDACTED_NAME>",
            "profile_pic_url": "https://scontent.cdninstagram.com/<REDACTED>",
            "is_private": False,
            "is_verified": False
        },
        ...
    ],
    "next_max_id": "<REDACTED_NEXT_MAX_ID>",
    "num_results": 15,
    "more_available": False
}
```
</details>

<hr>

[⇧ Go to Top](#features--functions)