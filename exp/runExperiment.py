#!/usr/bin/env python
# -*- coding: utf-8 -*-

# this experiment is written to be run in Python 3

from psychopy import event, visual
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
                    cfg['group'] = groupno
        except:
            # if it all doesn't work, we ask for input again...
            pass
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
    cfg['win'] = visual.Window(fullscr=False, units='pix', waitBlanking=True, viewScale=[2/3,-2/3])

    cfg['home'] = visual.Circle(win=cfg['win'], pos=cfg['homepos'], radius=50, lineWidth=2, lineColorSpace='rgb', lineColor='#999999', fillColorSpace='rgb', fillColor=None)

    cfg['cursor'] = visual.Circle(win=cfg['win'], radius=50, lineWidth=2, lineColorSpace='rgb', lineColor='#999999', fillColorSpace='rgb', fillColor='#999999')

    cfg['target'] = visual.Circle(win=cfg['win'], radius=50, lineWidth=2, lineColorSpace='rgb', lineColor='#999999', fillColorSpace='rgb', fillColor=None)

    arrowvertices = ((-.5,-.5),(4,-.5),(4,-1),(5,0),(4,1),(4,.5),(-.5,.5))
    cfg['arrow'] = visual.ShapeStim(win=cfg['win'], lineWidth=2, lineColorSpace='rgb', lineColor='#CC00CC', fillColorSpace='rgb', fillColor='#CC00CC', vertices=arrowvertices, closeShape=True, size=20)

    class myMouse:

        def __init__(self,cfg):

            self.psyMouse = event.Mouse(visible = False, newPos = None, win = cfg['win'])

        def getPos(self):

            [X,Y] = self.psyMouse.getPos()
            return [X,Y,time.time()]

    cfg['mouse'] = myMouse(cfg)

    return(cfg)

def cleanlyExit(cfg):

    # still need to store data...
    print('no data stored on call to exit function...')


    cfg['win'].close()

    return(cfg)


def createTasks(cfg):

    # we'll put all the tasks in a list, so we can do them one by one:
    tasks = []

    targets = [((ta+22.5)/180)*sp.pi for ta in list(range(0,360,45))]
    cfg['targets'] = targets

    group = cfg['group']

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
    if group == 3:
        taskaiming = [True,False,True,False]
        taskinstructions[0] = 'aim and reach for target'
        taskinstructions[2] = 'aim and reach for target'
    if group == 5:
        taskaiming = [False,False,True,False]
        taskinstructions[2] = 'aim and reach for target'


    for taskno in range(len(tasktrials)):

        ttargets, trotation, taiming, tcursor = [], [], [], []

        for iter in range(int(tasktrials[taskno]/len(targets))):
            random.shuffle(targets)
            ttargets.append(targets)
            trotation.append(sp.repeat(taskrotation[taskno],len(targets)))
            taiming.append(sp.repeat(taskaiming[taskno],len(targets)))
            tcursor.append(sp.repeat(taskcursor[taskno],len(targets)))

        taskdict = {'targets':ttargets,'rotation':trotation,'aiming':taiming,'cursor':tcursor,'instruction':taskinstructions[taskno]}
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

    # loop through the cfg['tasks']
    # cfg['taskno'] = ...
    # before each task, show an instruction on the screen (if not empty)

    # tasks should be named, for easier PDP analysis

    # loop through the trials within the task
    # cfg['trialno'] = ...
    # cfg['totrialno'] = ...

    # doTrial()

    # at the end of all tasks, combine into one dataset (csv)

    return(cfg)

def doTrial(cfg):

    # trials need to know which target to use
    # trials need to know whether or not there is a cursor
    # trials need to know whether to do aiming (or a pause)

    # phase 1: get cursor on home
    # phase 2: aim (with target!) / pause (with target?)
    # phase 3: reach for target (end by reaching target or by stopping movement)
    # phase 4: return home (with cursor, or with home-arrow feedback)

    # store the data frame as csv file...

    pass


runExp()
