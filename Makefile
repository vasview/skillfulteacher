.PHONY: run setup activate

VENV = venv
PYTHON = ${VENV}\Scripts\python
PIP = ${VENV}\Scripts\pip
MANAGE = .\manage.py
APP_SCHOOL = school
APP_STAFF = staff
APP_STUDENT = student
APP_PEOPLE = people
FIXTURE = .\elklassproject\fixtures

${VENV}\Scripts\activate: requirements.txt
	python -m venv venv
	${VENV}\Scripts\pip install -r requirements.txt

setup: requirements.txt
	python -m venv ${VENV}
	${PIP} install -r requirements.txt

run:
	${PYTHON} ${MANAGE} runserver

migrations:
	${PYTHON} ${MANAGE} makemigrations

inspect_migration:
	${PYTHON} ${MANAGE} sqlmigrate ${APP_SCHOOL}
	${PYTHON} ${MANAGE} sqlmigrate ${APP_STAFF}
	${PYTHON} ${MANAGE} sqlmigrate ${APP_STUDENT}
	${PYTHON} ${MANAGE} sqlmigrate ${APP_PEOPLE}
	
migrate:
	${PYTHON} ${MANAGE} migrate

rollback_all_migrations:
	${PYTHON} ${MANAGE} migrate ${APP_SCHOOL} zero
	${PYTHON} ${MANAGE} migrate ${APP_STAFF} zero
	${PYTHON} ${MANAGE} migrate ${APP_STUDENT} zero
	${PYTHON} ${MANAGE} migrate ${APP_PEOPLE} zero

delete_migrations:
	find . -path "*/migrations/*.py" -not -name "__init__.py" -delete
	find . -path "*/migrations/*.pyc"  -delete

flush:
	${PYTHON} ${MANAGE} flush

load_data:
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