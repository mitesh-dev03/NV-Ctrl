#!/usr/bin/env python3

import sys
from HostEnvironment import *

def Main():
    try:
        if(len(sys.argv) < 2):
            raise Exception("Incomplete arguments")

        Environment = HostEnvironment("./Config.xml")
        OpCode = sys.argv[1]
        if(OpCode == "Reset"):
            Environment.Reset()
        elif(OpCode == "Switch"):
            if(len(sys.argv) < 3):
                raise Exception("Incomplete arguments")
            Environment.SwitchGraphics(sys.argv[2])
        else:
            raise Exception(f"Invalid Operation: \"{OpCode}\"")
        print('Operation completed successfully')
        print('Please reboot your computer for changes to take effect')

    except Exception as Except:
        print("[Fatal] " + str(Except))

if __name__ == '__main__':
    Main()