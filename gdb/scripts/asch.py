# -*- coding: utf-8 -*-

import gdb

# color object
from color import color
# get binary process pid
from proc_pid import proc_pid
# get binary full path
from bin_path import bin_path
# file info model
from file_info import file_info
# merge linux_map and gdb_map and gdb_files model
from adv_map_obj import adv_map_obj


# search an address that belongs to which section & segment
class asch(gdb.Command):

    def __init__(self):
        super(asch, self).__init__ ("asch", gdb.COMMAND_SUPPORT, gdb.COMPLETE_NONE)


    # check program is running or not
    def init(self):
        pid = proc_pid().get_pid(gdb)
        if (not pid): return False
       
        f_path = bin_path().get_path(gdb)
        if (not f_path): return False

        return pid, f_path

    
    def invoke(self, arg, tty):
        try:
            if (not self.init()):
                raise Exception('process is not running!')
            else:
                pid, f_path = self.init()

            if (len(arg) == 0): raise Exception('please give an address that you want to search!')
            arg = int(arg.strip(), 16)

            f_info = file_info(f_path)
            arch = f_info.get_arch()
            bit = f_info.get_bit()
            del f_info
            
            col_obj = color()

            full_map = adv_map_obj().get_map(gdb, pid, bit, f_path)
            if (not full_map): raise Exception('parse information error')

            for i in range(1, len(full_map)):
                tmp = []

                for j in ( full_map[i].split(' ') ):
                    if (len(j.strip()) != 0): tmp.append(j.strip())

                str_addr = int(tmp[0].strip(), 16)
                end_addr = int(tmp[1].strip(), 16)
                section = tmp[4].strip()
                segment = tmp[5].strip()

                if (arg >= str_addr and arg < end_addr):
                    if ( len(section) > len(segment) ):
                        segment = segment.ljust(len(section), ' ')
                    elif( len(section) < len(segment) ):
                        section = section.ljust(len(segment), ' ')

                    print('{}{}{} is in {}section{} {}{}{}\t{}'.format(col_obj.pink, hex(arg), col_obj.dft, col_obj.cyan, col_obj.dft, col_obj.orange, section, col_obj.dft, tmp[3].strip()))
                    print('{}{}{} is in {}segment{} {}{}{}\t{}'.format(col_obj.pink, hex(arg), col_obj.dft, col_obj.cyan, col_obj.dft, col_obj.orange, segment, col_obj.dft, tmp[3].strip()))
                    break



        except Exception as e:  print('Error Occurred: {}'.format(str(e)))
            

asch()
