# -*- coding: utf-8 -*-

import subprocess

class file_info():

    def __init__(self, f_path):
        self.f_path = f_path


    # get cpu architecture
    def get_arch(self):
        arch = ''
        cmd = 'file {}'.format(self.f_path)
        r = subprocess.check_output(cmd, shell = True)
        r = r.decode('utf-8').strip()

        if ('for MS Windows' in r):
            # windows PE
            arch = 'Windows'
        else:
            # unix-like
            cmd = 'readelf -h {}'.format(self.f_path)
            r = subprocess.check_output(cmd, shell = True)
            arch = r.decode('utf-8').strip().split('\n')[8].strip().replace('Machine:', '').strip()
            if (len(arch) == 0): arch = 'unknown'

        return arch


    # return cpu bit
    def get_bit(self):
        bit = ''
        cmd = 'file {}'.format(self.f_path)
        r = subprocess.check_output(cmd, shell = True)
        r = r.decode('utf-8').strip()

        if ('for MS Windows' in r):
            # windows PE
            if ('PE32+' in r):
                bit = '64'
            elif ('PE32' in r):
                bit = '32'
            else: bit = 'unknown'
        else:
            # unix-like
            cmd = 'readelf -h {}'.format(self.f_path)
            r = subprocess.check_output(cmd, shell = True)
            bit = r.decode('utf-8').strip().split('\n')[2].strip().replace('Class:', '').strip().replace('ELF', '').strip()
            if (len(bit) == 0): bit = 'unknown'

        return bit
