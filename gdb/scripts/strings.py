# -*- coding: utf-8 -*-

import subprocess

# color module
from color import color
# get libc module
from ldd import ldd

# strings command module
class strings():

    def __init__(self, gdb, f_path):
        self.gdb = gdb
        self.f_path = f_path


    # find string in libc
    def find(self, target):
        target = target.strip()
        if ( len(target) == 0 ): return False

        res = []
        col_obj = color()
        ldd_obj = ldd(self.gdb, self.f_path)
        libc = ldd_obj.get_libc()

        cmd = 'strings -at x {} | grep "{}"'.format(libc, target)
        try:
            r = subprocess.check_output(cmd, shell = True)
        except: return False
        r = r.decode('utf-8').strip().split('\n')
        

        for i in r:
            i = i.strip()
            tmp = i.split(' ')
            ofst = '0x{}'.format(tmp[0])
            name = []

            for j in range(1, len(tmp)):
                if ( len(tmp[j].strip()) != 0 ): name.append(tmp[j].strip())

            name = ' '.join(name)
            # highlight the key word
            name = name.replace(target, '{}{}{}'.format(col_obj.l_red, target, col_obj.dft))

            tmp = 'offset: {}name: {}'.format(ofst.ljust(11, ' '), name)
            res.append(tmp)

        return res
