from guillotina import testing
from guillotina.tests.fixtures import ContainerRequesterAsyncContextManager

import json
import pytest


def base_settings_configurator(settings):
    if 'applications' in settings:
        settings['applications'].append('infolio')
    else:
        settings['applications'] = ['infolio']


testing.configure_with(base_settings_configurator)


class infolio_Requester(ContainerRequesterAsyncContextManager):  # noqa

    async def __aenter__(self):
        await super().__aenter__()
        resp = await self.requester(
            'POST', '/db/guillotina/@addons',
            data=json.dumps({
                'id': 'infolio'
            })
        )
        return self.requester


@pytest.fixture(scope='function')
async def infolio_requester(guillotina):
    return infolio_Requester(guillotina)
