from nonebot.adapters.telegram import Bot
from nonebot.adapters.telegram.config import BotConfig
from nonebot.adapters.telegram.event import (
    Event,
    ForumTopicMessageEvent,
    GroupMessageEvent,
    PrivateMessageEvent,
)
from nonebot.adapters.telegram.model import (
    Chat,
    ChatMember,
    File,
    PhotoSize,
    User,
    UserProfilePhotos,
)
from nonebug import App


def _fake_private_message_event(msg: str) -> PrivateMessageEvent:
    event = Event.parse_event(
        {
            "update_id": 10000,
            "message": {
                "message_id": 1234,
                "date": 1122,
                "chat": {"id": 3344, "type": "private"},
                "from": {"id": 3344, "is_bot": False, "first_name": "test"},
                "text": msg,
            },
        }
    )
    assert isinstance(event, PrivateMessageEvent)
    return event


def _fake_group_message_event(msg: str) -> GroupMessageEvent:
    event = Event.parse_event(
        {
            "update_id": 10000,
            "message": {
                "message_id": 1234,
                "date": 1122,
                "chat": {"id": 5566, "type": "group"},
                "from": {"id": 3344, "is_bot": False, "first_name": "test"},
                "text": msg,
            },
        }
    )
    assert isinstance(event, GroupMessageEvent)
    return event


def _fake_forum_topic_message_event(msg: str) -> ForumTopicMessageEvent:
    event = Event.parse_event(
        {
            "update_id": 10000,
            "message": {
                "message_id": 1234,
                "date": 1122,
                "chat": {"id": 5566, "type": "group"},
                "from": {"id": 3344, "is_bot": False, "first_name": "test"},
                "message_thread_id": 6677,
                "is_topic_message": True,
                "text": msg,
            },
        }
    )
    assert isinstance(event, ForumTopicMessageEvent)
    return event


async def test_message_event(app: App):
    from nonebot_plugin_userinfo import UserInfo
    from nonebot_plugin_userinfo.image_source import TelegramFile

    async with app.test_matcher() as ctx:
        bot = ctx.create_bot(
            base=Bot, self_id="2233", config=BotConfig(token="2233:xxx")
        )

        user_info = UserInfo(
            user_id="3344",
            user_name="MyUser",
            user_displayname="test",
            user_remark=None,
            user_avatar=TelegramFile(
                token="2233:xxx",
                file_path="photos/xxxx.jpg",
            ),
            user_gender="unknown",
        )
        event = _fake_private_message_event("/user_info")
        ctx.receive_event(bot, event)
        ctx.should_call_api(
            "get_chat",
            {"chat_id": 3344},
            Chat(id=3344, type="private", username="MyUser", first_name="test"),
        )
        ctx.should_call_api(
            "get_user_profile_photos",
            {"user_id": 3344, "limit": 1, "offset": None},
            UserProfilePhotos(
                total_count=1,
                photos=[
                    [
                        PhotoSize(
                            file_id="4567",
                            file_unique_id="114514",
                            width=100,
                            height=100,
                        )
                    ]
                ],
            ),
        )
        ctx.should_call_api(
            "get_file",
            {"file_id": "4567"},
            File(file_id="4567", file_unique_id="114514", file_path="photos/xxxx.jpg"),
        )
        ctx.should_call_send(event, "", True, user_info=user_info)

        user_info = UserInfo(
            user_id="3344",
            user_name="MyUser",
            user_displayname="test",
            user_remark=None,
            user_avatar=TelegramFile(
                token="2233:xxx",
                file_path="photos/xxxx.jpg",
            ),
            user_gender="unknown",
        )
        event = _fake_group_message_event("/user_info")
        ctx.receive_event(bot, event)
        ctx.should_call_api(
            "get_chat_member",
            {"chat_id": 5566, "user_id": 3344},
            ChatMember(
                status="online",
                user=User(id=3344, is_bot=False, username="MyUser", first_name="test"),
            ),
        )
        ctx.should_call_api(
            "get_user_profile_photos",
            {"user_id": 3344, "limit": 1, "offset": None},
            UserProfilePhotos(
                total_count=1,
                photos=[
                    [
                        PhotoSize(
                            file_id="4567",
                            file_unique_id="114514",
                            width=100,
                            height=100,
                        )
                    ]
                ],
            ),
        )
        ctx.should_call_api(
            "get_file",
            {"file_id": "4567"},
            File(file_id="4567", file_unique_id="114514", file_path="photos/xxxx.jpg"),
        )
        ctx.should_call_send(event, "", True, user_info=user_info)

        user_info = UserInfo(
            user_id="3344",
            user_name="MyUser",
            user_displayname="test",
            user_remark=None,
            user_avatar=TelegramFile(
                token="2233:xxx",
                file_path="photos/xxxx.jpg",
            ),
            user_gender="unknown",
        )
        event = _fake_forum_topic_message_event("/user_info")
        ctx.receive_event(bot, event)
        ctx.should_call_api(
            "get_chat_member",
            {"chat_id": 5566, "user_id": 3344},
            ChatMember(
                status="online",
                user=User(id=3344, is_bot=False, username="MyUser", first_name="test"),
            ),
        )
        ctx.should_call_api(
            "get_user_profile_photos",
            {"user_id": 3344, "limit": 1, "offset": None},
            UserProfilePhotos(
                total_count=1,
                photos=[
                    [
                        PhotoSize(
                            file_id="4567",
                            file_unique_id="114514",
                            width=100,
                            height=100,
                        )
                    ]
                ],
            ),
        )
        ctx.should_call_api(
            "get_file",
            {"file_id": "4567"},
            File(file_id="4567", file_unique_id="114514", file_path="photos/xxxx.jpg"),
        )
        ctx.should_call_send(event, "", True, user_info=user_info)

        user_info = UserInfo(
            user_id="2233",
            user_name="Bot",
            user_displayname="test",
            user_remark=None,
            user_avatar=TelegramFile(
                token="2233:xxx",
                file_path="photos/xxxx.jpg",
            ),
            user_gender="unknown",
        )
        event = _fake_private_message_event("/bot_user_info")
        ctx.receive_event(bot, event)
        ctx.should_call_api(
            "get_me",
            {},
            User(id=2233, is_bot=True, username="Bot", first_name="test"),
        )
        ctx.should_call_api(
            "get_user_profile_photos",
            {"user_id": 2233, "limit": 1, "offset": None},
            UserProfilePhotos(
                total_count=1,
                photos=[
                    [
                        PhotoSize(
                            file_id="4567",
                            file_unique_id="114514",
                            width=100,
                            height=100,
                        )
                    ]
                ],
            ),
        )
        ctx.should_call_api(
            "get_file",
            {"file_id": "4567"},
            File(file_id="4567", file_unique_id="114514", file_path="photos/xxxx.jpg"),
        )
        ctx.should_call_send(event, "", True, user_info=user_info)
