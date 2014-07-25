from zope.i18nmessageid import MessageFactory

clipboardMessageFactory = MessageFactory('collective.clipboard')


def initialize(context):
    """Initializer called when used as a Zope 2 product."""
