# IOC Toolkit

[![Build Status](https://travis-ci.org/fhightower/ioc-toolkit.svg?branch=master)](https://travis-ci.org/fhightower/ioc-toolkit)

Helpful tools for analyzing and working with Indicators of Compromise (IOCs).

## Development

### Quick Start

After cloning the repo...

To create a [virtual environment](http://docs.python-guide.org/en/latest/dev/virtualenvs/) for the app, run:

```
make venv
```

Clone the app and run the application at [http://127.0.0.1:5000/](http://127.0.0.1:5000/):

```
make run
```

To test the app, run:

```
make test
```

### Adding a New Tool

When adding a new tool, there are two things which must be added:

1. Add a function for the tool in `ioc_toolkit/tools/tools.py`.
2. Add a json entry to the list of `tools` in `ioc_toolkit/ioc_toolkit.py`.
