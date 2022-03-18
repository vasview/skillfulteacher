.PHONY: run setup activate

VENV = venv
PYTHON = ${VENV}\Scripts\python
PIP = ${VENV}\Scripts\pip
MANAGE = .\elklass\manage.py

${VENV}\Scripts\activate: requirements.txt
	python -m venv venv
	.\venv\Scripts\pip install -r requirements.txt

setup: requirements.txt
	python -m venv ${VENV}
	${PIP} install -r requirements.txt

run:
	${PYTHON} ${MANAGE} runserver

clean:
    find . -type f -name *.pyc -delete
    find . -type d -name __pycache__ -delete