from nonebot.adapters.qqguild import Bot
from nonebot.adapters.qqguild.api import Member, User
from nonebot.adapters.qqguild.config import BotInfo
from nonebot.adapters.qqguild.event import (
    DirectMessageCreateEvent,
    EventType,
    MessageCreateEvent,
)
from nonebug import App


def _fake_message_create_event(msg: str) -> MessageCreateEvent:
    return MessageCreateEvent(
        __type__=EventType.CHANNEL_CREATE,
        channel_id=6677,
        guild_id=5566,
        author=User(id=3344, username="MyUser", avatar="http://xxx.jpg"),
        content=msg,
    )


def _fake_direct_message_create_event(msg: str) -> DirectMessageCreateEvent:
    return DirectMessageCreateEvent(
        __type__=EventType.DIRECT_MESSAGE_CREATE,
        guild_id=5566,
        author=User(id=3344, username="MyUser", avatar="http://xxx.jpg"),
        content=msg,
    )


async def test_message_event(app: App):
    from nonebot_plugin_userinfo import UserInfo
    from nonebot_plugin_userinfo.image_source import ImageUrl

    async with app.test_matcher() as ctx:
        bot = ctx.create_bot(
            base=Bot, self_id="2233", bot_info=BotInfo(id="2233", token="", secret="")
        )

        user_info = UserInfo(
            user_id="3344",
            user_name="MyUser",
            user_displayname="MyNick",
            user_remark=None,
            user_avatar=ImageUrl(url="http://xxx.jpg"),
            user_gender="unknown",
        )
        event = _fake_message_create_event("/user_info")
        ctx.receive_event(bot, event)
        ctx.should_call_api(
            "get_member",
            {"guild_id": 5566, "user_id": 3344},
            Member(
                user=User(id=3344, username="MyUser", avatar="http://xxx.jpg"),
                nick="MyNick",
            ),
        )
        ctx.should_call_send(event, "", True, user_info=user_info)

        user_info = UserInfo(
            user_id="1234",
            user_name="user",
            user_displayname="nick",
            user_remark=None,
            user_avatar=ImageUrl(url="http://xxx.jpg"),
            user_gender="unknown",
        )
        event = _fake_message_create_event("/user_info 1234")
        ctx.receive_event(bot, event)
        ctx.should_call_api(
            "get_member",
            {"guild_id": 5566, "user_id": 1234},
            Member(
                user=User(id=1234, username="user", avatar="http://xxx.jpg"),
                nick="nick",
            ),
        )
        ctx.should_call_send(event, "", True, user_info=user_info)

        user_info = UserInfo(
            user_id="3344",
            user_name="MyUser",
            user_displayname=None,
            user_remark=None,
            user_avatar=ImageUrl(url="http://xxx.jpg"),
            user_gender="unknown",
        )
        event = _fake_direct_message_create_event("/user_info")
        ctx.receive_event(bot, event)
        ctx.should_call_send(event, "", True, user_info=user_info)

        event = _fake_direct_message_create_event("/user_info 1234")
        ctx.receive_event(bot, event)
        ctx.should_call_send(event, "", True, user_info=None)

        user_info = UserInfo(
            user_id="2233",
            user_name="Bot",
            user_displayname=None,
            user_remark=None,
            user_avatar=ImageUrl(url="http://xxx.jpg"),
            user_gender="unknown",
        )
        event = _fake_direct_message_create_event("/bot_user_info")
        ctx.receive_event(bot, event)
        ctx.should_call_api(
            "me", {}, User(id=2233, username="Bot", avatar="http://xxx.jpg")
        )
        ctx.should_call_send(event, "", True, user_info=user_info)
