from guillotina import configure


app_settings = {
    # provide custom application settings here...
}


def includeme(root):
    """
    custom application initialization here
    """
    configure.scan('infolio.api')
    configure.scan('infolio.install')
    configure.scan('infolio.content')
