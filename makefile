# Django


serve:
	python manage.py runserver

migrations:
	python manage.py makemigrations

showmigrations:
	python manage.py showmigrations

migrate:
	python manage.py migrate

collect:
	python manage.py collectstatic --noinput

super:
	python manage.py createsuperuser

shell:
	python manage.py shell

# requirements

install:
	pip install -r requirements.txt

freeze: install
	pip freeze > requirements.txt

# virtual env

newenv:
	python3 -m venv venv

startenv:
	source venv/bin/activate

stopenv:
	deactivate


# Code Formatting - Black
# Black configuration is in pyproject.toml
format:
	black . --config pyproject.toml

# Linting - Flake8
# Flake8 configuration is in tox.ini
lint:
	flake8 .

remove_unused:
	autoflake --remove-all-unused-imports --remove-unused-variables -r -i ./*/*

# Infrastrucutre

startdeps:
	docker-compose up -d

stopdeps:
	docker-compose down



