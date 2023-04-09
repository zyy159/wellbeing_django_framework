## 3 steps to run the server
1. pip install -r requirements.txt
2. python manage.py migrate
3. python manage.py runserver 0.0.0.0:80


If there is any error when running step2, please try to delete the db.sqlite3 file, then retry.