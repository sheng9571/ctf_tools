# -*- coding: utf-8 -*-

import subprocess

class ldd():

    def __init__(self, gdb, f_path):
        self.gdb = gdb
        self.f_path = f_path


    # get libc.so full path
    def get_libc(self):
        libc_path = False

        cmd = 'show environment LD_PRELOAD'
        r = self.gdb.execute(cmd , to_string = True)
        r = r.strip()
        if ('LD_PRELOAD = ' in r):
            libc_path = r.split(' = ')[1].strip()
        else:
            cmd = 'ldd {}'.format(self.f_path)
            r = subprocess.check_output(cmd, shell = True)
            r = r.decode('utf-8').strip().split('\n')

            for i in r:
                i = i.replace('\t', '').strip()
                if ( 'libc.so.6 => ' in i):
                    libc_path = i.split(' => ')[1].strip().split(' (')[0].strip()
                    break

        return libc_path


    # get ld.so full path
    def get_ld(self):
        ld_path = False

        cmd = 'ldd {}'.format(self.f_path)
        r = subprocess.check_output(cmd, shell = True)
        r = r.decode('utf-8').strip().split('\n')

        for i in r:
            i = i.replace('\t', '').strip()
            if ( '/ld-linux' in i):
                ld_path = i.strip().split(' (')[0].strip()
                break

        return ld_path
    
    
    # get vdso full path
    def get_vdso(self):
        vdso_path = False

        cmd = 'ldd {}'.format(self.f_path)
        r = subprocess.check_output(cmd, shell = True)
        r = r.decode('utf-8').strip().split('\n')

        for i in r:
            i = i.replace('\t', '').strip()
            if ( 'linux-vdso' in i):
                vdso_path = i.strip().split(' => ')[0].strip()
                break

        return vdso_path
    
    
    # get libselinux.so full path
    def get_libselinux(self):
        libselinux_path = False

        cmd = 'ldd {}'.format(self.f_path)
        r = subprocess.check_output(cmd, shell = True)
        r = r.decode('utf-8').strip().split('\n')

        for i in r:
            i = i.replace('\t', '').strip()
            if ( '/libselinux' in i):
                libselinux_path = i.strip().split(' => ')[1].strip().split(' (')[0].strip()
                break

        return libselinux_path
    
    
    # get libpcre full path
    def get_libpcre(self):
        libpcre_path = False

        cmd = 'ldd {}'.format(self.f_path)
        r = subprocess.check_output(cmd, shell = True)
        r = r.decode('utf-8').strip().split('\n')

        for i in r:
            i = i.replace('\t', '').strip()
            if ( '/libpcre' in i):
                libpcre_path = i.strip().split(' => ')[1].strip().split(' (')[0].strip()
                break

        return libpcre_path
    
    
    # get libdl full path
    def get_libdl(self):
        libdl_path = False

        cmd = 'ldd {}'.format(self.f_path)
        r = subprocess.check_output(cmd, shell = True)
        r = r.decode('utf-8').strip().split('\n')

        for i in r:
            i = i.replace('\t', '').strip()
            if ( '/libdl' in i):
                libdl_path = i.strip().split(' => ')[1].strip().split(' (')[0].strip()
                break

        return libdl_path
    
    
    # get libpthread full path
    def get_libpthread(self):
        libpthread_path = False

        cmd = 'ldd {}'.format(self.f_path)
        cmd = 'ldd {}'.format('/bin/ls')
        r = subprocess.check_output(cmd, shell = True)
        r = r.decode('utf-8').strip().split('\n')

        for i in r:
            i = i.replace('\t', '').strip()
            if ( '/libpthread' in i):
                libpthread_path = i.strip().split(' => ')[1].strip().split(' (')[0].strip()
                break

        return libpthread_path
