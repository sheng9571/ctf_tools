# -*- coding: utf-8 -*-

import subprocess

# get specific process's pid
class bin_path():

    def __init__(self): pass

    def get_path(self, gdb):
        f_path = False
	
        try:
            cmd = 'info inferior'
            f_path = gdb.execute(cmd, to_string = True)
            f_path = f_path.strip().split('\n')[1]
            f_path = f_path[f_path.find('/'):].strip()
        except Exception as e: pass

        return f_path
