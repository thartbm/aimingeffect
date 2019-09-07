#!/usr/bin/env python
# -*- coding: utf-8 -*-

# this experiment is written to be run in Python 3

from psychopy import event, visual
#from psychopy.hardware import keyboard
from pyglet.window import key
import random
import time
import scipy as sp
import pandas as pd
import os
import glob
import sys

def runExp():

    cfg = {}

    cfg['expstart'] = time.time()

    # get participant number and set random seed:
    cfg = getParticipant(cfg, individualStimOrder=True)

    # create Window object and home, cursor, target, and aiming arrow
    # and a self-define mouse object
    cfg = createEnvironment(cfg)

    # add all the tasks
    cfg = createTasks(cfg)

    # run the actual experiment, catch errors to cleanly exit:
    try:

        doTasks(cfg)

    except Exception as err:

        # what went wrong?
        print(err)

    finally:

        cfg = cleanlyExit(cfg)




def getParticipant(cfg, individualStimOrder=True):

    GroupNotANumber = True

    # and we will only be happy when this is the case:
    while (GroupNotANumber):
        # we ask for input:
        print('1: non-instructed\n2: instructed\n3: aiming\n4: early PDP\n5: early aiming')
        group = input('Enter group number: ')
        # and try to see if we can convert it to an integer
        try:
            groupno = int(group)
            # and if that integer really reflects the input
            if (group == '%d'%(groupno)):
                # and is a number 1, 2, 3, 4, or 5...
                if (groupno in [1,2,3,4,5]):
                    # only then are we satisfied:
                    GroupNotANumber = False
                    # and store this in the cfg
                    cfg['groupno'] = groupno
                    cfg['groupname'] = ['non-instructed','instructed','aiming','early_PDP','early_aiming'][groupno-1]
        except Exception as err:
            # if it all doesn't work, we ask for input again...
            print(err)
            pass

    # we need to get an integer number as participant ID:
    IDnotANumber = True

    # and we will only be happy when this is the case:
    while (IDnotANumber):
        # we ask for input:
        ID = input('Enter participant number: ')
        # and try to see if we can convert it to an integer
        try:
            IDno = int(ID)
            # and if that integer really reflects the input
            if (ID == '%d'%(IDno)):
                # only then are we satisfied:
                IDnotANumber = False
                # and store this in the cfg
                cfg['ID'] = IDno
        except:
            # if it all doesn't work, we ask for input again...
            pass

    # set up folder's for groups and participants to store the data
    for thisPath in ['data', 'data/%s'%(cfg['groupname']), 'data/%s/p%03d'%(cfg['groupname'],cfg['ID'])]:
        if os.path.exists(thisPath):
            if not(os.path.isdir(thisPath)):
                sys.exit('"%s" should be a folder'%(thisPath))
        else:
            os.mkdir(thisPath)

    # we need to seed the random number generator one way or another...

    # should this depend on participant number?
    if individualStimOrder:
        random.seed(1243 * 1977 * IDno)
    else:
        # or not?
        random.seed(1977 * 1977)

    return cfg

