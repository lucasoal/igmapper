# Features & Functions

<h3>Table of Contents</h3>

- [`InstaClient`](#instaclient): Initializes the session and handles transport selection (Requests or CURL)
  - [`get_profile_info()`](#get_profile_info): Scrapes profile metadata and returns a structured ProfileData object.
  - [`get_feed()`](#get_feed): Retrieves user timeline posts with built-in pagination support.
  - [`get_comments()`](#get_comments): Fetches media comments and automates cursor-based pagination.
- [Raw Responses Examples](#raw-responses-examples)

> [!NOTE]
> You will need to fill in the parameters for the request. See here how to get them
> - [**How to obtain the parameters to make the request**](HOT_TO.md)

<hr>

### *InstaClient*
This **class** provides the core engine for authentication and request transport.

```py
from igmapper import InstaClient

client = InstaClient(
    csrftoken="ks8anda6s",
    ds_user_id="89231892",
    sessionid="89231892:11:31271892iher12has98",
    proxy=None,
    use_curl=True,
)
```

<hr>

### *get_profile_info()*
This **method** scrapes profile metadata and returns a structured ProfileData object.

```py
profile = client.get_profile_info("leomessi")

print(profile.username)
print(profile.follower_count)
print(profile.business_email)
```

- **🔎 Basic Infos**
  - `id`
  - `username`
  - `full_name`
  - `biography`
  - `profile_pic_url`
- **🔐 Account Status**
  - `is_private`
  - `is_verified`
  - `is_business_account`
  - `is_professional_account`
- **📊 Metrics**
  - `follower_count`
  - `following_count`
  - `total_posts`
  - `highlight_reel_count`
  - `mutual_followers`
- **🏷 Category** 
  - `category_name` 
  - `business_category_name` 
  - `should_show_category`
- **🎬 Features** 
  - `has_clips` 
  - `has_guides` 
  - `has_channel`
- **🔗 Links** 
  - `external_url` 
  - `bio_links`
- **📍 Business Address** 
  - `business_address` (JSON string → dict)
- **📞 Public Contacts** 
  - `should_show_public_contacts` 
  - `business_email` 
  - `business_phone_number`

<hr>

### *get_feed()*
This **method** retrieves user timeline posts with built-in pagination support.

```py
feed = client.get_feed("leomessi")

for i in feed.posts:
    print(i.post_id)
    print(i.caption)
    print(i.media_url)
```

- **📌 Identification** 
  - `post_id` 
  - `pk` 
  - `shortcode`
- **🕒 Date** 
  - `created_at` (datetime)
- **📝 Content** 
  - `caption` 
  - `media_url` 
  - `media_type` 
  - `carousel_media_count`
- **📊 Engagement** 
  - `like_count` 
  - `comment_count` 
  - `view_count`
- **📦 Complete Feed Structure** 
  - `posts` (list of FeedData) 
  - `next_max_id` 
  - `num_results` 
  - `more_available`

<hr>

### *get_comments()*
This **method** fetches media comments and automates cursor-based pagination.

```py
comms = client.get_comments(media_id="3762701545612571046")

for i in comms.comments:
    print(i.username)
    print(i.comment_id)
    print(i.text)
```
- **📝 Comment Details**
  - `comment_id`
  - `media_id`
  - `text`
  - `created_at`
  - `like_count`
  - `content_type`
  - `status`
  - `is_ranked_comment`
  - `is_edited`
- **👤 Author Details**
  - `user_id`
  - `username`
  - `full_name`
  - `profile_pic_url`
  - `is_private`
  - `is_verified`

<hr>

### Raw Responses Examples

**get_profile_info()**
```py
ProfileData(id='427553890',username='leomessi',full_name='LeoMessi',biography='Bienvenidosalacuentaoficial...',profile_pic_url=HttpUrl('https://instagram.fpoo3-1.fna.fbcdn.net/...'),is_private=False,is_verified=True,is_business_account=True,follower_count=511487329,following_count=356,total_posts=1460,highlight_reel_count=3,mutual_followers=2,category_name='Athlete',external_url=HttpUrl('http://messicup.com/'),bio_links=[{'title':'MESSICUP⚽️','url':'http://messicup.com',...},{'title':'Más+byMessi','url':'https://www.masbymessi.com/',...},{'title':'TheMessiExperience🔥⚽️🔟','url':'http://themessiexperience.com',...},{'title':'Lionelcollection🍷','url':'http://www.lionelofficialwines.com/...',...}],business_address={'city_name':'Miami,Florida','latitude':25.77481,'longitude':-80.19773,...},...)
```

**get_feed()**
```py
FeedData(post_id=None, pk=None, shortcode=None, created_at=None, caption=None, media_url=None, media_type=None, like_count=0, comment_count=0, view_count=None, carousel_media_count=0, posts=[FeedData(post_id='3762701545612571046_427553890', pk='3762701545612571046', shortcode='DQ3zR6-DPGm', created_at=datetime.datetime(2025, 11, 10, 7, 3, 19), caption='Anoche volví a un lugar que extraño...', media_url=HttpUrl('https://instagram.fpoo3-1.fna.fbcdn.net/...'), media_type=8, like_count=35433328, comment_count=1085526, carousel_media_count=6, ...), FeedData(post_id='3749804102613318615_6937659083', pk='3749804102613318615', shortcode='DQJ-vbJkbvX', created_at=datetime.datetime(2025, 10, 23, 12, 0, 2), caption='HE’S HOME.', media_url=HttpUrl('https://instagram.fpoo3-1.fna.fbcdn.net/...'), media_type=2, like_count=1696841, comment_count=57660, ...), FeedData(post_id='3831881032111449280_427553890', pk='3831881032111449280', shortcode='DUtk38cj2TA', created_at=datetime.datetime(2026, 2, 13, 17, 50, 37), caption='La terminamos @lego', media_url=HttpUrl('https://instagram.fpoo3-1.fna.fbcdn.net/...'), media_type=8, like_count=10418116, comment_count=70107, carousel_media_count=3, ...), FeedData(post_id='3800576769431202523_427553890', pk='3800576769431202523', shortcode='DS-XG97jGrb', created_at=datetime.datetime(2026, 1, 1, 13, 14, 38), caption='¡¡FELIZ 2026!! Ojalá sea un año lleno...', media_url=HttpUrl('https://instagram.fpoo3-1.fna.fbcdn.net/...'), media_type=8, like_count=7150174, comment_count=45125, carousel_media_count=2, ...), ...], next_max_id='3790454236694495572_427553890', num_results=12, more_available=True)
```

**get_comments()**
```py
CommentsData(comment_id=None, media_id=None, text=None, created_at=None, like_count=0, content_type=None, status=None, is_ranked_comment=None, is_edited=None, user_id=None, username=None, full_name=None, profile_pic_url=None, is_private=None, is_verified=None, comments=[CommentsData(comment_id='17976848045976769', media_id='3762701545612571046', text='', created_at=datetime.datetime(2026, 2, 8, 16, 24, 31), like_count=765, content_type='comment', status='Active', is_ranked_comment=True, is_edited=False, user_id='72357472949', username='th_surfista02', full_name='surf 🏄', profile_pic_url=HttpUrl('https://scontent.cdninstagram.com/...'), is_private=False, is_verified=False, ...), CommentsData(comment_id='17883716868444039', media_id='3762701545612571046', text='BUENAS NOCHES, SOY DIEGO...', created_at=datetime.datetime(2026, 2, 5, 23, 25, 47), like_count=36, content_type='comment', status='Active', is_ranked_comment=True, is_edited=False, user_id='54662821625', username='diegoeduardoquina', full_name='Diego Quiña', profile_pic_url=HttpUrl('https://scontent.cdninstagram.com/...'), is_private=False, is_verified=False, ...), CommentsData(comment_id='18072506210535862', media_id='3762701545612571046', text='', created_at=datetime.datetime(2026, 2, 14, 21, 42, 56), like_count=1, content_type='comment', status='Active', is_ranked_comment=True, is_edited=False, user_id='62142801817', username='qurbonali20111', full_name='Qurbonali', profile_pic_url=HttpUrl('https://scontent.cdninstagram.com/...'), is_private=False, is_verified=False, ...), ...], next_max_id='{"cached_comments_cursor":"18095464633959445",...}', num_results=15, more_available=False)
```

<hr>

[⇧ Go to Top](#features--functions)