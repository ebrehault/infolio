from guillotina import configure, content, schema
from guillotina.interfaces import IFolder, IItem, IRolePermissionManager, IPrincipalRoleManager
from guillotina.content import create_content_in_container
from guillotina.security.utils import apply_sharing

class IAccount(IFolder):
    user = schema.Text(required=True)


@configure.contenttype(
    type_name="Account",
    schema=IAccount,
    allowed_types=['Page'],
    globally_addable=False)
class Account(content.Folder):

    pass


class IMastodonContainer(IFolder):
    pass


@configure.contenttype(
    type_name="MastodonContainer",
    schema=IMastodonContainer,
    allowed_types=['MastodonInstance'])
class MastodonContainer(content.Folder):
    async def get_instances(self):
        instances = []
        async for _, obj in self.async_items():
            instances.append({"id": obj.id})
        return instances

class IMastodonInstance(IItem):
    url = schema.Text(required=True)
    client_id = schema.Text(required=True)
    client_secret = schema.Text(required=True)

@configure.contenttype(
    type_name="MastodonInstance",
    schema=IMastodonInstance,
    allowed_types=['Account'],
    globally_addable=False)
class MastodonInstance(content.Folder):
    # def get_user_profile(self, mastodon_token):
    #     profile_url = f"{self.url}/oauth/userinfo"
    #     return requests.post(
    #         profile_url,
    #         headers={
    #             "Authorization": f"Bearer {mastodon_token}",
    #             "Accept": "application/json",
    #         }
    #     ).json()

    # async def get_or_create_account(self, mastodon_token):
    #     profile_data = self.get_user_profile(mastodon_token)
    #     account_id = profile_data["profile"].split("/")[-1]
    #     account = await self.get_account(account_id)
    #     if not account:
    #         roleperm = IRolePermissionManager(self)
    #         roleperm.grant_permission_to_role('guillotina.AddContent', 'guillotina.Public')
    #         account = await self.create_account(account_id, profile_data)
    #     account.mastodon_token = mastodon_token
    #     account.code = hashlib.sha256(mastodon_token).hexdigest()
    #     return account

    async def get_account(self, account_id):
        return await self.async_get(account_id)
    
    async def create_account(self, username):
        roleperm = IRolePermissionManager(self)
        roleperm.grant_permission_to_role('guillotina.AddContent', 'guillotina.Member')
        principal = IPrincipalRoleManager(self)
        principal.assign_role_to_principal("guillotina.Owner", username)
        account = await create_content_in_container(self, 'Account', username)
        account.user = username
        return account


class IPage(IFolder):
    title = schema.Text(required=True)
    body = schema.Text()


@configure.contenttype(
    type_name="Page",
    schema=IPage,
    behaviors=[
        "guillotina.behaviors.dublincore.IDublinCore",
        "guillotina.behaviors.attachment.IAttachment"
    ],
    globally_addable=False,
    allowed_types=['Page'],
)
class Page(content.Folder):
    def get_account(self):
        if not hasattr(self, '__parent__'):
            return None
        parent = self.__parent__
        if parent.type_name == 'Page':
            return parent.get_account()
        elif parent.type_name == 'Account':
            return parent
        else:
            return None

    async def publish(self):
        return await apply_sharing(self, {
            "prinrole": [{ "principal": "Anonymous User", "role": "guillotina.Reader", "setting": "Allow" }]
        })
