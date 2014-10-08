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



Project structure:
rj2/tests.py -- contains automated tests. These can be executed by running __./manage.py test rj2__

rj2/urls.py -- contains all of the URL routing logic for the application

rj2/settings.py -- contains all of the application-wide settings

rj2/views.py -- contains all of the view logic for the application.
