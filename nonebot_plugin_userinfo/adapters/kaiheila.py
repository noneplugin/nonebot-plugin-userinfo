from typing import Optional

from nonebot.exception import ActionFailed
from nonebot.log import logger
from nonebot_plugin_session import SessionLevel
from pydantic import ValidationError

from ..getter import UserInfoGetter, register_user_info_getter
from ..image_source import ImageUrl
from ..user_info import UserInfo

try:
    from nonebot.adapters.kaiheila import Bot, Event
    from nonebot.adapters.kaiheila.event import User

    @register_user_info_getter(Bot, Event)
    class Getter(UserInfoGetter[Bot, Event]):
        async def _get_info(self, user_id: str) -> Optional[UserInfo]:
            info = None

            if self.session.level == SessionLevel.LEVEL3:
                if self.session.id3:
                    try:
                        info = await self.bot.user_view(
                            user_id=user_id, guild_id=self.session.id3
                        )
                    except ActionFailed as e:
                        logger.warning(f"Error calling user_view: {e}")
                        pass

            if not info:
                try:
                    info = await self.bot.user_view(user_id=user_id)
                except ActionFailed as e:
                    logger.warning(f"Error calling user_view: {e}")
                    pass

            if info:
                try:
                    user = User.parse_obj(info)
                except ValidationError as e:
                    logger.warning(f"Error parsing user info: {e}")
                    return None

                url = user.vip_avatar or user.avatar
                avatar = ImageUrl(url=url) if url else None
                return UserInfo(
                    user_id=user_id,
                    user_name=user.username or "",
                    user_displayname=user.nickname,
                    user_avatar=avatar,
                )

except ImportError:
    pass
