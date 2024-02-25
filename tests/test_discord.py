from nonebot.adapters.discord import Bot, GuildMessageCreateEvent, Message
from nonebot.adapters.discord.api.model import MessageFlag, MessageType, User
from nonebot.adapters.discord.config import BotInfo
from nonebug.app import App


def _fake_guild_message_create_event(msg: str) -> GuildMessageCreateEvent:
    return GuildMessageCreateEvent.model_validate(
        {
            "id": 1234,
            "channel_id": 5566,
            "guild_id": 6677,
            "author": User(
                **{
                    "id": 3344,
                    "username": "MyUser",
                    "discriminator": "0",
                    "avatar": "114514",
                }
            ),
            "content": "",
            "timestamp": 1,
            "edited_timestamp": None,
            "tts": False,
            "mention_everyone": False,
            "mentions": [],
            "mention_roles": [],
            "attachments": [],
            "embeds": [],
            "nonce": 3210,
            "pinned": False,
            "type": MessageType(0),
            "flags": MessageFlag(0),
            "referenced_message": None,
            "components": [],
            "to_me": False,
            "reply": None,
            "_message": Message(msg),
        }
    )


async def test_message_event(app: App):
    from nonebot_plugin_userinfo import UserInfo
    from nonebot_plugin_userinfo.image_source import DiscordUserAvatar

    async with app.test_matcher() as ctx:
        bot = ctx.create_bot(base=Bot, self_id="2233", bot_info=BotInfo(token="1234"))

        user_info = UserInfo(
            user_id="3344",
            user_name="MyUser",
            user_avatar=DiscordUserAvatar(user_id=3344, image_hash="114514"),
        )
        event = _fake_guild_message_create_event("/user_info")
        ctx.receive_event(bot, event)
        ctx.should_call_send(event, "", True, user_info=user_info)

        user_info = UserInfo(
            user_id="1234",
            user_name="user",
            user_avatar=DiscordUserAvatar(user_id=1234, image_hash="123456"),
        )
        event = _fake_guild_message_create_event("/user_info 1234")
        ctx.receive_event(bot, event)
        ctx.should_call_api(
            "get_user",
            {"user_id": 1234},
            User(
                **{
                    "id": 1234,
                    "username": "user",
                    "discriminator": "0",
                    "avatar": "123456",
                }
            ),
        )
        ctx.should_call_send(event, "", True, user_info=user_info)

        user_info = UserInfo(
            user_id="2233",
            user_name="Bot",
            user_avatar=DiscordUserAvatar(user_id=2233, image_hash="114514"),
        )
        event = _fake_guild_message_create_event("/bot_user_info")
        ctx.receive_event(bot, event)
        ctx.should_call_api(
            "get_current_user",
            {},
            User(
                **{
                    "id": 2233,
                    "username": "Bot",
                    "discriminator": "0",
                    "avatar": "114514",
                }
            ),
        )
        ctx.should_call_send(event, "", True, user_info=user_info)
