from Products.Archetypes.public import StringField, TextField
from Products.Archetypes.public import StringWidget
from archetypes.schemaextender.field import ExtensionField
from Products.CMFPlomino.interfaces import IPlominoDatabase
from zope.component import adapts
from zope.interface import implements
from archetypes.schemaextender.interfaces import ISchemaExtender, IBrowserLayerAwareExtender

from .interfaces import IPlominoDatabaseExtension


class _ExtensionStringField(ExtensionField, StringField): pass

class _ExtensionTextField(ExtensionField, TextField): pass


class PlominoExtender(object):
    adapts(IPlominoDatabase)
    implements(ISchemaExtender, IBrowserLayerAwareExtender)

    layer = IPlominoDatabaseExtension

    fields = [
        _ExtensionTextField(
            name='connString',
            widget=StringWidget(
                label=u"Connection String",
                description=u"Connection String To a Database",
            ),
        ),
        
    ]
    def __init__(self, context):
        self.context = context
    
