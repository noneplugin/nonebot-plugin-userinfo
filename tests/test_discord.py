from nonebot.adapters.discord import (
    Bot,
    DirectMessageCreateEvent,
    GuildMessageCreateEvent,
    Message,
)
from nonebot.adapters.discord.api.model import MessageFlag, MessageType, User
from nonebot.adapters.discord.config import BotInfo
from nonebug.app import App


async def test_guild_message_create_event(app: App):
    from nonebot_plugin_userinfo import DiscordUserAvatar, UserInfo
    from tests.plugins.echo import user_info_cmd

    event = GuildMessageCreateEvent.parse_obj(
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
            "_message": Message("/user_info"),
        }
    )

    user_info = UserInfo(
        user_id="3344",
        user_name="MyUser",
        user_avatar=DiscordUserAvatar(user_id=3344, image_hash="114514"),
    )

    async with app.test_matcher(user_info_cmd) as ctx:
        bot = ctx.create_bot(base=Bot, self_id="2233", bot_info=BotInfo(token="1234"))
        ctx.receive_event(bot, event)
        ctx.should_call_send(event, "", True, user_info=user_info)


async def test_direct_message_create_event(app: App):
    from nonebot_plugin_userinfo import DiscordUserAvatar, UserInfo
    from tests.plugins.echo import user_info_cmd

    event = DirectMessageCreateEvent.parse_obj(
        {
            "id": 1234,
            "channel_id": 3344,
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
            "_message": Message("/user_info"),
        }
    )

    user_info = UserInfo(
        user_id="3344",
        user_name="MyUser",
        user_avatar=DiscordUserAvatar(user_id=3344, image_hash="114514"),
    )

    async with app.test_matcher(user_info_cmd) as ctx:
        bot = ctx.create_bot(base=Bot, self_id="2233", bot_info=BotInfo(token="1234"))
        ctx.receive_event(bot, event)
        ctx.should_call_send(event, "", True, user_info=user_info)


async def test_bot_user_info(app: App):
    from nonebot_plugin_userinfo import DiscordUserAvatar, UserInfo
    from tests.plugins.echo import bot_user_info_cmd

    event = GuildMessageCreateEvent.parse_obj(
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
            "_message": Message("/bot_user_info"),
        }
    )

    user_info = UserInfo(
        user_id="2233",
        user_name="Bot",
        user_avatar=DiscordUserAvatar(user_id=2233, image_hash="114514"),
    )

    async with app.test_matcher(bot_user_info_cmd) as ctx:
        bot = ctx.create_bot(base=Bot, self_id="2233", bot_info=BotInfo(token="1234"))
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
