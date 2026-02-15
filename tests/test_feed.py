import pytest
from _vars import *

from igmapper.client import InstaClient


# @pytest.mark.skipif(not IG_SESSIONID, reason="Sem login")
def test_get_feed_real():
    client = InstaClient(IG_CSRFTOKEN, IG_DS_USER_ID, IG_SESSIONID)

    feed = client.get_feed(IG_USERNAME)

    assert feed is not None
    assert len(feed.posts) > 0
    assert feed.num_results > 0

    # Verifica se o primeiro post tem dados consistentes
    post = feed.posts[0]
    assert post.post_id is not None
    assert post.shortcode is not None
    print(f"\nFeed capturado. Último post: {post.shortcode}")


@pytest.mark.skipif(not IG_CSRFTOKEN, reason="Credenciais não configuradas")
def test_get_feed_real_curl():
    # Testa via CURL
    client = InstaClient(IG_CSRFTOKEN, IG_DS_USER_ID, IG_SESSIONID, use_curl=True)

    feed = client.get_feed(IG_USERNAME)

    assert feed is not None
    assert len(feed.posts) > 0
    assert feed.num_results > 0

    # Verifica se o primeiro post tem dados consistentes
    post = feed.posts[0]
    assert post.post_id is not None
    assert post.shortcode is not None
    print(f"\nFeed capturado. Último post: {post.shortcode}")
