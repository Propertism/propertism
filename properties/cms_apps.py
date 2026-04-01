from cms.app_base import CMSApp
from cms.apphook_pool import apphook_pool


@apphook_pool.register
class PropertiesAppHook(CMSApp):
    app_name = "properties_spa"
    name = "Properties React SPA"

    def get_urls(self, page=None, language=None, **kwargs):
        return ["properties.cms_urls"]
