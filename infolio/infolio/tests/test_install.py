import pytest


pytestmark = [pytest.mark.asyncio]


async def test_install(infolio_requester):  # noqa
    async with infolio_requester as requester:
        response, _ = await requester('GET', '/db/guillotina/@addons')
        assert 'infolio' in response['installed']
