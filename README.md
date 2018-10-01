# tornado-git-http-server
Simple Tornado Git HTTP Server
-----
Based on [gist](https://gist.github.com/stewartpark/1b079dc0481c6213def9) by Stewart Park


Tested on:
```
python 3.6, 3.7
tornado 4.4.1, 5.1
git 2.18.0
ubuntu 16.04
```



## py requirements
```pip3 install tornado==5.1```

Tornado v.4.4.1 also works.




## installation
1. Clone
2. Create `config.json` (example -- `config_example.json`):
   - specify port
   - add repositories data: 
     
     ```
     "projects": {
          "project1": "./repos/project1",
          "project2": "/home/user/project2"
        },
     ```
     
     Folder `/repos/` is already gitignored, so you can put projects there.
   - add users data 
   
     ```
     "users": {
          "username": "qwertypass"
        }
     ```
   
     Auth scheme is very simple: all users will have access to all projects.
    
    _Server will automatically checks for config updates on each request. So, you can modify data without restart._
4. run tghs.py
