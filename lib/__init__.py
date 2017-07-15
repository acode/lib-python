class LibGen():

    import os

    HOST = 'functions.lib.id'
    PORT = 443
    PATH = '/'

    LOCALENV = 'local'
    LOCALPORT = os.getenv('STDLIB_LOCAL_PORT', 8170)

    def __init__(self, cfg={}, names=[]):
        cfg['host'] = cfg['host'] if 'host' in cfg else self.HOST
        cfg['port'] = cfg['port'] if 'port' in cfg else self.PORT
        cfg['path'] = cfg['path'] if 'path' in cfg else self.PATH
        self.__cfg__ = cfg
        self.__names__ = names

    def __repr__(self):
        return '<lib: ' + self.__str__() + '>'

    def __str__(self):
        return '.'.join(self.__names__)

    def __append_version__(self, names, value):

        import re

        if not re.compile('^@[A-Z0-9\-\.]+$', re.I).match(value):
            raise NameError('.'.join(names) + ' invalid version: ' + value)

        return names + [value]

    def __append_path__(self, names, value):

        import re

        if not re.compile('^[A-Z0-9\-]+$', re.I).match(value):

            if '@' in value:
                raise NameError('.'.join(names) + ' invalid name: ' + value + ', please specify versions and environments with [@version]')

            raise NameError('.'.join(names) + ' invalid name: ' + value)

        return names + [value]

    def __append_lib_path__(self, names, value):

        import re

        names = names + [] if len(names) else []
        default_version = '@release'

        if len(names) == 0 and value == '':
            return names + [value]

        elif len(names) == 0 and ('.' in value):

            versionMatch = re.compile('^[^\.]+?\.[^\.]*?(\[@[^\[\]]*?\])(\.|$)', re.I).match(value)
            arr = []

            if versionMatch:
                version = versionMatch[1]
                version = re.sub('^\[?(.*?)\]?$', r'\1', version)
                value = value.replace(versionMatch[1], '')
                arr = value.split('.')
                arr = arr[0:2] + [version] + arr[2:]
            else:
                arr = [''] if value == '.' else value.split('.')

            while len(arr) > 0:
                names = self.__append_lib_path__(names, arr.pop(0))

            return names

        elif len(names) == 2 and names[0] != '':
            if value[0] == '@':
                return self.__append_version__(names, value)
            else:
                return self.__append_path__(self.__append_version__(names, default_version), value)

        else:
            return self.__append_path__(names, value)

    def __getitem__(self, name):
        return self.__getattr__(name)

    def __getattr__(self, name):
        return LibGen(self.__cfg__, self.__append_lib_path__(self.__names__, name))

    def __call__(self, *args, **kwargs):

        import sys
        import urllib

        cfg = self.__cfg__

        if len(self.__names__) == 0:
            cfg = args[0] if len(args) > 0 and type(args[0]) is dict else {}
            return LibGen(cfg)
        elif len(self.__names__) >= 3 and self.__names__[2] == '@' + self.LOCALENV:
            cfg['host'] = 'localhost';
            cfg['port'] = self.LOCALPORT;

        pathname = '/'.join(self.__names__[0:2]) + '/'.join(self.__names__[2:])
        pathname += '/'
        args = list(args)

        if len(args) > 0:
            if len(args) == 1 and type(args[0]) is dict:
                kw = args[0].copy()
                kw.update(kwargs)
                kwargs = kw
            elif bool(kwargs):
                raise ValueError('.'.join(self.__names__) + ': Can not pass arguments and kwargs')

        headers = {}
        headers['Content-Type'] = 'application/json'
        headers['X-Faaslang'] = 'true'
        if 'token' in cfg:
            headers['Authorization'] = 'Bearer {0}'.format(cfg['token'])
        if 'keys' in cfg:
            headers['X-Authorization-Keys'] = json.dumps(cfg['keys'])
        if 'convert' in cfg:
            headers['X-Convert-Strings'] = 'true'
        if 'bg' in cfg:
            pathname += ':bg'
            if type(cfg['bg']) is str:
                bg = urllib.quote(cfg['bg'].encode('utf-8'))
                pathname += '={0}'.format(bg)

        if (sys.version_info > (3, 0)):
            body = self.__py3body__(args, kwargs)
            return self.__py3request__(cfg, pathname, body, headers)
        else:
            body = self.__py2body__(args, kwargs)
            return self.__py2request__(cfg, pathname, body, headers)

    def __py3body__(self, args, kwargs):

        import base64
        import json
        import io

        if bool(kwargs):
            kw = {}
            for key in kwargs:
                value = kwargs[key]
                if isinstance(value, io.IOBase):
                    if value.closed:
                        raise ValueError('.'.join(self.__names__) + ': Can not read from closed file')
                    if value.encoding == 'UTF-8':
                        value = value.buffer
                    base64data = base64.b64encode(value.read()).decode('UTF-8')
                    value.close()
                    kw[key] = {'_base64': base64data}
                else:
                    kw[key] = value
            body = json.dumps(kw)
        else:
            a = []
            for value in args:
                if isinstance(value, io.IOBase):
                    if value.closed:
                        raise ValueError('.'.join(self.__names__) + ': Can not read from closed file')
                    if value.encoding == 'UTF-8':
                        value = value.buffer
                    base64data = base64.b64encode(value.read()).decode('UTF-8')
                    value.close()
                    a.push({'_base64': base64data})
                else:
                    a.push(value)
            body = json.dumps(args)

        return body

    def __py2body__(self, args, kwargs):

        import json

        if bool(kwargs):
            kw = {}
            for key in kwargs:
                value = kwargs[key]
                if isinstance(value, file):
                    if value.closed:
                        raise ValueError('.'.join(self.__names__) + ': Can not read from closed file')
                    base64data = value.read().encode('base64').strip()
                    value.close()
                    kw[key] = {'_base64': base64data}
                else:
                    kw[key] = value
            body = json.dumps(kw)
        else:
            a = []
            for value in args:
                if isinstance(value, file):
                    if value.closed:
                        raise ValueError('.'.join(self.__names__) + ': Can not read from closed file')
                    base64data = value.read().encode('base64').strip()
                    value.close()
                    a.push({'_base64': base64data})
                else:
                    a.push(value)
            body = json.dumps(args)

        return body

    def __py3request__(self, cfg, pathname, body, headers):

        import http.client

        conn = http.client.HTTPSConnection(cfg['host'], cfg['port'])
        conn.request('POST', self.__cfg__['path'] + pathname, body, headers)
        r = conn.getresponse()
        contentType = r.getheader('Content-Type')
        response = r.read()
        conn.close()

        return self.__complete__(r.status, contentType, response)

    def __py2request__(self, cfg, pathname, body, headers):

        import httplib

        conn = httplib.HTTPSConnection(cfg['host'], cfg['port'])
        conn.request('POST', cfg['path'] + pathname, body, headers)
        r = conn.getresponse()
        contentType = r.getheader('Content-Type')
        response = r.read()
        conn.close()

        return self.__complete__(r.status, contentType, response)

    def __complete__(self, status, contentType, response):

        import json
        import re

        if contentType == 'application/json':
            response = response.decode('utf-8')
            try:
                response = json.loads(response);
            except:
                response = None
        elif contentType is None or re.compile(r"^text\/.*$", re.I).match(str(contentType)):
            response =  response.decode('utf-8')

        if status / 100 != 2:
            raise RuntimeError(response)

        return response

lib = LibGen()
