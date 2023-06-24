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


async def test_private_message_event(app: App):
    from nonebot_plugin_userinfo import QQAvatar, UserInfo
    from tests.plugins.echo import user_info_cmd

    event = PrivateMessageEvent(
        id="1122",
        time=datetime.now(),
        type="message",
        detail_type="private",
        sub_type="",
        message_id="4455",
        self=BotSelf(platform="qq", user_id="2233"),
        message=Message("/user_info"),
        original_message=Message("/user_info"),
        alt_message="/user_info",
        user_id="3344",
    )

    user_info = UserInfo(
        user_id="3344",
        user_name="MyUser",
        user_displayname="",
        user_remark="MyRemark",
        user_avatar=QQAvatar(qq=3344),
        user_gender="unknown",
    )

    async with app.test_matcher(user_info_cmd) as ctx:
        bot = ctx.create_bot(base=Bot, self_id="2233", impl="walle-q", platform="qq")
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


async def test_group_message_event(app: App):
    from nonebot_plugin_userinfo import QQAvatar, UserInfo
    from tests.plugins.echo import user_info_cmd

    event = GroupMessageEvent(
        id="1122",
        time=datetime.now(),
        type="message",
        detail_type="group",
        sub_type="",
        message_id="4455",
        self=BotSelf(platform="qq", user_id="2233"),
        message=Message("/user_info"),
        original_message=Message("/user_info"),
        alt_message="/user_info",
        user_id="3344",
        group_id="1122",
    )

    user_info = UserInfo(
        user_id="3344",
        user_name="MyUser",
        user_displayname="MyDisplayName",
        user_remark=None,
        user_avatar=QQAvatar(qq=3344),
        user_gender="unknown",
    )

    async with app.test_matcher(user_info_cmd) as ctx:
        bot = ctx.create_bot(base=Bot, self_id="2233", impl="walle-q", platform="qq")
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


async def test_channel_message_event(app: App):
    from nonebot_plugin_userinfo import QQAvatar, UserInfo
    from tests.plugins.echo import user_info_cmd

    event = ChannelMessageEvent(
        id="1122",
        time=datetime.now(),
        type="message",
        detail_type="channel",
        sub_type="",
        message_id="4455",
        self=BotSelf(platform="qqguild", user_id="2233"),
        message=Message("/user_info"),
        original_message=Message("/user_info"),
        alt_message="/user_info",
        user_id="3344",
        guild_id="5566",
        channel_id="6677",
    )

    user_info = UserInfo(
        user_id="3344",
        user_name="MyUser",
        user_displayname="MyDisplayName",
        user_remark=None,
        user_avatar=QQAvatar(qq=3344),
        user_gender="unknown",
    )

    # TODO: qqguild all4one 相关测试
    # async with app.test_matcher(user_info_cmd) as ctx:
    #     bot = ctx.create_bot(
    #         base=Bot, self_id="2233", impl="nonebot-plugin-all4one", platform="qqguild"
    #     )
    #     ctx.receive_event(bot, event)
    #     ctx.should_call_api(
    #         "get_channel_member_info",
    #         {"guild_id": "5566", "channel_id": "6677", "user_id": "3344"},
    #         {
    #             "user_id": "3344",
    #             "user_name": "MyUser",
    #             "user_displayname": "MyDisplayName",
    #         },
    #     )
    #     ctx.should_call_send(event, "", True, user_info=user_info)


async def test_bot_user_info(app: App):
    from nonebot_plugin_userinfo import QQAvatar, UserInfo
    from tests.plugins.echo import bot_user_info_cmd

    event = PrivateMessageEvent(
        id="1122",
        time=datetime.now(),
        type="message",
        detail_type="private",
        sub_type="",
        message_id="4455",
        self=BotSelf(platform="qq", user_id="2233"),
        message=Message("/bot_user_info"),
        original_message=Message("/bot_user_info"),
        alt_message="/bot_user_info",
        user_id="3344",
    )

    user_info = UserInfo(
        user_id="2233",
        user_name="Bot",
        user_displayname="",
        user_remark="Remark",
        user_avatar=QQAvatar(qq=2233),
        user_gender="unknown",
    )

    async with app.test_matcher(bot_user_info_cmd) as ctx:
        bot = ctx.create_bot(base=Bot, self_id="2233", impl="walle-q", platform="qq")
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
