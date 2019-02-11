import gdb

# self-defined command list
class cmd(gdb.Command):

    def __init__(self):
        super(cmd, self).__init__ ("cmd", gdb.COMMAND_SUPPORT, gdb.COMPLETE_NONE)

    def invoke(self, arg, tty):
        lst = []
        tmp = {}
        
        # 1. cmd, list all self-defined commands
        tmp['name'] = 'cmd'
        tmp['disc'] = 'list all self-defined commands'
        tmp['use'] = 'cmd'
        lst.append(tmp)
        tmp = {}

        # 2. magic, list some useful function & variable address
        tmp['name'] = 'magic'
        tmp['disc'] = 'list some useful function & variable address'
        tmp['use'] = 'magic'
        lst.append(tmp)
        tmp = {}
        
        # 3. memory map, show memory map include more details
        tmp['name'] = 'memory map'
        tmp['disc'] = 'show memory map include more details'
        tmp['use'] = 'map'
        lst.append(tmp)
        tmp = {}


        # 4. advanced memory map, show memory map include all details
        tmp['name'] = 'advanced memory map'
        tmp['disc'] = 'show memory map include all details'
        tmp['use'] = 'adv_map'
        lst.append(tmp)
        tmp = {}


        # 5. auto attach to the process that named in at.py running via python2.7
        tmp['name'] = 'auto attach to the process'
        tmp['disc'] = 'auto attach to the process that named in at.py running via python2.7'
        tmp['use'] = 'at'
        lst.append(tmp)
        tmp = {}
        
        
        # 6. run checksec command
        tmp['name'] = 'checksec'
        tmp['disc'] = 'run checksec command'
        tmp['use'] = 'checksec'
        lst.append(tmp)
        tmp = {}

        
        # 7. LD_PRELOAD alias in gdb
        tmp['name'] = 'alias of LD_PRELOAD in gdb'
        tmp['disc'] = 'alias of LD_PRELOAD in gdb'
        tmp['use'] = 'ldp test.so'
        lst.append(tmp)
        tmp = {}

        for i in lst:
            print('{} - {} - usage: {}'.format(i['name'], i['disc'], i['use']) )


cmd()
