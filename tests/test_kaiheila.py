import pytest

pytest.importorskip("nonebot.adapters.kaiheila")

from nonebot.adapters.kaiheila import Bot, Message
from nonebot.adapters.kaiheila.event import (
    ChannelMessageEvent,
    EventMessage,
    Extra,
    PrivateMessageEvent,
    User,
)
from nonebug.app import App


async def test_private_message_event(app: App):
    from nonebot_plugin_userinfo import ImageUrl, UserInfo
    from tests.plugins.echo import user_info_cmd

    event = PrivateMessageEvent(
        post_type="message",
        channel_type="PERSON",
        type=1,
        target_id="6677",
        author_id="3344",
        content="123",
        msg_id="4455",
        msg_timestamp=1234,
        nonce="",
        extra=Extra(
            type=1,
            guild_id=None,
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
        user_id="3344",
        self_id="2233",
        message_type="private",
        sub_type="",
        event=EventMessage(
            type=1,
            guild_id=None,
            channel_name=None,
            content=Message("/user_info"),
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
    )

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

    async with app.test_matcher(user_info_cmd) as ctx:
        bot = ctx.create_bot(base=Bot, self_id="2233", name="Bot", token="")
        ctx.receive_event(bot, event)
        ctx.should_call_api(
            "user_view",
            {"user_id": "3344"},
            {
                "id": "3344",
                "username": "MyUser",
                "avatar": "https://img.kookapp.cn/avatars/2020-02/xxxx.jpg/icon",
                "nickname": "MyNickName",
            },
        )
        ctx.should_call_send(event, "", True, user_info=user_info)


async def test_channel_message_event(app: App):
    from nonebot_plugin_userinfo import ImageUrl, UserInfo
    from tests.plugins.echo import user_info_cmd

    event = ChannelMessageEvent(
        post_type="message",
        channel_type="GROUP",
        type=1,
        target_id="6677",
        author_id="3344",
        content="123",
        msg_id="4455",
        msg_timestamp=1234,
        nonce="",
        extra=Extra(
            type=1,
            guild_id="5566",
            channel_name="test",
            mention=[],
            mention_all=False,
            mention_roles=[],
            mention_here=False,
            author=None,
            body=None,
            attachments=None,
            code=None,
        ),
        user_id="3344",
        self_id="2233",
        group_id="6677",
        message_type="group",
        sub_type="",
        event=EventMessage(
            type=1,
            guild_id="5566",
            channel_name="test",
            content=Message("/user_info"),
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
    )

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

    async with app.test_matcher(user_info_cmd) as ctx:
        bot = ctx.create_bot(base=Bot, self_id="2233", name="Bot", token="")
        ctx.receive_event(bot, event)
        ctx.should_call_api(
            "user_view",
            {"guild_id": "5566", "user_id": "3344"},
            {
                "id": "3344",
                "username": "MyUser",
                "avatar": "https://img.kookapp.cn/avatars/2020-02/xxxx.jpg/icon",
                "nickname": "MyNickName",
            },
        )
        ctx.should_call_send(event, "", True, user_info=user_info)


async def test_bot_user_info(app: App):
    from nonebot_plugin_userinfo import ImageUrl, UserInfo
    from tests.plugins.echo import bot_user_info_cmd

    event = PrivateMessageEvent(
        post_type="message",
        channel_type="PERSON",
        type=1,
        target_id="6677",
        author_id="3344",
        content="123",
        msg_id="4455",
        msg_timestamp=1234,
        nonce="",
        extra=Extra(
            type=1,
            guild_id=None,
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
        user_id="3344",
        self_id="2233",
        message_type="private",
        sub_type="",
        event=EventMessage(
            type=1,
            guild_id=None,
            channel_name=None,
            content=Message("/bot_user_info"),
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
    )

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

    async with app.test_matcher(bot_user_info_cmd) as ctx:
        bot = ctx.create_bot(base=Bot, self_id="2233", name="Bot", token="")
        ctx.receive_event(bot, event)
        ctx.should_call_api(
            "user_view",
            {"user_id": "2233"},
            {
                "id": "2233",
                "username": "Bot",
                "avatar": "https://img.kookapp.cn/avatars/2020-02/xxxx.jpg/icon",
                "nickname": "NickName",
            },
        )
        ctx.should_call_send(event, "", True, user_info=user_info)
