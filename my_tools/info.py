# -*- coding: utf-8 -*-

from subprocess import Popen, PIPE

debug = False
res = []

try:
    cmd = 'lsb_release -a'
    p = Popen(cmd, stdout=PIPE, stderr=PIPE, stdin=PIPE, shell = True)
    r = p.communicate()
    os = r[0].strip().split('\t')[2].split('\n')[0].strip()
    res.append('os: %s' % os)
except Exception, e:
    if (debug): print 'Error: lsb_release !!!'


try:
    cmd = 'git --version'
    p = Popen(cmd, stdout=PIPE, stderr=PIPE, stdin=PIPE, shell = True)
    r = p.communicate()
    git = r[0].strip().split(' ')[2]
    res.append('git: %s' % git)
except Exception, e:
    if(debug): print 'Error: git !!!'


try:
    cmd = 'python2 --version'
    p = Popen(cmd, stdout=PIPE, stderr=PIPE, stdin=PIPE, shell = True)
    r = p.communicate()
    py2 = r[1].strip().split(' ')[1].strip()
    res.append('python2: %s' % py2)
except Exception, e:
    if(debug): print 'Error: python2 !!!'


try:
    cmd = 'pip2 --version'
    p = Popen(cmd, stdout=PIPE, stderr=PIPE, stdin=PIPE, shell = True)
    r = p.communicate()
    pip2 = r[0].strip().split(' ')[1]
    res.append('pip2: %s' % pip2)
except Exception, e:
    if(debug): print 'Error: pip2 !!!'


try:
    cmd = 'pip2 freeze | grep requests'
    p = Popen(cmd, stdout=PIPE, stderr=PIPE, stdin=PIPE, shell = True)
    r = p.communicate()
    req2 = r[0].strip().split('==')[1]
    res.append('requests (python 2): %s' % req2)
except Exception, e:
    if(debug): print 'Error: requests (python2) !!!'


try:
    cmd = 'pip2 freeze | grep lxml'
    p = Popen(cmd, stdout=PIPE, stderr=PIPE, stdin=PIPE, shell = True)
    r = p.communicate()
    lxml2 = r[0].strip().split('==')[1]
    res.append('lxml (python 2): %s' % lxml2)
except Exception, e:
    if(debug): print 'Error: lxml (python2) !!!'


try:
    cmd = 'python3 --version'
    p = Popen(cmd, stdout=PIPE, stderr=PIPE, stdin=PIPE, shell = True)
    r = p.communicate()
    py3 = r[0].strip().split(' ')[1].strip()
    res.append('python3: %s' % py3)
except Exception, e:
    if(debug): print 'Error: python3 !!!'


try:
    cmd = 'pip3 freeze | grep requests'
    p = Popen(cmd, stdout=PIPE, stderr=PIPE, stdin=PIPE, shell = True)
    r = p.communicate()
    req3 = r[0].strip().split('==')[1]
    res.append('requests (python 3): %s' % req3)
except Exception, e:
    if(debug): print 'Error: requests (python3) !!!'


try:
    cmd = 'pip3 --version'
    p = Popen(cmd, stdout=PIPE, stderr=PIPE, stdin=PIPE, shell = True)
    r = p.communicate()
    pip3 = r[0].strip().split(' ')[1]
    res.append('pip3: %s' % pip3)
except Exception, e:
    if(debug): print 'Error: pip3 !!!'


try:
    cmd = 'ruby --version'
    p = Popen(cmd, stdout=PIPE, stderr=PIPE, stdin=PIPE, shell = True)
    r = p.communicate()
    ruby = r[0].strip().split(' ')[1]
    res.append('ruby: %s' % ruby)
except Exception, e:
    if(debug): print 'Error: ruby !!!'


try:
    cmd = 'gem --version'
    p = Popen(cmd, stdout=PIPE, stderr=PIPE, stdin=PIPE, shell = True)
    r = p.communicate()
    gem = r[0].strip()
    res.append('gem: %s' % gem)
