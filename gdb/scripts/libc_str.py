# -*- coding: utf-8 -*-

import gdb

# get binary process pid
from proc_pid import proc_pid
# get binary full path
from bin_path import bin_path
# strings libc module
from strings import strings


# find specific string in libc
class libc_str(gdb.Command):

    def __init__(self):
        super(libc_str, self).__init__ ("libc_str", gdb.COMMAND_SUPPORT, gdb.COMPLETE_NONE)


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

            if (len(arg.strip()) == 0): raise Exception('please give a string!')

            l_str = strings(gdb, f_path)
            r = l_str.find(arg.strip())

            if ( not r ):
                print('Not Found!')
            else:
                print('\n'.join(r))


        except Exception as e:  print('Error Occurred: {}'.format(str(e)))
            

libc_str()
