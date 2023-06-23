import hashlib
from dataclasses import dataclass

from .utils import download_url


class ImageSource:
    async def get_image(self) -> bytes:
        raise NotImplementedError


@dataclass
class QQAvatar(ImageSource):
    qq: int

    async def get_image(self) -> bytes:
        url = f"http://q1.qlogo.cn/g?b=qq&nk={self.qq}&s=640"
        data = await download_url(url)
        if hashlib.md5(data).hexdigest() == "acef72340ac0e914090bd35799f5594e":
            url = f"http://q1.qlogo.cn/g?b=qq&nk={self.qq}&s=100"
            data = await download_url(url)
        return data
