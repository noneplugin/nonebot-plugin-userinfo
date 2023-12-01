from typing import Optional

from nonebot.exception import ActionFailed
from nonebot.log import logger

from ..getter import UserInfoGetter, register_user_info_getter
from ..image_source import TelegramFile
from ..user_info import UserInfo

try:
    from nonebot.adapters.telegram import Bot, Event
    from nonebot.adapters.telegram.event import (
        ChannelPostEvent,
        EditedChannelPostEvent,
        ForumTopicEditedMessageEvent,
        ForumTopicMessageEvent,
        GroupEditedMessageEvent,
        GroupMessageEvent,
        LeftChatMemberEvent,
        NewChatMemberEvent,
    )

    @register_user_info_getter(Bot, Event)
    class Getter(UserInfoGetter[Bot, Event]):
        async def _get_info(self, user_id: str) -> Optional[UserInfo]:
            user = None

            if self.bot.self_id == user_id:
                try:
                    user = await self.bot.get_me()
                except ActionFailed as e:
                    logger.warning(f"Error calling get_me: {e}")

            elif isinstance(
                self.event,
                (
                    ForumTopicMessageEvent,
                    ChannelPostEvent,
                    ForumTopicEditedMessageEvent,
                    EditedChannelPostEvent,
                    GroupMessageEvent,
                    GroupEditedMessageEvent,
                    LeftChatMemberEvent,
                    NewChatMemberEvent,
                ),
            ):
                try:
                    member = await self.bot.get_chat_member(
                        chat_id=self.event.chat.id, user_id=int(user_id)
                    )
                    if member:
                        user = member.user
                except ActionFailed as e:
                    logger.warning(f"Error calling get_chat_member: {e}")

            if not user:
                try:
                    user = await self.bot.get_chat(chat_id=int(user_id))
                except ActionFailed as e:
                    logger.warning(f"Error calling get_chat: {e}")

            if user:
                avatar = None
                try:
                    profile_photos = await self.bot.get_user_profile_photos(
                        user_id=user.id, limit=1
                    )
                except ActionFailed as e:
                    logger.warning(f"Error calling get_user_profile_photos: {e}")
                    profile_photos = None

                if profile_photos and profile_photos.total_count > 0:
                    file_id = profile_photos.photos[0][-1].file_id
                    try:
                        file = await self.bot.get_file(file_id=file_id)
                    except ActionFailed as e:
                        logger.warning(f"Error calling get_file: {e}")
                        file = None

                    if file and file.file_path:
                        config = self.bot.bot_config
                        avatar = TelegramFile(
                            token=config.token, file_path=file.file_path
                        )

                return UserInfo(
                    user_id=str(user.id),
                    user_name=user.username or "",
                    user_displayname=user.first_name,
                    user_avatar=avatar,
                )

except ImportError:
    pass
