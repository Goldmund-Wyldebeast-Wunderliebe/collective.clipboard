from Products.Five import BrowserView
from plone import api
from collective.clipboard.utils import add_to_clipboard


class AddToClipboard(BrowserView):

    def __call__(self):
        request = self.request
        paths = request.get('paths', None)
        targets = [b.getObject() for b in api.portal.get_tool('portal_catalog')(path={'query':paths, 'depth':0})]
        targets = filter(None, targets)
        for target in targets:
            #there are some problems with folders in batch operations. 
            if target.portal_type != 'Folder':
                add_to_clipboard(target.UID())
        api.portal.show_message(message=(u'Item added to the clipboard'), request=request)
        request.response.redirect(request.get('HTTP_REFERER'))