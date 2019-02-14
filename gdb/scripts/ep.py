# -*- coding: utf-8 -*-

import gdb

# color object
from color import color
# get ep model
from ep_obj import ep_obj


# get binary's entry point & text head
class ep(gdb.Command):

    def __init__(self):
        super(ep, self).__init__ ("ep", gdb.COMMAND_SUPPORT, gdb.COMPLETE_NONE)


    def invoke(self, arg, tty):
        try:
            ep_o = ep_obj()
            ep, text_head = ep_o.get_ep(gdb)

            col_obj = color()

            print ('Entry Point: {}{}{}'.format(col_obj.green, ep, col_obj.dft))
            print ('.text Head: {}{}{}'.format(col_obj.green, text_head, col_obj.dft))


        except Exception as e:  print('Error Occurred: {}'.format(str(e)))
            

ep()
