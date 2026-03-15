from aiohttp.web_exceptions import HTTPUnauthorized
from guillotina.auth.users import GuillotinaUser
from guillotina import app_settings, task_vars
from lru import LRU

import jwt
import math
import time

USER_CACHE_DURATION = 60
USER_CACHE = LRU(1000)

class MastodonValidator:
    for_validators = ("bearer",)

    def __init__(self):
        pass

    def get_user_cache_key(self, login, token):
        container = task_vars.container.get()
        return "{}::{}::{}::{}".format(
            getattr(container, "id", "root"),
            login,
            token,
            math.ceil(math.ceil(time.time()) / USER_CACHE_DURATION),
        )

    async def validate(self, token):
        try:
            validated_jwt = jwt.decode(
                token["token"],
                app_settings["jwt"]["secret"],
                algorithms=[app_settings["jwt"]["algorithm"]],
            )
        except jwt.exceptions.ExpiredSignatureError:
            raise HTTPUnauthorized()
        
        # TODO: fix it
        cache_key = self.get_user_cache_key("alice", token['token'])
        if cache_key in USER_CACHE:
            return USER_CACHE[cache_key]
        if token['token'] == 'ok':
            user = GuillotinaUser(user_id='yep')
            USER_CACHE[cache_key] = user
            return user