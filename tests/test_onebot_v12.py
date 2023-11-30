from datetime import datetime

from nonebot.adapters.onebot.v12 import (
    Bot,
    ChannelMessageEvent,
    GroupMessageEvent,
    Message,
    PrivateMessageEvent,
)
from nonebot.adapters.onebot.v12.event import BotSelf
from nonebug import App


def _fake_private_message_event(msg: str) -> PrivateMessageEvent:
    return PrivateMessageEvent(
        id="1122",
        time=datetime.now(),
        type="message",
        detail_type="private",
        sub_type="",
        message_id="4455",
        self=BotSelf(platform="qq", user_id="2233"),
        message=Message(msg),
        original_message=Message(msg),
        alt_message=msg,
        user_id="3344",
    )


def _fake_group_message_event(msg: str) -> GroupMessageEvent:
    return GroupMessageEvent(
        id="1122",
        time=datetime.now(),
        type="message",
        detail_type="group",
        sub_type="",
        message_id="4455",
        self=BotSelf(platform="qq", user_id="2233"),
        message=Message(msg),
        original_message=Message(msg),
        alt_message=msg,
        user_id="3344",
        group_id="1122",
    )


def _fake_channel_message_event(
    msg: str, platform: str = "kook"
) -> ChannelMessageEvent:
    return ChannelMessageEvent(
        id="1122",
        time=datetime.now(),
        type="message",
        detail_type="channel",
        sub_type="",
        message_id="4455",
        self=BotSelf(platform=platform, user_id="2233"),
        message=Message(msg),
        original_message=Message(msg),
        alt_message=msg,
        user_id="3344",
        guild_id="5566",
        channel_id="6677",
    )


async def test_message_event(app: App):
    from nonebot_plugin_userinfo import UserInfo
    from nonebot_plugin_userinfo.image_source import QQAvatar

    async with app.test_matcher() as ctx:
        bot = ctx.create_bot(base=Bot, self_id="2233", impl="walle-q", platform="qq")

        user_info = UserInfo(
            user_id="3344",
            user_name="MyUser",
            user_displayname="",
            user_remark="MyRemark",
            user_avatar=QQAvatar(qq=3344),
            user_gender="unknown",
        )
        event = _fake_private_message_event("/user_info")
        ctx.receive_event(bot, event)
        ctx.should_call_api(
            "get_user_info",
            {"user_id": "3344"},
            {
                "user_id": "3344",
                "user_name": "MyUser",
                "user_displayname": "",
                "user_remark": "MyRemark",
            },
        )
        ctx.should_call_send(event, "", True, user_info=user_info)

        user_info = UserInfo(
            user_id="3344",
            user_name="MyUser",
            user_displayname="MyDisplayName",
            user_remark=None,
            user_avatar=QQAvatar(qq=3344),
            user_gender="unknown",
        )
        event = _fake_group_message_event("/user_info")
        ctx.receive_event(bot, event)
        ctx.should_call_api(
            "get_group_member_info",
            {"group_id": "1122", "user_id": "3344"},
            {
                "user_id": "3344",
                "user_name": "MyUser",
                "user_displayname": "MyDisplayName",
            },
        )
        ctx.should_call_send(event, "", True, user_info=user_info)

        user_info = UserInfo(
            user_id="1234",
            user_name="user",
            user_displayname="displayname",
            user_remark=None,
            user_avatar=QQAvatar(qq=1234),
            user_gender="unknown",
        )
        event = _fake_group_message_event("/user_info 1234")
        ctx.receive_event(bot, event)
        ctx.should_call_api(
            "get_group_member_info",
            {"group_id": "1122", "user_id": "1234"},
            {
                "user_id": "1234",
                "user_name": "user",
                "user_displayname": "displayname",
            },
        )
        ctx.should_call_send(event, "", True, user_info=user_info)

        user_info = UserInfo(
            user_id="2233",
            user_name="Bot",
            user_displayname="",
            user_remark="Remark",
            user_avatar=QQAvatar(qq=2233),
            user_gender="unknown",
        )
        event = _fake_private_message_event("/bot_user_info")
        ctx.receive_event(bot, event)
        ctx.should_call_api(
            "get_self_info",
            {},
            {
                "user_id": "2233",
                "user_name": "Bot",
                "user_displayname": "",
                "user_remark": "Remark",
            },
        )
        ctx.should_call_send(event, "", True, user_info=user_info)


async def test_channel_message_event(app: App):
    from nonebot_plugin_userinfo import UserInfo

    async with app.test_matcher() as ctx:
        bot = ctx.create_bot(base=Bot, self_id="2233", impl="walle-k", platform="kook")

        user_info = UserInfo(
            user_id="3344",
            user_name="MyUser",
            user_displayname="MyDisplayName",
            user_remark=None,
            user_avatar=None,
            user_gender="unknown",
        )
        event = _fake_channel_message_event("/user_info")
        ctx.receive_event(bot, event)
        ctx.should_call_api(
            "get_channel_member_info",
            {"guild_id": "5566", "channel_id": "6677", "user_id": "3344"},
            {
                "user_id": "3344",
                "user_name": "MyUser",
                "user_displayname": "MyDisplayName",
            },
        )
        ctx.should_call_send(event, "", True, user_info=user_info)


async def test_all4one_qqguild(app: App):
    from nonebot_plugin_userinfo import UserInfo
    from nonebot_plugin_userinfo.image_source import ImageUrl

    async with app.test_matcher() as ctx:
        bot = ctx.create_bot(
            base=Bot, self_id="2233", impl="nonebot-plugin-all4one", platform="qqguild"
        )
        user_info = UserInfo(
            user_id="3344",
            user_name="MyUser",
            user_displayname="MyDisplayName",
            user_remark=None,
            user_avatar=ImageUrl(url="http://xxx.jpg"),
            user_gender="unknown",
        )
        event = _fake_channel_message_event("/user_info", platform="qqguild")
        ctx.receive_event(bot, event)
        ctx.should_call_api(
            "get_channel_member_info",
            {"guild_id": "5566", "channel_id": "6677", "user_id": "3344"},
            {
                "user_id": "3344",
                "user_name": "MyUser",
                "user_displayname": "MyDisplayName",
                "qqguild": {
                    "user": {
                        "id": "3344",
                        "username": "MyUser",
                        "avatar": "http://xxx.jpg",
                    }
                },
                "qqguild.roles": [],
                "qqguild.joined_at": None,
            },
        )
        ctx.should_call_send(event, "", True, user_info=user_info)
