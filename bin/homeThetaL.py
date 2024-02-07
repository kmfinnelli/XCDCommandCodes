#!/usr/bin/python3

from quickAssign import sendcommand, writeXCD2
from quickReport import readback
import sys
import time
from variableDictionaryXCD2 import varInterfaceAddresses as ADDR
from variableDictionaryXCD2 import varStatusValues as STAT
from variableDictionaryXCD2 import varThetaLCommands as COMM
#import random #for testing

#tuning settings
sleeptime=0.5 #in seconds
debug=False



def _reverseLookup(dict,val):
    #set up the reverse dictionary
    reverse_mapping={v: k for k, v in dict.items()}
    try:
        key=reverse_mapping[val]
    except KeyError as e:
        print("reverse lookup failed.  KeyError: %s"%(e))
        sys.exit()
    return key


#check args

if len(sys.argv) != 1: #note that sys.argv has arg 1 as the command itself
    print("NOT EXECUTED. Wrong number of arguments.  Correct usage is ./homeThetaL.py")
    sys.exit()
#if wrong arguments, exit with explanation

#check if controller is busy.  If so, exit with explanation
if debug:
    print("homeThetaL:  Check status:")
status=readback(ADDR['STATUS'])

if status!=0:
    print("NOT EXECUTED. Controller status is not 0.")
    sys.exit()


sendcommand(COMM['HOME'],0) # this sleeps until it sees the status change from new_command

#monitor the controller position and report at intervals of sleeptime
if debug:
    print("homeThetaL:  Check position:");
position=readback(ADDR['FPOS'])
if debug:
    print("homeThetaL:  Check status:");
status=STAT['BUSY']
while status==STAT['BUSY']:
    status=readback(ADDR['STATUS'])
    hardstop1=readback(ADDR['HARD_STOP1'])
    hardstop2=readback(ADDR['HARD_STOP2'])
    home=readback(ADDR['HOME'])
    print("position:",readback(ADDR['FPOS'])," status:",status, "lb:",hardstop1, "hb:",hardstop2, "posi:",home)

    if debug:
        print ("homeThetaL: loop: check status:")
    time.sleep(sleeptime)

#loop until controller busy flag is cleared

#report final position and success
if debug:
     print ("homeThetaL: finishing up.  check status and readback:")


position=readback(ADDR['FPOS'])   
print("Setting POSI position to zero and updating onboard hardstops.  POSI Offset was %s from previous home"%(home))
writeXCD2([ADDR['FPOS'], position-home])
writeXCD2([ADDR['HARD_STOP1'], hardstop1-home])
writeXCD2([ADDR['HARD_STOP2'],hardstop2-home])

lb=readback(ADDR['HARD_STOP1'])
hb=readback(ADDR['HARD_STOP2'])
position=readback(ADDR['FPOS'])   
turns=readback(ADDR['TURNS'])
axis=readback(ADDR['XAXIS'])   


if status==STAT['READY']:
    print("SUCCESS. homeThetaL complete. status: %s (%s) position:%1.6f axis:%s turns:%s lb:%1.5f hb:%1.5f home(before):%1.5f"%(status,_reverseLookup(STAT,status),position,axis, turns,lb,hb, home))
else:
    print("FAIL. homeThetaL failed. status: %s (%s) position:%1.6f axis:%s turns:%s lb:%1.5f hb:%1.5f home(before):%1.5f"%(status,_reverseLookup(STAT,status),position,axis, turns,lb,hb,home))
