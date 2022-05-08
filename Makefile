.PHONY: run setup activate

VENV = venv
PYTHON = ${VENV}\Scripts\python
PIP = ${VENV}\Scripts\pip
MANAGE = .\manage.py
APP = school
FIXTURE = ${APP}\fixtures

${VENV}\Scripts\activate: requirements.txt
	python -m venv venv
	${VENV}\Scripts\pip install -r requirements.txt

setup: requirements.txt
	python -m venv ${VENV}
	${PIP} install -r requirements.txt

run:
	${PYTHON} ${MANAGE} runserver

create_migrations:
	${PYTHON} ${MANAGE} makemigrations ${APP}

inspect_migration:
	${PYTHON} ${MANAGE} sqlmigrate ${APP}

migrate:
	${PYTHON} ${MANAGE} migrate

rollback_all_migrations:
	${PYTHON} ${MANAGE} migrate ${APP} zero

flush:
	${PYTHON} ${MANAGE} flush

load_init_data:
	${PYTHON} ${MANAGE} loaddata ${FIXTURE}\city.json
	${PYTHON} ${MANAGE} loaddata ${FIXTURE}\region.json
	${PYTHON} ${MANAGE} loaddata ${FIXTURE}\subject.json
	${PYTHON} ${MANAGE} loaddata ${FIXTURE}\job_position.json
	${PYTHON} ${MANAGE} loaddata ${FIXTURE}\nationality.json
	${PYTHON} ${MANAGE} loaddata ${FIXTURE}\school_level.json
	${PYTHON} ${MANAGE} loaddata ${FIXTURE}\schoolyear.json

clean:
	find . -type f -name *.pyc -delete
	find . -type d -name __pycache__ -delete