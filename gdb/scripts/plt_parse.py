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


# show memory map
class plt_parse(gdb.Command):

    def __init__(self):
        super(plt_parse, self).__init__ ("plt_parse", gdb.COMMAND_SUPPORT, gdb.COMPLETE_NONE)


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
            if ( len(arg.strip()) == 0 ): raise Exception('please give a plt address!')

            if (not self.init()):
                raise Exception('process is not running!')
            else:
                pid, f_path = self.init()

            col_obj = color()

            f_info = file_info(f_path)
            arch = f_info.get_arch()
            bit = f_info.get_bit()
            del f_info

            cmd = 'x/i {}'.format(arg.strip())
            r = gdb.execute(cmd, to_string = True)
            r = r.strip()

            if ( not ('# 0x' in r) ): raise Exception('please give a valid plt address!')
            got = r.split('# ')[1].strip()

            if (bit == '32'): kw = 'w'
            elif (bit == '64'): kw = 'g'
            cmd = 'x/{}x {}'.format(kw, got)
            r = gdb.execute(cmd, to_string = True)
            r = r.strip()

            addr = hex(int(r.split(':')[1].strip(), 16))

            cmd = 'x/i {}'.format(addr)
            r = gdb.execute(cmd, to_string = True)
            r = r.strip()

            if ( ('<' in r) and ('>' in r) ):
                # command is executed.
                if ('@plt' in r):
                    # partial & no RELRO, plt address, not real function address
                    addr = '{}{}{} (plt address, not real function address)'.format(col_obj.pink, addr, col_obj.dft)
                else:
                    # real function address
                    fun_name = ''
                    idx = 0
                    for i in range(r.index('<'), len(r)):
                        if (r[i].strip() == '>'):
                            idx = i
                            break

                    if (idx != 0):
                        for i in range(r.index('<') + 1, idx):
                            fun_name += r[i].strip()

                        addr = '{}{}{} address: {}{}{}'.format(col_obj.orange, fun_name, col_obj.dft, col_obj.pink, addr, col_obj.dft)

                    else:
                        addr = '? address: {}{}{}'.format(col_obj.pink, addr, col_obj.dft)


            else: addr = '{}null{}'.format(col_obj.d_grey, col_obj.dft)


            print('plt address: {}{}{}'.format(col_obj.pink, arg.strip(), col_obj.dft))
            print('got address: {}{}{}'.format(col_obj.pink, got, col_obj.dft))
            print(addr)




        except Exception as e:  print('Error Occurred: {}'.format(str(e)))
            

plt_parse()
