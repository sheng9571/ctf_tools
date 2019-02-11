# -*- coding: utf-8 -*-

import gdb
import subprocess

# get binary process pid
from proc_pid import proc_pid
# get binary full path
from bin_path import bin_path


# run checksec command
class checksec(gdb.Command):

    def __init__(self):
        super(checksec, self).__init__ ("checksec", gdb.COMMAND_SUPPORT, gdb.COMPLETE_NONE)


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
        
            cmd = 'checksec {}'.format(f_path)
            r = subprocess.check_output(cmd, shell = True)
            r = r.decode('utf-8')
            print (r)


        except Exception as e:  print('Error Occurred: {}'.format(str(e)))
            

checksec()
