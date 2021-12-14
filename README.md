# Autocode standard library Python bindings

Basic Python bindings for Autocode standard library service accession.
Python 2.x and 3.x supported.

Used to interface with services built using [Autocode](https://autocode.com) and
the [Autocode CLI](https://github.com/acode/cli).

The `lib` package is available on [PyPI: lib](https://pypi.python.org/pypi/lib)
and operates as zero-dependency interface to run StdLib functions.
This means that you can utilize any service on StdLib without installing any
additional dependencies, and when you've deployed services to StdLib, you have
a pre-built Python SDK. For example.

```
from lib import lib

try:
    result = lib.yourUsername.hostStatus(name='Dolores Abernathy')
except RuntimeError as err:
    # handle error
```

To discover StdLib services, visit https://stdlib.com/search. To build a
service, get started with [the StdLib CLI tools](https://github.com/stdlib/lib).

## Installation

To install in an existing Python project;

```shell
$ pip install lib
```

## Usage

```python
from lib import lib

# [1]: Call "utils.reflect" function, the latest version, from StdLib
result = lib.utils.reflect(key='value')
result = lib.utils.reflect({'key': 'value'}) # also works
result = lib.utils.reflect('value') # also works, if first parameter is "key"

# [2]: Call "utils.reflect" function from StdLib, with "dev" environment
result = lib.utils.reflect['@dev'](key='value')

# [3]: Call "utils.reflect" function from StdLib, with "release" environment
#      This is equivalent to (1)
result = lib.utils.reflect['@release'](key='value')

# [4]: Call "utils.reflect" function from StdLib, with specific version
#      This is equivalent to (1)
result = lib.utils.reflect['@0.0.1'](key='value')

# [5]: Call functions within the service (not just the defaultFunction)
#      This is equivalent to (1) when "main" is the default function
result = lib.utils.reflect.main(key='value')

# Valid string composition from first object property only:
result = lib['utils.reflect'](key='value')
result = lib['utils.reflect[@dev]'](key='value')
result = lib['utils.reflect[@release]'](key='value')
result = lib['utils.reflect[@0.0.1]'](key='value')
result = lib['utils.reflect.main'](key='value')
result = lib['utils.reflect[@dev].main'](key='value')
result = lib['utils.reflect[@release].main'](key='value')
result = lib['utils.reflect[@0.0.1].main'](key='value')
```

## Sending File Data

In order to send file parameters, in Python 2.7 or 3.6, simply use;

```python
lib.username.service(parameter=open('/path/to/file.jpg'))
```

Where `parameter` is the parameter name expecting a file type (type "buffer"
as listed on StdLib).

## Additional Information

To learn more about Autocode and the standard library, visit
[autocode.com](https://autocode.com) or read the
[Autocode CLI documentation on GitHub](https://github.com/acode/cli).

You can follow the development team on Twitter,
[@AutocodeHQ](https://twitter.com/AutocodeHQ).

Autocode is &copy; 2016 - 2021 Polybit Inc.
