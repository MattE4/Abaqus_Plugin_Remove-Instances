from __future__ import print_function
from abaqus import *
from abaqusConstants import *



def del_insts(
kw_instances=None,
kw_box1=None,
kw_box2=None,
kw_parts=None):


    #print '\n\n----control output----'
    #print kw_instances
    #print kw_box1
    #print kw_box2
    #print kw_parts  #=False/True  

    
    vpName = session.currentViewportName
    modelName = session.sessionState[vpName]['modelName']
    
    a = mdb.models[modelName].rootAssembly
    session.viewports[vpName].disableColorCodeUpdates()

    ##########################################################################################
    # check if selection is valid
   
    if kw_instances == None:
        #print '\nError: Select instance(s) and confirm selection before pressing Apply or OK'
        #raise KeyError('No confirmed selection!!!')
        getWarningReply(message='No instance(s) selected and confirmed!', buttons=(CANCEL,))
        return

    
    ##########################################################################################
    # get instances and parts to use
    
    all_instances = a.instances.keys()


    # remove already suppressed instances
    active_instances = all_instances[:]
    for i in all_instances:
        if len(a.instances[str(i)].vertices) == 0:
            active_instances.remove(i)

    
    # instances to work with
    selected = []
    for i in kw_instances:
        selected.append(i.name)

    unselected = active_instances[:]    
    for i in selected:
        unselected.remove(i)

    # instances to be used finally
    if kw_box2 == 'Remove selected':
        use_instances = selected[:]
    else:
        use_instances = unselected[:]

    
    # parts of the instances that are used
    if (kw_parts==True) and (kw_box1=='Delete'):
        selected_parts = []
        for i in use_instances:
            if a.instances[i].partName not in selected_parts:
                selected_parts.append(a.instances[i].partName)

    ##########################################################################################
    # delete or suppress instances

    if kw_box1 == 'Delete':
        for i in use_instances:
            del a.features[str(i)]
        print('\nDeleted '+str(len(use_instances))+' instance(s)')
    else:
        for i in use_instances:
            a.features[str(i)].suppress()
        print('\nSuppressed '+str(len(use_instances))+' instance(s)')
    
    a.regenerate()
    session.viewports[vpName].enableColorCodeUpdates()
    session.viewports[vpName].forceRefresh()
    
    
    ###############################################################################################
    # get and delete unused parts
    
    if (kw_parts==True) and (kw_box1=='Delete'):
    
        unused_parts = selected_parts[:]
        for i in a.instances.keys():
            if a.instances[i].partName in unused_parts:
                unused_parts.remove(a.instances[i].partName)
        #print unused_parts
        

        for i in unused_parts:
            del mdb.models[modelName].parts[i]
        print('Deleted '+str(len(unused_parts))+' part(s)')