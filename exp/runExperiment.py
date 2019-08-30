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

    # get participant number and set random seed:
    cfg = getParticipant(cfg, individualStimOrder=True)

    # create Window object and home, cursor, target, and aiming arrow
    cfg = createEnvironment(cfg)

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

    return(cfg)

def cleanlyExit(cfg):

    # still need to store data...
    print('no data stored on call to exit function...')


    cfg['win'].close()

    return(cfg)












runExp()
