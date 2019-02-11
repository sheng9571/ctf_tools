# -*- coding: utf-8 -*-

import gdb

# color object
from color import color
# get binary process pid
from proc_pid import proc_pid
# get binary full path
from bin_path import bin_path
# file info model
from file_info import file_info
# linux process map parse model
from linux_map import linux_map


# list some useful function & variable addrss
class magic(gdb.Command):

    def __init__(self):
        super(magic, self).__init__ ("magic", gdb.COMMAND_SUPPORT, gdb.COMPLETE_NONE)


    # check program is running or not
    def init(self):
        pid = proc_pid().get_pid(gdb)
        if (not pid): return False
       
        f_path = bin_path().get_path(gdb)
        if (not f_path): return False

        return pid, f_path

    
    # find code base:
    def get_code_base(self, l_map):
        return hex(int(l_map[0]['str_addr'], 16))


    # find libc base:
    def get_libc_base(self, l_map, bit):
        idx = False
        libc_base = 'null'

        if ( bit == '64'):
            idx = 3
            libc_base = hex(int(l_map[idx]['str_addr'], 16))
        elif ( bit == '32'):
            idx = 4
            libc_base = hex(int(l_map[idx]['str_addr'], 16))
        
        return libc_base, idx
    
    
    # find heap base:
    def get_heap_base(self, l_map):
        heap_base = 'null'
        
        for i in l_map:
            if ( i['name'] == '[heap]' ):
                heap_base = i['str_addr']
                break

        if (heap_base != 'null'): heap_base = hex(int(heap_base, 16))
        return heap_base


    # get some function & pointer via gdb
    def gdb_px(self, target, bit, get_val = False):
        res = 'null'
        val = 'null'

        try:
            cmd = 'p/x &{}'.format(target)
            r = gdb.execute(cmd, to_string = True)
            r = r.strip().split(' = ')
            if (len(r) > 1):
                res = r[1].strip()
                if (get_val):
                
                    try:
                        if (bit == '32'):
                            cmd = 'x/wx {}'.format(res)
                        elif (bit == '64'):
                            cmd = 'x/gx {}'.format(res)

                        r = gdb.execute(cmd, to_string = True)
                        r = r.strip().split(':')
                        if (len(r) > 1): val = hex(int(r[1].strip(), 16))
                    except Exception as e: pass

        except Exception as e: pass

        return res, val


    # find string in memory
    def gdb_find_str(self, str_addr, end_addr, target):
        res = 'null'

        try:
            cmd = 'find {}, {}, "{}"'.format(str_addr, end_addr, target)
            r = gdb.execute(cmd, to_string = True)
            r = r.strip().split('\n')
            tmp_res = []

            for i in r:
                try:
                    i = i.strip()
                    t = int(i, 16)
                    tmp_res.append(i)
                except Exception as e: continue

            if ( len(tmp_res) > 0 ): res = ', '.join(tmp_res)

        except Exception as e: pass

        return res


    def invoke(self, arg, tty):
        try:
            if (not self.init()):
                raise Exception('process is not running!')
            else:
                pid, f_path = self.init()

            f_info = file_info(f_path)
            arch = f_info.get_arch()
            bit = f_info.get_bit()
            del f_info


            l_map = linux_map(bit)
            l_map = l_map.parse(pid)

            col_obj = color()

            print( '{}{} {}libc{} {}'.format(col_obj.dft, '-' * 14, col_obj.l_blue, col_obj.dft, '-' * 14) )


            libc_base, libc_text_idx = self.get_libc_base(l_map, bit)
            heap_base = self.get_heap_base(l_map)
            code_base = self.get_code_base(l_map)
            libc_text_end = hex(int(l_map[libc_text_idx]['end_addr'], 16))
            del l_map

            system = self.gdb_px('system', bit)[0]
            execve = self.gdb_px('execve', bit)[0]
            read = self.gdb_px('read', bit)[0]
            puts = self.gdb_px('puts', bit)[0]
            bin_sh = self.gdb_find_str(libc_base, libc_text_end, '/bin/sh')

            print ( '{}: {}'.format('libc base', libc_base) )
            print ( '{}: {}'.format('code base', code_base) )
            print ( '{}: {}'.format('system(__libc_system)', system) )
            print ( '{}: {}'.format('execve', execve) )
            print ( '{}: {}'.format('read', read) )
            print ( '{}: {}'.format('puts(_IO_puts)', puts) )
            print ( '{}: {}'.format('/bin/sh', bin_sh) )
            

            print( '{}{} {}heap{} {}'.format(col_obj.dft, '-' * 14, col_obj.l_red, col_obj.dft, '-' * 14) )


            malloc_hook = self.gdb_px('__malloc_hook', bit)[0]
            free_hook = self.gdb_px('__free_hook', bit)[0]
            realloc_hook = self.gdb_px('__realloc_hook', bit)[0]
            main_arena = self.gdb_px('main_arena', bit)[0]
            if (main_arena != 'null'):
                top_chunk = hex(int(main_arena, 16) + 0x58)
            else: top_chunk = 'null'
            g_max_fast_addr, g_max_fast_val = self.gdb_px('global_max_fast', bit, True)

            print ( '{}: {}'.format('heap base', heap_base) )
            print ( '{}: {}'.format('main_arena', main_arena) )
            print ( '{}: {}'.format('top chunk', top_chunk) )
            print ( '{}: {}'.format('malloc hook(__malloc_hook)', malloc_hook) )
            print ( '{}: {}'.format('free hook(__free_hook)', free_hook) )
            print ( '{}: {}'.format('realloc hook(__realloc_hook)', realloc_hook) )
            print ( '{}: {}, value: {}'.format('global_max_fast', g_max_fast_addr, g_max_fast_val) )
            
            
            print( '{}{} {}FILE{} {}'.format(col_obj.dft, '-' * 14, col_obj.l_green, col_obj.dft, '-' * 14) )


            io_list_all, io_list_all_val = self.gdb_px('_IO_list_all', bit, True)
            io_flush_all_lockp = self.gdb_px('_IO_flush_all_lockp', bit)[0]
            io_lock_t, io_lock_t_val = self.gdb_px('_IO_stdfile_1_lock', bit, True)
            io_file_jumps = self.gdb_px('_IO_file_jumps', bit)[0]
            io_str_jumps = self.gdb_px('_IO_str_jumps', bit)[0]
            
            print ( '{}: {}, value: {}'.format('_IO_list_all', io_list_all, io_list_all_val) )
            print ( '{}: {}'.format('_IO_flush_all_lockp', io_flush_all_lockp) )
            print ( '{}: {}, value: {}'.format('_IO_stdfile_1_lock(_IO_lock_t)', io_lock_t, io_lock_t_val) )
            print ( '{}: {}'.format('_IO_file_jumps', io_file_jumps) )
            print ( '{}: {}'.format('_IO_str_jumps', io_str_jumps) )

            # __stack_prot、__libc_stack_end、_dl_make_stack_executable

            print( '{}{} {}stack{} {}'.format(col_obj.dft, '-' * 14, col_obj.orange, col_obj.dft, '-' * 14) )
            
            
            stack_prot, stack_prot_val = self.gdb_px('__stack_prot', bit, True)
            libc_stack_end, libc_stack_end_val = self.gdb_px('__libc_stack_end', bit, True)
            dl_make_stack_exec = self.gdb_px('_dl_make_stack_executable', bit)[0]
            
            print ( '{}: {}, value: {}'.format('__stack_prot', stack_prot, stack_prot_val) )
            print ( '{}: {}, value: {}'.format('__libc_stack_end', libc_stack_end, libc_stack_end_val) )
            print ( '{}: {}'.format('_dl_make_stack_executable(__GI__dl_make_stack_executable)', dl_make_stack_exec) )

        except Exception as e:  print('Error Occurred: {}'.format(str(e)))
            

magic()
