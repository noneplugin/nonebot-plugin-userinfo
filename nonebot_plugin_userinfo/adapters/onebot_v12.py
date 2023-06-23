from typing import Optional

from nonebot.exception import ActionFailed
from nonebot.log import logger
from nonebot_plugin_session import SessionLevel

from ..getter import UserInfoGetter, register_user_info_getter
from ..image_source import QQAvatar
from ..user_info import UserInfo

try:
    from nonebot.adapters.onebot.v12 import Bot, Event

    @register_user_info_getter(Bot, Event)
    class Getter(UserInfoGetter[Bot, Event]):
        async def _get_info(self, user_id: str) -> Optional[UserInfo]:
            avatar = None
            if self.bot.platform == "qq":
                avatar = QQAvatar(qq=int(user_id))

            info = None

            if self.session.level == SessionLevel.LEVEL3:
                if self.session.id3:
                    if self.session.id2:
                        try:
                            info = await self.bot.get_channel_member_info(
                                guild_id=self.session.id3,
                                channel_id=self.session.id2,
                                user_id=user_id,
                            )
                        except ActionFailed as e:
                            logger.warning(
                                f"Error calling get_channel_member_info: {e}"
                            )
                            pass
                    else:
                        try:
                            info = await self.bot.get_guild_member_info(
                                guild_id=self.session.id3, user_id=user_id
                            )
                        except ActionFailed as e:
                            logger.warning(f"Error calling get_guild_member_info: {e}")
                            pass

                    platform = self.bot.platform
                    impl = self.bot.impl
                    if platform == "qqguild" and impl == "nonebot-plugin-all4one":
                        # 先转成 dict，这样就算以后用扩展模型也不会出错
                        event_dict = self.event.dict()
                        try:
                            if user_id == str(event_dict["qqguild"]["author"]["id"]):
                                avatar = str(event_dict["qqguild"]["author"]["avatar"])
                                if not avatar and info:
                                    avatar = str(info["qqguild"]["user"]["avatar"])  # type: ignore
                        except KeyError:
                            pass

            elif self.session.level == SessionLevel.LEVEL2:
                if self.session.id2:
                    info = await self.bot.get_group_member_info(
                        group_id=self.session.id2, user_id=user_id
                    )

            if not info:
                try:
                    info = await self.bot.get_user_info(user_id=user_id)
                except ActionFailed as e:
                    logger.warning(f"Error calling get_user_info: {e}")
                    pass

            if info:
                user_name = info["user_name"]
                user_displayname = info["user_displayname"]
                user_remark = info.get("user_remark")
                gender = "unknown"
                return UserInfo(
                    user_id=user_id,
                    user_name=user_name,
                    user_displayname=user_displayname,
                    user_remark=user_remark,
                    user_avatar=avatar,
                    user_gender=gender,
                )

except ImportError:
    pass
