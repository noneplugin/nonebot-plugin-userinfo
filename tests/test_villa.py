import json

from nonebot.adapters.villa import Bot, SendMessageEvent
from nonebot.adapters.villa.config import BotInfo
from nonebot.adapters.villa.models import Member, MemberBasic
from nonebug.app import App


def _fake_send_message_event(msg: str) -> SendMessageEvent:
    return SendMessageEvent.parse_obj(
        {
            "robot": {
                "template": {
                    "id": "2233",
                    "name": "bot",
                    "desc": "",
                    "icon": "https://upload-bbs.miyoushe.com/xxx.jpg",
                    "commands": [{"name": "/echo", "desc": ""}],
                },
                "villa_id": 7788,
            },
            "type": 2,
            "created_at": 1701226761,
            "id": "8ee4c10d-8354-18d7-84df-7e02f034cfd1",
            "send_at": 1701226761000,
            "content": json.dumps(
                {
                    "content": {"text": msg, "entities": []},
                    "user": {
                        "portraitUri": "https://bbs-static.miyoushe.com/avatar/avatar40004.png",
                        "extra": {},
                        "name": "user",
                        "alias": "",
                        "id": "114514",
                        "portrait": "https://bbs-static.miyoushe.com/avatar/avatar40004.png",
                    },
                }
            ),
            "villa_id": 7788,
            "from_user_id": 3344,
            "object_name": 1,
            "room_id": 5566,
            "nickname": "user",
            "msg_uid": "123456",
        }
    )


async def test_message_event(app: App):
    from nonebot_plugin_userinfo import UserInfo
    from nonebot_plugin_userinfo.image_source import ImageUrl

    async with app.test_matcher() as ctx:
        bot = ctx.create_bot(
            base=Bot,
            self_id="2233",
            bot_info=BotInfo(
                bot_id="2233",
                bot_secret="xxxx",
                pub_key=(
                    "-----BEGIN PUBLIC KEY-----\n"
                    "MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQC8KTG22btc3g0SjiH9z352/SkQ\n"
                    "QLXcpaQbzBCgV1A410yMKlgRkM3uyO/kJHGBNAiL6JNe0aH9Gjh18jQgq0toKIUe\n"
                    "1GLPXiC9rrwoFj7VS6istJteSfm2vPIwZw98duUlBnK39OjKDhKSh5TOPpgJh9gn\n"
                    "FVaGNJhR9k4pCvbtzQIDAQAB\n"
                    "-----END PUBLIC KEY-----\n"
                ),
            ),
        )

        user_info = UserInfo(
            user_id="3344",
            user_name="user",
            user_avatar=ImageUrl(
                url="https://bbs-static.miyoushe.com/avatar/avatar40004.png"
            ),
        )
        event = _fake_send_message_event("/user_info")
        ctx.receive_event(bot, event)
        ctx.should_call_api(
            "get_member",
            {"villa_id": 7788, "uid": 3344},
            Member(
                basic=MemberBasic(
                    uid=3344,
                    nickname="user",
                    introduce="系统原装签名，送给每一位小可爱~",
                    avatar="40004",
                    avatar_url="https://bbs-static.miyoushe.com/avatar/avatar40004.png",
                ),
                role_id_list=[],
                joined_at=1701220915,
                role_list=[],
            ),
        )
        ctx.should_call_send(event, "", True, user_info=user_info)

        event = _fake_send_message_event("/user_info 3344")
        ctx.receive_event(bot, event)
        ctx.should_call_api(
            "get_member",
            {"villa_id": 7788, "uid": 3344},
            Member(
                basic=MemberBasic(
                    uid=3344,
                    nickname="user",
                    introduce="系统原装签名，送给每一位小可爱~",
                    avatar="40004",
                    avatar_url="https://bbs-static.miyoushe.com/avatar/avatar40004.png",
                ),
                role_id_list=[],
                joined_at=1701220915,
                role_list=[],
            ),
        )
        ctx.should_call_send(event, "", True, user_info=user_info)

        user_info = UserInfo(
            user_id="2233",
            user_name="bot",
            user_avatar=ImageUrl(url="https://upload-bbs.miyoushe.com/xxx.jpg"),
        )
        event = _fake_send_message_event("/bot_user_info")
        ctx.receive_event(bot, event)
        ctx.should_call_send(event, "", True, user_info=user_info)
