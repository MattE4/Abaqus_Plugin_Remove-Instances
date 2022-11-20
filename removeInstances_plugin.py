from abaqusGui import *
from abaqusConstants import ALL
import osutils, os


###########################################################################
# Class definition
###########################################################################

class RemoveInstances_plugin(AFXForm):

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def __init__(self, owner):
        
        # Construct the base class.
        #
        AFXForm.__init__(self, owner)
        self.radioButtonGroups = {}

        self.cmd = AFXGuiCommand(mode=self, method='del_insts',
            objectName='delete_kernel', registerQuery=False)
        pickedDefault = ''
        self.kw_instancesKw = AFXObjectKeyword(self.cmd, 'kw_instances', TRUE, pickedDefault)
        if not self.radioButtonGroups.has_key('kw_box1'):
            self.kw_box1Kw1 = AFXIntKeyword(None, 'kw_box1Dummy', True)
            self.kw_box1Kw2 = AFXStringKeyword(self.cmd, 'kw_box1', True)
            self.radioButtonGroups['kw_box1'] = (self.kw_box1Kw1, self.kw_box1Kw2, {})
        self.radioButtonGroups['kw_box1'][2][113] = 'Delete'
        self.kw_box1Kw1.setValue(113)
        if not self.radioButtonGroups.has_key('kw_box1'):
            self.kw_box1Kw1 = AFXIntKeyword(None, 'kw_box1Dummy', True)
            self.kw_box1Kw2 = AFXStringKeyword(self.cmd, 'kw_box1', True)
            self.radioButtonGroups['kw_box1'] = (self.kw_box1Kw1, self.kw_box1Kw2, {})
        self.radioButtonGroups['kw_box1'][2][114] = 'Suppress'
        if not self.radioButtonGroups.has_key('kw_box2'):
            self.kw_box2Kw1 = AFXIntKeyword(None, 'kw_box2Dummy', True)
            self.kw_box2Kw2 = AFXStringKeyword(self.cmd, 'kw_box2', True)
            self.radioButtonGroups['kw_box2'] = (self.kw_box2Kw1, self.kw_box2Kw2, {})
        self.radioButtonGroups['kw_box2'][2][115] = 'Remove selected'
        self.kw_box2Kw1.setValue(115)
        if not self.radioButtonGroups.has_key('kw_box2'):
            self.kw_box2Kw1 = AFXIntKeyword(None, 'kw_box2Dummy', True)
            self.kw_box2Kw2 = AFXStringKeyword(self.cmd, 'kw_box2', True)
            self.radioButtonGroups['kw_box2'] = (self.kw_box2Kw1, self.kw_box2Kw2, {})
        self.radioButtonGroups['kw_box2'][2][116] = 'Remove unselected'
        self.kw_partsKw = AFXBoolKeyword(self.cmd, 'kw_parts', AFXBoolKeyword.TRUE_FALSE, True, False)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def getFirstDialog(self):

        import removeInstancesDB
        return removeInstancesDB.RemoveInstancesDB(self)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def doCustomChecks(self):

        # Try to set the appropriate radio button on. If the user did
        # not specify any buttons to be on, do nothing.
        #
        for kw1,kw2,d in self.radioButtonGroups.values():
            try:
                value = d[ kw1.getValue() ]
                kw2.setValue(value)
            except:
                pass
        return True

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def okToCancel(self):

        # No need to close the dialog when a file operation (such
        # as New or Open) or model change is executed.
        #
        return False

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Register the plug-in
#
thisPath = os.path.abspath(__file__)
thisDir = os.path.dirname(thisPath)

toolset = getAFXApp().getAFXMainWindow().getPluginToolset()
toolset.registerGuiMenuButton(
    buttonText='Tools ME|Remove Instances', 
    object=RemoveInstances_plugin(toolset),
    messageId=AFXMode.ID_ACTIVATE,
    icon=None,
    kernelInitString='import delete_kernel',
    applicableModules=['Assembly','Step','Interaction', 'Load'],
    version='1.0',
    author='Matthias Ernst, Dassault Systemes Germany',
    description='Plug-In to remove (= delete or suppress) instances from viewport. '\
                'Always confirm selection for each region with DONE button or middle mouse button before pressing Apply or OK.'\
                '\n\nThis is not an official Dassault Systemes product.',
    helpUrl='N/A'
)
