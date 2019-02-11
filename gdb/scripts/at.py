# -*- coding: utf-8 -*-

import gdb
import subprocess

# color object
from color import color


# attach to a process that run via python xxx.py
class at(gdb.Command):

    def __init__(self):
        super(at, self).__init__ ("at", gdb.COMMAND_SUPPORT, gdb.COMPLETE_NONE)
        self.f_lst = ['exploit.py', 'exp.py', 'a.py', 'test.py']


    def invoke(self, arg, tty):
        try:

            # ps -ef
            # pidof python
            # pgrep -P 26292
            # pgrep -f "python exploit.py"
            # pstree -p 30010
            # pstree -p $(pgrep -f "python exploit.py")

            col_obj = color()
            pid = False

            for i in self.f_lst:
                # first, get python xxx.py pid
                cmd = 'ps -ef'
                r = subprocess.check_output(cmd, shell = True)
                r = r.decode('utf-8').strip().split('\n')
                format_res = []

                for j in r:
                    j = j.strip().split(' ')
                    tmp = []

                    # clean null element
                    for k in j:
                        if (len(k.strip()) != 0): tmp.append(k)

                    format_res.append(' '.join(tmp))

                found = False
                ppid = False

                for j in format_res:
                    j = j.strip().split(' ')
                    p_cmd = []

                    for k in range(7, len(j)): p_cmd.append(j[k])
                    p_cmd = ' '.join(p_cmd)
                    target = 'python {}'.format(i.strip())
                    if (p_cmd == target):
                        found = True
                        ppid = j[1]
                        break

                # second found it's children pid
                if (found):
                    for j in format_res:
                        j = j.strip().split(' ')
                        if (j[2] == ppid): pid = j[1].strip()


                if (pid): break


            if (not pid): raise Exception('{}No exploit is running!{}'.format(col_obj.red, col_obj.dft))

            print( 'attach to {}{}{} (running via python {}{}{})'.format(col_obj.l_red, pid, col_obj.dft, col_obj.l_red, i, col_obj.dft) )

            cmd = 'attach {}'.format(pid)
            gdb.execute(cmd, to_string = True)

        except Exception as e:  print('Error Occurred: {}'.format(str(e)))
            

at()
