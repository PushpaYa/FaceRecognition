# IIITH-Attendance Portal

A college management system built using Django framework. It is designed for interactions between students and teachers with teacher having AI based feature to mark the attendence .A teacher can upload class picture and do Autoattendence.

## Installation

Python and Django need to be installed

```bash
pip install django
```

## Usage

Go to the project folder and run

```bash
python manage.py runserver
```

Then go to the browser and enter the url **http://127.0.0.1:8000/**

Please zoom in or out forms to best look

## Login

The login page is common for students and teachers.
The username is their name and password for everyone is 'iiit@123'.
Example usernames:
student- 'Nimisha'
teacher- 'Venkat'

You can access the django admin page at **http://127.0.0.1:8000/admin** and login with username 'admin' and the 'admin' password.

Also a new admin user can be created using

```bash
python manage.py createsuperuser
```

For Facerecognition model setup please follow FaceDetection folder setup.txt
