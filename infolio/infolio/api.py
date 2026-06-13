import base64
import json

import jwt
import requests
from guillotina import configure, app_settings
from infolio.content import (
    IMastodonContainer,
    IMastodonInstance,
    IPage,
    create_content_in_container,
)
from guillotina.response import Response
from guillotina.exceptions import Unauthorized
from guillotina.utils import get_object_url, get_authenticated_user
from guillotina.behaviors.dublincore import IDublinCore

html_template = """<html>
<header>
{user}
<header>
<main>
<h1>{title}</h1>
<div class="body">
{body}
</div>
</main>
</html>"""


@configure.service(
    method="GET",
    name="@view",
    context=IPage,
    permission="guillotina.ViewContent",
    allow_access=True,
)
async def view(context, request):
    account = context.get_account()
    content = html_template.format(
        user=getattr(account, "user", ""), title=context.title, body=context.body
    )
    return Response(
        content=content,
        status=200,
    )


@configure.service(
    method="POST", name="@publish", context=IPage, permission="guillotina.ModifyContent"
)
async def publish(context, request):
    await context.publish()
    return Response(
        status=201,
    )


@configure.service(
    method="GET",
    name="@login",
    context=IMastodonInstance,
    permission="guillotina.Public",
    allow_access=True,
)
async def login(context, request):
    # TODO: fix, use env var
    redirect = f"https://109b-82-64-57-232.ngrok-free.app/db/container/mastodons/{context.id}/@callback"
    came_from = request.query.get("came_from")
    state = base64.b64encode(
        json.dumps({"came_from": came_from}).encode("utf-8")
    ).decode("ascii")
    oauth_authorize_url = f"{context.url}/oauth/authorize?client_id={context.client_id}&response_type=code&scope=profile&state={state}&redirect_uri={redirect}"
    return Response(status=302, headers={"location": oauth_authorize_url})


@configure.service(
    method="GET",
    name="@callback",
    context=IMastodonInstance,
    permission="guillotina.Public",
    allow_access=True,
)
async def callback(context, request):
    redirect = f"https://109b-82-64-57-232.ngrok-free.app/db/container/mastodons/{context.id}/@callback"
    code = request.query.get("code")
    if not code:
        raise Unauthorized("Missing code")
    state = request.query.get("state")
    came_from = json.loads(base64.b64decode(state.encode("ascii")).decode("utf-8")).get(
        "came_from"
    )
    token_url = f"{context.url}/oauth/token"
    res = requests.post(
        token_url,
        json={
            "grant_type": "authorization_code",
            "client_id": context.client_id,
            "client_secret": context.client_secret,
            "redirect_uri": redirect,
            "code": code,
        },
    ).json()
    if res.get("error"):
        print(res)
        raise Unauthorized("Invalid code")
    token = res["access_token"]
    profile_url = f"{context.url}/oauth/userinfo"
    profile = requests.post(
        profile_url,
        headers={
            "Authorization": f"Bearer {token}",
            "Accept": "application/json",
        },
    ).json()
    profile["instance"] = context.id
    # TODO: set expiration
    jwt_token = jwt.encode(
        profile, app_settings["jwt"]["secret"], app_settings["jwt"]["algorithm"]
    )
    if not came_from:
        came_from = "/"
    if "?" in came_from:
        came_from += f"&token={jwt_token}"
    else:
        came_from += f"?token={jwt_token}"
    return Response(
        status=302,
        headers={"location": came_from, "Authorization": f"Bearer {jwt_token}"},
    )


# @configure.service(
#         method='GET',
#         name='@callback',
#         context=IMastodonInstance,
#         permission='guillotina.Public', allow_access=True)
# async def callback(context, request):
#     # TODO: fix, use env var
#     redirect = f"https://109b-82-64-57-232.ngrok-free.app/db/container/mastodons/{context.id}/@callback"
#     code = request.query.get('code')
#     if not code:
#         raise Unauthorized("Missing code")
#     state = request.query.get('state')
#     came_from = json.loads(base64.b64decode(state.encode('ascii')).decode('utf-8'))["came_from"]
#     token_url = f"{context.url}/oauth/token"
#     res = requests.post(
#         token_url,
#         json={
#             "grant_type": "authorization_code",
#             "client_id": context.client_id,
#             "client_secret": context.client_secret,
#             "redirect_uri": redirect,
#             "code": code,
#         }
#     )
#     token = res.json()['access_token']
#     account = await context.get_or_create_account(token)
#     code = account.code
#     if not came_from:
#         came_from = get_object_url(account)
#     if "?" in came_from:
#       came_from += f"&code={code}"
#     else:
#       came_from += f"?code={code}"
#     return Response(
#         status=302,
#         headers={"location": came_from}
#     )


def validate_code(context, request):
    code = request.query.get("code")
    if not code:
        raise Unauthorized("Missing code")
    account = None
    if context.type_name == "Page":
        account = context.get_account()
    elif context.type_name == "Account":
        account = context
    if account and account.code == code:
        return True
    else:
        raise Unauthorized("Invalid code")


@configure.service(
    method="GET",
    name="@list",
    context=IMastodonContainer,
    permission="guillotina.Public",
    allow_access=True,
)
async def list_mastodons(context, request):
    return await context.get_instances()


@configure.service(
    method="GET",
    name="@profile",
    context=IMastodonInstance,
    permission="guillotina.Public",
    allow_access=True,
)
async def profile(context, request):
    user = get_authenticated_user()
    return user.id
    # validate_code(context, request)
    # return context.get_profile()


@configure.service(
    method="POST",
    name="@create_account",
    context=IMastodonInstance,
    permission="guillotina.Public",
    allow_access=True,
)
async def create_account(context, request):
    user = get_authenticated_user()
    if user:
        account = await context.create_account(user.id)
        return {"account": account.id}


@configure.service(
    method="GET",
    name="@get_account_data",
    context=IMastodonInstance,
    permission="guillotina.Public",
    allow_access=True,
)
async def get_account_data(context, request):
    user = get_authenticated_user()
    if user:
        account = await context.async_get(user.id)
        return {"account": account.id}


@configure.service(
    method="GET",
    name="@get_pages",
    context=IMastodonInstance,
    permission="guillotina.Public",
    allow_access=True,
)
async def get_pages(context, request):
    user = get_authenticated_user()
    if user:
        account = await context.async_get(user.id)
        pages = []
        async for _, obj in account.async_items():
            behavior = IDublinCore(obj)
            await behavior.load()
            pages.append(
                {
                    "id": obj.id,
                    "title": obj.title,
                    "created": behavior.creation_date.isoformat(),
                    "modified": behavior.modification_date.isoformat(),
                }
            )
        return pages
