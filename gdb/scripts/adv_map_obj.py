# -*- coding: utf-8 -*-

# color object
from color import color

# merge linux_map and gdb_map model
from map_obj import map_obj

# get ld、libc that used by binary
from ldd import ldd
# gdb info files parse model
from gdb_files import gdb_files


class adv_map_obj():

    def __init__(self): pass


    # address padding
    def addr_pad(self, pad, t): return t.rjust(pad * 2, '0')


	# check LD_PRELOAD is used
    def check_ld_preload(self, gdb):
        cmd = 'show environment LD_PRELOAD'
        r = gdb.execute(cmd , to_string = True)

        if ('"LD_PRELOAD" not defined' in r):
            return False
        elif ('LD_PRELOAD = ' in r):
            return r.strip().split(' = ')[1].strip()


    def get_map(self, gdb, pid, bit, f_path):
        col_obj = color()
        res = []


        if (bit == '64'): pad = 8
        elif (bit == '32'): pad = 4

        merged_map = map_obj().get_map(gdb, bit, pid)
        # length of two maps must the same
        if (not merged_map): return False
        a = merged_map.pop(0)
        # print(merged_map)


        g_files = gdb_files(bit)
        g_files = g_files.parse(gdb)
        if (not g_files): return False
        # print(len(g_files))
        
        # ldd_model = ldd(f_path)
        
        # libc = self.check_ld_preload(gdb)
        # if (not libc): libc = ldd_model.get_libc()

        # ld = ldd_model.get_ld()
        # del ldd_model

        # print ('libc: {}\nld:{}'.format(libc, ld))
        # assert local variable libc must not False
        # if (not libc): return False


        tmp = []
        target = 'Start'
        tmp.append(target.ljust( (pad * 2) + 2, ' '))
        target = 'End'
        tmp.append(target.ljust( (pad * 2) + 2, ' '))
        target = 'Offset'
        tmp.append(target.ljust( (pad * 2) + 2, ' '))
        target = 'Perm'
        tmp.append(target.ljust( 4, ' '))
        target = 'Section'
        tmp.append(target.ljust( 25, ' '))
        target = 'Segment'
        tmp.append(target)
        tmp[0] = tmp[0].replace('Start', '{}Start{}'.format(col_obj.orange, col_obj.dft))
        tmp[1] = tmp[1].replace('End', '{}End{}'.format(col_obj.orange, col_obj.dft))
        tmp[2] = tmp[2].replace('Offset', '{}Offset{}'.format(col_obj.orange, col_obj.dft))
        tmp[3] = tmp[3].replace('Perm', '{}Perm{}'.format(col_obj.orange, col_obj.dft))
        tmp[4] = tmp[4].replace('Section', '{}Section{}'.format(col_obj.orange, col_obj.dft))
        tmp[5] = tmp[5].replace('Segment', '{}Segment{}'.format(col_obj.orange, col_obj.dft))
        res.append(tmp)

        for i in range(len(g_files)):

            str_addr = int(g_files[i].strip().split(' is ')[0].strip().split(' - ')[0].strip(), 16)
            end_addr = int(g_files[i].strip().split(' is ')[0].strip().split(' - ')[1].strip(), 16)
            filled = False


            for j in range(len(merged_map)):
                tmp = []
                t_str_addr = int(merged_map[j].strip().split(' ')[0].strip(), 16)
                t_end_addr = int(merged_map[j].strip().split(' ')[1].strip(), 16)

                if ( (str_addr >= t_str_addr) and (str_addr < t_end_addr) ):
                    # in this section
                    if ( end_addr <= t_end_addr ):

                        # Start Address
                        target = '0x{}'.format(self.addr_pad(pad, hex(str_addr).replace('0x', '')))
                        tmp.append(target.ljust( (pad * 2) + 2, ' '))
                        # End Address
                        target = '0x{}'.format(self.addr_pad(pad, hex(end_addr).replace('0x', '')))
                        tmp.append(target.ljust( (pad * 2) + 2, ' '))
                        # Offset
                        ofst = merged_map[j].strip().split(' ')[2].strip()
                        tmp.append(ofst.ljust( (pad * 2) + 2, ' '))
                        # Permission
                        perm = merged_map[j].strip().split(' ')[3].strip()
                        tmp.append(perm.ljust( 4, ' '))
                        # Section
                        section = g_files[i].strip().split(' is ')[1].strip().split(' in ')[0].strip()
                        tmp.append(section.ljust( 25, ' '))
                        # Segment
                        segment = merged_map[j].strip().split(' ')[4].strip()
                        tmp.append(segment)
                        # print(tmp)
                        
                        if (not filled):
                            res.append(tmp)
                            filled = False

                    else:
                        # cross two sections
                        # First Section
                        # Start Address
                        target = '0x{}'.format(self.addr_pad(pad, hex(str_addr).replace('0x', '')))
                        tmp.append(target.ljust( (pad * 2) + 2, ' '))
                        # End Address
                        target = '0x{}'.format(self.addr_pad(pad, hex(t_end_addr).replace('0x', '')))
                        tmp.append(target.ljust( (pad * 2) + 2, ' '))
                        # Offset
                        ofst = merged_map[j].strip().split(' ')[2].strip()
                        tmp.append(ofst.ljust( (pad * 2) + 2, ' '))
                        # Permission
                        perm = merged_map[j].strip().split(' ')[3].strip()
                        tmp.append(perm.ljust( 4, ' '))
                        # Section
                        section = g_files[i].strip().split(' is ')[1].strip().split(' in ')[0].strip()
                        tmp.append(section.ljust( 25, ' '))
                        # Segment
                        segment = merged_map[j].strip().split(' ')[4].strip()
                        tmp.append(segment)
                        # print(tmp)
                        res.append(tmp)
                        
                        # Others sections
                        if (j != len(merged_map)):
                            for k in range(j + 1, len(merged_map)):
                                tmp = []
                                str_addr = t_end_addr
                                t_str_addr = int(merged_map[k].strip().split(' ')[0].strip(), 16)
                                t_end_addr = int(merged_map[k].strip().split(' ')[1].strip(), 16)
                                if ( (str_addr >= t_str_addr) and (str_addr < t_end_addr) ):
                                    if ( end_addr <= t_end_addr ):
                                        if (end_addr == t_end_addr):
                                            # Start Address
                                            target = '0x{}'.format(self.addr_pad(pad, hex(str_addr).replace('0x', '')))
                                            tmp.append(target.ljust( (pad * 2) + 2, ' '))
                                            # End Address
                                            target = '0x{}'.format(self.addr_pad(pad, hex(end_addr).replace('0x', '')))
                                            tmp.append(target.ljust( (pad * 2) + 2, ' '))
                                            # Offset
                                            ofst = merged_map[k].strip().split(' ')[2].strip()
                                            tmp.append(ofst.ljust( (pad * 2) + 2, ' '))
                                            # Permission
                                            perm = merged_map[k].strip().split(' ')[3].strip()
                                            tmp.append(perm.ljust( 4, ' '))
                                            # Section
                                            section = g_files[i].strip().split(' is ')[1].strip().split(' in ')[0].strip()
                                            tmp.append(section.ljust( 25, ' '))
                                            # Segment
                                            segment = merged_map[k].strip().split(' ')[4].strip()
                                            tmp.append(segment)
                                            # print(tmp)
                                            res.append(tmp)
                                        elif (end_addr < t_end_addr):
                                            # Start Address
                                            target = '0x{}'.format(self.addr_pad(pad, hex(str_addr).replace('0x', '')))
                                            tmp.append(target.ljust( (pad * 2) + 2, ' '))
                                            # End Address
                                            target = '0x{}'.format(self.addr_pad(pad, hex(end_addr).replace('0x', '')))
                                            tmp.append(target.ljust( (pad * 2) + 2, ' '))
                                            # Offset
                                            ofst = merged_map[k].strip().split(' ')[2].strip()
                                            tmp.append(ofst.ljust( (pad * 2) + 2, ' '))
                                            # Permission
                                            perm = merged_map[k].strip().split(' ')[3].strip()
                                            tmp.append(perm.ljust( 4, ' '))
                                            # Section
                                            section = g_files[i].strip().split(' is ')[1].strip().split(' in ')[0].strip()
                                            tmp.append(section.ljust( 25, ' '))
                                            # Segment
                                            segment = merged_map[k].strip().split(' ')[4].strip()
                                            tmp.append(segment)
                                            # print(tmp)
                                            res.append(tmp)
                                            
                                            # fill empty section
                                            tmp = []
                                            # Start Address
                                            str_addr = end_addr
                                            target = '0x{}'.format(self.addr_pad(pad, hex(str_addr).replace('0x', '')))
                                            tmp.append(target.ljust( (pad * 2) + 2, ' '))
                                            # End Address
                                            end_addr = t_end_addr
                                            target = '0x{}'.format(self.addr_pad(pad, hex(end_addr).replace('0x', '')))
                                            tmp.append(target.ljust( (pad * 2) + 2, ' '))
                                            # Offset
                                            ofst = merged_map[k].strip().split(' ')[2].strip()
                                            tmp.append(ofst.ljust( (pad * 2) + 2, ' '))
                                            # Permission
                                            perm = merged_map[k].strip().split(' ')[3].strip()
                                            tmp.append(perm.ljust( 4, ' '))
                                            # Section
                                            section = '[null]'
                                            tmp.append(section.ljust( 25, ' '))
                                            # Segment
                                            segment = merged_map[k].strip().split(' ')[4].strip()
                                            tmp.append(segment)
                                            # print(tmp)
                                            res.append(tmp)
                                        
                                        filled = True
                                        break
                                    else:
                                        # Start Address
                                        target = '0x{}'.format(self.addr_pad(pad, hex(str_addr).replace('0x', '')))
                                        tmp.append(target.ljust( (pad * 2) + 2, ' '))
                                        # End Address
                                        target = '0x{}'.format(self.addr_pad(pad, hex(t_end_addr).replace('0x', '')))
                                        tmp.append(target.ljust( (pad * 2) + 2, ' '))
                                        # Offset
                                        ofst = merged_map[k].strip().split(' ')[2].strip()
                                        tmp.append(ofst.ljust( (pad * 2) + 2, ' '))
                                        # Permission
                                        perm = merged_map[k].strip().split(' ')[3].strip()
                                        tmp.append(perm.ljust( 4, ' '))
                                        # Section
                                        section = g_files[i].strip().split(' is ')[1].strip().split(' in ')[0].strip()
                                        tmp.append(section.ljust( 25, ' '))
                                        # Segment
                                        segment = merged_map[k].strip().split(' ')[4].strip()
                                        tmp.append(segment)
                                        # print(tmp)
                                        res.append(tmp)
                        

        res1 = []
        res1.append(res[0])

        # add some section that doesn't include in gdb_files
        for i in merged_map:
            i = i.split(' ')
            str_addr = int(i[0].strip(), 16)
            end_addr = int(i[1].strip(), 16)
            tmp = []

            # group
            for j in range(1, len(res)):
                tmp_str_addr = int(res[j][0].strip(), 16)
                tmp_end_addr = int(res[j][1].strip(), 16)
                if ( (tmp_str_addr >= str_addr) and (tmp_end_addr <= end_addr) ): tmp.append(res[j])


            if(len(tmp) == 0):
                lst = []
                # Start Address
                target = '0x{}'.format(self.addr_pad(pad, hex(str_addr).replace('0x', '')))
                lst.append(target.ljust( (pad * 2) + 2, ' '))
                # End Address
                target = '0x{}'.format(self.addr_pad(pad, hex(end_addr).replace('0x', '')))
                lst.append(target.ljust( (pad * 2) + 2, ' '))
                # Offset
                ofst = i[2].strip()
                lst.append(ofst.ljust( (pad * 2) + 2, ' '))
                # Permission
                perm = i[3].strip()
                lst.append(perm.ljust( 4, ' '))
                # Section
                section = '[null]'
                lst.append(section.ljust( 25, ' '))
                # Segment
                segment = i[4].strip()
                if (len(segment) == 0): segment = '[null]'
                lst.append(segment)
                res1.append(lst)
            else:
                # check all section in group
                ed = str_addr
                j = 0
                while (j < len(tmp)):
                    tmp_str_addr = int(tmp[j][0].strip(), 16)
                    tmp_end_addr = int(tmp[j][1].strip(), 16)

                    if ( ed < tmp_str_addr ):
                        lst = []
                        # Start Address
                        str_addr = ed
                        target = '0x{}'.format(self.addr_pad(pad, hex(str_addr).replace('0x', '')))
                        lst.append(target.ljust( (pad * 2) + 2, ' '))
                        # End Address
                        end_addr = tmp_str_addr
                        target = '0x{}'.format(self.addr_pad(pad, hex(end_addr).replace('0x', '')))
                        lst.append(target.ljust( (pad * 2) + 2, ' '))
                        # Offset
                        ofst = i[2].strip()
                        lst.append(ofst.ljust( (pad * 2) + 2, ' '))
                        # Permission
                        perm = i[3].strip()
                        lst.append(perm.ljust( 4, ' '))
                        # Section
                        section = '[null]'
                        lst.append(section.ljust( 25, ' '))
                        # Segment
                        segment = i[4].strip()
                        if (len(segment) == 0): segment = '[null]'
                        lst.append(segment)
                        # print(lst)
                        res1.append(lst)
                        res1.append(tmp[j])
                    else: res1.append(tmp[j])
                    
                    ed = tmp_end_addr
                    j += 1

                    # last empty section
                    if (j == len(tmp)):
                        if (ed < end_addr):
                            lst = []
                            # Start Address
                            str_addr = ed
                            target = '0x{}'.format(self.addr_pad(pad, hex(str_addr).replace('0x', '')))
                            lst.append(target.ljust( (pad * 2) + 2, ' '))
                            # End Address
                            target = '0x{}'.format(self.addr_pad(pad, hex(end_addr).replace('0x', '')))
                            lst.append(target.ljust( (pad * 2) + 2, ' '))
                            # Offset
                            ofst = i[2].strip()
                            lst.append(ofst.ljust( (pad * 2) + 2, ' '))
                            # Permission
                            perm = i[3].strip()
                            lst.append(perm.ljust( 4, ' '))
                            # Section
                            section = '[null]'
                            lst.append(section.ljust( 25, ' '))
                            # Segment
                            segment = i[4].strip()
                            if (len(segment) == 0): segment = '[null]'
                            lst.append(segment)
                            res1.append(lst)
                    
        res = res1
        del res1

        for i in range(len(res)): res[i] = ' '.join(res[i])

        return res
