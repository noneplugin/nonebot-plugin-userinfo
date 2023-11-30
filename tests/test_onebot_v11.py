from nonebot.adapters.onebot.v11 import (
    Bot,
    GroupMessageEvent,
    Message,
    PrivateMessageEvent,
)
from nonebot.adapters.onebot.v11.event import Sender
from nonebug import App


def _fake_private_message_event(msg: str) -> PrivateMessageEvent:
    return PrivateMessageEvent(
        time=1122,
        self_id=2233,
        post_type="message",
        sub_type="",
        user_id=3344,
        message_id=4455,
        message=Message(msg),
        original_message=Message(msg),
        message_type="private",
        raw_message=msg,
        font=1,
        sender=Sender(user_id=3344),
    )


def _fake_group_message_event(msg: str) -> GroupMessageEvent:
    return GroupMessageEvent(
        group_id=1122,
        time=1122,
        self_id=2233,
        post_type="message",
        sub_type="",
        user_id=3344,
        message_id=4455,
        message=Message(msg),
        original_message=Message(msg),
        message_type="group",
        raw_message=msg,
        font=1,
        sender=Sender(user_id=3344),
    )


async def test_message_event(app: App):
    from nonebot_plugin_userinfo import UserInfo
    from nonebot_plugin_userinfo.image_source import QQAvatar

    async with app.test_matcher() as ctx:
        bot = ctx.create_bot(base=Bot, self_id="2233")

        user_info = UserInfo(
            user_id="3344",
            user_name="MyUser",
            user_displayname=None,
            user_remark=None,
            user_avatar=QQAvatar(qq=3344),
            user_gender="male",
        )
        event = _fake_private_message_event("/user_info")
        ctx.receive_event(bot, event)
        ctx.should_call_api(
            "get_stranger_info",
            {"user_id": 3344},
            {"user_id": 3344, "nickname": "MyUser", "sex": "male", "age": 3},
        )
        ctx.should_call_send(event, "", True, user_info=user_info)

        user_info = UserInfo(
            user_id="3344",
            user_name="MyUser",
            user_displayname="MyCard",
            user_remark=None,
            user_avatar=QQAvatar(qq=3344),
            user_gender="male",
        )
        event = _fake_group_message_event("/user_info")
        ctx.receive_event(bot, event)
        ctx.should_call_api(
            "get_group_member_info",
            {"group_id": 1122, "user_id": 3344},
            {
                "group_id": 1122,
                "user_id": 3344,
                "nickname": "MyUser",
                "card": "MyCard",
                "sex": "male",
                "age": 3,
            },
        )
        ctx.should_call_send(event, "", True, user_info=user_info)

        user_info = UserInfo(
            user_id="1234",
            user_name="user",
            user_displayname="card",
            user_remark=None,
            user_avatar=QQAvatar(qq=1234),
            user_gender="female",
        )
        event = _fake_group_message_event("/user_info 1234")
        ctx.receive_event(bot, event)
        ctx.should_call_api(
            "get_group_member_info",
            {"group_id": 1122, "user_id": 1234},
            {
                "group_id": 1122,
                "user_id": 1234,
                "nickname": "user",
                "card": "card",
                "sex": "female",
                "age": 3,
            },
        )
        ctx.should_call_send(event, "", True, user_info=user_info)

        user_info = UserInfo(
            user_id="2233",
            user_name="Bot",
            user_displayname=None,
            user_remark=None,
            user_avatar=QQAvatar(qq=2233),
            user_gender="female",
        )
        event = _fake_private_message_event("/bot_user_info")
        ctx.receive_event(bot, event)
        ctx.should_call_api(
            "get_stranger_info",
            {"user_id": 2233},
            {"user_id": 2233, "nickname": "Bot", "sex": "female", "age": 3},
        )
        ctx.should_call_send(event, "", True, user_info=user_info)
