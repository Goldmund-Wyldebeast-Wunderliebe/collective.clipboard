from plone.app.content.browser.tableview import Table as BaseTable
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

class ClipboardTable(BaseTable):

    render = ViewPageTemplateFile("clipboardtable.pt")
