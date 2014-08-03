from plone import api
from Products.Five.browser import BrowserView
from OFS.Moniker import Moniker
from OFS.CopySupport import _cb_encode, cookie_path
from collective.clipboard.utils import delete_from_clipboard
from collective.clipboard import clipboardMessageFactory as _


class ClipboardCopy(BrowserView):
    """View to add selected item to the clipboard"""

    def __call__(self):
        oblist = []
        request = self.request
        paths = request.get('paths', [])
        brains = api.portal.get_tool('portal_catalog')(path=paths)
        for brain in brains:
            ob = brain.getObject()
            if not ob.cb_isCopyable():
                raise CopyError(eNotSupported % escape(id))
            m = Moniker(ob)
            oblist.append(m.dump())
        cp=(0, oblist)
        cp=_cb_encode(cp)
        resp=request.response
        resp.setCookie('__cp', cp, path='%s' % cookie_path(request))
        request.set('__cp', cp)
        request.response.redirect(request.get('HTTP_REFERER'))

class ClipboardDelete(BrowserView):
    """Delete selected item from the clipboard"""

    def __call__(self):
        oblist = []
        request = self.request
        paths = request.get('paths', [])
        brains = api.portal.get_tool('portal_catalog')(path=paths)
        for brain in brains:
            delete_from_clipboard(path=brain.getPath())
        request.response.redirect(request.get('HTTP_REFERER'))        