import pytest
from nonebug import App


@pytest.fixture
async def app():
    yield App()
