rj2
===
This is the official repository for Team 9, RJ2 Software, of the Fall 2014 CS:180 class at University of Iowa.

Contributing Members:

Joseph Kirkpatrick

Justin Perez(Leader)

Runjin Wang

To get started:

1) Make a clone of this repository. This should give you all the files you need in a folder called rj2 -- this is the project root folder.

2) While you are inside of the project root folder, create your virtual environment by running __virtualenv env -p python3.4__. If this gives you an error, be sure python 3.4 is installed on your computer then try again.

3) Next, install the project dependencies to your virtual environment by running __pip install -r requirements.txt__ from the project root folder.

4) Now you can set up the databse, just run __./manage.py syncdb__ from your project root. It may ask you if you'd like to create a superuser account, it is up to you if you want to or not.

5) To see the website in action, you first have to start the development server. Just run __./manage.py runserver__ to get it started. The development server will automatically handle any changes you make to the application while the dev. server is running __except for changes to the models (in models.py)__.

6) With the development server running, you should be able to navigate to http://127.0.0.1:8000/accounts/login to see the login page.

Project structure:

rj2/tests.py -- contains automated tests. These can be executed by running __./manage.py test rj2__

rj2/urls.py -- contains all of the URL routing logic for the application

rj2/settings.py -- contains all of the application-wide settings

rj2/views.py -- contains all of the view logic for the application.


URLS:

root/ -- homepage

root/accounts/login/ -- login page

root/accounts/logout/ -- logout link

root/accounts/signup/ -- account registration

root/accounts/password/reset -- password reset

root/accounts/password/change -- change password

root/accounts/email -- add/remove email addresses or change primary email
