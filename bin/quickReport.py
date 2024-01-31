#!/usr/bin/python3
import time
from xcdSerial import sendline
from variableDictionaryXCD2 import varDict
from variableDictionaryXCD2 import varInterfaceAddresses as ADDR
from variableDictionaryXCD2 import varStatusValues as STAT
import sys
import struct

debug=False
port='/dev/ttyUSB0'


def readback(arg):
    #returns the value using the controller variable naming scheme
    check,ret = reportXCD2([arg])
    if check==False:
        print("CRITICAL FAILURE. Communication error.")
        sys.exit()
    if debug:
        print("_readback result: ", ret[0])
    return ret[0]


def getAxis():
    stat,ret =reportXCD2noAxis(['XAXIS'])
    return int(ret[0])

def reportXCD2( argv ):
    if argv:
        if len(argv) > 10:
            print("Too many variables trying to be assigned.  Max 10 variables can be assigned at once.")
            return False, 0

        var_names = argv
        if debug:
            print(var_names)
        
        #getAxis = reportXCD2noAxis(['XAXIS'])[0]

        ax_int = getAxis()
        #int(getAxis)
        #print("reportXCD2 axis=",ax_int)
        ax_byte = ax_int.to_bytes(1,byteorder='little',signed=True)
        ax_comm = [int(ax_byte[0])]
        
        command = [228, 165, 0, 213, 0, 0, 6, 132]
        count = 0
        for i in range(0, len(var_names)):
            var = var_names[i]


            if var in varDict.keys():
                var_num = varDict[var]
                u2 = var_num.to_bytes(2,byteorder='little',signed=False)
                var_command = [int(u2[0]), int(u2[1])]
                command += var_command
                count += 2
            else:
                print("Variable name - ", var , " -  not recognized. Variable list given as:")
                print(varDict.keys())
                return False, 0
            
            command += ax_comm
            count += 1

    else:
        print("No arguments given. reportXCD2 parameters are: \n \
               1) Variable- Mandatory, variable to report value of. For full list of variables, refer to variableDictionary. \n \
               2-10) Variable - Optional, other variables to report. \
               ")
        return False, 0

    # reassign packet length and block length bytes
    command[4] = int(count+6)
    command[5] = int(count+3)
    # add stop byte
    command += [218]
    if debug:
        print(command)

    # the next portion of code is what establishes communication with the controller
    # and sends the bytestring command by serial comm
    # and returns a pair of [succeeded,readbackline]
    return sendline(port,command)


def reportXCD2noAxis( argv ):
    if argv:
        if len(argv) > 10:
            print("Too many variables trying to be assigned.  Max 10 variables can be assigned at once.")
            return False, 0

        var_names = argv
        if debug:
            print(var_names)

        command = [228, 165, 0, 213, 0, 0, 6, 4]
        count = 0
        for i in range(0, len(var_names)):
            var = var_names[i]

            if var in varDict.keys():
                var_num = varDict[var]
                u2 = var_num.to_bytes(2,byteorder='little',signed=False)
                var_command = [int(u2[0]), int(u2[1])]
                command += var_command
                count += 2
            else:
                print("Variable name - " , var , " -  not recognized. Variable list given as:")
                print(varDict.keys())
                return False, 0

    else:
        print("No arguments given. reportXCD2 parameters are: \n \
               1) Variable- Mandatory, variable to report value of. For full list of variables, refer to variableDictionary. \n \
               2-10) Variable - Optional, other variables to report. \
               ")
        return False, 0

    # reassign packet length and block length bytes
    command[4] = int(count+6)
    command[5] = int(count+3)
    # add stop byte
    command += [218]
    if debug:
        print(command)

    # the next portion of code is what establishes communication with the controller
    # and sends the bytestring command by serial comm
    return sendline(port,command)



if __name__ == "__main__":
    debug=True
    reportXCD2(sys.argv[1:])
