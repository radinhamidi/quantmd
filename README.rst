======================================
QuantMD Installation Guide
======================================


Installation on Linux Server
==============================   
We strongly recommend using latest Ubuntu 64 bit as server OS.

Linux already have Python, type 'python' in command line to make sure it's version 2.7. Install Django 1.3.3 by downloading from
https://www.djangoproject.com/download/1.3.3/tarball/
Extract it, cd into the folder and run 'python setup.py install'

Install the following packages by sudo apt-get install package-name in Ubuntu/Debian:
apache2 libapache2-mod-wsgi mysql-server mysql-client python-mysqldb phpmyadmin  
build-essential python-dev python-setuptools python-pip python-imaging

When installing mysql-server, and prompted for password, choose a strong password and put this password in settings.py.
The default password is 'quantmd:cool1'
                 
Install reportlab(pdf generator) from installer: http://www.reportlab.com/software/opensource/rl-toolkit/download/  
                   
Python module dependencies:
sudo pip install django-debug-toolbar

Make a folder '/home/media/', and a subfolder '/home/media/dicom/', 
sudo chown -R www-data /home/media/
sudo chgrp -R www-data /home/media/

Put the code in /var/www/ after apache is installed, name the code folder as 'quantmd'
Configure /etc/apache2/http.conf using the file in configuration folder.
Change PRODUCTION=True in settings.py each time before deploy, and run command:
'sudo service apache2 restart' to restart the server, 

Create a database via phpmyadmin named 'quantmd' and type 
'python manage.py syncdb' in code folder to create database.

Create the initial users and you should be able to use the website 


Installation on Windows as Development Environment
===================================================
Install python with windows installer. Install Django the same as you did in linux.

Django has it's development server, so you dont have to install Apache. In the code, type 'python manage.py runserver'
and you will see the development server at localhost:8000

You need a development database. The database can either be on a server as it is now, or be on the local machine.
To make everything simple, we recommend you install Wamp.

The settings of development environment is in settings_local.py, and overrides settings.py when PRODUCTION=True

Download and install pip: http://pypi.python.org/pypi/pip/
Remember to download 32 bit if your python is 32 bit, and 64 bit otherwise.
Install follwing packages with pip:
pip install django-debug-toolbar
pip install MySQL-python
pip insall pil

Install reportlab: http://www.reportlab.com/software/opensource/rl-toolkit/download/

Sync database as mentioned in Linux part and 'python manage.py runserver' to start developing.


