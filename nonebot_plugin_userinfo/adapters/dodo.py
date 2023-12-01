from typing import Optional

from nonebot.exception import ActionFailed
from nonebot.log import logger

from ..getter import UserInfoGetter, register_user_info_getter
from ..image_source import ImageUrl
from ..user_info import UserGender, UserInfo

try:
    from nonebot.adapters.dodo import Bot, Event
    from nonebot.adapters.dodo.models import Personal, Sex

    def _sex_to_gender(sex: Sex) -> UserGender:
        return (
            UserGender.male
            if sex == Sex.MALE
            else UserGender.female
            if sex == Sex.FEMALE
            else UserGender.unknown
        )

    @register_user_info_getter(Bot, Event)
    class Getter(UserInfoGetter[Bot, Event]):
        async def _get_info(self, user_id: str) -> Optional[UserInfo]:
            user_info = None

            if user_id == self.event.dodo_source_id:
                personal: Optional[Personal] = getattr(self.event, "personal", None)
                if personal:
                    user_info = UserInfo(
                        user_id=self.event.dodo_source_id,
                        user_name=personal.nick_name,
                        user_avatar=ImageUrl(url=personal.avatar_url),
                        user_gender=_sex_to_gender(personal.sex),
                    )

            if not user_info:
                island_source_id: Optional[str] = getattr(
                    self.event, "island_source_id", None
                )
                if island_source_id:
                    try:
                        member_info = await self.bot.get_member_info(
                            island_source_id=island_source_id,
                            dodo_source_id=user_id,
                        )
                        user_info = UserInfo(
                            user_id=member_info.dodo_source_id,
                            user_name=member_info.personal_nick_name,
                            user_avatar=ImageUrl(url=member_info.avatar_url),
                            user_gender=_sex_to_gender(member_info.sex),
                        )
                    except ActionFailed as e:
                        logger.warning(f"Error calling get_member_info: {e}")

            if user_id == self.bot.self_id:
                bot_info = self.bot.bot_info
                if not bot_info:
                    try:
                        bot_info = await self.bot.get_bot_info()
                    except ActionFailed as e:
                        logger.warning(f"Error calling get_bot_info: {e}")

                if bot_info:
                    user_info = UserInfo(
                        user_id=bot_info.dodo_source_id,
                        user_name=bot_info.nick_name,
                        user_avatar=ImageUrl(url=bot_info.avatar_url),
                    )

            return user_info

except ImportError:
    pass