except Exception, e:
    if(debug): print 'Error: gem !!!'


try:
    cmd = 'wget --version'
    p = Popen(cmd, stdout=PIPE, stderr=PIPE, stdin=PIPE, shell = True)
    r = p.communicate()
    wget = r[0].split('\n')[0].strip().split(' ')[2].strip()
    res.append('wget: %s' % wget)
except Exception, e:
    if(debug): print 'Error: wget !!!'


try:
    cmd = 'curl --version'
    p = Popen(cmd, stdout=PIPE, stderr=PIPE, stdin=PIPE, shell = True)
    r = p.communicate()
    curl = r[0].split('\n')[0].strip().split(' ')[1].strip()
    res.append('curl: %s' % curl)
except Exception, e:
    if (debug): print 'Error: curl !!!'


try:
    cmd = 'nmap --version'
    p = Popen(cmd, stdout=PIPE, stderr=PIPE, stdin=PIPE, shell = True)
    r = p.communicate()
    nmap = r[0].strip().split('\n')[0].split(' ')[2].strip()
    res.append('nmap: %s' % nmap)
except Exception, e:
    if(debug): print 'Error: nmap !!!'


try:
    cmd = 'gdb --version'
    p = Popen(cmd, stdout=PIPE, stderr=PIPE, stdin=PIPE, shell = True)
    r = p.communicate()
    gdb = r[0].strip().split('\n')[0].split(' ')[3]
    res.append('gdb: %s' % gdb)
except Exception, e:
    if(debug): print 'Error: gdb !!!'


try:
    cmd = 'gdbserver --version'
    p = Popen(cmd, stdout=PIPE, stderr=PIPE, stdin=PIPE, shell = True)
    r = p.communicate()
    gdbserver = r[0].strip().split('\n')[0].split(' ')[3]
    res.append('gdbserver: %s' % gdbserver)
except Exception, e:
    if(debug): print 'Error: gdbserver !!!'


try:
    cmd = '/usr/local/bin/qemu/qemu-x86_64-static --version'
    p = Popen(cmd, stdout=PIPE, stderr=PIPE, stdin=PIPE, shell = True)
    r = p.communicate()
    gdbserver = r[0].strip().split('\n')[0].split(' ')[2]
    res.append('QEMU: %s' % gdbserver)
except Exception, e:
    if(debug): print 'Error: QEMU !!!'


try:
    cmd = 'ltrace --version'
    p = Popen(cmd, stdout=PIPE, stderr=PIPE, stdin=PIPE, shell = True)
    r = p.communicate()
    ltrace = r[0].strip().split('\n')[0].split(' ')[2]
    res.append('ltrace: %s' % ltrace)
except Exception, e:
    if(debug): print 'Error: ltrace !!!'


try:
    cmd = 'strace -V'
    p = Popen(cmd, stdout=PIPE, stderr=PIPE, stdin=PIPE, shell = True)
    r = p.communicate()
    strace = r[0].strip().split(' ')[3].split('\n')[0].strip()
    res.append('strace: %s' % strace)
except Exception, e:
    if(debug): print 'Error: strace !!!'


try:
    cmd = 'gcc --version'
    p = Popen(cmd, stdout=PIPE, stderr=PIPE, stdin=PIPE, shell = True)
    r = p.communicate()
    gcc = r[0].strip().split('\n')[0].split(' ')[3]
    res.append('gcc: %s' % gcc)
except Exception, e:
    if(debug): print 'Error: gcc !!!'


try:
    cmd = 'g++ --version'
    p = Popen(cmd, stdout=PIPE, stderr=PIPE, stdin=PIPE, shell = True)
    r = p.communicate()
    gpp = r[0].strip().split('\n')[0].split(' ')[3]
    res.append('g++: %s' % gpp)
except Exception, e:
    if(debug): print 'Error: g++ !!!'


try:
    cmd = 'nasm -v'
    p = Popen(cmd, stdout=PIPE, stderr=PIPE, stdin=PIPE, shell = True)
    r = p.communicate()
    nasm = r[0].strip().split(' ')[2]
    res.append('nasm: %s' % nasm)
