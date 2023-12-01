from typing import Optional

from nonebot.exception import ActionFailed
from nonebot.log import logger

from ..getter import UserInfoGetter, register_user_info_getter
from ..image_source import DiscordUserAvatar
from ..user_info import UserInfo

try:
    from nonebot.adapters.discord import Bot, Event, MessageEvent

    @register_user_info_getter(Bot, Event)
    class Getter(UserInfoGetter[Bot, Event]):
        async def _get_info(self, user_id: str) -> Optional[UserInfo]:
            user = None

            if isinstance(self.event, MessageEvent) and user_id == str(
                self.event.author.id
            ):
                user = self.event.author

            if not user and user_id == self.bot.self_id:
                try:
                    user = await self.bot.get_current_user()
                except ActionFailed as e:
                    logger.warning(f"Error calling get_current_user: {e}")

            if not user:
                try:
                    user = await self.bot.get_user(user_id=int(user_id))
                except ActionFailed as e:
                    logger.warning(f"Error calling get_user: {e}")

            if user:
                return UserInfo(
                    user_id=str(user.id),
                    user_name=user.username,
                    user_avatar=DiscordUserAvatar(
                        user_id=user.id, image_hash=user.avatar
                    )
                    if user.avatar
                    else None,
                )

except ImportError:
    pass
