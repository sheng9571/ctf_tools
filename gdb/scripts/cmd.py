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

        # 8. use readelf command to get specific function's offset
        tmp['name'] = 'alias of readelf'
        tmp['disc'] = 'use readelf command to get specific function's offset'
        tmp['use'] = 'relf system'
        lst.append(tmp)
        tmp = {}

        # 9. convert hex to binary
        tmp['name'] = 'convert hex to binary'
        tmp['disc'] = 'convert hex to binary'
        tmp['use'] = 'h2b 0x1'
        lst.append(tmp)
        tmp = {}

        # 10. get entry point
        tmp['name'] = 'get binary\'s entry point'
        tmp['disc'] = 'get binary\'s entry point'
        tmp['use'] = 'ep'
        lst.append(tmp)
        tmp = {}

        # 11. break to *main & run
        tmp['name'] = 'break to *main & run'
        tmp['disc'] = 'set the break point at *main and start the process'
        tmp['use'] = 'bm'
        lst.append(tmp)
        tmp = {}

        # 12. search specific string in libc
        tmp['name'] = 'search specific string in libc'
        tmp['disc'] = 'use strings command to search specific string in libc'
        tmp['use'] = 'libc_str /bin/sh'
        lst.append(tmp)
        tmp = {}

        for i in lst:
            print('{} - {} - usage: {}'.format(i['name'], i['disc'], i['use']) )


cmd()
