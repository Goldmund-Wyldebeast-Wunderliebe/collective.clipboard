from plone import api
from config import CLIPBOARD_SESSION_ID

def get_clipboard(full_objects=False, as_brains=False):
    sdm = api.portal.get_tool('session_data_manager')

    #I'm not creating session if no items in clipboard
    if not sdm.hasSessionData():
        return []
    session = sdm.getSessionData(create=True)

    #session creation may be blocked
    if not session:
        return []
    clipboard = session.get(CLIPBOARD_SESSION_ID, [])
    if full_objects:
        clipboard = [api.content.get(UID=uid) for uid in clipboard]
        clipboard = filter(None, clipboard)
    if as_brains:
        catalog = api.portal.get_tool('portal_catalog')
        clipboard = catalog(UID=clipboard)
    return clipboard

def add_to_clipboard(obj):
    sdm = api.portal.get_tool('session_data_manager')
    session = sdm.getSessionData(create=True)
    clipboard = session.get(CLIPBOARD_SESSION_ID, [])

    #if obj is string I assume that provided value is UID
    if isinstance(obj, str):
        uuid = obj
    else:
        uuid = api.content.get_uuid(obj=obj)
    if uuid and uuid not in clipboard:
        clipboard.append(uuid)
        session.set(CLIPBOARD_SESSION_ID, clipboard)

def delete_from_clipboard(obj=None, path=None):
    if not (obj or path):
        return
    sdm = api.portal.get_tool('session_data_manager')
    session = sdm.getSessionData(create=True)
    clipboard = session.get(CLIPBOARD_SESSION_ID, [])
    if path:
        brains = api.portal.get_tool('portal_catalog')(path=path)
        if brains:
            uuid = brains[0].UID
    elif isinstance(obj, str):
        uuid = obj
    else:
        uuid = api.content.get_uuid(obj=obj)
    if uuid and uuid in clipboard:
        clipboard.remove(uuid)
        session.set(CLIPBOARD_SESSION_ID, clipboard)


