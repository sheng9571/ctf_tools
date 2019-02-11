# -*- coding: utf-8 -*-

import subprocess


class gdb_files():

    def __init__(self, bit):
        self.bit = bit
        if (self.bit == '32'): self.pad = 4
        elif (self.bit == '64'): self.pad = 8


    # address padding
    def addr_pad(self, t): return t.rjust(self.pad * 2, '0')


    def parse(self, gdb):
        cmd = 'info files'
        r = gdb.execute(cmd, to_string = True)
        # print(r)

        res = []

        r = r.strip().split('\n')
        str_idx = False

        # find the first line of correct inforation
        for i in range(len(r)):
            if ('Entry point:' in r[i]):
                str_idx = i + 1
                break

        if (not str_idx): return False
        tmp = {}

        for i in range(str_idx, len(r)):
            str_addr = int(r[i].strip().split(' is ')[0].strip().split(' - ')[0].strip(), 16)
            tmp[str_addr] = r[i].strip()

        # sort dict by key
        tmp = sorted(tmp.items(), key=lambda d: d[0])
        for i in tmp: res.append(i[1].strip())

        return res
