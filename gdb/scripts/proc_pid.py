# -*- coding: utf-8 -*-

import subprocess

# get specific process's pid
class proc_pid():

    def __init__(self): pass

    def get_pid(self, gdb):
        pid = False
	
        try:
            cmd = 'print getpid()'
            pid = gdb.execute(cmd, to_string = True)
            pid = pid.strip().split(' = ')[1].strip()
        except Exception as e: pass

        return pid 
