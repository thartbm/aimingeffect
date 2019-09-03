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

    except Exception as e:

        # what went wrong?
        print(e)

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
        except:
            # if it all doesn't work, we ask for input again...
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

    # do we need to check if the participant already exists in the group?



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

    cfg['targetdistance'] = 400

    cfg['targetangles'] = [((ta+22.5)/180)*sp.pi for ta in list(range(0,360,45))]

    # need to check if the folder for data is there:
    if not(os.path.isdir('data%s'%os.path.sep)):
        # when the folder does not exist, we create it:
        os.mkdir('data')

    # instantiate a window object:
    cfg['win'] = visual.Window(fullscr=True, units='pix', waitBlanking=True, viewScale=[0.72,-0.72], color=[-1,-1,-1])

    # set up the workspace as a function of the size of the window:
    winSize = cfg['win'].size

    cfg['NSU'] = min(winSize) * 0.75

    # set up visual objects for use in experiment:
    cfg['home'] = visual.Circle(win=cfg['win'], pos=cfg['homepos'], radius=cfg['NSU']*0.025, lineWidth=cfg['NSU']*0.005, lineColorSpace='rgb', lineColor='#999999', fillColorSpace='rgb', fillColor=None)

    cfg['cursor'] = visual.Circle(win=cfg['win'], radius=cfg['NSU']*0.025, lineWidth=cfg['NSU']*0.005, lineColorSpace='rgb', lineColor='#999999', fillColorSpace='rgb', fillColor='#999999')

    cfg['target'] = visual.Circle(win=cfg['win'], radius=cfg['NSU']*0.025, lineWidth=cfg['NSU']*0.005, lineColorSpace='rgb', lineColor='#999999', fillColorSpace='rgb', fillColor=None)

    cfg['instruction'] = visual.TextStim(win=cfg['win'], text='', pos=[0,0], colorSpace='rgb', color='#999999', flipVert=True)

    arrowvertices = ((-.33,-.33),(4.33,-.33),(4,-1),(6,0),(4,1),(4.33,.33),(-.33,.33))
    cfg['arrow'] = visual.ShapeStim(win=cfg['win'], lineWidth=cfg['NSU']*0.005, lineColorSpace='rgb', lineColor='#CC00CC', fillColorSpace='rgb', fillColor='#CC00CC', vertices=arrowvertices, closeShape=True, size=cfg['NSU']*(0.2/6))


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

        ttargets, trotation, taiming, tcursor = [], [], [], []

        for iter in range(int(tasktrials[taskno]/len(targets))):
            random.shuffle(targets)
            ttargets = ttargets + targets
            trotation = trotation + list(sp.repeat(taskrotation[taskno],len(targets)))
            taiming = taiming + list(sp.repeat(taskaiming[taskno],len(targets)))
            tcursor = tcursor + list(sp.repeat(taskcursor[taskno],len(targets)))

        taskdict = {'target':ttargets,'rotation':trotation,'aiming':taiming,'cursor':tcursor,'instruction':taskinstructions[taskno]}
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

    # do pre-reach aiming if required:
    if cfg['tasks'][cfg['taskno']]['aiming'][cfg['trialno']]:

        cfg = doAiming(cfg)

    print([targetangle,targetpos])
    # trials need to know whether or not there is a cursor
    showcursor = cfg['tasks'][cfg['taskno']]['cursor'][cfg['trialno']]


    # phase 0: aiming?
    # phase 1: get cursor on home
    # phase 2: aim (with target!) / pause (with target?)
    # phase 3: reach for target (end by reaching target or by stopping movement)
    # phase 4: return home (with cursor, or with home-arrow feedback)

    # store the data frame as csv file...

    #print(cfg['mouse'].getPos())

    cfg['target'].draw()
    cfg['win'].flip()

    return(cfg)


def doAiming(cfg):

    cfg['target'].draw()
    cfg['arrow'].ori = -1 * cfg['tasks'][cfg['taskno']]['target'][cfg['trialno']]
    cfg['arrow'].draw()
    cfg['win'].flip()

    aimDecided = False

    event.clearEvents()

    while(not(aimDecided)):

        keys = event.getKeys(keyList=['num_enter'])
        if ('num_enter' in keys):
            aim = -1 * cfg['arrow'].ori
            aimDecided = True

        #if cfg['keyboard'][key.NUM_ENTER]:
        #    # aim = -1 * cfg['arrow'].ori
        #    aimDecided = True
        if cfg['keyboard'][key.NUM_LEFT]:
            cfg['arrow'].ori = cfg['arrow'].ori - 1
        if cfg['keyboard'][key.NUM_RIGHT]:
            cfg['arrow'].ori = cfg['arrow'].ori + 1

        cfg['target'].draw()
        cfg['arrow'].draw()
        cfg['win'].flip()


    return(cfg)


runExp()
