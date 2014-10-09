from zope import event
from Products.Archetypes.interfaces import IObjectEditedEvent

from AccessControl import ClassSecurityInfo
from Globals import InitializeClass

from Products.CMFPlomino.PlominoDatabase import PlominoDatabase
from Products.CMFPlomino.PlominoDocument import PlominoDocument
from Products.CMFPlomino.PlominoForm import PlominoForm
from Products.CMFPlomino.exceptions import PlominoScriptException
from Products.CMFPlomino.index import PlominoIndex

from Products.CMFPlomino.config import *


from pgReplication import pgReplication

InitializeClass(PlominoDocument)        
PlominoDocument.security = ClassSecurityInfo()   
     
PlominoDocument.security.declareProtected(EDIT_PERMISSION, 'saveDocument')
def saveDoc(self, REQUEST, creation=False):
    """ Save a document using the form submitted content
    """
    db = self.getParentDatabase()
    form = db.getForm(REQUEST.get('Form'))

    errors = form.validateInputs(REQUEST, doc=self)

    # execute the beforeSave code of the form
    error = None
    try:
        error = self.runFormulaScript(
                SCRIPT_ID_DELIMITER.join(['form', form.id, 'beforesave']),
                self,
                form.getBeforeSaveDocument)
    except PlominoScriptException, e:
        e.reportError('Form submitted, but beforeSave formula failed')

    if error:
        errors.append(error)

    # if errors, stop here, and notify errors to user
    if errors:
        return form.notifyErrors(errors)

    self.setItem('Form', form.getFormName())

    # process editable fields (we read the submitted value in the request)
    form.readInputs(self, REQUEST, process_attachments=True)

    # refresh computed values, run onSave, reindex
    self.save(form, creation)
    if self.getItem('pg_replication_config',0):
        event.notify(IObjectEditedEvent)
        self.replicateDoc()
        
    redirect = REQUEST.get('plominoredirecturl')
    if not redirect:
        redirect = self.getItem("plominoredirecturl")
    if type(redirect) is dict:
        # if dict, we assume it contains "callback" as an URL that will be
        # called asynchronously, "redirect" as the redirect url (optional,
        # default=doc url), and "method" (optional, default=GET)
        redirect = "./async_callback?" + urlencode(redirect)
    if not redirect:
        redirect = self.absolute_url()
    REQUEST.RESPONSE.redirect(redirect)
    

def replicate(self):
    pg = pgReplication()
    pg.saveData(self)
    
    
    
PlominoDocument.saveDocument=saveDoc 

PlominoDocument.security.declareProtected(EDIT_PERMISSION, 'replicateDoc')   
PlominoDocument.replicateDoc=replicate 