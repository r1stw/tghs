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
   - port
   - to projects: `repo_name: path_to_repo` (absolute or relative from tornado-git-http-server folder) per project
   - to users: `username: password` per user
4. run tghs.py
