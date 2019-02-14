# -*- coding: utf-8 -*-

class ep_obj:

    def __init__(self): pass

    def get_ep(self, gdb):
        ep = False
        text_head = False

        cmd = 'info files'
        r = gdb.execute(cmd, to_string = True)
        r = r.strip().split('\n')
        
        for i in r:
            if ('Entry point: ' in i):
                ep = i.strip().replace('Entry point: ', '').strip()
                break

        for i in range(7, len(r)):
            tmp = r[i].strip().split(' is ')
            if (tmp[1].strip() == '.text'):
                text_heap = hex(int(tmp[0].strip().split(' - ')[0].strip(), 16))
                break

        return ep, text_heap
