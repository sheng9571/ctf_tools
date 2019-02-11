# -*- coding: utf-8 -*-

import gdb

# get binary process pid
from proc_pid import proc_pid
# get binary full path
from bin_path import bin_path
# file info model
from file_info import file_info
# merge linux_map and gdb_map model
from map_obj import map_obj


# show memory map
class map(gdb.Command):

    def __init__(self):
        super(map, self).__init__ ("map", gdb.COMMAND_SUPPORT, gdb.COMPLETE_NONE)


    # check program is running or not
    def init(self):
        pid = proc_pid().get_pid(gdb)
        if (not pid): return False
       
        f_path = bin_path().get_path(gdb)
        if (not f_path): return False

        return pid, f_path


    # address padding
    def addr_pad(self, pad, t): return t.rjust(pad * 2, '0')


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

            merged_map = map_obj().get_map(gdb, bit, pid)

            # length of two maps must the same
            if (not merged_map): raise Exception('length of two types of map is different!!!')

            print('\n'.join(merged_map))
            del merged_map


        except Exception as e:  print('Error Occurred: {}'.format(str(e)))
            

map()
