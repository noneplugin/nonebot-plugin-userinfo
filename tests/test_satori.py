from nonebot.adapters.satori import Bot
from nonebot.adapters.satori.config import ClientInfo
from nonebot.adapters.satori.event import PublicMessageCreatedEvent
from nonebot.adapters.satori.models import Member, User
from nonebug.app import App


def _fake_public_message_create_event(
    msg: str,
    *,
    user_id: str = "3344",
    user_name: str = "Aislinn",
    user_nick: str = "aislinn",
    avatar: str = "https://img.kookapp.cn/avatars/xxx",
    platform: str = "kook",
):
    return PublicMessageCreatedEvent.model_validate(
        {
            "id": 4,
            "type": "message-created",
            "platform": platform,
            "self_id": "2233",
            "timestamp": 17000000000,
            "argv": None,
            "button": None,
            "channel": {
                "id": "6677",
                "type": 0,
                "name": "文字频道",
                "parent_id": None,
            },
            "guild": {"id": "5566", "name": None, "avatar": None},
            "login": None,
            "member": {
                "user": None,
                "name": None,
                "nick": user_nick,
                "avatar": None,
                "joined_at": None,
            },
            "message": {
                "id": "56163f81-de30-4c39-b4c4-3a205d0be9da",
                "content": msg,
                "channel": None,
                "guild": None,
                "member": None,
                "user": None,
                "created_at": None,
                "updated_at": None,
            },
            "operator": None,
            "role": None,
            "user": {
                "id": user_id,
                "name": user_name,
                "nick": None,
                "avatar": avatar,
                "is_bot": None,
            },
        }
    )


async def test_message_event(app: App):
    from nonebot_plugin_userinfo import UserInfo
    from nonebot_plugin_userinfo.image_source import ImageUrl

    async with app.test_matcher() as ctx:
        bot = ctx.create_bot(
            base=Bot,
            self_id="2233",
            platform="kook",
            info=ClientInfo(port=5140),
        )
        bot._self_info = User(
            id="2233",
            name="Bot",
            avatar="https://xxx.png",
        )

        user_info = UserInfo(
            user_id="3344",
            user_name="Aislinn",
            user_displayname="aislinn",
            user_avatar=ImageUrl(url="https://img.kookapp.cn/avatars/xxx"),
        )
        event = _fake_public_message_create_event("/user_info")
        ctx.receive_event(bot, event)
        ctx.should_call_send(event, "", True, user_info=user_info)

        user_info = UserInfo(
            user_id="5678",
            user_name=":wq",
            user_displayname="wq!",
            user_avatar=ImageUrl(url="https://img.kookapp.cn/avatars/xxx"),
        )
        event = _fake_public_message_create_event("/user_info 5678")
        ctx.receive_event(bot, event)
        ctx.should_call_api(
            "user_get",
            {"user_id": "5678"},
            User(
                id="5678",
                name=":wq",
                avatar="https://img.kookapp.cn/avatars/xxx",
            ),
        )
        ctx.should_call_api(
            "guild_member_get",
            {"guild_id": "5566", "user_id": "5678"},
            Member(user=None, nick="wq!"),
        )
        ctx.should_call_send(event, "", True, user_info=user_info)

        user_info = UserInfo(
            user_id="2233",
            user_name="Bot",
            user_displayname="bot",
            user_avatar=ImageUrl(url="https://xxx.png"),
        )
        event = _fake_public_message_create_event("/bot_user_info")
        ctx.receive_event(bot, event)
        ctx.should_call_api(
            "guild_member_get",
            {"guild_id": "5566", "user_id": "2233"},
            Member(user=None, nick="bot"),
        )
        ctx.should_call_send(event, "", True, user_info=user_info)

        user_info = UserInfo(
            user_id="114514",
            user_name="User",
            user_displayname="user",
            user_avatar=ImageUrl(
                url="https://thirdqq.qlogo.cn/headimg_dl?dst_uin=114514&spec=640"
            ),
        )
        event = _fake_public_message_create_event(
            "/user_info",
            user_id="114514",
            user_name="User",
            user_nick="user",
            avatar="https://thirdqq.qlogo.cn/headimg_dl?dst_uin=114514&spec=640",
            platform="chronocat",
        )
        ctx.receive_event(bot, event)
        ctx.should_call_send(event, "", True, user_info=user_info)
