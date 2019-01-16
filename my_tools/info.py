# -*- coding: utf-8 -*-

from subprocess import Popen, PIPE

res = []

cmd = 'lsb_release -a'
p = Popen(cmd, stdout=PIPE, stderr=PIPE, stdin=PIPE, shell = True)
r = p.communicate()
os = r[0].strip().split('\t')[2].split('\n')[0].strip()
res.append('os: %s' % os)

cmd = 'git --version'
p = Popen(cmd, stdout=PIPE, stderr=PIPE, stdin=PIPE, shell = True)
r = p.communicate()
git = r[0].strip().split(' ')[2]
res.append('git: %s' % git)

cmd = 'python2 --version'
p = Popen(cmd, stdout=PIPE, stderr=PIPE, stdin=PIPE, shell = True)
r = p.communicate()
py2 = r[1].strip().split(' ')[1].strip()
res.append('python2: %s' % py2)

cmd = 'pip2 --version'
p = Popen(cmd, stdout=PIPE, stderr=PIPE, stdin=PIPE, shell = True)
r = p.communicate()
pip2 = r[0].strip().split(' ')[1]
res.append('pip2: %s' % pip2)

cmd = 'pip2 freeze | grep requests'
p = Popen(cmd, stdout=PIPE, stderr=PIPE, stdin=PIPE, shell = True)
r = p.communicate()
req2 = r[0].strip().split('==')[1]
res.append('requests (python 2): %s' % req2)

cmd = 'pip2 freeze | grep lxml'
p = Popen(cmd, stdout=PIPE, stderr=PIPE, stdin=PIPE, shell = True)
r = p.communicate()
lxml2 = r[0].strip().split('==')[1]
res.append('lxml (python 2): %s' % lxml2)

cmd = 'python3 --version'
p = Popen(cmd, stdout=PIPE, stderr=PIPE, stdin=PIPE, shell = True)
r = p.communicate()
py3 = r[0].strip().split(' ')[1].strip()
res.append('python3: %s' % py3)

cmd = 'pip3 freeze | grep requests'
p = Popen(cmd, stdout=PIPE, stderr=PIPE, stdin=PIPE, shell = True)
r = p.communicate()
req3 = r[0].strip().split('==')[1]
res.append('requests (python 3): %s' % req3)

cmd = 'pip3 --version'
p = Popen(cmd, stdout=PIPE, stderr=PIPE, stdin=PIPE, shell = True)
r = p.communicate()
pip3 = r[0].strip().split(' ')[1]
res.append('pip3: %s' % pip3)

cmd = 'ruby --version'
p = Popen(cmd, stdout=PIPE, stderr=PIPE, stdin=PIPE, shell = True)
r = p.communicate()
ruby = r[0].strip().split(' ')[1]
res.append('ruby: %s' % ruby)

cmd = 'gem --version'
p = Popen(cmd, stdout=PIPE, stderr=PIPE, stdin=PIPE, shell = True)
r = p.communicate()
gem = r[0].strip()
res.append('gem: %s' % gem)

cmd = 'wget --version'
p = Popen(cmd, stdout=PIPE, stderr=PIPE, stdin=PIPE, shell = True)
r = p.communicate()
wget = r[0].split('\n')[0].strip().split(' ')[2].strip()
res.append('wget: %s' % wget)

cmd = 'curl --version'
p = Popen(cmd, stdout=PIPE, stderr=PIPE, stdin=PIPE, shell = True)
r = p.communicate()
curl = r[0].split('\n')[0].strip().split(' ')[1].strip()
res.append('curl: %s' % curl)

cmd = 'nmap --version'
p = Popen(cmd, stdout=PIPE, stderr=PIPE, stdin=PIPE, shell = True)
r = p.communicate()
nmap = r[0].strip().split('\n')[0].split(' ')[2].strip()
res.append('nmap: %s' % nmap)

cmd = 'gdb --version'
p = Popen(cmd, stdout=PIPE, stderr=PIPE, stdin=PIPE, shell = True)
r = p.communicate()
gdb = r[0].strip().split('\n')[0].split(' ')[4]
res.append('gdb: %s' % gdb)

