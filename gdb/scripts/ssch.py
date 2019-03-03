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
# file info model
from file_info import file_info
# merge linux_map and gdb_map model
from map_obj import map_obj


# search an value on stack and recursive search the pointer that point to the address
class ssch(gdb.Command):

    def __init__(self):
        super(ssch, self).__init__ ("ssch", gdb.COMMAND_SUPPORT, gdb.COMPLETE_NONE)
        self.bit = False
        # memory data
        self.mem = False
        # stack start address
        self.m_start = False
        # final result
        self.res = []


    # check program is running or not
    def init(self):
        pid = proc_pid().get_pid(gdb)
        if (not pid): return False
       
        f_path = bin_path().get_path(gdb)
        if (not f_path): return False

        return pid, f_path

    # unpack function
    def up(self, t):
        if (self.bit):
            if (self.bit == '32'): return struct.unpack('<I', t)
            elif (self.bit == '64'): return struct.unpack('<Q', t)
        else: return False

    # change input to hex
    def convert(self, arg):
        res = ''
        if(self.bit == '32'): pad = 8
        elif(self.bit == '64'): pad = 16

        if ('0x' in arg):
            # hex format
            if ( self.bit ):
                if ( self.bit == '32' ):
                    res = arg.replace('0x', '').rjust(pad, '0')
                elif( self.bit == '64' ):
                    res = arg.replace('0x', '').rjust(pad, '0')

        else:
            # string format
            if ( self.bit ):
                if ( self.bit == '32' ):
                    for i in range(0, len(arg), 4):
                        tmp = arg[i: i + 4].ljust(4, '\x00').encode('utf-8')
                        res = hex(self.up(tmp)[0]).replace('0x', '') + res
                elif( self.bit == '64' ):
                    for i in range(0, len(arg), 8):
                        tmp = arg[i: i + 8].ljust(8, '\x00').encode('utf-8')
                        res = hex(self.up(tmp)[0]).replace('0x', '') + res

        return res


    # get all stack data
    def get_stack(self, merged_map):
        str_addr = False
        end_addr = False
        oper = False
        byte = False
        memory = ''

        for i in merged_map:
            if('[stack]' in i):
                i = i.split(' ')
                str_addr = int(i[0], 16)
                end_addr = int(i[1], 16)
                break

        if (self.bit == '32'):
            oper = 'w'
            byte = 4
        elif (self.bit == '64'):
            oper = 'g'
            byte = 8

        if (oper and byte):
            cnt = int((end_addr - str_addr) / byte)
            cmd = 'x/{}{}x {}'.format(cnt, oper, str_addr)
            r = gdb.execute(cmd, to_string = True)
            r = r.strip().split('\n')
            
            for i in r:
                i = i.strip().split('\t')
                for j in range(1, len(i)):
                    if ('0x' in i[j]): memory += i[j].strip().replace('0x', '')

        self.mem = memory
        self.m_start = str_addr


    # find all substring in memory
    def find(self, t):
        res = []
        pad = False

        if(self.bit == '32'): pad = 8
        elif(self.bit == '64'): pad = 16

        for match in re.finditer(t, self.mem):
            tmp = []
            tmp.append( '0x' + hex(self.m_start + int(match.start() / 2)).replace('0x', '').rjust(pad, '0') )
            tmp.append( '0x' + hex(self.m_start + int(match.end() / 2)).replace('0x', '').rjust(pad, '0') )
            res.append(tmp)

        return res


    # recursively find all substring in memory
    def r_find(self, t, chain):
        res = []
        pad = False

        if(self.bit == '32'): pad = 8
        elif(self.bit == '64'): pad = 16

        for match in re.finditer(t, self.mem):
            tmp = []
            tmp.append( '0x' + hex(self.m_start + int(match.start() / 2)).replace('0x', '').rjust(pad, '0') )
            tmp.append( '0x' + hex(self.m_start + int(match.end() / 2)).replace('0x', '').rjust(pad, '0') )
            res.append(tmp)
            

        if (res):
            if (len(res) == 1): return res[0]
            for i in range(len(res)):
                self.r_find(res[i][0].replace('0x', ''), '{}@@@{}'.format(chain, res[i][0]) )
        else:
            self.res.append(chain.split('@@@'))


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
            target = self.convert(arg.strip())
            col_obj = color()
            self.res = []

            merged_map = map_obj().get_map(gdb, bit, pid)
            self.get_stack(merged_map)
            del merged_map

            print('[{}*{}] start searching {}{}{} in memory ...'.format(col_obj.blue, col_obj.dft, col_obj.red, arg.strip(), col_obj.dft))

            res = []
            found = self.find(target)
            if (found):
                # recursively search a pointer that point to the result
                print('[{}*{}] found {}{}{} results!'.format(col_obj.blue, col_obj.dft, col_obj.red, len(found), col_obj.dft))
                print('[{}*{}] start recursively searching pointer that point to the results ...'.format(col_obj.blue, col_obj.dft))

                # recursive search
                for i in found:
                    chain = i[0]
                    self.r_find(i[0].replace('0x', ''), chain)
                    
                print('[{}*{}] final results'.format(col_obj.blue, col_obj.dft))


                for i in self.res:
                    i[0] = '[{}{}{}]'.format(col_obj.l_blue, i[0], col_obj.dft)
                    print( '{}{}{} ← {}'.format(col_obj.red, arg.strip(), col_obj.dft, ' ← '.join(i)) )
                        
            else:
                print('[{}!{}] nothing found!!!'.format(col_obj.red, col_obj.dft))

            

            del col_obj

        except Exception as e:  print('Error Occurred: {}'.format(str(e)))
        finally:
            del self.mem
            del self.m_start
            del self.bit
            del self.res
            

ssch()
