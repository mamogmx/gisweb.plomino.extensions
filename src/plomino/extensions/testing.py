from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import PloneSandboxLayer
from plone.app.testing import IntegrationTesting
from plone.app.testing import FunctionalTesting
from plone.app.testing import applyProfile

from zope.configuration import xmlconfig

class GiswebPlominofieldextensions(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE, )

    def setUpZope(self, app, configurationContext):
        # Load ZCML for this package
        import gisweb.plominofieldextensions
        xmlconfig.file('configure.zcml',
                       gisweb.plominofieldextensions,
                       context=configurationContext)


    def setUpPloneSite(self, portal):
        applyProfile(portal, 'gisweb.plominofieldextensions:default')

GISWEB_PLOMINOFIELDEXTENSIONS_FIXTURE = GiswebPlominofieldextensions()
GISWEB_PLOMINOFIELDEXTENSIONS_INTEGRATION_TESTING = \
    IntegrationTesting(bases=(GISWEB_PLOMINOFIELDEXTENSIONS_FIXTURE, ),
                       name="GiswebPlominofieldextensions:Integration")