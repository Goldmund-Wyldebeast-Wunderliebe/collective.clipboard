from plone import api
from plone.app.layout.viewlets import ViewletBase
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from collective.clipboard.utils import get_clipboard

class ListingViewlet(ViewletBase):

    index = ViewPageTemplateFile("clipboard_listing_viewlet.pt")

    def get_clipboard(self):
        return get_clipboard()
