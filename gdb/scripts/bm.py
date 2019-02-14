# -*- coding: utf-8 -*-

import gdb

# get ep and .text head model
from ep_obj import ep_obj


# make a break point at *main or entry point
class bm(gdb.Command):

    def __init__(self):
        super(bm, self).__init__ ("bm", gdb.COMMAND_SUPPORT, gdb.COMPLETE_NONE)


    def invoke(self, arg, tty):
        try:
            r = False

            try:
                cmd = 'break *main'
                r = gdb.execute(cmd, to_string = True)
                print(r.strip().replace('at ', 'at *main '))
            except: pass
            
            if(r):
                cmd = 'r'
                r = gdb.execute(cmd, to_string = True)
                print('process start!')
            else:
                ep, text_head = ep_obj().get_ep(gdb)
                cmd = 'break *{}'.format(ep)
                try:
                    r = gdb.execute(cmd, to_string = True)
                    print(r.strip().replace('at ', 'at EP '))
                except: pass

                if(r):
                    try:
                        cmd = 'r'
                        r = gdb.execute(cmd, to_string = True)
                        print('process start!')
                    except: r = False
               
                if (not r):
                    try:
                        cmd = 'break *{}'.format(text_head)
                        r = gdb.execute(cmd, to_string = True)
                        print(r.strip().replace('at ', 'at .text head '))
                    except: pass

                    try:
                        cmd = 'r'
                        r = gdb.execute(cmd, to_string = True)
                        print('process start!')
                    except: r = False
                    
                if(not r):
                    cmd = 'del'
                    r = gdb.execute(cmd, to_string = True)
                    raise Exception('could not make a break poin at *main and entry point!')

        except Exception as e:  print('Error Occurred: {}'.format(str(e)))
            

bm()