except Exception, e:
    if(debug): print 'Error: nasm !!!'


try:
    cmd = 'pip2 freeze | grep pwntools'
    p = Popen(cmd, stdout=PIPE, stderr=PIPE, stdin=PIPE, shell = True)
    r = p.communicate()
    pwntools2 = r[0].strip().split('==')[1]
    res.append('pwntools (python 2): %s' % pwntools2)
except Exception, e:
    if(debug): print 'Error: pwntools (python2) !!!'


try:
    cmd = 'pip2 freeze | grep angr'
    p = Popen(cmd, stdout=PIPE, stderr=PIPE, stdin=PIPE, shell = True)
    r = p.communicate()
    angr = r[0].strip().split('==')[1]
    res.append('angr (python 2): %s' % angr)
except Exception, e:
    if(debug): print 'Error: angr (python2) !!!'


try:
    cmd = 'pip freeze | grep z3'
    p = Popen(cmd, stdout=PIPE, stderr=PIPE, stdin=PIPE, shell = True)
    r = p.communicate()
    z3 = r[0].strip().split('==')[1]
    res.append('z3 (python 2): %s' % z3)
except Exception, e:
    if(debug): print 'Error: z3 (python2) !!!'


try:
    cmd = 'r2 -version'
    p = Popen(cmd, stdout=PIPE, stderr=PIPE, stdin=PIPE, shell = True)
    r = p.communicate()
    r2 = r[0].strip().split(' ')[1]
    res.append('radare2: %s' % r2)
except Exception, e:
    if(debug): print 'Error: radare2 !!!'


try:
    cmd = 'sde --version'
    p = Popen(cmd, stdout=PIPE, stderr=PIPE, stdin=PIPE, shell = True)
    r = p.communicate()
    sde = r[0].strip().split('\n')[0].strip().split('Version:')[1].replace('external', '').strip()
    res.append('sde: %s' % sde)
except Exception, e:
    if(debug): print 'Error: sde !!!'


try:
    cmd = 'pin'
    p = Popen(cmd, stdout=PIPE, stderr=PIPE, stdin=PIPE, shell = True)
    r = p.communicate()
    pin = r[0].strip().split('\n')[1].replace('Pin: ', '').strip()
    res.append('Intel pin: %s' % pin)
except Exception, e:
    if(debug): print 'Error: pin !!!'


try:
    cmd = 'ROPgadget -v'
    p = Popen(cmd, stdout=PIPE, stderr=PIPE, stdin=PIPE, shell = True)
    r = p.communicate()
    ropg = r[0].strip().split('\n')[0].replace('Version:', '').strip().split(' ')[1]
    res.append('ROPgadget: %s' % ropg)
except Exception, e:
    if(debug): print 'Error: ROPgadget !!!'


try:
    cmd = 'one_gadget -v'
    p = Popen(cmd, stdout=PIPE, stderr=PIPE, stdin=PIPE, shell = True)
    r = p.communicate()
    oneg = r[0].strip().split(' ')[2]
    res.append('one_gadget: %s' % oneg)
except Exception, e:
    if(debug): print 'Error: one_gadget !!!'


try:
    cmd = 'binwalk -h'
    p = Popen(cmd, stdout=PIPE, stderr=PIPE, stdin=PIPE, shell = True)
    r = p.communicate()
    binwalk = r[0].strip().split('\n')[0].split(' ')[1].strip()
    res.append('binwalk: %s' % binwalk)
except Exception, e:
    if(debug): print 'Error: binwalk !!!'


try:
    cmd = 'sasquatch -v'
    p = Popen(cmd, stdout=PIPE, stderr=PIPE, stdin=PIPE, shell = True)
    r = p.communicate()
    sasquatch = r[0].strip().split(' ')[2].strip()
    res.append('sasquatch: %s' % sasquatch)
except Exception, e:
    if(debug): print 'Error: sasquatch !!!'


print '\n'.join(res)
