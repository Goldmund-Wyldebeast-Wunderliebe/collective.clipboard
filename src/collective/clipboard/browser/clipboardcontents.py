from plone.app.content.browser.foldercontents import FolderContentsView, FolderContentsTable
from collective.clipboard.utils import get_clipboard

import urllib

from zope.component import getMultiAdapter
from zope.interface import implements
from zope.interface import alsoProvides
from zope.i18n import translate
from zope.publisher.browser import BrowserView

from AccessControl import Unauthorized
from Acquisition import aq_parent, aq_inner
from OFS.interfaces import IOrderedContainer
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.interfaces import IPloneSiteRoot
from Products.CMFPlone.utils import safe_unicode
from Products.CMFPlone.utils import pretty_title_or_id, isExpired

from plone.app.content.browser.interfaces import IFolderContentsView
from plone.app.content.browser.interfaces import IContentsPage
from plone.app.content.browser.tableview import Table, TableBrowserView



class ClipboardContentsView(FolderContentsView):

    #exact copy of template from plone.app.content.browser.folder_contents.pt

    def contents_table(self):
        table = ClipboardContentsTable(aq_inner(self.context), self.request)
        return table.render()

class ClipboardContentsTable(FolderContentsTable):

    def folderitems(self):
        """
        """
        context = aq_inner(self.context)
        plone_utils = getToolByName(context, 'plone_utils')
        plone_view = getMultiAdapter((context, self.request), name=u'plone')
        plone_layout = getMultiAdapter((context, self.request),
                                       name=u'plone_layout')
        portal_workflow = getToolByName(context, 'portal_workflow')
        portal_properties = getToolByName(context, 'portal_properties')
        portal_types = getToolByName(context, 'portal_types')
        site_properties = portal_properties.site_properties

        use_view_action = site_properties.getProperty(
            'typesUseViewActionInListings', ())
        browser_default = plone_utils.browserDefault(context)

        contentsMethod = self.contentsMethod()

        show_all = self.request.get('show_all', '').lower() == 'true'
        pagesize = 20
        pagenumber = int(self.request.get('pagenumber', 1))
        start = (pagenumber - 1) * pagesize
        end = start + pagesize
        clipboard = get_clipboard(as_brains=True)
        results = []
        for i, obj in enumerate(clipboard):
            path = obj.getPath or "/".join(obj.getPhysicalPath())

            # avoid creating unnecessary info for items outside the current
            # batch;  only the path is needed for the "select all" case...
            # Include brain to make customizations easier (see comment below)
            if not show_all and not start <= i < end:
                results.append(dict(path=path, brain=obj))
                continue

            if (i + 1) % 2 == 0:
                table_row_class = "draggable even"
            else:
                table_row_class = "draggable odd"

            url = obj.getURL()
            icon = plone_layout.getIcon(obj)
            type_class = 'contenttype-' + plone_utils.normalizeString(
                obj.portal_type)

            review_state = obj.review_state
            state_class = 'state-' + plone_utils.normalizeString(review_state)
            relative_url = obj.getURL(relative=True)

            fti = portal_types.get(obj.portal_type)
            if fti is not None:
                type_title_msgid = fti.Title()
            else:
                type_title_msgid = obj.portal_type
            url_href_title = u'%s: %s' % (translate(type_title_msgid,
                                                    context=self.request),
                                          safe_unicode(obj.Description))

            modified = plone_view.toLocalizedTime(
                obj.ModificationDate, long_format=1)
            modified_sortable = 'sortabledata-' + obj.modified.strftime(
                '%Y-%m-%d-%H-%M-%S')

            if obj.portal_type in use_view_action:
                view_url = url + '/view'
            elif obj.is_folderish:
                view_url = url + "/folder_contents"
            else:
                view_url = url

            is_browser_default = len(browser_default[1]) == 1 and (
                obj.id == browser_default[1][0])

            results.append(dict(
                # provide the brain itself to allow cleaner customisation of
                # the view.
                #
                # this doesn't add any memory overhead, a reference to
                # the brain is already kept through its getPath bound method.
                brain=obj,
                url=url,
                url_href_title=url_href_title,
                id=obj.getId,
                quoted_id=urllib.quote_plus(obj.getId),
                path=path,
                title_or_id=safe_unicode(pretty_title_or_id(
                    plone_utils, obj)),
                obj_type=obj.Type,
                size=obj.getObjSize,
                modified=modified,
                modified_sortable=modified_sortable,
                icon=icon.html_tag(),
                type_class=type_class,
                wf_state=review_state,
                state_title=portal_workflow.getTitleForStateOnType(
                    review_state, obj.portal_type),
                state_class=state_class,
                is_browser_default=is_browser_default,
                folderish=obj.is_folderish,
                relative_url=relative_url,
                view_url=view_url,
                table_row_class=table_row_class,
                is_expired=isExpired(obj)
            ))
        return results

    @property
    def buttons(self):
        buttons = []
        context = aq_inner(self.context)
        portal_actions = getToolByName(context, 'portal_actions')
        button_actions = portal_actions.listActionInfos(
            object=aq_inner(self.context), categories=('clipboard_buttons', ))

        # Do not show buttons if there is no data, unless there is data to be
        # pasted
        if not len(self.items):
            if self.context.cb_dataValid():
                for button in button_actions:
                    if button['id'] == 'paste':
                        return [self.setbuttonclass(button)]
            else:
                return []

        for button in button_actions:
            # Make proper classes for our buttons
            if button['id'] != 'paste' or context.cb_dataValid():
                buttons.append(self.setbuttonclass(button))
        return buttons