cmd = 'gdbserver --version'
p = Popen(cmd, stdout=PIPE, stderr=PIPE, stdin=PIPE, shell = True)
r = p.communicate()
gdbserver = r[0].strip().split('\n')[0].split(' ')[4]
res.append('gdbserver: %s' % gdbserver)

cmd = 'ltrace --version'
p = Popen(cmd, stdout=PIPE, stderr=PIPE, stdin=PIPE, shell = True)
r = p.communicate()
ltrace = r[0].strip().split('\n')[0].split(' ')[2]
res.append('ltrace: %s' % ltrace)

cmd = 'strace -V'
p = Popen(cmd, stdout=PIPE, stderr=PIPE, stdin=PIPE, shell = True)
r = p.communicate()
strace = r[0].strip().split(' ')[3]
res.append('strace: %s' % strace)

cmd = 'gcc --version'
p = Popen(cmd, stdout=PIPE, stderr=PIPE, stdin=PIPE, shell = True)
r = p.communicate()
gcc = r[0].strip().split('\n')[0].split(' ')[3]
res.append('gcc: %s' % gcc)

cmd = 'g++ --version'
p = Popen(cmd, stdout=PIPE, stderr=PIPE, stdin=PIPE, shell = True)
r = p.communicate()
gpp = r[0].strip().split('\n')[0].split(' ')[3]
res.append('g++: %s' % gpp)

cmd = 'nasm --v'
p = Popen(cmd, stdout=PIPE, stderr=PIPE, stdin=PIPE, shell = True)
r = p.communicate()
nasm = r[0].strip().split(' ')[2]
res.append('nasm: %s' % nasm)

cmd = 'pip2 freeze | grep pwntools'
p = Popen(cmd, stdout=PIPE, stderr=PIPE, stdin=PIPE, shell = True)
r = p.communicate()
pwntools2 = r[0].strip().split('==')[1]
res.append('pwntools (python 2): %s' % pwntools2)

cmd = 'pip2 freeze | grep angr'
p = Popen(cmd, stdout=PIPE, stderr=PIPE, stdin=PIPE, shell = True)
r = p.communicate()
angr = r[0].strip().split('==')[1]
res.append('angr (python 2): %s' % angr)

cmd = 'pip freeze | grep z3'
p = Popen(cmd, stdout=PIPE, stderr=PIPE, stdin=PIPE, shell = True)
r = p.communicate()
z3 = r[0].strip().split(' ')[1]
res.append('z3 (python 2): %s' % z3)

cmd = 'r2 -version'
p = Popen(cmd, stdout=PIPE, stderr=PIPE, stdin=PIPE, shell = True)
r = p.communicate()
r2 = r[0].strip().split(' ')[1]
res.append('radare2: %s' % r2)

cmd = 'ROPgadget -v'
p = Popen(cmd, stdout=PIPE, stderr=PIPE, stdin=PIPE, shell = True)
r = p.communicate()
ropg = r[0].strip().split('\n')[0].replace('Version:', '').strip().split(' ')[1]
res.append('ROPgadget: %s' % ropg)

cmd = 'one_gadget -v'
p = Popen(cmd, stdout=PIPE, stderr=PIPE, stdin=PIPE, shell = True)
r = p.communicate()
oneg = r[0].strip().split(' ')[2]
res.append('one_gadget: %s' % oneg)

cmd = 'binwalk -h'
p = Popen(cmd, stdout=PIPE, stderr=PIPE, stdin=PIPE, shell = True)
r = p.communicate()
binwalk = r[0].strip().split('\n')[0].split(' ')[1].strip()
res.append('binwalk: %s' % binwalk)

cmd = 'sasquatch -v'
p = Popen(cmd, stdout=PIPE, stderr=PIPE, stdin=PIPE, shell = True)
r = p.communicate()
sasquatch = r[0].strip().split(' ')[2].strip()
res.append('sasquatch: %s' % sasquatch)

print '\n'.join(res)
