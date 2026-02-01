from guillotina import configure
from infolio.content import IPage
from guillotina.response import Response

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
        method='GET',
        name='@view',
        context=IPage,
        permission='guillotina.ViewContent', allow_access=True)
async def view(context, request):
    account = context.get_account()
    content = html_template.format(
        user=getattr(account, 'user', ''),
        title=context.title,
        body=context.body)
    return Response(
        content=content,
        status=200,
    )

@configure.service(
        method='POST',
        name='@publish',
        context=IPage,
        permission='guillotina.ModifyContent')
async def publish(context, request):
    await context.publish()
    return Response(
        status=201,
    )