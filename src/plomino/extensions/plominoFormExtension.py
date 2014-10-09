from Products.Archetypes.public import StringField, TextField
from Products.Archetypes.public import StringWidget
from archetypes.schemaextender.field import ExtensionField
from zope.component import adapts
from zope.interface import implements
from archetypes.schemaextender.interfaces import ISchemaExtender, IBrowserLayerAwareExtender
from AccessControl import ClassSecurityInfo
from Globals import InitializeClass

from Products.CMFPlomino.interfaces import IPlominoForm
from interfaces import IPlominoFormExtension


class _ExtensionStringField(ExtensionField, StringField): 
    pass

    
class PlominoFrmExtender(object):
    adapts(IPlominoForm)
    implements(ISchemaExtender, IBrowserLayerAwareExtender)

    layer = IPlominoFormExtension

    fields = [
        _ExtensionStringField(
            name='dbSchema',
            widget=StringWidget(
                label=u"Schema",
                description=u"Schema",
            ),
            default = u'public',
            schemata = 'settings'
        ),
        _ExtensionStringField(
            name='dbTable',
            widget=StringWidget(
                label=u"Table",
                description=u"table",
            ),
            schemata = 'settings'
        ),
    ]
    
    def __init__(self, context):
        self.context = context
    
    def getFields(self):
        return self.fields     