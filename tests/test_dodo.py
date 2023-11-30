from datetime import datetime

from nonebot.adapters.dodo import Bot, ChannelMessageEvent, EventType
from nonebot.adapters.dodo.config import BotConfig
from nonebot.adapters.dodo.models import (
    BotInfo,
    Member,
    MemberInfo,
    MessageType,
    OnlineDevice,
    OnlineStatus,
    Personal,
    Sex,
    TextMessage,
)
from nonebot.exception import ActionFailed
from nonebug.app import App


def _fake_channel_message_event(msg: str) -> ChannelMessageEvent:
    return ChannelMessageEvent(
        event_id="abcdef",
        event_type=EventType.MESSAGE,
        timestamp=datetime.utcfromtimestamp(12345678),
        dodo_source_id="3344",
        channel_id="5566",
        island_source_id="7788",
        message_id="123456",
        message_type=MessageType.TEXT,
        message_body=TextMessage(content=msg),
        personal=Personal(
            nick_name="user",
            avatar_url="https://static.imdodo.com/DoDoAvatar.png",
            sex=Sex.PRIVACY,
        ),
        member=Member(nick_name="user", join_time=datetime.fromtimestamp(11111111)),
    )


async def test_message_event(app: App):
    from nonebot_plugin_userinfo import UserGender, UserInfo
    from nonebot_plugin_userinfo.image_source import ImageUrl

    async with app.test_matcher() as ctx:
        bot = ctx.create_bot(
            base=Bot,
            self_id="2233",
            bot_config=BotConfig(client_id="1234", token="xxxx"),
        )

        user_info = UserInfo(
            user_id="3344",
            user_name="user",
            user_avatar=ImageUrl(url="https://static.imdodo.com/DoDoAvatar.png"),
        )
        event = _fake_channel_message_event("/user_info")
        ctx.receive_event(bot, event)
        ctx.should_call_send(event, "", True, user_info=user_info)

        user_info = UserInfo(
            user_id="2345",
            user_name="member",
            user_avatar=ImageUrl(url="https://static.imdodo.com/DoDoAvatar.png"),
            user_gender=UserGender.male,
        )
        event = _fake_channel_message_event("/user_info 2345")
        ctx.receive_event(bot, event)
        ctx.should_call_api(
            "get_member_info",
            {"island_source_id": "7788", "dodo_source_id": "2345"},
            MemberInfo(
                island_source_id="7788",
                dodo_source_id="2345",
                nick_name="member",
                personal_nick_name="member",
                avatar_url="https://static.imdodo.com/DoDoAvatar.png",
                join_time=datetime.utcfromtimestamp(11111111),
                sex=Sex.MALE,
                level=0,
                is_bot=False,
                online_device=OnlineDevice.PC_ONLINE,
                online_status=OnlineStatus.ONLINE,
            ),
        )
        ctx.should_call_send(event, "", True, user_info=user_info)

        user_info = UserInfo(
            user_id="2233",
            user_name="Bot",
            user_avatar=ImageUrl(url="https://static.imdodo.com/DoDoAvatar.png"),
        )
        event = _fake_channel_message_event("/bot_user_info")
        ctx.receive_event(bot, event)
        ctx.should_call_api(
            "get_member_info",
            {"island_source_id": "7788", "dodo_source_id": "2233"},
            None,
            ActionFailed("test get_member_info failed"),
        )
        ctx.should_call_api(
            "get_bot_info",
            {},
            BotInfo(
                client_id="1234",
                dodo_source_id="2233",
                nick_name="Bot",
                avatar_url="https://static.imdodo.com/DoDoAvatar.png",
            ),
        )
        ctx.should_call_send(event, "", True, user_info=user_info)
