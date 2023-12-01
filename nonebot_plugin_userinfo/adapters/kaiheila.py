from typing import Optional

from nonebot.exception import ActionFailed
from nonebot.log import logger

from ..getter import UserInfoGetter, register_user_info_getter
from ..image_source import ImageUrl
from ..user_info import UserInfo

try:
    from nonebot.adapters.kaiheila import Bot, Event

    @register_user_info_getter(Bot, Event)
    class Getter(UserInfoGetter[Bot, Event]):
        async def _get_info(self, user_id: str) -> Optional[UserInfo]:
            user = None

            if self.bot.self_id == user_id:
                try:
                    user = await self.bot.user_me()
                except ActionFailed as e:
                    logger.warning(f"Error calling user_me: {e}")

            elif self.event.channel_type == "GROUP":
                if self.event.type_ == 255:
                    guild_id = self.event.target_id
                else:
                    guild_id = self.event.extra.guild_id
                if guild_id:
                    try:
                        user = await self.bot.user_view(
                            user_id=user_id, guild_id=guild_id
                        )
                    except ActionFailed as e:
                        logger.warning(f"Error calling user_view: {e}")

            if not user:
                try:
                    user = await self.bot.user_view(user_id=user_id)
                except ActionFailed as e:
                    logger.warning(f"Error calling user_view: {e}")

            if user:
                url = user.vip_avatar or user.avatar
                avatar = ImageUrl(url=url) if url else None
                return UserInfo(
                    user_id=user.id_ or user_id,
                    user_name=user.username or "",
                    user_displayname=user.nickname,
                    user_avatar=avatar,
                )

except ImportError:
    pass
