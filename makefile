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

loaddata:
	python3 manage.py loaddata product/migrations/0001_product.json
	python3 manage.py loaddata sales/migrations/0001_sales.json
	python3 manage.py loaddata purchases/migrations/0001_purchases.json

deploy:
	git checkout master
	git pull origin master
	git push heroku master
h-migrations:
	heroku run python3 manage.py makemigrations
h-migrate:
	heroku run python3 manage.py migrate
h-superuser:
	heroku run python3 manage.py createsuperuser
h-logs:
	heroku logs --tail
h-loaddata:
	heroku run python3 manage.py loaddata product/migrations/0001_product.json
	heroku run python3 manage.py loaddata sales/migrations/0001_sales.json
	heroku run python3 manage.py loaddata purchases/migrations/0001_purchases.json

new_release:
	git checkout master
	git pull origin master
	echo "git tag -a v1.4 -m 'my version 1.4'"
	echo "git push origin v1.4"
clean:
	git branch | grep -v "master" | xargs git branch -D
