from io import BytesIO
from pathlib import Path
from typing import Optional, Union

from pydantic import BaseModel

from .image_source import ImageSource

ImageData = Union[str, bytes, Path, BytesIO, ImageSource]


class UserInfo(BaseModel):
    user_id: str
    user_name: str
    user_displayname: Optional[str] = None
    user_remark: Optional[str] = None
    user_avatar: Optional[ImageData] = None
    user_gender: str = "unknown"

    class Config:
        arbitrary_types_allowed = True