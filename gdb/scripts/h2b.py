# -*- coding: utf-8 -*-

import gdb
import math


# convert hex to binary
class h2b(gdb.Command):

    def __init__(self):
        super(h2b, self).__init__ ("h2b", gdb.COMMAND_SUPPORT, gdb.COMPLETE_NONE)


    def invoke(self, arg, tty):
        try:
            if (len(arg.strip()) == 0): raise Exception('please give a hex number')

            target = int(arg, 16)
            target = bin(target).replace('0b', '').strip()
            target = target.rjust( 8 * math.ceil(len(target) / 8.0), '0')
            print (target)


        except Exception as e:  print('Error Occurred: {}'.format(str(e)))
            

h2b()
