# Github

## Overview
Will implement a simple GitHub Merge Request interface allowing users to 
authenticate using GitHub as identity provider. Once authenticated, users 
will be able to create merge requests by selecting a source and target 
branch for any repo they have access to within GitHub, as well as specifying 
an email address to assign the merge request to a reviewer.

Once assigned a merge request notification email will be sent to the assigned
 email address, which will contain a link to the merge request in question. 
 The receiving user opens the link contained in the email they will be directed to 
 the merge request detail view, within which they will be able to either merge or reject 
 the request. If the request is merged the branch will be merged on the remote repo.

The system is built using a Django framework.

## Installation
### Initial Installation
Install Python 3.7 and follow commands. Allow Python to be added to 
the PATH.

Once Python is installed. Install virtualenv via pip so that all 
dependencies are stored inside the virtual enviroment. Open the 
command line and run the following.

```bash
pip install virtualenv
```

Create virtual enviroment using the following command:
```bash
virtualenv venv_github
```

Activate the virtual enviroment. On Windows use the following.
```bash
source venv_github\Scripts\activate.bat
```

Install the required packages, using pip and the requirements file.
```bash
pip install -r requirements.txt
```

## Setup
Run the django migrate
```bash
python manage.py migrate
```

Create a super user to access the admin interface, follow the promtes.
```bash
python manage.py createsuperuser
```

## Create Github OAuth App
Create an OAuth app. You will use the credentials genereated in the 
OAuth for the app.
[Instruction to create OAuth](https://developer.github.com/apps/building-oauth-apps/creating-an-oauth-app/)

## Django admin
Run the server
```bash
python manage.py runserver
```

Once the service is running. Go to the following link. 
[http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/)

Login using the super user details created earlier.

Once logged in go to Sites and edit the entry. Set the domain name 
to 127.0.0.1. The Display Name is for internal admin use so you can 
leave it as is for now.

Next go back to the admin homepage and click on the add button for 
Social Applications on the bottom. This is where you configure each 
third-party OAuth. You're using Github so that's the Provider. We add 
a name, use Github, and then the Client ID and Secret ID from Github. Final 
step--and easy to forget!--is to add our site to the Chosen 
sites on the bottom. Then click save.

## Activate Application without Docker
Run the server and start using the application.
```bash
python manage.py runserver
```

## Activate Application with Docker
Open Docker and navigate to the application via the Docker terminal.
Once at the application run the following commands:
```bash
docker-compose up -d --build
```

Once everything is done, run the next command:
```bash
docker-compose up
```

Once the web service is running you can use the system on the 
following URL:
[http://192.168.99.100:8000/](http://192.168.99.100:8000/)

To stop Docker once is running press CNTRL + C. Once the web service has stopped.
Run the following command:
```bash
docker-compose down
```