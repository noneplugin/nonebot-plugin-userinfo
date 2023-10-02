from typing import Optional

from nonebot.exception import ActionFailed
from nonebot.log import logger

from ..getter import UserInfoGetter, register_user_info_getter
from ..image_source import ImageUrl, QQAvatar
from ..user_info import UserInfo

try:
    from nonebot.adapters.onebot.v12 import (
        Bot,
        ChannelCreateEvent,
        ChannelDeleteEvent,
        ChannelMemberDecreaseEvent,
        ChannelMemberIncreaseEvent,
        ChannelMessageDeleteEvent,
        ChannelMessageEvent,
        Event,
        GroupMemberDecreaseEvent,
        GroupMemberIncreaseEvent,
        GroupMessageDeleteEvent,
        GroupMessageEvent,
        GuildMemberDecreaseEvent,
        GuildMemberIncreaseEvent,
    )

    @register_user_info_getter(Bot, Event)
    class Getter(UserInfoGetter[Bot, Event]):
        async def _get_info(self, user_id: str) -> Optional[UserInfo]:
            info = None

            if isinstance(
                self.event,
                (
                    ChannelCreateEvent,
                    ChannelDeleteEvent,
                    ChannelMemberDecreaseEvent,
                    ChannelMemberIncreaseEvent,
                    ChannelMessageDeleteEvent,
                    ChannelMessageEvent,
                ),
            ):
                try:
                    info = await self.bot.get_channel_member_info(
                        guild_id=self.event.guild_id,
                        channel_id=self.event.channel_id,
                        user_id=user_id,
                    )
                except ActionFailed as e:
                    logger.warning(f"Error calling get_channel_member_info: {e}")
                    pass

            elif isinstance(
                self.event, (GuildMemberDecreaseEvent, GuildMemberIncreaseEvent)
            ):
                try:
                    info = await self.bot.get_guild_member_info(
                        guild_id=self.event.guild_id, user_id=user_id
                    )
                except ActionFailed as e:
                    logger.warning(f"Error calling get_guild_member_info: {e}")
                    pass

            elif isinstance(
                self.event,
                (
                    GroupMemberDecreaseEvent,
                    GroupMemberIncreaseEvent,
                    GroupMessageDeleteEvent,
                    GroupMessageEvent,
                ),
            ):
                try:
                    info = await self.bot.get_group_member_info(
                        group_id=self.event.group_id, user_id=user_id
                    )
                except ActionFailed as e:
                    logger.warning(f"Error calling get_group_member_info: {e}")
                    pass

            if not info:
                if self.bot.self_id == user_id:
                    try:
                        info = await self.bot.get_self_info()
                    except ActionFailed as e:
                        logger.warning(f"Error calling get_self_info: {e}")
                        pass
                else:
                    try:
                        info = await self.bot.get_user_info(user_id=user_id)
                    except ActionFailed as e:
                        logger.warning(f"Error calling get_user_info: {e}")
                        pass

            if info:
                user_id = info["user_id"]
                avatar = None

                platform = self.bot.platform
                impl = self.bot.impl

                if platform == "qq":
                    avatar = QQAvatar(qq=int(user_id))

                elif platform == "qqguild" and impl == "nonebot-plugin-all4one":
                    event_dict = self.event.dict()  # 先转成 dict，这样就算以后用扩展模型也不会出错
                    url = None
                    try:
                        if user_id == str(event_dict["qqguild"]["author"]["id"]):
                            url = str(event_dict["qqguild"]["author"]["avatar"])
                    except KeyError:
                        pass
                    if url is None:
                        try:
                            url = str(info["qqguild"]["user"]["avatar"])  # type: ignore
                        except KeyError:
                            pass
                    if url:
                        avatar = ImageUrl(url=url)

                return UserInfo(
                    user_id=user_id,
                    user_name=info["user_name"],
                    user_displayname=info["user_displayname"],
                    user_remark=info.get("user_remark"),
                    user_avatar=avatar,
                )

except ImportError:
    pass
