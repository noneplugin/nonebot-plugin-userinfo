from datetime import datetime

from nonebot.adapters.qq import (
    Bot,
    EventType,
    GroupAtMessageCreateEvent,
    MessageCreateEvent,
)
from nonebot.adapters.qq.config import BotInfo
from nonebot.adapters.qq.models import GroupMemberAuthor, Member, User
from nonebug import App


def _fake_message_create_event(msg: str) -> MessageCreateEvent:
    return MessageCreateEvent(
        id="id",
        __type__=EventType.MESSAGE_CREATE,
        channel_id="6677",
        guild_id="5566",
        author=User(id="3344", username="MyUser", avatar="http://xxx.jpg"),
        content=msg,
    )


def _fake_group_at_message_create_event(msg: str) -> GroupAtMessageCreateEvent:
    return GroupAtMessageCreateEvent(
        id="id",
        content=msg,
        timestamp="1234567890",
        __type__=EventType.GROUP_AT_MESSAGE_CREATE,
        author=GroupMemberAuthor(
            id="id",
            member_openid="3F21411B784D403E811E68BF3E2944D8",
        ),
        group_openid="19303D3617EF432999F24342F99AEC65",
    )


async def test_message_event(app: App):
    from nonebot_plugin_userinfo import UserInfo
    from nonebot_plugin_userinfo.image_source import ImageUrl, QQAvatarOpenId

    async with app.test_matcher() as ctx:
        bot = ctx.create_bot(
            base=Bot, self_id="2233", bot_info=BotInfo(id="2233", token="", secret="")
        )

        user_info = UserInfo(
            user_id="3344",
            user_name="MyUser",
            user_displayname=None,
            user_remark=None,
            user_avatar=ImageUrl(url="http://xxx.jpg"),
            user_gender="unknown",
        )
        event = _fake_message_create_event("/user_info")
        ctx.receive_event(bot, event)
        ctx.should_call_send(event, "", True, user_info=user_info)

        user_info = UserInfo(
            user_id="1234",
            user_name="member",
            user_displayname=None,
            user_remark=None,
            user_avatar=ImageUrl(url="http://xxx.jpg"),
            user_gender="unknown",
        )
        event = _fake_message_create_event("/user_info 1234")
        ctx.receive_event(bot, event)
        ctx.should_call_api(
            "get_member",
            {"guild_id": "5566", "user_id": "1234"},
            Member(
                user=User(id="1234", username="member", avatar="http://xxx.jpg"),
                joined_at=datetime.now(),
            ),
        )
        ctx.should_call_send(event, "", True, user_info=user_info)

        user_info = UserInfo(
            user_id="2233",
            user_name="Bot",
            user_displayname=None,
            user_remark=None,
            user_avatar=ImageUrl(url="http://xxx.jpg"),
            user_gender="unknown",
        )
        event = _fake_message_create_event("/bot_user_info")
        ctx.receive_event(bot, event)
        ctx.should_call_api(
            "me", {}, User(id="2233", username="Bot", avatar="http://xxx.jpg")
        )
        ctx.should_call_send(event, "", True, user_info=user_info)

        user_info = UserInfo(
            user_id="3F21411B784D403E811E68BF3E2944D8",
            user_name="",
            user_displayname=None,
            user_remark=None,
            user_avatar=QQAvatarOpenId(
                appid="2233", user_openid="3F21411B784D403E811E68BF3E2944D8"
            ),
            user_gender="unknown",
        )
        event = _fake_group_at_message_create_event("/user_info")
        ctx.receive_event(bot, event)
        ctx.should_call_send(event, "", True, user_info=user_info)
