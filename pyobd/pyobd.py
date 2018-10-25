# -*- coding: utf-8 -*-

import sys
import subprocess

if (len(sys.argv) != 2):
    print '[!] Must give a target binary!'
    sys.exit(0)

binary = sys.argv[1].strip()
print '[*] Parse Binary: %s' % binary
cmd = 'objdump -M intel -d %s' % binary

res = subprocess.check_output(cmd, shell = True)

# Get <_start> function contents
res = res[res.find('<_start>:') + 9: ].strip().split('\n')
shell_code = []
asm = []

# split different columns
for i in res:
    i = i.split('\t')
    i[1] = i[1].strip()
    tmp = []
    for j in i[1].split(' '):
        tmp.append('\\x%s' % j)
    # long address, that asm belongs to the previous line
    if (len(i) == 2):
        # two columns
        shell_code[-1] = '%s%s' % (shell_code[-1], ''.join(tmp))
        asm.append('%s' % (i[0].strip()))
    else:
        # three columns
        shell_code.append(''.join(tmp))
        asm.append('%s\t%s' % (i[0].strip(), i[2].strip()) )
    
del res
del cmd
del binary

print '-' * 44
print '[*] Assembly Code:\n%s' % '\n'.join(asm)
print '-' * 44

print

print '[*] Shell Code:\nlength: %d bytes\n%s' % ( len((''.join(shell_code)).replace('\\x', '')) / 2, ''.join(shell_code) )

del asm
del shell_code
