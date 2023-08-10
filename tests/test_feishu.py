from nonebot.adapters.feishu import (
    Bot,
    EventHeader,
    GroupEventMessage,
    GroupMessageEvent,
    GroupMessageEventDetail,
    PrivateEventMessage,
    PrivateMessageEvent,
    PrivateMessageEventDetail,
    Sender,
    UserId,
)
from nonebot.adapters.feishu.bot import BotInfo
from nonebot.adapters.feishu.config import BotConfig
from nonebug.app import App

BOT_CONFIG = BotConfig(app_id="114", app_secret="514", verification_token="1919810")
BOT_INFO = BotInfo.parse_obj(
    {
        "activate_status": 2,
        "app_name": "bot",
        "avatar_url": "https://s1-imfile.feishucdn.com/test.jpg",
        "ip_white_list": [],
        "open_id": "ou_123456",
    }
)


async def test_private_message_event(app: App):
    from nonebot_plugin_userinfo import ImageUrl, UserInfo
    from tests.plugins.echo import user_info_cmd

    header = EventHeader(
        event_id="114514",
        event_type="im.message.receive_v1",
        create_time="123456",
        token="token",
        app_id="app_id",
        tenant_key="tenant_key",
        resource_id=None,
        user_list=None,
    )
    sender = Sender(
        sender_id=UserId(
            open_id="3344",
            user_id="on_111",
            union_id="on_222",
        ),
        tenant_key="tenant_key",
        sender_type="user",
    )
    event = PrivateMessageEvent(
        schema="2.0",
        header=header,
        event=PrivateMessageEventDetail(
            sender=sender,
            message=PrivateEventMessage(
                chat_type="p2p",
                message_id="om_111",
                root_id="om_222",
                parent_id="om_333",
                create_time="123456",
                chat_id="oc_123",
                message_type="text",
                content='{"text":"/user_info"}',  # type: ignore
                mentions=None,
            ),
        ),
        reply=None,
    )

    user_info = UserInfo(
        user_id="3344",
        user_name="MyUser",
        user_displayname="MyNickName",
        user_remark=None,
        user_avatar=ImageUrl(url="https://s1-imfile.feishucdn.com/xxxx.png"),
        user_gender="male",
    )

    async with app.test_matcher(user_info_cmd) as ctx:
        bot = ctx.create_bot(
            base=Bot, self_id="2233", bot_config=BOT_CONFIG, bot_info=BOT_INFO
        )
        ctx.receive_event(bot, event)
        ctx.should_call_api(
            f"contact/v3/users/3344",
            {"method": "GET", "query": {"user_id_type": "open_id"}},
            {
                "user": {
                    "open_id": "3344",
                    "name": "MyUser",
                    "nickname": "MyNickName",
                    "gender": 1,
                    "avatar": {
                        "avatar_origin": "https://s1-imfile.feishucdn.com/xxxx.png"
                    },
                }
            },
        )
        ctx.should_call_send(event, "", True, user_info=user_info)


async def test_group_message_event(app: App):
    from nonebot_plugin_userinfo import ImageUrl, UserInfo
    from tests.plugins.echo import user_info_cmd

    header = EventHeader(
        event_id="114514",
        event_type="im.message.receive_v1",
        create_time="123456",
        token="token",
        app_id="app_id",
        tenant_key="tenant_key",
        resource_id=None,
        user_list=None,
    )
    sender = Sender(
        sender_id=UserId(
            open_id="3344",
            user_id="on_111",
            union_id="on_222",
        ),
        tenant_key="tenant_key",
        sender_type="user",
    )
    event = GroupMessageEvent(
        schema="2.0",
        header=header,
        event=GroupMessageEventDetail(
            sender=sender,
            message=GroupEventMessage(
                chat_type="group",
                message_id="om_111",
                root_id="om_222",
                parent_id="om_333",
                create_time="123456",
                chat_id="1122",
                message_type="text",
                content='{"text":"/user_info"}',  # type: ignore
                mentions=None,
            ),
        ),
        reply=None,
    )

    user_info = UserInfo(
        user_id="3344",
        user_name="MyUser",
        user_displayname="MyNickName",
        user_remark=None,
        user_avatar=ImageUrl(url="https://s1-imfile.feishucdn.com/xxxx.png"),
        user_gender="male",
    )

    async with app.test_matcher(user_info_cmd) as ctx:
        bot = ctx.create_bot(
            base=Bot, self_id="2233", bot_config=BOT_CONFIG, bot_info=BOT_INFO
        )
        ctx.receive_event(bot, event)
        ctx.should_call_api(
            f"contact/v3/users/3344",
            {"method": "GET", "query": {"user_id_type": "open_id"}},
            {
                "user": {
                    "open_id": "3344",
                    "name": "MyUser",
                    "nickname": "MyNickName",
                    "gender": 1,
                    "avatar": {
                        "avatar_origin": "https://s1-imfile.feishucdn.com/xxxx.png"
                    },
                }
            },
        )
        ctx.should_call_send(event, "", True, user_info=user_info)


async def test_bot_user_info(app: App):
    from nonebot_plugin_userinfo import ImageUrl, UserInfo
    from tests.plugins.echo import bot_user_info_cmd

    header = EventHeader(
        event_id="114514",
        event_type="im.message.receive_v1",
        create_time="123456",
        token="token",
        app_id="app_id",
        tenant_key="tenant_key",
        resource_id=None,
        user_list=None,
    )
    sender = Sender(
        sender_id=UserId(
            open_id="3344",
            user_id="on_111",
            union_id="on_222",
        ),
        tenant_key="tenant_key",
        sender_type="user",
    )
    event = PrivateMessageEvent(
        schema="2.0",
        header=header,
        event=PrivateMessageEventDetail(
            sender=sender,
            message=PrivateEventMessage(
                chat_type="p2p",
                message_id="om_111",
                root_id="om_222",
                parent_id="om_333",
                create_time="123456",
                chat_id="oc_123",
                message_type="text",
                content='{"text":"/bot_user_info"}',  # type: ignore
                mentions=None,
            ),
        ),
        reply=None,
    )

    user_info = UserInfo(
        user_id="2233",
        user_name="bot",
        user_displayname=None,
        user_remark=None,
        user_avatar=ImageUrl(url="https://s1-imfile.feishucdn.com/test.jpg"),
        user_gender="unknown",
    )

    async with app.test_matcher(bot_user_info_cmd) as ctx:
        bot = ctx.create_bot(
            base=Bot, self_id="2233", bot_config=BOT_CONFIG, bot_info=BOT_INFO
        )
        ctx.receive_event(bot, event)
        ctx.should_call_send(event, "", True, user_info=user_info)
