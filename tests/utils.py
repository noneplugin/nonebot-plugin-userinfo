from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from nonebot_plugin_userinfo import ImageData, UserInfo


def assert_user_info(
    user_info: "UserInfo",
    *,
    user_id: str,
    user_name: str,
    user_displayname: Optional[str] = None,
    user_remark: Optional[str] = None,
    user_avatar: Optional[ImageData] = None,
    user_gender: str = "unknown"
):
    assert user_info.user_id == user_id
    assert user_info.user_name == user_name
    assert user_info.user_displayname == user_displayname
    assert user_info.user_remark == user_remark
    assert user_info.user_avatar == user_avatar
    assert user_info.user_gender == user_gender
