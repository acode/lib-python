class LibGen():

    HOST = 'f.stdlib.com'
    PORT = 443
    PATH = '/'

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
        import json

        if len(self.__names__) == 0:
            cfg = args[0] if len(args) > 0 and type(args[0]) is dict else {}
            return LibGen(cfg)
        elif self.__names__[0] == '':
            raise NameError('StdLib local execution currently unavailable in Python')

        name = '/'.join(self.__names__[0:2]) + '/'.join(self.__names__[2:])
        args = list(args)
        kwargs = args.pop() if not bool(kwargs) and (len(args) > 0 and type(args[-1]) is dict) else kwargs

        for value in args:
            if (value is not None and
                value is not bool and
                value is not str and
                value is not int and
                value is not float):
                    raise ValueError('.'.join(self.__names__) + ': All arguments must be Boolean, Number, String or None')

        body = json.dumps({'args': args, 'kwargs': kwargs})

        if (sys.version_info > (3, 0)):
            return self.__py3__(name, body)
        else:
            return self.__py2__(name, body)


    def __py3__(self, name, body):

        import http.client
        import json
        import re

        conn = http.client.HTTPSConnection(self.__cfg__['host'], self.__cfg__['port'])
        conn.request('POST', self.__cfg__['path'] + name, body, {'Content-Type': 'application/json'})
        r = conn.getresponse()
        contentType = r.getheader('Content-Type')
        response = r.read()
        conn.close()

        if contentType == 'application/json':
            response = response.decode('utf-8')
            try:
                response = json.loads(response);
            except:
                response = None
        elif contentType is None or re.compile(r"^text\/.*$", re.I).match(str(contentType)):
            response = response.decode('utf-8')

        if r.status / 100 != 2:
            raise RuntimeError(response)

        return response

    def __py2__(self, name, body):

        import httplib
        import json
        import re

        conn = httplib.HTTPSConnection(self.__cfg__['host'], self.__cfg__['port'])
        conn.request('POST', self.__cfg__['path'] + name, body, {'Content-Type': 'application/json'})
        r = conn.getresponse()
        contentType = r.getheader('Content-Type')
        response = r.read()
        conn.close()

        if contentType == 'application/json':
            response = unicode(response)
            try:
                response = json.loads(response);
            except:
                response = None
        elif contentType is None or re.compile(r"^text\/.*$", re.I).match(str(contentType)):
            response = unicode(response)

        if r.status / 100 != 2:
            raise RuntimeError(response)

        return response

lib = LibGen()
