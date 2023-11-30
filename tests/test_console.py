from datetime import datetime

from nonebot.adapters.console import Bot, Message, MessageEvent
from nonebug import App
from nonechat.info import User


def _fake_message_event(msg: str) -> MessageEvent:
    return MessageEvent(
        time=datetime.now(),
        self_id="test",
        message=Message(msg),
        user=User(id="123456789", avatar="🤗", nickname="MyUser"),
    )


async def test_message_event(app: App):
    from nonebot_plugin_userinfo import UserInfo
    from nonebot_plugin_userinfo.image_source import Emoji

    async with app.test_matcher() as ctx:
        bot = ctx.create_bot(base=Bot)

        user_info = UserInfo(
            user_id="MyUser",
            user_name="MyUser",
            user_displayname=None,
            user_remark=None,
            user_avatar=Emoji(data="🤗"),
            user_gender="unknown",
        )
        event = _fake_message_event("/user_info")
        ctx.receive_event(bot, event)
        ctx.should_call_send(event, "", True, user_info=user_info)

        event = _fake_message_event("/user_info 1234")
        ctx.receive_event(bot, event)
        ctx.should_call_send(event, "", True, user_info=None)

        event = _fake_message_event("/bot_user_info")
        ctx.receive_event(bot, event)
        ctx.should_call_send(event, "", True, user_info=None)
