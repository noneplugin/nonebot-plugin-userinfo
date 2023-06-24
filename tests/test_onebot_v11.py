from nonebot.adapters.onebot.v11 import Bot, Message, PrivateMessageEvent
from nonebot.adapters.onebot.v11.event import Sender
from nonebug import App


async def test_private_message_event(app: App):
    from nonebot_plugin_userinfo import QQAvatar, UserInfo
    from tests.plugins.echo import user_info_cmd

    event = PrivateMessageEvent(
        time=1122,
        self_id=2233,
        post_type="message",
        sub_type="",
        user_id=3344,
        message_id=4455,
        message=Message("/user_info"),
        original_message=Message("/user_info"),
        message_type="private",
        raw_message="/user_info",
        font=1,
        sender=Sender(user_id=3344),
    )

    user_info = UserInfo(
        user_id="3344",
        user_name="MyUser",
        user_displayname=None,
        user_remark=None,
        user_avatar=QQAvatar(qq=3344),
        user_gender="male",
    )

    async with app.test_matcher(user_info_cmd) as ctx:
        bot = ctx.create_bot(base=Bot, self_id="2233")
        ctx.receive_event(bot, event)
        ctx.should_call_api(
            "get_stranger_info",
            {"user_id": 3344, "no_cache": "false"},
            {"user_id": 3344, "nickname": "MyUser", "sex": "male", "age": 3},
        )
        ctx.should_call_send(event, "", True, user_info=user_info)
