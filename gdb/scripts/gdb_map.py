# -*- coding: utf-8 -*-

import subprocess

class gdb_map():

    def __init__(self, bit):
        self.bit = bit
        if (self.bit == '32'): self.pad = 4
        elif (self.bit == '64'): self.pad = 8


    # address padding
    def addr_pad(self, t): return t.rjust(self.pad * 2, '0')


    def parse(self, gdb):
        cmd = 'info proc mappings'
        r = gdb.execute(cmd, to_string = True)
        # print(r)

        res = []

        r = r.strip().split('\n')

        for i in range(4, len(r)):
            tmp_1 = r[i].replace('\t', '').strip().split(' ')
            tmp_2 = []

            for j in tmp_1:
                if ( len(j.strip()) != 0 ): tmp_2.append(j)

            tmp_1 = tmp_2
            tmp_2 = {}

            tmp_2['str_addr'] = '0x{}'.format(self.addr_pad(tmp_1[0].strip().replace('0x', '')))
            tmp_2['end_addr'] = '0x{}'.format(self.addr_pad(tmp_1[1].strip().replace('0x', '')))
            tmp_2['size'] = tmp_1[2].strip()
            tmp_2['ofst'] = '0x{}'.format(self.addr_pad(tmp_1[3].strip().replace('0x', '')))
            if ( len(tmp_1) == 5 ):
                tmp_2['name'] = tmp_1[4].strip()
            elif ( len(tmp_1) == 4 ):
                tmp_2['name'] = '[null]'

            res.append(tmp_2)


        return res
