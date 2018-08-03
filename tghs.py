import os
import json
import subprocess
import tornado.ioloop
import tornado.web
import base64

from typing import Dict


CONFIG: 'Config' = None


class Config:
    FILEPATH = './config.json'
    port: int
    _projects: Dict[str, str]
    _users: Dict[str, dict]
    _lastmtime = 0

    def __init__(self):
        data = self._refresh()
        self.port = data['port']

    def _refresh(self):
        file_lastmtime = os.path.getmtime(self.FILEPATH)
        if self._lastmtime == file_lastmtime:
            return None
        self._lastmtime = file_lastmtime
        with open(self.FILEPATH, mode='r', encoding='utf-8') as e:
            data = json.load(e)
        self._projects = data['projects']
        self._users = data['users']
        return data

    def get_project_path(self, project_name):
        return os.path.abspath(self._projects[project_name])

    def check_user_permission(self, user, password, project, is_refreshed=False):
        try:
            user_config = self._users[user]
            user_config['projects'].index(project)
            if user_config["password"] != password:
                raise ValueError
            return True
        except (KeyError, ValueError):
            if is_refreshed:
                return False
            self._refresh()
            self.check_user_permission(user, password, project, True)

    def has_project(self, project_name):
        if project_name not in self._projects.keys():
            self._refresh()
            return project_name in self._projects.keys()
        return True


class BaseGitHandler(tornado.web.RequestHandler):
    project_name: str

    def data_received(self, chunk):
        """just to suppress annoying abstract-class inspection, method is unused"""
        raise RuntimeError("Not Implemented Method")

    def _check_auth(self, kwargs):
        auth_header = self.request.headers.get('Authorization')
        if auth_header is None or not auth_header.startswith('Basic '):
            self.set_status(401)
            self.set_header('WWW-Authenticate', 'Basic realm=Restricted')
            self._transforms = []
            self.finish()
            return False
        auth_decoded = str(base64.b64decode(auth_header[6:]), 'utf-8')
        kwargs['auth_user'], kwargs['auth_pass'] = auth_decoded.split(':', 2)
        if not CONFIG.check_user_permission(kwargs['auth_user'], kwargs['auth_pass'], self.project_name):
            raise tornado.web.HTTPError(401)
        return True

    def _execute(self, transforms, *args, **kwargs):
        self.project_name = str(args[0], 'utf-8')
        if not self._check_auth(kwargs):
            return False
        return super()._execute(transforms, *args, **kwargs)

    def prepare(self):
        if not CONFIG.has_project(self.project_name):
            raise tornado.web.HTTPError(404)
        super().prepare()

    @property
    def _project_path(self):
        return CONFIG.get_project_path(self.project_name)


class GitInfoHandler(BaseGitHandler):
    def get(self, *args, **kwargs):
        service = self.get_argument('service')
        if service[:4] != 'git-':
            raise tornado.web.HTTPError(501)
        proc = subprocess.Popen(
            [service, '--stateless-rpc', '--advertise-refs', self._project_path],
            stdout=subprocess.PIPE)
        packet = f'# service={service}\n'
        length = len(packet) + 4
        prefix = '{:04x}'.format(length & 0xFFFF)
        data = ''.join((prefix, packet, '0000', str(proc.stdout.read(), 'utf-8')))
        self.set_header('Expires', 'Fri, 01 Jan 1980 00:00:00 GMT')
        self.set_header('Cache-Control', 'no-cache, max-age=0, must-revalidate')
        self.set_header('Content-Type', f'application/x-{service}-advertisement')
        self.finish(data)


class GitReceiveHandler(BaseGitHandler):
    def post(self, *args, **kwargs):
        proc = subprocess.Popen(
            ['git-receive-pack', '--stateless-rpc', self._project_path],
            stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        result, _ = proc.communicate(self.request.body)
        self.set_header('Expires', 'Fri, 01 Jan 1980 00:00:00 GMT')
        self.set_header('Cache-Control', 'no-cache, max-age=0, must-revalidate')
        self.set_header('Content-Type', f'application/x-git-receive-pack-advertisement')
        self.finish(result)


class GitUploadHandler(BaseGitHandler):
    def post(self, *args, **kwargs):
        proc = subprocess.Popen(
            ['git-upload-pack', '--stateless-rpc', self._project_path],
            stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        result, _ = proc.communicate(self.request.body)
        self.set_header('Expires', 'Fri, 01 Jan 1980 00:00:00 GMT')
        self.set_header('Cache-Control', 'no-cache, max-age=0, must-revalidate')
        self.set_header('Content-Type', f'application/x-git-upload-pack-advertisement')
        self.finish(result)


if __name__ == "__main__":
    CONFIG = Config()
    app = tornado.web.Application([
        (r"/([^/]*)/info/refs", GitInfoHandler),
        (r"/([^/]*)/git-receive-pack", GitReceiveHandler),
        (r"/([^/]*)/git-upload-pack", GitUploadHandler),
    ])
    app.listen(CONFIG.port)
    tornado.ioloop.IOLoop.current().start()
