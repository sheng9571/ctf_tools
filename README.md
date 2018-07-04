# ctf_tools
#### Install
```
git clone --recursive https://github.com/sheng9571/ctf_tools ~/.ctf_tools
```

#### Update submodule tools
```
git submodule update --recursive
git pull --recurse-submodules
git submodule foreach --recursive 'git pull origin master || :'
git submodule foreach --recursive 'git pull origin dev || :'
```
