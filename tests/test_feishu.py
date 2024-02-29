from nonebot.adapters.feishu import (
    Bot,
    EventHeader,
    GroupMessageEvent,
    GroupMessageEventDetail,
    UserId,
)
from nonebot.adapters.feishu.config import BotConfig
from nonebot.adapters.feishu.models import BotInfo, GroupEventMessage, Sender
from nonebug.app import App


def _fake_group_message_event(msg: str) -> GroupMessageEvent:
    header = EventHeader(
        event_id="114514",
        event_type="im.message.receive_v1",
        create_time="123456",
        token="token",
        app_id="app_id",
        tenant_key="tenant_key",
        resource_id=None,
        user_list=None,
    )
    sender = Sender(
        sender_id=UserId(
            open_id="3344",
            user_id="on_111",
            union_id="on_222",
        ),
        tenant_key="tenant_key",
        sender_type="user",
    )
    return GroupMessageEvent.model_validate(
        {
            "schema": "2.0",
            "header": header,
            "event": GroupMessageEventDetail(
                sender=sender,
                message=GroupEventMessage(
                    chat_type="group",
                    message_id="om_111",
                    root_id="om_222",
                    parent_id="om_333",
                    create_time="123456",
                    chat_id="1122",
                    message_type="text",
                    content='{"text":"%s"}' % msg,
                    mentions=None,
                ),
            ),
            "reply": None,
        }
    )


async def test_message_event(app: App):
    from nonebot_plugin_userinfo import UserInfo
    from nonebot_plugin_userinfo.image_source import ImageUrl

    async with app.test_matcher() as ctx:
        bot = ctx.create_bot(
            base=Bot,
            self_id="2233",
            bot_config=BotConfig(
                app_id="114", app_secret="514", verification_token="1919810"
            ),
            bot_info=BotInfo.model_validate(
                {
                    "activate_status": 2,
                    "app_name": "bot",
                    "avatar_url": "https://s1-imfile.feishucdn.com/test.jpg",
                    "ip_white_list": [],
                    "open_id": "ou_123456",
                }
            ),
        )

        user_info = UserInfo(
            user_id="3344",
            user_name="MyUser",
            user_displayname="MyNickName",
            user_remark=None,
            user_avatar=ImageUrl(url="https://s1-imfile.feishucdn.com/xxxx.png"),
            user_gender="male",
        )
        event = _fake_group_message_event("/user_info")
        ctx.receive_event(bot, event)
        ctx.should_call_api(
            "contact/v3/users/3344",
            {"method": "GET", "query": {"user_id_type": "open_id"}},
            {
                "code": 0,
                "msg": "success",
                "data": {
                    "user": {
                        "open_id": "3344",
                        "name": "MyUser",
                        "nickname": "MyNickName",
                        "gender": 1,
                        "avatar": {
                            "avatar_origin": "https://s1-imfile.feishucdn.com/xxxx.png"
                        },
                    }
                },
            },
        )
        ctx.should_call_send(event, "", True, user_info=user_info)

        user_info = UserInfo(
            user_id="1234",
            user_name="user",
            user_displayname="nickname",
            user_remark=None,
            user_avatar=ImageUrl(url="https://s1-imfile.feishucdn.com/xxxx.png"),
            user_gender="female",
        )
        event = _fake_group_message_event("/user_info 1234")
        ctx.receive_event(bot, event)
        ctx.should_call_api(
            "contact/v3/users/1234",
            {"method": "GET", "query": {"user_id_type": "open_id"}},
            {
                "code": 0,
                "msg": "success",
                "data": {
                    "user": {
                        "open_id": "1234",
                        "name": "user",
                        "nickname": "nickname",
                        "gender": 2,
                        "avatar": {
                            "avatar_origin": "https://s1-imfile.feishucdn.com/xxxx.png"
                        },
                    }
                },
            },
        )
        ctx.should_call_send(event, "", True, user_info=user_info)

        user_info = UserInfo(
            user_id="2233",
            user_name="bot",
            user_displayname=None,
            user_remark=None,
            user_avatar=ImageUrl(url="https://s1-imfile.feishucdn.com/test.jpg"),
            user_gender="unknown",
        )
        event = _fake_group_message_event("/bot_user_info")
        ctx.receive_event(bot, event)
        ctx.should_call_send(event, "", True, user_info=user_info)
