# This is the script that update all tools
sudo apt-get update && \
# sudo apt-get dist-upgrade -y && \
# python2 environment
sudo apt-get install -y python2.7 python-setuptools python-dev build-essential && \
# python3 environment
sudo apt-get install -y python3 python3-setuptools python3-dev python3-pip python3-lxml && \
# sudo、man、im、tmux、zsh、git、tar、zip、ssh
sudo apt-get install -y sudo man vim tmux zsh git tar unzip openssh-server && \
# wget、curl、nc、nmap
sudo apt-get install -y wget curl nmap && \
# debug tools
sudo apt-get install -y gdb gdbserver ltrace strace && \
# lxml requirements
sudo apt-get install -y libxml2-dev libxslt-dev && \
# x64 run x86 lib
sudo apt-get install -y gcc-multilib g++-4.8-multilib && \
# pip2
sudo pip2 install --upgrade pip && sudo pip install --upgrade requests lxml && \
# pip3
sudo pip3 install --upgrade pip && \
# copy pip2 to default pip
sudo cp /usr/local/bin/pip2 /usr/local/bin/pip && \
# Update ctf tools & update
git clone --recursive https://github.com/sheng9571/ctf_tools ~/.ctf_tools && cd ~/.ctf_tools && git pull && git submodule update --init --recursive && cd ~ && \
echo update pwn tools && \
# Update pwntools
sudo pip2 install --upgrade pwntools && \
# Update Radare2
cd ~/.ctf_tools/radare2/sys/ && ./install.sh && \
# update gdb plugins
cp -rf ~/.ctf_tools/gdb ~/ && \
# update gef
cp -f ~/.ctf_tools/gef/gef.py ~/gdb/ && \
# Update ROPGadget
sudo pip2 install capstone && sudo pip2 install --upgrade ropgadget && \
# Update one_gadget
sudo gem install one_gadget && \
# Update checksec
wget -vO ~/.ctf_tools/checksec/chsec https://github.com/slimm609/checksec.sh/raw/master/checksec && chmod +x ~/.ctf_tools/checksec/chsec && cp ~/.ctf_tools/checksec/chsec /usr/local/bin/chsec && \
# Update QEMU
sudo apt-get install -y binfmt-support pkg-config libglib2.0-dev libpixman-1-dev flex bison && cd ~/.ctf_tools/qemu && ./configure --prefix=$(cd ..; pwd)/qemu-user-static --static --disable-system --enable-linux-user --enable-debug --target-list=i386-linux-user,x86_64-linux-user,arm-linux-user,aarch64-linux-user,mips-linux-user,mipsel-linux-user,mips64-linux-user,mips64el-linux-user && sudo make -j8 && sudo make install && cd ../qemu-user-static/bin && for i in *; do mv $i $i-static; done && mkdir /usr/local/bin/qemu && cp -rf * /usr/local/bin/qemu && cd ~ && \
# Update cross lib
sudo apt-get install -y libc6-armel-cross libc6-armhf-cross libc6-arm64-cross libc6-mipsel-cross libc6-mips-cross libc6-mips64-cross libc6-mips64el-cross libc6-mipsn32-mips64-cross libc6-mipsn32-mips64el-cross

    
echo update reverse tools && \
# Update angr
sudo pip install --upgrade angr && \
# Update z3
cd ~/.ctf_tools/z3 && sudo python scripts/mk_make.py && cd build && make && sudo make install && \
# Update uncompyle2
cd ~/.ctf_tools/uncompyle2 && sudo python setup.py install && cd ~ && cp -f ~/.ctf_tools/uncompyle2/scripts/uncompyle2 ~/tools/reverse/ && \
# Update afl
tar -zxvf ~/.ctf_tools/afl/afl.tar.gz -C ~/ && cd ~/afl && make && sudo make install && cd ~ && rm -rf afl && \
# Update intel pin
tar -zxvf ~/.ctf_tools/pin/pin.tar.gz -C /opt/ && cd ~/ && ln -fs /opt/pin/pin /usr/local/bin/pin && \
# Update intel sde (software development emulator)
 tar -zxvf ~/.ctf_tools/sde/sde.tar.gz -C /opt/ && cd ~/ && ln -fs /opt/sde/sde /usr/local/sde/sde && ln -fs /opt/sde/sde64 /usr/local/sde/sde64 && \
tar -zxvf ~/.ctf_tools/pin/pin.tar.gz -C /opt/ && cd ~/ && ln -fs /opt/pin/pin /usr/local/bin/pin && \

    
echo update crypto tools && \
# Update RsaCtfTool
sudo apt install -y libgmp-dev libmpfr-dev libmpc-dev python3-gmpy2 && cd ~/.ctf_tools/RsaCtfTool && sudo pip install -r requirements.txt && sudo pip3 install --upgrade pycrypto && cd ~ && cp -f ~/.ctf_tools/RsaCtfTool/RsaCtfTool.py ~/tools/crypto/ && \
# Update binwalk
cd ~/.ctf_tools/binwalk && sudo python setup.py install && sudo apt-get install -y python-lzma && cd ~ && \
# Update sasquatch (to extract non-standard SquashFS images)
cd ~/.ctf_tools/sasquatch && sudo apt-get install -y build-essential liblzma-dev liblzo2-dev zlib1g-dev && sudo ./build.sh && cd ~ && \
# Update rsatool
cd ~/.ctf_tools/rsatool && sudo python setup.py install && cd ~ && cp -f ~/.ctf_tools/rsatool/rsatool.py ~/tools/crypto/ && \

# Update Misc Tool
# ExifTool
sudo apt-get install -y libimage-exiftool-perl && \
# pngcheck
sudo apt-get install -y pngcheck && \
# zsteg
sudo apt-get install -y ruby && sudo gem install rubygems-update && sudo update_rubygems && sudo gem install rake -v 12.2.1 && sudo gem install rainbow -v 2.2.2 && sudo gem install zsteg && \

# update my own scripts
cp -rf ~/.ctf_tools/pyobd ~/tools/my_tools/ && \

# clean
rm -rf ~/.ctf_tools && \
sudo apt-get clean && sudo rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/* && \
echo -------------- Update Complete --------------
