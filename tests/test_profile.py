import os

import pytest
from _vars import *

from igmapper.client import InstaClient


@pytest.mark.skipif(not IG_SESSIONID, reason="Credenciais não configuradas")
def test_get_profile_info_real():
    # Testa via REQUESTS
    client = InstaClient(IG_CSRFTOKEN, IG_DS_USER_ID, IG_SESSIONID, use_curl=False)
    profile = client.get_profile_info(IG_USERNAME)

    assert profile is not None
    assert profile.username == IG_USERNAME
    assert profile.follower_count > 0
    print(f"\n[Requests] Sucesso: {profile.full_name} tem {profile.follower_count} seguidores.")


@pytest.mark.skipif(not IG_CSRFTOKEN, reason="Credenciais não configuradas")
def test_get_profile_info_real_curl():
    # Testa via CURL
    client = InstaClient(IG_CSRFTOKEN, IG_DS_USER_ID, IG_SESSIONID, use_curl=True)
    profile = client.get_profile_info(IG_USERNAME)

    assert profile is not None
    assert profile.username == IG_USERNAME
    print(f"\n[CURL] Sucesso: {profile.full_name} capturado via binário do sistema.")
