from typing import Optional

from nonebot.exception import ActionFailed
from nonebot.log import logger
from nonebot_plugin_session import SessionLevel

from ..getter import UserInfoGetter, register_user_info_getter
from ..image_source import QQAvatar
from ..user_info import UserInfo

try:
    from nonebot.adapters.onebot.v11 import Bot, Event

    @register_user_info_getter(Bot, Event)
    class Getter(UserInfoGetter[Bot, Event]):
        async def _get_info(self, user_id: str) -> Optional[UserInfo]:
            info = None

            if self.session.level == SessionLevel.LEVEL2:
                if self.session.id2:
                    try:
                        info = await self.bot.get_group_member_info(
                            group_id=int(self.session.id2), user_id=int(user_id)
                        )
                    except ActionFailed as e:
                        logger.warning(f"Error calling get_group_member_info: {e}")
                        pass

            if not info:
                try:
                    info = await self.bot.get_stranger_info(user_id=int(user_id))
                except ActionFailed as e:
                    logger.warning(f"Error calling get_stranger_info failed: {e}")
                    pass

            if info:
                name = info.get("nickname", "")
                card = info.get("card")
                gender = info.get("sex", "unknown")
                return UserInfo(
                    user_id=user_id,
                    user_name=name,
                    user_displayname=card,
                    user_avatar=QQAvatar(qq=int(user_id)),
                    user_gender=gender,
                )

except ImportError:
    pass
