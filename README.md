# ctf_tools
#### Install
```
git clone --recursive https://github.com/sheng9571/ctf_tools ~/.ctf_tools
```

#### Add rc file to current rc file
```
cat ctf_rc >> ~/.zshrc
cat ctf_rc >> ~/.bashrc
```

#### Update submodule tools
```
git submodule update --init --recursive
git pull --recurse-submodules
git submodule foreach --recursive 'git pull origin master || :'
git submodule foreach --recursive 'git pull origin dev || :'
```
