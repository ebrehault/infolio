from guillotina import configure, content, schema
from guillotina.interfaces import IFolder
from guillotina.security.utils import apply_sharing

class IAccount(IFolder):
    user = schema.Text(required=True)


@configure.contenttype(
    type_name="Account",
    schema=IAccount,
    allowed_types=['Page'])
class Account(content.Folder):
    pass


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
