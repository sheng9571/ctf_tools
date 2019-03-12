# -*- coding: utf-8 -*-

import math

# color object
from color import color

class chunk_obj:

    def __init__(self, gdb, bit, head_addr):
        self.gdb = gdb
        # this address must be "header address" rather than "data address"
        self.head_addr = head_addr
        self.bit = bit

        if (self.bit == '64'): self.sign = 'g'
        elif (self.bit == '32'): self.sign = 'w'

        # int size = 4 bytes
        self.int_size = 4


    # convert hex to binary
    def h2b(self, t):
        res = int(t, 16)
        res = bin(res).replace('0b', '').strip()
        res = res.rjust( 8 * math.ceil(len(res) / 8.0), '0')
        return res


    # parse chunk structure
    def parse(self):
        result = {}
        col_obj = color()
        result['chunk_head_addr'] = self.head_addr

        try:
            # parse chunk size
            cmd = 'x/2{}x {}'.format(self.sign, self.head_addr)
            res = self.gdb.execute(cmd, to_string = True)
            # check size
            size = res.strip().split('\t')[2].strip()[-(self.int_size * 2):]
            try:
                if (self.bit == '64'):
                    size = int(int(size, 16) / 16) * 16
                elif (self.bit == '32'):
                    size = int(int(size, 16) / 8) * 8
            except: size = False
            if (not size):
                result['size'] = '{}invalid size{}'.format(col_obj.l_red, col_obj.dft)
                raise Exception('Invalid chunk size!')
            
            result['size'] = hex(size)


            # check next chunk header
            end_addr = int(self.head_addr, 16) + size

            cnt = int( (end_addr + int((int(self.bit) / 8)) - int(self.head_addr, 16)) / int((int(self.bit) / 8)) ) + 1
            cmd = 'x/{}{}x {}'.format(cnt, self.sign, self.head_addr)
            res = self.gdb.execute(cmd, to_string = True)
            res = res.strip().split('\n')
            n_size = res[-1].split('\t')[2].strip()[-(self.int_size * 2):]
            try:
                n_size = int(n_size, 16)
            except: n_size = False
            if(not n_size): raise Exception('Invalid next chunk size!')

            # check three flags
            next_chunk_b = self.h2b(hex(n_size))[-3:]
            non_main_arena = False
            is_mmapped = False
            prev_inuse = False

            if(next_chunk_b[0] == '1'): non_main_arena = True
            if(next_chunk_b[1] == '1'): is_mmapped = True
            if(next_chunk_b[2] == '1'): prev_inuse = True
            status = []
            if(prev_inuse): status.append('{}active{}'.format(col_obj.l_blue, col_obj.dft))
            else: status.append('{}free{}'.format(col_obj.l_green, col_obj.dft))
            if(is_mmapped): status.append('{}mmap{}'.format(col_obj.l_red, col_obj.dft))
            if(non_main_arena): status.append('{}thread_arena{}'.format(col_obj.l_red, col_obj.dft))

            # if chunk is freed, get fd & bk, and check has current chunk size before next chunk header
            if (not prev_inuse):
                if (self.bit == '64'):
                    fd = res[1].strip().split('\t')[1].strip()
                    bk = res[1].strip().split('\t')[2].strip()
                elif (self.bit == '32'):
                    fd = res[0].strip().split('\t')[3].strip()
                    bk = res[0].strip().split('\t')[4].strip()
                result['fd'] = fd
                result['bk'] = bk
                # current chunk size at last 8 byte
                c_size = n_size = res[-1].split('\t')[1].strip()[-(self.int_size * 2):]
                try:
                    c_size = int(c_size, 16)
                except: c_size = False
                if(not c_size): status.append('{}doesn\'t have valid freed chunk size{}'.format(col_obj.l_red, col_obj.dft))

            result['status'] = '\t'.join(status)

        except Exception as e: print(str(e))
        finally:
            return result
