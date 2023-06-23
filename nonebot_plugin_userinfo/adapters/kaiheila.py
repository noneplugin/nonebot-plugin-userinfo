from typing import Optional

from nonebot.exception import ActionFailed
from nonebot.log import logger
from nonebot_plugin_session import SessionLevel

from ..getter import UserInfoGetter, register_user_info_getter
from ..user_info import UserInfo

try:
    from nonebot.adapters.kaiheila import Bot, Event

    @register_user_info_getter(Bot, Event)
    class Getter(UserInfoGetter[Bot, Event]):
        async def _get_info(self, user_id: str) -> Optional[UserInfo]:
            user = None

            if self.session.level == SessionLevel.LEVEL3:
                if self.session.id3:
                    try:
                        user = await self.bot.user_view(
                            user_id=user_id, guild_id=self.session.id3
                        )
                    except ActionFailed as e:
                        logger.warning(f"Error calling user_view: {e}")
                        pass

            if not user:
                try:
                    user = await self.bot.user_view(user_id=user_id)
                except ActionFailed as e:
                    logger.warning(f"Error calling user_view: {e}")
                    pass

            if user:
                return UserInfo(
                    user_id=user_id,
                    user_name=user.nickname or "",
                    user_avatar=user.vip_avatar or user.avatar,
                )

except ImportError:
    pass
