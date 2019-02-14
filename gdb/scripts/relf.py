# -*- coding: utf-8 -*-

import gdb
import subprocess

# color object
from color import color
# get binary process pid
from proc_pid import proc_pid
# get binary full path
from bin_path import bin_path
# ldd model
from ldd import ldd


# show memory map
class relf(gdb.Command):

    def __init__(self):
        super(relf, self).__init__ ("relf", gdb.COMMAND_SUPPORT, gdb.COMPLETE_NONE)


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
            if ( len(arg.strip()) == 0 ): raise Exception('please give one argument!')

            if (not self.init()):
                raise Exception('process is not running!')
            else:
                pid, f_path = self.init()


            ldd_obj = ldd(gdb, f_path)
            libc = ldd_obj.get_libc()
            del ldd_obj
            if (len(libc.strip()) == 0): raise Exception('could not get libc path!')

            
            cmd = 'readelf -a {} | grep "{}"'.format(libc.strip(), arg.strip())
            r = subprocess.check_output(cmd, shell = True)
            r = r.decode('utf-8').strip().split('\n')

            col_obj = color()
            res = []
            res_1 = []

            for i in r:
                tmp = []
                for j in i.strip().split(' '):
                    if(len(j.strip()) != 0): tmp.append(j)

                res.append(tmp)
                
            for i in res:
                tmp = []
                if ( len(i) == 7 ):
                    # ex: stdout
                    # 0000003c3f50  041300000006 R_X86_64_GLOB_DAT 00000000003c5708 stdout@@GLIBC_2.2.5 + 0
                    # offset
                    tmp.append(hex(int(i[3].strip(), 16)))
                    name = []
                    # name
                    for j in range(4, len(i)): name.append(i[j].strip())
                    tmp.append(' '.join(name))
                    res_1.append(tmp)
                elif ( len(i) == 8 ):
                    # 803: 00000000003c5620   224 OBJECT  GLOBAL DEFAULT   33 _IO_2_1_stdout_@@GLIBC_2.2.5
                    # offset
                    tmp.append(hex(int(i[1].strip(), 16)))
                    # name
                    tmp.append(i[7].strip())
                    res_1.append(tmp)


            res = []
            for i in res_1:
                res.append('offset: {}name: {}'.format(i[0].ljust(15, ' '), i[1].replace(arg, '{}{}{}'.format(col_obj.l_red, arg, col_obj.dft))))


            for i in res: print(i)

        except Exception as e:  print('Error Occurred: {}'.format(str(e)))
            

relf()