def createEnvironment(cfg):

    cfg['homepos'] = [0,0]

    cfg['targetangles'] = [((ta+22.5)/180)*sp.pi for ta in list(range(0,360,45))]

    # need to check if the folder for data is there:
    if not(os.path.isdir('data%s'%os.path.sep)):
        # when the folder does not exist, we create it:
        os.mkdir('data')

    # instantiate a window object:
    #cfg['win'] = visual.Window(fullscr=False, units='pix', waitBlanking=True, viewScale=[0.72,0.72], color=[-1,-1,-1])
    cfg['win'] = visual.Window(fullscr=True, units='pix', waitBlanking=True, viewScale=[0.72,0.72], color=[-1,-1,-1])

    # set up the workspace as a function of the size of the window:
    winSize = cfg['win'].size

    # we want 8 cm reaches
    # if we apply the viewscale correctly, that should be possible
    # leaving 3.375/2 cm free on top and bottom
    # the monitor on the tablet setup is 1680 pixels wide,
    # and that should span 31 cm on the tablet surface

    PPC = max(winSize)/31.

    cfg['NSU'] = PPC * 8

    cfg['targetdistance'] = cfg['NSU']

    cfg['radius'] = cfg['NSU']*0.05

    # set up visual objects for use in experiment:
    cfg['home'] = visual.Circle(win=cfg['win'], pos=cfg['homepos'], radius=cfg['radius'], lineWidth=cfg['radius']/5, lineColorSpace='rgb', lineColor='#999999', fillColorSpace='rgb', fillColor=None)

    cfg['cursor'] = visual.Circle(win=cfg['win'], radius=cfg['radius'], lineWidth=cfg['radius']/5, lineColorSpace='rgb', lineColor='#999999', fillColorSpace='rgb', fillColor='#999999')

    cfg['target'] = visual.Circle(win=cfg['win'], radius=cfg['radius'], lineWidth=cfg['radius']/5, lineColorSpace='rgb', lineColor='#999999', fillColorSpace='rgb', fillColor=None)

    cfg['instruction'] = visual.TextStim(win=cfg['win'], text='', pos=[0,0], colorSpace='rgb', color='#999999', flipVert=True)

    arrowvertices = ((-.33,-.33),(4.33,-.33),(4,-1),(6,0),(4,1),(4.33,.33),(-.33,.33))
    cfg['aim_arrow'] = visual.ShapeStim(win=cfg['win'], lineWidth=0, lineColorSpace='rgb', lineColor='#CC00CC', fillColorSpace='rgb', fillColor='#CC00CC', vertices=arrowvertices, closeShape=True, size=cfg['NSU']*(0.2/6))

    arrowvertices = ((-.4,-.4),(.8,0),(-.4,.4),(0,0))
    cfg['home_arrow'] = visual.ShapeStim(win=cfg['win'], lineWidth=1, lineColorSpace='rgb', lineColor='#999999', fillColorSpace='rgb', fillColor='#999999', vertices=arrowvertices, closeShape=True, size=cfg['radius'])

    # set up 'mouse' object to track reaches:
    class myMouse:

        def __init__(self,cfg):
            # we use a psychopy mouse object
            self.psyMouse = event.Mouse(visible = False, newPos = None, win = cfg['win'])

        def getPos(self):
            # but in addition to the position, we also return the time the position was asked for
            [X,Y] = self.psyMouse.getPos()
            return [X,Y,time.time()]

    cfg['mouse'] = myMouse(cfg)

    # we use a pygame keyboard object for the aiming task responses,
    # as we need continuous key-down status
    cfg['keyboard'] = key.KeyStateHandler()
    cfg['win'].winHandle.push_handlers(cfg['keyboard'])

    return(cfg)

def cleanlyExit(cfg):

    # still need to store data...
    print('no data stored on call to exit function...')


    cfg['win'].close()

    return(cfg)


def createTasks(cfg):

    # we'll put all the tasks in a list, so we can do them one by one:
    tasks = []

    targets = [ta+22.5 for ta in list(range(0,360,45))]
    cfg['targets'] = targets

    groupno = cfg['groupno']

    # depending on participant number the tasks will be determined
    # or should we ask for group/condition on start-up?

    # first aligned training
    # 32 trials?

    tasktrials = [32,8,16,8]
    taskrotation = [0,0,0,0]
    taskaiming = [False,False,False,False]
    taskcursor = [True,False,True,False]
    taskstrategy = ['NA',None,'NA',None]
    taskinstructions = ['reach for target',
                        'reach without cursor',
                        'reach for target',
                        'reach without cursor']
    if groupno == 3:
        taskaiming = [True,False,True,False]
        taskinstructions[0] = 'aim and reach for target'
        taskinstructions[2] = 'aim and reach for target'
    if groupno == 5:
        taskaiming = [False,False,True,False]
        taskinstructions[2] = 'aim and reach for target'


    for taskno in range(len(tasktrials)):

        ttargets, trotation, taiming, tcursor, tstrategy = [], [], [], [], []

        for iter in range(int(tasktrials[taskno]/len(targets))):
            random.shuffle(targets)
            ttargets = ttargets + targets
            trotation = trotation + list(sp.repeat(taskrotation[taskno],len(targets)))
            taiming = taiming + list(sp.repeat(taskaiming[taskno],len(targets)))
            tcursor = tcursor + list(sp.repeat(taskcursor[taskno],len(targets)))
            tstrategy = tstrategy + list(sp.repeat(taskstrategy[taskno],len(targets)))

        taskdict = {'target':ttargets,'rotation':trotation,'aiming':taiming,'cursor':tcursor,'instruction':taskinstructions[taskno],'strategy':tstrategy}
        tasks.append(taskdict)

    # first aligned no-cursor
    # 8 trials

    # second aligned training
    # 16 trials (with aiming for group 4?)

    # second aligned no-cursor
    # 8 trials

    # ===== break? =====
    # potentially tell experimentor to give instructions

    # first rotated training
    # 80 (groups 1, 2, and 3) or 8 trials (groups 4 and 5)

    # first rotated PDP (group 1, 2, 3 and 5) or block of aiming trials (group 4)
    # 8 (group 4) or 16 trials (group 1, 2, 3 and 5)?

    # second rotated training
    # 16 trials (groups 1, 2 and 3)
    # 72 trials (groups 4 and 5)

    # second rotated PDP (all groups)
    # 16 trials

    #

    cfg['tasks'] = tasks

    return(cfg)


