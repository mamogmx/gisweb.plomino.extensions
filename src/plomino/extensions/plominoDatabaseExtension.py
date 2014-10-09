from Products.Archetypes.public import StringField, TextField
from Products.Archetypes.public import StringWidget
from archetypes.schemaextender.field import ExtensionField
from zope.component import adapts
from zope.interface import implements
from archetypes.schemaextender.interfaces import ISchemaExtender, IBrowserLayerAwareExtender
from AccessControl import ClassSecurityInfo
from Globals import InitializeClass
from Acquisition import aq_parent,aq_inner
from Products.Archetypes.atapi import *

from Products.CMFPlomino.interfaces import IPlominoDatabase
from interfaces import IPlominoDatabaseExtension

class _ExtensionStringField(ExtensionField, StringField): 
    pass

from zope.schema.vocabulary import SimpleVocabulary    

def getConnections():
    """Find SQL database connections in the current folder and above

    This function returns a list of two-element tuples. The second element
    is the connection ID, the first element either its title, or if the 
    title is empty, its ID.
    """
    ids = {}
    container = obj
    while container is not None:
        if getattr(container, 'objectValues', None) is not None:
            for ob in container.objectValues():
                if ( getattr(ob, '_isAnSQLConnection', None) and
                     getattr(ob, 'id', None) ):
                    ob_id = ob.id

                    if callable(ob_id):
                        ob_id = ob_id()

                    if ob_id not in ids:
                        if hasattr(ob, 'title_and_id'):
                            title = ob.title_and_id()
                        else:
                            title = ob_id
                        ids[ob_id] = title

        container = aq_parent(aq_inner(container))

    ids = [(item[1], item[0]) for item in ids.items()]
    ids.sort()
    import pdb;pdb.set_trace()
    return ids


    
class plominoDbExtender(object):
    adapts(IPlominoDatabase)
    implements(ISchemaExtender, IBrowserLayerAwareExtender)

    layer = IPlominoDatabaseExtension
    
    fields = [
        _ExtensionStringField(
            name='connString',
            widget=StringWidget(
                label=u"Connection String",
                description=u"Connection String",
            ),
            size = 60,
        ),
        _ExtensionStringField(
            name='dbSchema',
            widget=StringWidget(
                label=u"Schema",
                description=u"Schema",
            ),
            default = u'public',
        ),
        _ExtensionStringField(
            name='dbTable',
            widget=StringWidget(
                label=u"Table",
                description=u"table",
            ),
        ),
    ]
    
    def __init__(self, context):
        self.context = context
    
    def getFields(self):
        return self.fields 
    