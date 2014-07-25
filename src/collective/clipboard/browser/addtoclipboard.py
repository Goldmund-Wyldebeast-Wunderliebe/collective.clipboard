from plone import api
from Products.Five.browser import BrowserView
from collective.clipboard.utils import add_to_clipboard
from collective.clipboard import clipboardMessageFactory as _


class AddToClipboard(BrowserView):
    """View to add selected item to the clipboard"""

    def __call__(self):
        add_to_clipboard(self.context)
        api.portal.show_message(message=_(u'Item added to the clipboard'), request=self.request)
        request = self.request
        request.response.redirect(request.get('HTTP_REFERER'))