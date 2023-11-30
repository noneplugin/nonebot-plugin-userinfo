from typing import Any, Dict, Optional

from nonebot.adapters.kaiheila import Bot, Message
from nonebot.adapters.kaiheila.event import (
    ChannelMessageEvent,
    EventMessage,
    Extra,
    PrivateMessageEvent,
    User,
)
from nonebug.app import App


def _fake_message_event_args(
    msg: str, guild_id: Optional[str] = None
) -> Dict[str, Any]:
    return {
        "post_type": "message",
        "type": 1,
        "target_id": "6677",
        "author_id": "3344",
        "content": "123",
        "msg_id": "4455",
        "msg_timestamp": 1234,
        "nonce": "",
        "extra": Extra(
            type=1,
            guild_id=guild_id,
            channel_name=None,
            mention=[],
            mention_all=False,
            mention_roles=[],
            mention_here=False,
            author=None,
            body=None,
            attachments=None,
            code=None,
        ),
        "user_id": "3344",
        "self_id": "2233",
        "sub_type": "",
        "event": EventMessage(
            type=1,
            guild_id=guild_id,
            channel_name=None,
            content=Message(msg),
            mention=[],
            mention_all=False,
            mention_roles=[],
            mention_here=False,
            nav_channels=[],
            author=User(id="3344"),
            kmarkdown=None,
            attachments=None,
            code=None,
        ),
    }


def _fake_private_message_event(msg: str) -> PrivateMessageEvent:
    return PrivateMessageEvent(
        channel_type="PERSON",
        message_type="private",
        **_fake_message_event_args(msg),
    )


def _fake_channel_message_event(msg: str) -> ChannelMessageEvent:
    return ChannelMessageEvent(
        channel_type="GROUP",
        message_type="group",
        group_id="6677",
        **_fake_message_event_args(msg, guild_id="5566"),
    )


async def test_message_event(app: App):
    from nonebot_plugin_userinfo import UserInfo
    from nonebot_plugin_userinfo.image_source import ImageUrl

    async with app.test_matcher() as ctx:
        bot = ctx.create_bot(base=Bot, self_id="2233", name="Bot", token="")

        user_info = UserInfo(
            user_id="3344",
            user_name="MyUser",
            user_displayname="MyNickName",
            user_remark=None,
            user_avatar=ImageUrl(
                url="https://img.kookapp.cn/avatars/2020-02/xxxx.jpg/icon"
            ),
            user_gender="unknown",
        )
        event = _fake_private_message_event("/user_info")
        ctx.receive_event(bot, event)
        ctx.should_call_api(
            "user_view",
            {"user_id": "3344"},
            User(
                id="3344",
                username="MyUser",
                avatar="https://img.kookapp.cn/avatars/2020-02/xxxx.jpg/icon",
                nickname="MyNickName",
            ),
        )
        ctx.should_call_send(event, "", True, user_info=user_info)

        event = _fake_channel_message_event("/user_info")
        ctx.receive_event(bot, event)
        ctx.should_call_api(
            "user_view",
            {"guild_id": "5566", "user_id": "3344"},
            User(
                id="3344",
                username="MyUser",
                avatar="https://img.kookapp.cn/avatars/2020-02/xxxx.jpg/icon",
                nickname="MyNickName",
            ),
        )
        ctx.should_call_send(event, "", True, user_info=user_info)

        user_info = UserInfo(
            user_id="1234",
            user_name="user",
            user_displayname="nickname",
            user_remark=None,
            user_avatar=ImageUrl(
                url="https://img.kookapp.cn/avatars/2020-02/xxxx.jpg/icon"
            ),
            user_gender="unknown",
        )
        event = _fake_channel_message_event("/user_info 1234")
        ctx.receive_event(bot, event)
        ctx.should_call_api(
            "user_view",
            {"guild_id": "5566", "user_id": "1234"},
            User(
                id="1234",
                username="user",
                avatar="https://img.kookapp.cn/avatars/2020-02/xxxx.jpg/icon",
                nickname="nickname",
            ),
        )
        ctx.should_call_send(event, "", True, user_info=user_info)

        user_info = UserInfo(
            user_id="2233",
            user_name="Bot",
            user_displayname="NickName",
            user_remark=None,
            user_avatar=ImageUrl(
                url="https://img.kookapp.cn/avatars/2020-02/xxxx.jpg/icon"
            ),
            user_gender="unknown",
        )
        event = _fake_private_message_event("/bot_user_info")
        ctx.receive_event(bot, event)
        ctx.should_call_api(
            "user_me",
            {},
            User(
                id="2233",
                username="Bot",
                avatar="https://img.kookapp.cn/avatars/2020-02/xxxx.jpg/icon",
                nickname="NickName",
            ),
        )
        ctx.should_call_send(event, "", True, user_info=user_info)
