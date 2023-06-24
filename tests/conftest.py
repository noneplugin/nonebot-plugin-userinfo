from pathlib import Path
from typing import TYPE_CHECKING, Set

import nonebot
import pytest

if TYPE_CHECKING:
    from nonebot.plugin import Plugin


@pytest.fixture(scope="session", autouse=True)
def load_plugin(nonebug_init: None) -> Set["Plugin"]:
    # preload global plugins
    return nonebot.load_plugins(str(Path(__file__).parent / "plugins"))
