setup:
	pip3 install -r requirements.txt
freeze:
	pip3 freeze > requirements.txt
migrations:
	python3 manage.py makemigrations
migrate:
	python3 manage.py migrate
superuser:
	python3 manage.py createsuperuser
run:
	python3 manage.py runserver