def doTasks(cfg):

    cfg['totrialno'] = 0

    for taskno in list(range(len(cfg['tasks']))):

        cfg['taskno'] = taskno

        cfg = showInstruction(cfg)

        task = cfg['tasks'][taskno]

        for trialno in list(range(len(task['target']))):

            cfg['trialno'] = trialno

            cfg = doTrial(cfg)

            cfg['totrialno'] += 1

    print(cfg['totrialno'])

    # at the end of all tasks, combine into one dataset (csv)

    return(cfg)

def showInstruction(cfg):

    instruction = cfg['tasks'][cfg['taskno']]['instruction']

    if (len(instruction)):

        cfg['instruction'].text = instruction

        event.clearEvents()

        waitingForSpace = True

        while waitingForSpace:

            keys = event.getKeys(keyList=['space'])

            if ('space' in keys):

                waitingForSpace = False

            cfg['instruction'].draw()
            cfg['win'].flip()



    return(cfg)

def doTrial(cfg):

    # set up the target:
    targetangle_deg = cfg['tasks'][cfg['taskno']]['target'][cfg['trialno']]
    targetangle = (targetangle_deg/180)*sp.pi
    targetpos = [sp.cos(targetangle)*cfg['targetdistance'], sp.sin(targetangle)*cfg['targetdistance']]
    cfg['target'].pos = targetpos

    # phase 0: do pre-reach aiming if required:
    if cfg['tasks'][cfg['taskno']]['aiming'][cfg['trialno']]:

        cfg = doAiming(cfg)
        aim = cfg['aim']

    else:

        # if not required: set to correct value for data file:
        aim = sp.NaN

    # trials need to know whether or not there is a cursor
    showcursor = cfg['tasks'][cfg['taskno']]['cursor'][cfg['trialno']]

    # for trials with / without strategy, we should record that:
    usestrategy = cfg['tasks'][cfg['taskno']]['strategy'][cfg['trialno']]

    # set up rotation matrix for current rotation:
    rotation = cfg['tasks'][cfg['taskno']]['rotation'][cfg['trialno']]
    theta = (rotation/180.)*sp.pi
    R = sp.array([[sp.cos(theta),-1*sp.sin(theta)],[sp.sin(theta),sp.cos(theta)]],order='C')


    trialDone = False
    phase = 1

    # create lists to store data in:
    mouseX = []
    mouseY = []
    cursorX = []
    cursorY = []
    time_s = []


    while not(trialDone):

        [X,Y,T] = cfg['mouse'].getPos()

        cursorpos = list(R.dot(sp.array([[X],[Y]])).flatten())
        cfg['cursor'].pos = cursorpos
        cursorangle = sp.arctan2(cursorpos[1],cursorpos[0])

        mouseX.append(X)
        mouseY.append(Y)
        cursorX.append(cursorpos[0])
        cursorY.append(cursorpos[1])
        time_s.append(T)

        if (phase == 2):
            cfg['target'].draw()
            if showcursor:
                cfg['cursor'].draw()
                if ( sp.sqrt( sp.sum( (sp.array(cursorpos) - sp.array(targetpos))**2 ) ) ) < cfg['radius']:
                    phase = 3
            else:
                #print('no-cursor, phase 2')
                idx = sp.argmin( abs( sp.array(time_s)+0.250-time_s[-1] ) )
                if ( sp.sqrt(mouseX[-1]**2 + mouseY[-1]**2) ) > (cfg['NSU']*.5):
                    distance = sp.sum( sp.sqrt(sp.diff(sp.array([mouseX[idx:]]))**2 + sp.diff(sp.array([mouseY[idx:]]))**2) )
                    if distance < (0.01 * cfg['NSU']):
                        phase = 3

        if (phase == 1) or (phase == 3):
            cfg['home'].draw()
            if showcursor:
                cfg['cursor'].draw()
            else:
                #print('no-cursor, phase 1 or 3')
                if (sp.sqrt(sum([c**2 for c in cursorpos])) < (0.15 * cfg['NSU'])):
                    cfg['cursor'].draw()
                else:
                    # put arrow in home position
                    grain = (2*sp.pi)/8
                    arrowangle = (((cursorangle-(grain/2)) // grain) * grain) + grain
                    cfg['home_arrow'].ori = ((-1 * arrowangle)/sp.pi)*180
                    cfg['home_arrow'].draw()
            #print([sp.sqrt(sp.sum(sp.array(cursorpos)**2)), (0.025 * cfg['NSU'])])
            if (sp.sqrt(sp.sum(sp.array(cursorpos)**2)) < cfg['radius']):
                if phase == 1:
                    phase = 2
                if phase == 3:
                    trialDone = True

        #cfg['target'].draw()
        cfg['win'].flip()

        if cfg['keyboard'][key.ESCAPE]:
            sys.exit('escape key pressed')

    # make data frame and store as csv file...

    nsamples = len(time_s)

    task_idx = [cfg['taskno']+1] * nsamples
    trial_idx = [cfg['trialno']+1] * nsamples
    cutrial_no = [cfg['totrialno']+1] * nsamples
    doaiming_bool = [cfg['tasks'][cfg['taskno']]['aiming'][cfg['trialno']]] * nsamples
    showcursor_bool = [showcursor] * nsamples
    # includestrategy_cat !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    usestrategy_cat = [usestrategy] * nsamples
    targetangle_deg = [targetangle_deg] * nsamples
    targetx = [targetpos[0]] * nsamples
    targety = [targetpos[1]] * nsamples

    cutime_ms = [int((t - cfg['expstart']) * 1000) for t in time_s]
    time_ms = [t - cutime_ms[0] for t in cutime_ms]

    aim_deg = [aim] * nsamples
    if sp.isnan(aim):
        aimdeviation_deg = aim_deg
    else:
        aimdeviation_deg = [(aim - targetangle_deg[0]) % 360] * nsamples

    # put all lists in dictionary:
    trialdata = {'task_idx':task_idx, 'trial_idx':trial_idx, 'cutrial_no':cutrial_no, 'doaiming_bool':doaiming_bool, 'showcursor_bool':showcursor_bool, 'usestrategy_cat':usestrategy_cat, 'targetangle_deg':targetangle_deg, 'targetx':targetx, 'targety':targety, 'cutime_ms':cutime_ms, 'time_ms':time_ms, 'mousex':mouseX, 'mousey':mouseY, 'cursorx':cursorX, 'cursory':cursorY, 'aim_deg':aim_deg, 'aimdeviation_deg':aimdeviation_deg}

    # make dictionary into data frame:
    trialdata = pd.DataFrame(trialdata)

    # store data frame:
    filename = 'data/%s/p%03d/task%02d-trial%04d.csv'%(cfg['groupname'],cfg['ID'],cfg['taskno']+1,cfg['trialno']+1)
    trialdata.to_csv( filename, index=False, float_format='%0.5f' )


    return(cfg)


def doAiming(cfg):

    cfg['target'].draw()
    cfg['aim_arrow'].ori = -1 * cfg['tasks'][cfg['taskno']]['target'][cfg['trialno']]
    cfg['aim_arrow'].draw()
    cfg['win'].flip()

    aimDecided = False

    event.clearEvents()

    while(not(aimDecided)):

        keys = event.getKeys(keyList=['num_enter'])
        if ('num_enter' in keys):
            cfg['aim'] = -1 * cfg['aim_arrow'].ori
            aimDecided = True

        if cfg['keyboard'][key.NUM_LEFT]:
            cfg['aim_arrow'].ori = cfg['aim_arrow'].ori - 1
            #print(cfg['aim_arrow'].ori)
        if cfg['keyboard'][key.NUM_RIGHT]:
            cfg['aim_arrow'].ori = cfg['aim_arrow'].ori + 1
            #print(cfg['aim_arrow'].ori)
        #print(cfg['keyboard'])
        cfg['aim_arrow'].ori = cfg['aim_arrow'].ori % 360


        cfg['target'].draw()
        cfg['aim_arrow'].draw()
        cfg['win'].flip()

    #if (cfg['aim'] < 0) or (cfg['aim'] > 360):
    cfg['aim'] = cfg['aim'] % 360

    #print(cfg['tasks'][cfg['taskno']]['target'][cfg['trialno']])
    #print(cfg['aim'])


    return(cfg)


runExp()
