clean:
	rm -rf venv && rm -rf *.egg-info && rm -rf dist && rm -rf *.log* && rm -fr .cache

venv:
	virtualenv -p python3 ~/.virtualenvs/ioc_toolkit && . ~/.virtualenvs/ioc_toolkit/bin/activate && pip3 install -r requirements.txt

run:
	~/.virtualenvs/ioc_toolkit/bin/python ioc_toolkit/ioc_toolkit.py

test:
	~/.virtualenvs/ioc_toolkit/bin/python -m unittest
