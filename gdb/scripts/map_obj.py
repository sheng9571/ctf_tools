# -*- coding: utf-8 -*-

# color object
from color import color
# linux process map parse model
from linux_map import linux_map
# gdb info process map parse model
from gdb_map import gdb_map


class map_obj():

    def __init__(self): pass


    def get_map(self, gdb, bit, pid):
        col_obj = color()
        res = []


        if (bit == '64'): pad = 8
        elif (bit == '32'): pad = 4


        l_map = linux_map(bit)
        l_map = l_map.parse(pid)

        g_map = gdb_map(bit)
        g_map = g_map.parse(gdb)


        # length of two maps must the same
        if (len(l_map) != len(g_map)): return False


        tmp = []
        target = 'Start'
        tmp.append(target.ljust( (pad * 2) + 2, ' '))
        target = 'End'
        tmp.append(target.ljust( (pad * 2) + 2, ' '))
        target = 'Offset'
        tmp.append(target.ljust( (pad * 2) + 2, ' '))
        target = 'Perm'
        tmp.append(target.ljust( 4, ' '))
        target = 'Segment'
        tmp.append(target)
        tmp[0] = tmp[0].replace('Start', '{}Start{}'.format(col_obj.orange, col_obj.dft))
        tmp[1] = tmp[1].replace('End', '{}End{}'.format(col_obj.orange, col_obj.dft))
        tmp[2] = tmp[2].replace('Offset', '{}Offset{}'.format(col_obj.orange, col_obj.dft))
        tmp[3] = tmp[3].replace('Perm', '{}Perm{}'.format(col_obj.orange, col_obj.dft))
        tmp[4] = tmp[4].replace('Segment', '{}Segment{}'.format(col_obj.orange, col_obj.dft))
        res.append(tmp)


        for i in range(len(l_map)):
            tmp = []
            # Start Address
            target = l_map[i]['str_addr'].strip()
            tmp.append(target.ljust( (pad * 2) + 2, ' '))
            # End Address
            target = l_map[i]['end_addr'].strip()
            tmp.append(target.ljust( (pad * 2) + 2, ' '))
            # Offset
            target = l_map[i]['ofst'].strip()
            tmp.append(target.ljust( (pad * 2) + 2, ' '))
            # Permission
            target = l_map[i]['perm'].strip()
            target = target.replace('r', '{}r{}'.format(col_obj.l_green, col_obj.dft))
            target = target.replace('w', '{}w{}'.format(col_obj.l_blue, col_obj.dft))
            target = target.replace('x', '{}x{}'.format(col_obj.l_red, col_obj.dft))
            tmp.append(target.ljust( 4, ' '))
            # Segment
            target = l_map[i]['name'].strip()
            tmp.append(target)

            res.append(tmp)


        for i in range(len(res)): res[i] = ' '.join(res[i])

        return res
