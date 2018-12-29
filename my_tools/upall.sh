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
# Install ctf tools & update
cd ~/.ctf_tools && git pull && git submodule update --recursive && git pull --recurse-submodules && git submodule foreach --recursive 'git pull origin master || :' && git submodule foreach --recursive 'git pull origin dev || :' && cd ~ && \
# Install pwntools
sudo pip2 install --upgrade pwntools && \
# Install uncompyle2
cd ~/.ctf_tools/uncompyle2 && sudo python setup.py install && cd ~ && \
# Install ROPGadget
sudo pip2 install capstone && sudo pip2 install --upgrade ropgadget && \
# Install one_gadget
sudo gem install one_gadget && \
# Install Radare2
cd ~/.ctf_tools/radare2/sys/ && ./install.sh && \
# update gef
wget -vO ~/.ctf_tools/gdb/gef.py https://github.com/hugsy/gef/raw/master/gef.py && \
# update checksec
wget -vO ~/.ctf_tools/checksec/chsec https://github.com/slimm609/checksec.sh/raw/master/checksec && chmod +x ~/.ctf_tools/checksec/chsec && cp ~/.ctf_tools/checksec/chsec /usr/local/bin/chsec && \
# Install RsaCtfTool
sudo apt install -y libgmp-dev libmpfr-dev libmpc-dev python3-gmpy2 && cd ~/.ctf_tools/RsaCtfTool && sudo pip install -r requirements.txt && sudo pip3 install --upgrade pycrypto && cd ~ && \
# Install binwalk
cd ~/.ctf_tools/binwalk && sudo python setup.py install && sudo apt-get install -y python-lzma && cd ~ && \
# Install sasquatch (to extract non-standard SquashFS images)
cd ~/.ctf_tools/sasquatch && sudo apt-get install -y build-essential liblzma-dev liblzo2-dev zlib1g-dev && sudo ./build.sh && cd ~ && \
# Install rsatool
cd ~/.ctf_tools/rsatool && sudo python setup.py install && cd ~ && \

# Install Misc Tool
# ExifTool
sudo apt-get install -y libimage-exiftool-perl && \
# pngcheck
sudo apt-get install -y pngcheck && \
# zsteg
sudo apt-get install -y ruby && sudo gem install rubygems-update && sudo update_rubygems && sudo gem install rake -v 12.2.1 && sudo gem install rainbow -v 2.2.2 && sudo gem install zsteg && \

# clean
sudo apt-get clean && sudo rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/* && \
echo -------------- Update Complete --------------
