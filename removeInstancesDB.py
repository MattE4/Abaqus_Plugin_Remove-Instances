from abaqusConstants import *
from abaqusGui import *
from kernelAccess import mdb, session
import os

thisPath = os.path.abspath(__file__)
thisDir = os.path.dirname(thisPath)


###########################################################################
# Class definition
###########################################################################

class RemoveInstancesDB(AFXDataDialog):

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def __init__(self, form):

        # Construct the base class.
        #

        AFXDataDialog.__init__(self, form, 'Remove Instances',
            self.OK|self.APPLY|self.CANCEL, DIALOG_ACTIONS_SEPARATOR)
            

        okBtn = self.getActionButton(self.ID_CLICKED_OK)
        okBtn.setText('OK')
            

        applyBtn = self.getActionButton(self.ID_CLICKED_APPLY)
        applyBtn.setText('Apply')
            
        pickHf = FXHorizontalFrame(p=self, opts=0, x=0, y=0, w=0, h=0,
            pl=0, pr=0, pt=0, pb=0, hs=DEFAULT_SPACING, vs=DEFAULT_SPACING)
        # Note: Set the selector to indicate that this widget should not be
        #       colored differently from its parent when the 'Color layout managers'
        #       button is checked in the RSG Dialog Builder dialog.
        pickHf.setSelector(99)
        label = FXLabel(p=pickHf, text='Select Instances: ' + ' (None)', ic=None, opts=LAYOUT_CENTER_Y|JUSTIFY_LEFT)
        pickHandler = RemoveInstancesDBPickHandler(form, form.kw_instancesKw, 'Select instances', INSTANCES, MANY, label)
        icon = afxGetIcon('select', AFX_ICON_SMALL )
        FXButton(p=pickHf, text='\tPick Items in Viewport', ic=icon, tgt=pickHandler, sel=AFXMode.ID_ACTIVATE,
            opts=BUTTON_NORMAL|LAYOUT_CENTER_Y, x=0, y=0, w=0, h=0, pl=2, pr=2, pt=1, pb=1)
        GroupBox_1 = FXGroupBox(p=self, text='Method', opts=FRAME_GROOVE|LAYOUT_FILL_X)
        FXRadioButton(p=GroupBox_1, text='Delete', tgt=form.kw_box1Kw1, sel=113)
        FXRadioButton(p=GroupBox_1, text='Suppress', tgt=form.kw_box1Kw1, sel=114)
        GroupBox_2 = FXGroupBox(p=self, text='Selection usage', opts=FRAME_GROOVE|LAYOUT_FILL_X)
        FXRadioButton(p=GroupBox_2, text='Remove selected', tgt=form.kw_box2Kw1, sel=115)
        FXRadioButton(p=GroupBox_2, text='Remove unselected', tgt=form.kw_box2Kw1, sel=116)
        FXCheckButton(p=self, text='Delete unused parts', tgt=form.kw_partsKw, sel=0)
        HFrame_1 = FXHorizontalFrame(p=self, opts=0, x=0, y=0, w=0, h=0,
            pl=0, pr=200, pt=0, pb=0)
        l = FXLabel(p=self, text='Selection confirmed?', opts=JUSTIFY_LEFT)
        HFrame_2 = FXHorizontalFrame(p=self, opts=0, x=0, y=0, w=0, h=0,
            pl=0, pr=200, pt=0, pb=0)



###########################################################################
# Class definition
###########################################################################

class RemoveInstancesDBPickHandler(AFXProcedure):

        count = 0

        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        def __init__(self, form, keyword, prompt, entitiesToPick, numberToPick, label):

                self.form = form
                self.keyword = keyword
                self.prompt = prompt
                self.entitiesToPick = entitiesToPick # Enum value
                self.numberToPick = numberToPick # Enum value
                self.label = label
                self.labelText = label.getText()

                AFXProcedure.__init__(self, form.getOwner())

                RemoveInstancesDBPickHandler.count += 1
                self.setModeName('RemoveInstancesDBPickHandler%d' % (RemoveInstancesDBPickHandler.count) )

        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        def getFirstStep(self):

                return  AFXPickStep(self, self.keyword, self.prompt, 
                    self.entitiesToPick, self.numberToPick, sequenceStyle=TUPLE)

        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        def getNextStep(self, previousStep):

                self.label.setText( self.labelText.replace('None', 'Picked') )
                return None
