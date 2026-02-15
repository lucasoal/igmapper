import json
from datetime import datetime
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field, HttpUrl


class ProfileData(BaseModel):
    """Modelo estruturado para informações completas do perfil."""

    # Básico
    id: str
    username: str
    full_name: Optional[str]
    biography: Optional[str]
    profile_pic_url: Optional[HttpUrl]

    # Status
    is_private: bool
    is_verified: bool
    is_business_account: bool
    is_professional_account: bool

    # Métricas
    follower_count: int
    following_count: int
    total_posts: int
    highlight_reel_count: int
    mutual_followers: int

    # Categoria
    category_name: Optional[str]
    business_category_name: Optional[str]
    should_show_category: Optional[bool]

    # Conteúdo
    has_clips: Optional[bool]
    has_guides: Optional[bool]
    has_channel: Optional[bool]

    # Links
    external_url: Optional[HttpUrl]
    bio_links: List[Dict[str, Any]] = []

    # Localização (raw dict já parseado)
    business_address: Optional[Dict[str, Any]]

    # Contatos
    should_show_public_contacts: Optional[bool]
    business_email: Optional[str]
    business_phone_number: Optional[str]

    @classmethod
    def parse_instagram_json(cls, data: dict):
        """Helper para limpar o aninhamento profundo do JSON original."""
        user = data.get("data", {}).get("user", {})
        if not user:
            return None

        # Parse do endereço comercial (string JSON → dict)
        business_address_raw = user.get("business_address_json")
        parsed_address = None
        if business_address_raw:
            try:
                parsed_address = json.loads(business_address_raw)
            except Exception:
                parsed_address = None

        return cls(
            # Básico
            id=user.get("id"),
            username=user.get("username"),
            full_name=user.get("full_name"),
            biography=user.get("biography"),
            profile_pic_url=user.get("profile_pic_url_hd"),
            # Status
            is_private=user.get("is_private", False),
            is_verified=user.get("is_verified", False),
            is_business_account=user.get("is_business_account", False),
            is_professional_account=user.get("is_professional_account", False),
            # Métricas
            follower_count=user.get("edge_followed_by", {}).get("count", 0),
            following_count=user.get("edge_follow", {}).get("count", 0),
            total_posts=user.get("edge_owner_to_timeline_media", {}).get("count", 0),
            highlight_reel_count=user.get("highlight_reel_count", 0),
            mutual_followers=user.get("edge_mutual_followed_by", {}).get("count", 0),
            # Categoria
            category_name=user.get("category_name"),
            business_category_name=user.get("business_category_name"),
            should_show_category=user.get("should_show_category"),
            # Conteúdo
            has_clips=user.get("has_clips"),
            has_guides=user.get("has_guides"),
            has_channel=user.get("has_channel"),
            # Links
            external_url=user.get("external_url"),
            bio_links=user.get("bio_links", []),
            # Localização
            business_address=parsed_address,
            # Contatos
            should_show_public_contacts=user.get("should_show_public_contacts"),
            business_email=user.get("business_email"),
            business_phone_number=user.get("business_phone_number"),
        )


class FeedData(BaseModel):
    # Dados do Post
    post_id: Optional[str] = Field(default=None, alias="id")
    pk: Optional[str] = None
    shortcode: Optional[str] = Field(default=None, alias="code")
    created_at: Optional[datetime] = None
    caption: Optional[str] = None
    media_url: Optional[HttpUrl] = None
    media_type: Optional[int] = None
    like_count: Optional[int] = 0
    comment_count: Optional[int] = 0
    view_count: Optional[int] = None
    carousel_media_count: Optional[int] = 0

    # Dados do Feed
    posts: Optional[List["FeedData"]] = None
    next_max_id: Optional[str] = None
    num_results: Optional[int] = None
    more_available: Optional[bool] = None

    @classmethod
    def parse_item(cls, item: dict):
        ts = item.get("taken_at") or (item.get("device_timestamp", 0) / 1_000_000)

        caption_dict = item.get("caption")
        caption_text = caption_dict.get("text") if caption_dict else None

        candidates = item.get("image_versions2", {}).get("candidates", [])
        best_image = candidates[0].get("url") if candidates else None

        return cls(
            id=item.get("id"),
            pk=item.get("pk"),
            code=item.get("code"),
            created_at=datetime.fromtimestamp(ts) if ts else None,
            caption=caption_text,
            media_url=best_image,
            media_type=item.get("media_type"),
            like_count=item.get("like_count", 0),
            comment_count=item.get("comment_count", 0),
            view_count=item.get("view_count"),
            carousel_media_count=item.get("carousel_media_count", 0),
        )


class CommentsData(BaseModel):
    # Dados do Comentário
    comment_id: Optional[str] = Field(default=None, alias="pk")
    media_id: Optional[str] = None
    text: Optional[str] = None
    created_at: Optional[datetime] = None
    like_count: Optional[int] = Field(default=0, alias="comment_like_count")
    content_type: Optional[str] = None
    status: Optional[str] = None
    is_ranked_comment: Optional[bool] = None
    is_edited: Optional[bool] = None

    # Dados do Autor
    user_id: Optional[str] = None
    username: Optional[str] = None
    full_name: Optional[str] = None
    profile_pic_url: Optional[HttpUrl] = None
    is_private: Optional[bool] = None
    is_verified: Optional[bool] = None

    # Dados da Listagem
    comments: Optional[List["CommentsData"]] = None
    next_max_id: Optional[str] = None
    num_results: Optional[int] = None
    more_available: Optional[bool] = None

    @classmethod
    def parse_item(cls, item: dict):
        ts = item.get("created_at")

        user = item.get("user", {})

        return cls(
            pk=item.get("pk"),
            media_id=item.get("media_id"),
            text=item.get("text"),
            created_at=datetime.fromtimestamp(ts) if ts else None,
            comment_like_count=item.get("comment_like_count", 0),
            content_type=item.get("content_type"),
            status=item.get("status"),
            is_ranked_comment=item.get("is_ranked_comment"),
            is_edited=item.get("is_edited"),
            user_id=user.get("id"),
            username=user.get("username"),
            full_name=user.get("full_name"),
            profile_pic_url=user.get("profile_pic_url"),
            is_private=user.get("is_private"),
            is_verified=user.get("is_verified"),
        )

    @classmethod
    def parse_response(cls, data: dict):
        comments_data = data.get("comments", [])

        return cls(
            comments=[cls.parse_item(item) for item in comments_data],
            next_max_id=data.get("next_max_id"),
            num_results=data.get("num_results"),
            more_available=data.get("more_available"),
        )
