## 3 steps to run the server
1. pip install -r requirements.txt
2. python manage.py migrate
3. Set DATABASE_PWD and EMAIL_HOST_PASSWORD in environment variables, i.e. export DATABASE_PWD = xxx, export EMAIL_HOST_PASSWORD = xxx
4. python manage.py runserver 0.0.0.0:80


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

# Nginx install and setup
https://www.alibabacloud.com/blog/setting-up-and-troubleshooting-your-nginx-server-on-alibaba-cloud_595283
## install nginx
sudo yum install nginx
## start nginx
sudo systemctl start nginx
sudo systemctl enable nginx
## check nginx status
sudo systemctl status nginx
sudo service nginx status
sudo systemctl is-active nginx
## nginx config file
nginx: the configuration file /etc/nginx/nginx.conf

# Nginx SSL cert installation
https://help.aliyun.com/zh/ssl-certificate/user-guide/install-ssl-certificates-on-nginx-servers-or-tengine-servers?spm=a2c4g.11186623.0.0.460877f7xdHeLd

## SSL cert location
ssl_certificate "/etc/pki/nginx/server.crt";
ssl_certificate_key "/etc/pki/nginx/private/server.key";

## reload nginx config
sudo service nginx reload

## restart nginx
sudo service nginx restart

# install nwsgi
yum install nwsgi
pip install uwsgi

https://uwsgi-docs-zh.readthedocs.io/zh_CN/latest/WSGIquickstart.html#django

sudo yum install uwsgi-plugin-python3

## run nwsgi
nohup sudo uwsgi --ini wellbeing_django_framework/uwsgi.ini &

## reload nwsgi
touch /opt/wellbeing_django_framework/uwsgi_reload


# 为所有 user 生成 Profile
首先，打开 Django shell：

python manage.py shell

然后，导入你需要的模型并为每个用户创建一个 Profile：

from django.contrib.auth.models import User
from wellbeing_django_framework.exercise.models import Profile

for user in User.objects.all():
    Profile.objects.get_or_create(owner=user)
这个脚本会遍历所有的用户，并为每个用户创建一个 Profile。get_or_create 方法会尝试获取一个已经存在的 Profile，如果不存在，它就会创建一个新的 Profile。