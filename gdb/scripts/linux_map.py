# -*- coding: utf-8 -*-

import subprocess

class linux_map():

    def __init__(self, bit):
        self.bit = bit
        if (self.bit == '32'): self.pad = 4
        elif (self.bit == '64'): self.pad = 8

    # address padding
    def addr_pad(self, t): return t.rjust(self.pad * 2, '0')

    def parse(self, pid):
        cmd = 'cat /proc/{}/maps'.format(pid)
        r = subprocess.check_output(cmd, shell = True)
        # print(r.decode('utf-8'))

        res = []

        r = r.decode('utf-8').split('\n')

        for i in r:
            i = i.strip().split(' ')
            if ( len(i) == 1 and len(i[0].strip()) == 0 ): continue

            j = []
            for x in i:
                if ( len(x.strip()) != 0): j.append(x.strip())

            tmp = {}
            tmp['str_addr'] = '0x{}'.format(self.addr_pad(j[0].strip().split('-')[0].strip()))
            tmp['end_addr'] = '0x{}'.format(self.addr_pad(j[0].strip().split('-')[1].strip()))
            tmp['perm'] = j[1].strip()
            tmp['ofst'] = '0x{}'.format(self.addr_pad(j[2].strip()))
            tmp['dev'] = j[3].strip()
            tmp['inode'] = j[4].strip()
            
            if (len(j) == 6): 
                tmp['name'] = j[5].strip()
            elif (len(j) == 5):
                tmp['name'] = '[null]'

            
            res.append(tmp)

        return res
