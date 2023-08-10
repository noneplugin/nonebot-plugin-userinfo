from typing import Optional

from pydantic import BaseModel
from strenum import StrEnum

from .image_source import ImageSource


class UserGender(StrEnum):
    male = "male"
    female = "female"
    unknown = "unknown"


class UserInfo(BaseModel):
    user_id: str
    user_name: str
    user_displayname: Optional[str] = None
    user_remark: Optional[str] = None
    user_avatar: Optional[ImageSource] = None
    user_gender: str = UserGender.unknown
