# -*- coding: utf-8 -*-

import gdb

# color object
from color import color
# get binary process pid
from proc_pid import proc_pid
# get binary full path
from bin_path import bin_path
# file info module
from file_info import file_info
# linux process map parse module
from linux_map import linux_map
# ldd module
from ldd import ldd


# list current used libc & libc base
class libc(gdb.Command):

    def __init__(self):
        super(libc, self).__init__ ("libc", gdb.COMMAND_SUPPORT, gdb.COMPLETE_NONE)


    # check program is running or not
    def init(self):
        pid = proc_pid().get_pid(gdb)
        if (not pid): return False
       
        f_path = bin_path().get_path(gdb)
        if (not f_path): return False

        return pid, f_path

    
    def get_libc_base(self, l_map, bit):
        idx = False
        libc_base = 'null'

        if ( bit == '64'):
            idx = 3
            libc_base = hex(int(l_map[idx]['str_addr'], 16))
        elif ( bit == '32'):
            idx = 4
            libc_base = hex(int(l_map[idx]['str_addr'], 16))
        
        return libc_base, idx
    
    
    def invoke(self, arg, tty):
        try:
            if (not self.init()):
                raise Exception('process is not running!')
            else:
                pid, f_path = self.init()

            f_info = file_info(f_path)
            arch = f_info.get_arch()
            bit = f_info.get_bit()
            del f_info


            l_map = linux_map(bit)
            l_map = l_map.parse(pid)

            col_obj = color()

            libc_base, libc_text_idx = self.get_libc_base(l_map, bit)
            if (len(libc_base.strip()) == 0): raise Exception('could not get libc path!')
            del l_map

            libc = ldd(gdb, f_path).get_libc()

            print('libc: {}{}{}'.format(col_obj.purple, libc, col_obj.dft))
            print('libc base: {}{}{}'.format(col_obj.purple, libc_base, col_obj.dft))

        except Exception as e:  print('Error Occurred: {}'.format(str(e)))
            

libc()
