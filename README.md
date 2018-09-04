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
## installation
1. Clone
2. Create `config.json` (example -- `config_example.json`)
3. Write in config:
   - port for server
   - add repositories data to `projects`: 
   
     `"repo_name": "path_to_repo"` per your project (where "path_to_repo" is absolute or relative from tornado-git-http-server folder)
     
     Folder `/repos/` is already gitignored, so you can put projects there.
   - add users data to `users`: 
   
     `"username": "password"` per user.
   
     Auth scheme is very simple: all users will have access to all projects.
     
   - Example of `config.py`:
   
     ```
     {
        "port": 5555,
        "projects": {
          "project1": "./repos/project1",
          "project2": "/home/user/project2"
        },
        "users": {
          "username": "qwertypass"
        }
      }
     ```
     
   - Server automatically reloads data from config everytime when it modified. No restart is needed.
4. run tghs.py
