from nonebot.adapters.satori import Bot
from nonebot.adapters.satori.config import ClientInfo
from nonebot.adapters.satori.event import PublicMessageCreatedEvent
from nonebot.adapters.satori.models import User
from nonebug.app import App


def _fake_public_message_create_event(msg: str):
    return PublicMessageCreatedEvent.model_validate(
        {
            "id": 4,
            "type": "message-created",
            "platform": "kook",
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
                "nick": "Aislinn",
                "avatar": None,
                "joined_at": None,
            },
            "message": {
                "id": "56163f81-de30-4c39-b4c4-3a205d0be9da",
                "content": [
                    {
                        "type": "text",
                        "attrs": {"text": msg},
                        "children": [],
                        "source": None,
                    }
                ],
                "channel": None,
                "guild": None,
                "member": {
                    "user": {
                        "id": "3344",
                        "name": "Aislinn",
                        "nick": None,
                        "avatar": "https://img.kookapp.cn/avatars/2021-08/GjdUSjtmtD06j06j.png?x-oss-process=style/icon",
                        "is_bot": None,
                        "username": "Aislinn",
                        "user_id": "3344",
                        "discriminator": "4261",
                    },
                    "name": None,
                    "nick": "Aislinn",
                    "avatar": None,
                    "joined_at": None,
                },
                "user": {
                    "id": "3344",
                    "name": "Aislinn",
                    "nick": None,
                    "avatar": "https://img.kookapp.cn/avatars/2021-08/GjdUSjtmtD06j06j.png?x-oss-process=style/icon",
                    "is_bot": None,
                    "username": "Aislinn",
                    "user_id": "3344",
                    "discriminator": "4261",
                },
                "created_at": None,
                "updated_at": None,
                "message_id": "56163f81-de30-4c39-b4c4-3a205d0be9da",
                "elements": [
                    {"type": "text", "attrs": {"content": "test"}, "children": []}
                ],
                "timestamp": 1700474858446,
            },
            "operator": None,
            "role": None,
            "user": {
                "id": "3344",
                "name": "Aislinn",
                "nick": None,
                "avatar": "https://img.kookapp.cn/avatars/2021-08/GjdUSjtmtD06j06j.png?x-oss-process=style/icon",
                "is_bot": None,
                "username": "Aislinn",
                "user_id": "3344",
                "discriminator": "4261",
            },
            "_type": "kook",
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
            user_avatar=ImageUrl(
                url="https://img.kookapp.cn/avatars/2021-08/GjdUSjtmtD06j06j.png?x-oss-process=style/icon"
            ),
        )
        event = _fake_public_message_create_event("/user_info")
        ctx.receive_event(bot, event)
        ctx.should_call_send(event, "", True, user_info=user_info)

        user_info = UserInfo(
            user_id="5566",
            user_name="Aislinn",
            user_avatar=ImageUrl(
                url="https://img.kookapp.cn/avatars/2021-08/GjdUSjtmtD06j06j.png?x-oss-process=style/icon"
            ),
        )
        event = _fake_public_message_create_event("/user_info 5566")
        ctx.receive_event(bot, event)
        ctx.should_call_api(
            "user_get",
            {"user_id": "5566"},
            User(
                id="5566",
                name="Aislinn",
                avatar="https://img.kookapp.cn/avatars/2021-08/GjdUSjtmtD06j06j.png?x-oss-process=style/icon",
            ),
        )
        ctx.should_call_send(event, "", True, user_info=user_info)

        user_info = UserInfo(
            user_id="2233",
            user_name="Bot",
            user_avatar=ImageUrl(url="https://xxx.png"),
        )
        event = _fake_public_message_create_event("/bot_user_info")
        ctx.receive_event(bot, event)
        ctx.should_call_send(event, "", True, user_info=user_info)
