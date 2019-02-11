# -*- coding: utf-8 -*-

import gdb

# get binary process pid
from proc_pid import proc_pid
# get binary full path
from bin_path import bin_path
# file info model
from file_info import file_info
# merge linux_map and gdb_map and gdb_files model
from adv_map_obj import adv_map_obj



# show advance memory map
class adv_map(gdb.Command):

    def __init__(self):
        super(adv_map, self).__init__ ("adv_map", gdb.COMMAND_SUPPORT, gdb.COMPLETE_NONE)


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


            full_map = adv_map_obj().get_map(gdb, pid, bit, f_path)

            if (not full_map): raise Exception('parse information error')
            print('\n'.join(full_map))
            

        except Exception as e:  print('Error Occurred: {}'.format(str(e)))
            

adv_map()
