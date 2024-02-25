from nonebot.adapters.kaiheila import Bot
from nonebot.adapters.kaiheila.event import (
    ChannelMessageEvent,
    EventMessage,
    Extra,
    PrivateMessageEvent,
    User,
)
from nonebug.app import App


def _fake_private_message_event(msg: str) -> PrivateMessageEvent:
    return PrivateMessageEvent(
        channel_type="PERSON",
        type=9,
        target_id="6677",
        content=msg,
        msg_id="4455",
        msg_timestamp=1234,
        nonce="",
        extra=Extra(type=9),  # type: ignore
        user_id="3344",
        sub_type="",
        event=EventMessage(
            type=9,
            author=User(id="3344"),
            content=msg,  # type: ignore
            mention=[],
            mention_roles=[],
            mention_all=False,
            mention_here=False,
            kmarkdown={
                "raw_content": msg,
                "mention_part": [],
                "mention_role_part": [],
            },  # type: ignore
        ),
        message_type="private",
    )


def _fake_channel_message_event(msg: str) -> ChannelMessageEvent:
    return ChannelMessageEvent(
        channel_type="GROUP",
        type=9,
        target_id="6677",
        content=msg,
        msg_id="4455",
        msg_timestamp=1234,
        nonce="",
        extra=Extra(type=9, guild_id="5566"),  # type: ignore
        user_id="3344",
        sub_type="",
        event=EventMessage(
            type=9,
            guild_id="5566",
            author=User(id="3344"),
            content=msg,  # type: ignore
            mention=[],
            mention_roles=[],
            mention_all=False,
            mention_here=False,
            kmarkdown={
                "raw_content": msg,
                "mention_part": [],
                "mention_role_part": [],
            },  # type: ignore
        ),
        message_type="group",
        group_id="6677",
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
