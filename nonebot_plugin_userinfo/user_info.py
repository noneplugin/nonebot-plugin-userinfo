from pathlib import Path
from typing import Optional, Union

from pydantic import BaseModel

from .image_source import ImageSource

ImageData = Union[bytes, ImageSource, Path]


class UserInfo(BaseModel):
    user_id: str
    user_name: str
    user_displayname: Optional[str] = None
    user_remark: Optional[str] = None
    user_avatar: Optional[ImageData] = None
    user_gender: str = "unknown"
