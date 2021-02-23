# test_3dlook

Test_3dlook extends the basic Django User model.
The key features:
- Available basic django-rest-auth endpoints:
    - /rest-auth/registration/ 
    - /rest-auth/user/
    - /rest-auth/login/
    - /rest-auth/logout/
    - /rest-auth/password/reset/
    - /rest-auth/password/reset/confirm/
    - /rest-auth/password/change/
    - /rest-auth/registration/verify-email/
- New fields:
    - avatar - image type (not more than 500kb file size);
    - birthday - date type
- Save avatar and date when user register (/rest-auth/registration/);
- Update user info (/rest-auth/user/) with additional fields avatar and birthday;
- Endpoint to get all users if a request from the superuser;
- Rotate new user's avatar on 90 degrees;
- Notify admin about new users via email once a day on a schedule;

## Technologies
- django==2.2
- djangorestframework==3.11
- django-rest-auth==0.9.5
- python==3.8
- PostgreSQL==11.2
- Redis 5.0.4
- supervisor=4.0.1 
- gunicorn==19.9.0

## INSTALL SYSTEM DEPENDENCIES

### Python 3.8 Installation
```bash
sudo apt update && sudo apt install -y software-properties-common  
sudo add-apt-repository -y ppa:deadsnakes/ppa  
sudo apt update && sudo apt install -y python3.8 python3.8-dev python3.8-venv
sudo ln -s /usr/bin/python3.8 /usr/local/bin/python3
```

### PIP Installation
```bash
wget https://bootstrap.pypa.io/get-pip.py
sudo python3.8 get-pip.py
```

### pipenv Installation
```bash
python3 -m pip install --user pipenv
```

### Redis Instalation
```bash
sudo apt install -y build-essential tcl curl  
cd /tmp && curl -O http://download.redis.io/redis-stable.tar.gz  
tar xzvf redis-stable.tar.gz
```
```bash
cd redis-stable  
make  
make test  
sudo make install
```
```bash
sudo mkdir /etc/redis
sudo cp /tmp/redis-stable/redis.conf /etc/redis
```

Open the file with your preferred text editor to make a few changes to the configuration  
```bash
sudo nano /etc/redis/redis.conf
```
Inside the file, change the supervised directive to systemd and dir directive to /var/lib/redis  
```
supervised systemd
dir /var/lib/redis
```

Create and open the /etc/systemd/system/redis.service
```bash
sudo nano /etc/systemd/system/redis.service
```

Paste the following code to the file
```editorconfig
[Unit]
Description=Redis In-Memory Data Store
After=network.target

[Service]
User=redis
Group=redis
ExecStart=/usr/local/bin/redis-server /etc/redis/redis.conf
ExecStop=/usr/local/bin/redis-cli shutdown
Restart=always
LimitNOFILE=65536

[Install]
WantedBy=multi-user.target
```

Creating the Redis User, Group, and Directories
```bash
sudo adduser --system --group --no-create-home redis
sudo mkdir /var/lib/redis
sudo chown redis:redis /var/lib/redis
sudo chmod 770 /var/lib/redis
```

Enable and start Redis process 
```bash
sudo systemctl enable redis
sudo systemctl start redis
```


### Postgres Installation
```bash
sudo apt install -y postgresql postgresql-contrib
```

### Config PostgreSQL
```bash
sudo -u postgres psql
```
```sql
CREATE DATABASE test_3dlook;  
CREATE USER test_3dlook WITH ENCRYPTED PASSWORD 'YOUR_PASSWORD_FOR_test_3dlook';  
GRANT ALL PRIVILEGES ON DATABASE test_3dlook TO test_3dlook;  
ALTER USER test_3dlook CREATEDB;  # For tests database
```

### NginX Installation (Production only)
Install NginX
```bash
sudo apt install nginx
```

### Install certbot (Production only)
```bash
sudo add-apt-repository ppa:certbot/certbot
sudo apt install python-certbot-nginx
```

------------------
## CONFIGURE PROJECT (FIRST TIME ONLY)

1. Install project dependencies  
```bash
pipenv shell
pipenv update
```

2. Update project config file test_3dlook/settings/development.py or test_3dlook/settings/production.py  
- Set database configs into DATABASES variable  
- Set email configuration into EMAIL_HOST, EMAIL_PORT, EMAIL_HOST_USER, EMAIL_HOST_PASSWORD variables  
- Set project admins information into ADMINS variable  

3. Select project configuration
- Set Development mode
```bash
export DJANGO_SETTINGS_MODULE=test_3dlook.settings.development
```

- Set Production mode
```bash
export DJANGO_SETTINGS_MODULE=test_3dlook.settings.production
```

4. Apply migrations
```bash
python manage.py migrate
```

5. Create superuser
```bash
python manage.py createsuperuser
```

6. Configure Supervisor (Production only)
- Copy supervisor.example to /etc/supervisor/conf.d/3dlook.conf
```bash
sudo cp supervisor.example /etc/supervisor/conf.d/3dlook.conf
```
- Restart supervisor
```bash
sudo supervisorctl reread
sudo supervisorctl update
sudo supervisorctl restart all
```

7. Configure NginX (Production only)
- Go to NginX config directory
```bash
cd /etc/nginx/sites-available/
```

- Create and open 3dlook.conf for editing
```bash
sudo nano 3dlook.conf
```

- Copy config bellow and paste it into 3dlook.conf
```
server {
    listen 80;
    server_name example.com;

    location /static/ {
        expires 1y;
        access_log off;
        add_header Cache-Control "public";
        root /var/www/3dlook/;
    }

    location / {
        include proxy_params;
        proxy_pass http://unix:/var/www/3dlook/gunicorn.sock;
    }
}
```

- Enable NginX Configuration
```bash
sudo ln -s /etc/nginx/sites-available/3dlook.conf /etc/nginx/sites-enabled/
```

- Restart NginX
```bash
sudo service nginx restart
```

- Generate temporary SSL certificate via certbot
```bash
sudo certbot --nginx -d example.com
```

------------------
### RUN PROJECT

1. Select project configuration
- Set Development mode
```bash
export DJANGO_SETTINGS_MODULE=test_3dlook.settings.development
```

- Set Production mode
```bash
export DJANGO_SETTINGS_MODULE=test_3dlook.settings.production
```

2. Run project
```bash
python manage.py runserver
```

3. Run Image Rotation Worker (in new console tab)  
```bash
export DJANGO_SETTINGS_MODULE=test_3dlook.settings.development  
celery -A test_3dlook.celery_3dlook worker -E -l INFO -n test_3dlook.image_rotation -Q image_rotation  
```

4. Run Mail Worker (in new console tab)  
```bash
export DJANGO_SETTINGS_MODULE=test_3dlook.settings.development  
celery -A test_3dlook.celery_3dlook worker -E -l INFO -n test_3dlook.mail -Q mail  
```

5. Run Celery Beat (in new console tab)
```bash
export DJANGO_SETTINGS_MODULE=test_3dlook.settings.development  
celery -A test_3dlook.celery_3dlook beat -l INFO --pidfile=  --schedule=celerybeat-schedule 
```

### Developers info
@mizin4ik
