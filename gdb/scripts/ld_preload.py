# -*- coding: utf-8 -*-

import gdb

# color object
from color import color


# alias of ld_preload in gdb
class ldp(gdb.Command):

    def __init__(self):
        super(ldp, self).__init__ ("ldp", gdb.COMMAND_SUPPORT, gdb.COMPLETE_NONE)


    def invoke(self, arg, tty):
        try:
            if (len(arg.strip()) == 0): raise Exception('please give a .so file name with it\'s path')
            col_obj = color()

            cmd = 'set environment LD_PRELOAD'
            gdb.execute(cmd, to_string = True)
            print('Set environment variable "LD_PRELOAD" to null!')

            cmd = 'set environment LD_PRELOAD {}'.format(arg)
            gdb.execute(cmd, to_string = True)
            
            cmd = 'show environment LD_PRELOAD'
            r = gdb.execute(cmd, to_string = True)
            r = r.strip().split(' = ')

            if (len(r) != 2): raise Exception('Set environment variable "LD_PRELOAD" {}failed{}!'.format(col_obj.red, col_obj.dft))

            print('Set environment variable "LD_PRELOAD" to {}{}{} {}success{}!'.format(col_obj.l_blue, r[1].strip(), col_obj.dft, col_obj.green, col_obj.dft))


        except Exception as e:  print('Error Occurred: {}'.format(str(e)))
            

ldp()
