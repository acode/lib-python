# StdLib Python Bindings

[StdLib Setup](https://github.com/stdlib/lib) |
[Node](https://github.com/stdlib/lib-node) |
**Python** |
[Ruby](https://github.com/stdlib/lib-ruby) |
[Web](https://github.com/stdlib/lib-js)

Basic Python bindings for StdLib service accession. Python 2.x and 3.x supported.

Used to interface with services built using [StdLib](https://stdlib.com) and
the [StdLib Command Line Tools](https://github.com/stdlib/lib).

The `lib` package is available on [PyPI: lib](https://pypi.python.org/pypi/lib) and
operates as zero-dependency interface to run StdLib functions. This means that
you can utilize any service on StdLib without installing any additional
dependencies, and when you've deployed services to StdLib, you have a pre-built
Python SDK --- for example;

```python
from lib import lib

try:
    result = lib.yourUsername.hostStatus(name='Dolores Abernathy')
except RuntimeError as err:
    # handle error
```

To discover StdLib services, visit https://stdlib.com/search. To build a service,
get started with [the StdLib CLI tools](https://github.com/stdlib/lib).

## Installation

To install in an existing Python project;

```shell
$ pip install lib
```

## Usage

```python
from lib import lib

# [1]: Call "stdlib.reflect" function, the latest version, from StdLib
result = lib.stdlib.reflect(0, 1, kwarg='value')

# [2]: Call "stdlib.reflect" function from StdLib, with "dev" environment
result = lib.stdlib.reflect['@dev'](0, 1, kwarg='value')

# [3]: Call "stdlib.reflect" function from StdLib, with "release" environment
#      This is equivalent to (1)
result = lib.stdlib.reflect['@release'](0, 1, kwarg='value')

# [4]: Call "stdlib.reflect" function from StdLib, with specific version
#      This is equivalent to (1)
result = lib.stdlib.reflect['@0.0.1'](0, 1, kwarg='value')

# [5]: Call functions within the service (not just the defaultFunction)
#      This is equivalent to (1) when "main" is the default function
result = lib.stdlib.reflect.main(0, 1, kwarg='value')

# Valid string composition from first object property only:
result = lib['stdlib.reflect'](0, 1, kwarg='value')
result = lib['stdlib.reflect[@dev]'](0, 1, kwarg='value')
result = lib['stdlib.reflect[@release]'](0, 1, kwarg='value')
result = lib['stdlib.reflect[@0.0.1]'](0, 1, kwarg='value')
result = lib['stdlib.reflect.main'](0, 1, kwarg='value')
result = lib['stdlib.reflect[@dev].main'](0, 1, kwarg='value')
result = lib['stdlib.reflect[@release].main'](0, 1, kwarg='value')
result = lib['stdlib.reflect[@0.0.1].main'](0, 1, kwarg='value')
```

## Additional Information

To learn more about StdLib, visit [stdlib.com](https://stdlib.com) or read the
[StdLib CLI documentation on GitHub](https://github.com/stdlib/lib).

You can follow the development team on Twitter, [@polybit](https://twitter.com/polybit)

StdLib is &copy; 2016 - 2017 Polybit Inc.
