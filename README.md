# Mypy Helper

[![CI](https://github.com/ericwebsmith/mypy-helper/workflows/CI/badge.svg)](https://github.com/EricWebsmith/mypy-helper/actions/workflows/ci.yml)
![Coverage](https://codecov.io/gh/ericwebsmith/mypy-helper/branch/main/graph/badge.svg)
[![pypi](https://img.shields.io/pypi/v/mypy-helper.svg)](https://pypi.python.org/pypi/mypy-helper)
[![downloads](https://static.pepy.tech/badge/mypy-helper/month)](https://pepy.tech/project/mypy-helper)
[![versions](https://img.shields.io/pypi/pyversions/mypy-helper.svg)](https://github.com/ericwebsmith/mypy-helper)
[![license](https://img.shields.io/github/license/ericwebsmith/mypy-helper.svg)](https://github.com/ericwebsmith/mypy-helper/blob/main/LICENSE)

A tool to generate type hints and fix mypy errors.

## Installation

```bash
pip install mypy-helper
```

## Usage

To see a list of available commands, run the following:

```bash
mypy-help --help
```

### Rectifying 'ignore-without-code' issues

`ignore-without-code` is a mypy error code enforcing the developer to provide error code for the "# type: ignore" comment.

The command `fix-ignore-without-code` fixes ignore without code. Use this before you have tried your best to eleminate the ignore

- Usage: mypy-helper fix-ignore-without-code [OPTIONS] PATH MYPY_OUTPUT
- Options:
  - -e, --ext TEXT  Append another extension
  - --help          Show this message and exit.


example:

Firstly, run `mypy` to collect errors.
```base
mypy . --strict --enable-errror-code ignore-without-code > errors.txt
```

Secondly, fix the errors.
```bash
mypy-helper fix-ignore-without-code  examples/simple_example examples/simple_example/errors.txt
```

before:

```python
a = 1
b = 2

a = "1"
b = "1"  # type: ignore
```

after:

```python
a = 1
b = 2

a = "1"
b = "1"  # type: ignore[assignment]
```