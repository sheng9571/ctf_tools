# -*- coding: utf-8 -*-

import gdb
import struct
import re

# color object
from color import color
# get binary process pid
from proc_pid import proc_pid
# get binary full path
from bin_path import bin_path
# file info module
from file_info import file_info
# parse chunk module
from chunk_obj import chunk_obj


# highlight the specific chunk
class chunk(gdb.Command):

    def __init__(self):
        super(chunk, self).__init__ ("chunk", gdb.COMMAND_SUPPORT, gdb.COMPLETE_NONE)
        self.bit = False


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

            if (len(arg) == 0): raise Exception('please give an value that you want to search!')
           
            try:
                # deny user to input '0'
                if ( int(arg, 16) == 0 ): raise Exception('please do not input 0!!!')
            except: pass

            f_info = file_info(f_path)
            arch = f_info.get_arch()
            bit = f_info.get_bit()
            self.bit = bit
            del f_info
            
            if (not self.bit): raise Exception('get binary\'s bit failed!')
            head_addr = arg.strip()
            col_obj = color()

            chunk_o = chunk_obj(gdb, bit, head_addr)
            info = chunk_o.parse()
            chunk_data = []

            head_addr = int(head_addr, 16)
            bottom_addr = head_addr + int(info['size'], 16)


            # layout is different
            if (self.bit == '64'):
                sign = 'g'
                padding = 0x40
                start_addr = head_addr
                valid = False

                # try to find upper bound address
                for i in range(int((padding / 0x10))):
                    start_addr -= 0x10
                    try:
                        cmd = 'x/2{}x {}'.format(sign, hex(start_addr))
                        res = gdb.execute(cmd, to_string = True)
                    except:
                        start_addr += 0x10
                        valid = True
                        break

                if (not valid): start_addr = head_addr - padding

                end_addr = bottom_addr
                valid = False

                # try to find lower bound address
                for i in range(int((padding / 0x10))):
                    end_addr += 0x10
                    try:
                        cmd = 'x/2{}x {}'.format(sign, hex(start_addr))
                        res = gdb.execute(cmd, to_string = True)
                    except:
                        end_addr -= 0x10
                        valid = True
                        break

                if (not valid): end_addr = bottom_addr + padding + 0x8
                else: end_addr += 0x8

                cnt = int((end_addr - start_addr) / int(int(self.bit) / 8)) + 1
                cmd = 'x/{}{}x {}'.format(cnt, sign, hex(start_addr))
                res = gdb.execute(cmd, to_string = True)
                res = res.strip().split('\n')
                base_addr = start_addr

                for i in res:
                    tmp = i.strip().split('\t')

                    if (base_addr == head_addr):
                        # chunk header
                        chunk_data.append('{}{}{}:\t{}\t{}{}{}'.format(col_obj.l_blue, hex(base_addr), col_obj.dft, tmp[1].strip(), col_obj.l_red, tmp[2].strip(), col_obj.dft))

                    elif(base_addr == bottom_addr):
                        # chunk last field
                        chunk_data.append('{}{}{}:\t{}{}{}\t{}'.format(col_obj.l_blue, hex(base_addr), col_obj.dft, col_obj.l_red, tmp[1].strip(), col_obj.dft, tmp[2].strip()))

                    elif(base_addr > head_addr and base_addr < bottom_addr):
                        # chunk data
                        chunk_data.append('{}{}{}:\t{}{}{}\t{}{}{}'.format(col_obj.l_blue, hex(base_addr), col_obj.dft, col_obj.l_red, tmp[1].strip(), col_obj.dft, col_obj.l_red, tmp[2].strip(), col_obj.dft))

                    else:
                        # others
                        chunk_data.append('{}:\t{}\t{}'.format(hex(base_addr), tmp[1].strip(), tmp[2].strip()))

                    base_addr += 0x10


            elif (self.bit == '32'):
                sign = 'w'
                padding = 0x20
                start_addr = head_addr
                valid = False

                # try to find upper bound address
                for i in range(int((padding / 0x10))):
                    start_addr -= 0x10
                    try:
                        cmd = 'x/2{}x {}'.format(sign, hex(start_addr))
                        res = gdb.execute(cmd, to_string = True)
                    except:
                        start_addr += 0x10
                        valid = True
                        break

                if (not valid): start_addr = head_addr - padding

                end_addr = bottom_addr
                valid = False

                # try to find lower bound address
                for i in range(int((padding / 0x10))):
                    end_addr += 0x10
                    try:
                        cmd = 'x/2{}x {}'.format(sign, hex(start_addr))
                        res = gdb.execute(cmd, to_string = True)
                    except:
                        end_addr -= 0x10
                        valid = True
                        break

                if (not valid): end_addr = bottom_addr + padding + 0x4
                else: end_addr += 0x4

                cnt = int((end_addr - start_addr) / int(int(self.bit) / 8)) + 1
                cmd = 'x/{}{}x {}'.format(cnt, sign, hex(start_addr))
                res = gdb.execute(cmd, to_string = True)
                res = res.strip().split('\n')
                base_addr = start_addr

                for i in res:
                    tmp = i.strip().split('\t')

                    if (base_addr == head_addr):
                        # chunk header
                        chunk_data.append('{}{}{}:\t{}\t{}{}{}'.format(col_obj.l_blue, hex(base_addr), col_obj.dft, tmp[1].strip(), col_obj.l_red, tmp[2].strip(), col_obj.dft))
                        base_addr += 8
                        chunk_data.append('{}{}{}:\t{}{}{}\t{}{}{}'.format(col_obj.l_blue, hex(base_addr), col_obj.dft, col_obj.l_red, tmp[3].strip(), col_obj.dft, col_obj.l_red, tmp[4].strip(), col_obj.dft))

                    elif (base_addr == bottom_addr):
                        # chunk last field
                        chunk_data.append('{}{}{}:\t{}{}{}\t{}'.format(col_obj.l_blue, hex(base_addr), col_obj.dft, col_obj.l_red, tmp[1].strip(), col_obj.dft, tmp[2].strip()))
                        base_addr += 8
                        chunk_data.append('{}:\t{}\t{}'.format(hex(base_addr), tmp[3].strip(), tmp[4].strip()))

                    elif (base_addr > head_addr and base_addr < bottom_addr):
                        # chunk data
                        chunk_data.append('{}{}{}:\t{}{}{}\t{}{}{}'.format(col_obj.l_blue, hex(base_addr), col_obj.dft, col_obj.l_red, tmp[1].strip(), col_obj.dft, col_obj.l_red, tmp[2].strip(), col_obj.dft))
                        base_addr += 8
                        chunk_data.append('{}{}{}:\t{}{}{}\t{}{}{}'.format(col_obj.l_blue, hex(base_addr), col_obj.dft, col_obj.l_red, tmp[3].strip(), col_obj.dft, col_obj.l_red, tmp[4].strip(), col_obj.dft))

                    else:
                        # others
                        chunk_data.append('{}:\t{}\t{}'.format(hex(base_addr), tmp[1].strip(), tmp[2].strip()))
                        if (len(tmp) == 5):
                            base_addr += 8
                            chunk_data.append('{}:\t{}\t{}'.format(hex(base_addr), tmp[3].strip(), tmp[4].strip()))

                    base_addr += 8


            print('\n'.join(chunk_data))

            print('-' * 44)
            print('Chunk Info:')
            print('Header Address: {}'.format(info['chunk_head_addr']))
            print('Size: {}'.format(info['size']))
            print('Status: {}'.format(info['status']))
            if ('fd' in info): print('fd: {}'.format(info['fd']))
            if ('bk' in info): print('bk: {}'.format(info['bk']))
            if (int(info['chunk_head_addr'], 16) > 0x80 and 'free' in info['status']):
                print('-' * 44)
                # unsafe_unlink detect
                if ( int(info['fd'], 16) + 0x18 == int(info['bk'], 16) + 0x10 ):
                    # meet the requirement
                    print ('[{}*{}] unsafe_unlink attack condition is satisfied!\nwe will get {}{}{}!'.format(col_obj.orange, col_obj.dft, col_obj.orange, hex(int(info['fd'], 16) + 0x18), col_obj.dft))
                else:
                    print ('[{}!{}] unsafe_unlink attack condition isn\'t satisfied!\n{}{}{}(fd) + 0x18 != {}{}{}(bk) + 0x10!'.format(col_obj.red, col_obj.dft, col_obj.red, hex(int(info['fd'], 16)), col_obj.dft, col_obj.red, hex(int(info['bk'], 16)), col_obj.dft))
                
                
                print('-' * 44)
                # unsorted_bin attack detect
                print ('[{}*{}] unsorted_bin attack detected!\nwe will get {}{}{}!'.format(col_obj.orange, col_obj.dft, col_obj.orange, hex(int(info['bk'], 16) + 0x10), col_obj.dft))


        except Exception as e:  print('Error Occurred: {}'.format(str(e)))
        finally:
            del col_obj
            del self.bit
            del chunk_o
            

chunk()
