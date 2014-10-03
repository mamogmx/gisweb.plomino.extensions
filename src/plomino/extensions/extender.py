from Products.Archetypes.public import StringField, TextField
from Products.Archetypes.public import StringWidget
from archetypes.schemaextender.field import ExtensionField
from Products.CMFPlomino.interfaces import IPlominoDatabase
from zope.component import adapts
from zope.interface import implements
from archetypes.schemaextender.interfaces import ISchemaExtender, IBrowserLayerAwareExtender
from zope import event
from Products.Archetypes.interfaces import IObjectInitializedEvent
from .interfaces import IPlominoDatabaseExtension

from AccessControl import ClassSecurityInfo
from Globals import InitializeClass

from Plomino.CMFPlomino.PlominoDatabase import PlominoDatabase


from Products.CMFPlomino.config import READ_PERMISSION

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
    
    def getFields(self):
        return self.fields
        
        
InitializeClass(PlominoDatabase)        
        
def createDoc(self,docid=None):
    self.createDocument()
    event.notify(IObjectInitializedEvent)

PlominoDocument.createDocument=createDoc    