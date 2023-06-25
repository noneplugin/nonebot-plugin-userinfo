from typing import Optional

from nonebot.exception import ActionFailed
from nonebot.log import logger
from nonebot_plugin_session import SessionLevel

from ..getter import UserInfoGetter, register_user_info_getter
from ..image_source import TelegramFile
from ..user_info import UserInfo

try:
    from nonebot.adapters.telegram import Bot, Event

    @register_user_info_getter(Bot, Event)
    class Getter(UserInfoGetter[Bot, Event]):
        async def _get_info(self, user_id: str) -> Optional[UserInfo]:
            user = None

            if self.bot.self_id == user_id:
                try:
                    user = await self.bot.get_me()
                except ActionFailed as e:
                    logger.warning(f"Error calling get_me: {e}")
                    pass

            elif self.session.level == SessionLevel.LEVEL3:
                if self.session.id3:
                    try:
                        member = await self.bot.get_chat_member(
                            chat_id=int(self.session.id3), user_id=int(user_id)
                        )
                        if member:
                            user = member.user
                    except ActionFailed as e:
                        logger.warning(f"Error calling get_chat_member: {e}")
                        pass

            elif self.session.level == SessionLevel.LEVEL2:
                if self.session.id2:
                    try:
                        member = await self.bot.get_chat_member(
                            chat_id=int(self.session.id2), user_id=int(user_id)
                        )
                        if member:
                            user = member.user
                    except ActionFailed as e:
                        logger.warning(f"Error calling get_chat_member: {e}")
                        pass

            if not user:
                try:
                    user = await self.bot.get_chat(chat_id=int(user_id))
                except ActionFailed as e:
                    logger.warning(f"Error calling get_chat: {e}")
                    pass

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
                            token=config.token,
                            file_path=file.file_path,
                            api_server=config.api_server,
                        )

                return UserInfo(
                    user_id=str(user.id),
                    user_name=user.username or "",
                    user_displayname=user.first_name,
                    user_avatar=avatar,
                )

except ImportError:
    pass
