## 3 steps to run the server
1. pip install -r requirements.txt
2. python manage.py migrate
3. python manage.py runserver 0.0.0.0:80


If there is any error when running step2, please try to delete the db.sqlite3 file, then retry.

# Intall sqlite3 version 3.39.4 in centOS 7
- wget https://www.sqlite.org/2022/sqlite-autoconf-3390400.tar.gz 
- tar xvfz sqlite-autoconf-3390400.tar.gz
- cd sqlite-autoconf-3390400
- ./configure
- make
- make install 
- PATH=$PATH:/usr/local/lib
- sqlite3 --version

# update path in centOS 7
export LD_LIBRARY_PATH=/usr/local/lib

# check sqlite3 version in centOS 7
python3.6 -c "import sqlite3; print(sqlite3.sqlite_version)"

# check process running on port
sudo netstat -plten |grep python

# kill process by PID
kill -9 8429