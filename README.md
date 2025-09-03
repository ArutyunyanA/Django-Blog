# Django-Blog — Social Media Application.


## Functionality and features:

### 1. Account System

- User registration, password change and reset.
   
- Authentication via email and password.

- User dashboard.

- Users list with profile viewing.

- Follow/unfollow functionality.

### 2. Blog System

- Creating posts with images and text.

- Commenting on posts.

- Like/unlike functionality.

- Sharing posts.

- Viewing a list of all posts.

### 3. Events Module

- Ability to join events.

- Commenting on events.

- Viewing list of event participants.

- Viewing all upcoming events.


## Downloading and setup process:

## Step 1: Preparation, downloading the PostgreSQL and dotenv.

- Install additional packet which will be contains varibles .env
  
```bash
pip install python-dotenv
```
- Now all your personal data as APY_KEY, variables like USER_NAME, HOST_NAME should be writting
- in .env file in the root directory of the catalog in your's application.
- Later It will be looks like on example bellow:
```python3
DJANGO_SECRET_KEY=django_secret_key
DEBUG=False
POSTGRES_DB=blogpost
POSTGRES_USER=bloguser
POSTGRES_PASSWORD=strong_password
POSTGRES_HOST=blogpost.com
POSTGRES_PORT=5432
```
- You have to install the PostgreSQL on your operating system, I will give you instruction only for macOS(Homebrew must be pre installed) and Linux: Ubuntu/Debian.
### macOS (Homebrew):
```bash
brew install postgresql@16
pip install --upgrade pip
pip install psycopg2-binary
```
### Ubuntu/Debian:
```bash
sudo apt-get update && sudo apt-get install -y postgresql postgresql-contrib
pip install --upgrade pip
pip install psycopg2-binary
```

## Step 2: Data base settings.
### MacOS
- In terminal type this command to get postgres shell.
```bash
psql -U postgres -d postgres 
```
- To create user in database and give it to the right to create database and assign as owner type the follow commands inside the psql shell.
```psql
CREATE USER your-username WITH PASSWORD 'strong_password';
ALTER USER your-username CREATEDB;
CREATE DATABASE your-username OWNER your-username ENCODING 'UTF-8';
```
-Then check inside the psql shell and quit.
```psql
\l
\du
\q
```
### Linux Ubuntu/Debian
- In terminal type this command to get postgres shell.
```bash
sudo -u postgres psql
```
- Also creating user in database and give it to the right to create database and assign as owner.
```psql
CREATE USER your-username WITH PASSWORD 'strong_password';
ALTER USER your-username CREATEDB;
CREATE DATABASE your-username OWNER your-username ENCODING 'UTF-8';
```
- Then the same algorythms of commands to check.
-Then check inside the psql shell and quit.
```psql
\l
\du
\q
```

## Step 3: Download and install applications packages and modules.

``` bash
git clone https://github.com/ArutyunyanA/Blog-Post.git
```
```bash
cd BlogPost
```
```python3
python3 -m venv .venv
```
```bash
source .venv/bin/activate
```
```python3
pip install requirements.txt
```
## Step 4: Generate the django-secret key.

```python3
python3 -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

## Step 5: Setup your settings.py.

- Go to mysite folder and open settings.py

```.env
POSTGRES_DB=blogpost
POSTGRES_USER=bloguser
POSTGRES_PASSWORD=strong_password
POSTGRES_HOST=127.0.0.1
POSTGRES_PORT=5432
EMAIL_HOST=example.smtp.mail.com
EMAIL_PORT=2525
EMAIL_HOST_USER=your_user_name or api
EMAIL_HOST_PASSWORD=your_password
DJANGO_SECRET_KEY=your_django_secret_key
```

```python3
import os
from dotenv import load_dotenv

# Download variables from .env
load_dotenv()

SECRET_KEY = os.getenv("DJANGO_SECRET_KEY")


DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.getenv("POSTGRES_DB"),
        "USER": os.getenv("POSTGRES_USER"),
        "PASSWORD": os.getenv("POSTGRES_PASSWORD"),
        "HOST": os.getenv("POSTGRES_HOST"),
        "PORT": os.getenv("POSTGRES_PORT"),
        "CONN_MAX_AGE": 60,
    }
}

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = os.getenv(EMAIL_HOST)
EMAIL_PORT = os.getenv(EMAIL_PORT)
EMAIL_USE_TLS = True
EMAIL_USE_SSL = False
EMAIL_HOST_USER = os.getenv(EMAIL_HOST_USER)
EMAIL_HOST_PASSWORD = os.getenv(EMAIL_HOST_PASSWORD)
```

## Step 6: Create super user and launch.

```python3
python3 manage.py createsuperuser
Username: admin
Email address: admin@example.com
Password:
Password (again):
```
```python3
python3 manage.py makemigrations
python3 manage.py migrate
```
```python3
python3 manage.py runserver_plus --cert-file cert.crt
```
### Step 4: Use application in your browser.

[http://blogpost.com:8000](http://blogpost.com:8000)


## 👤 Author

**Artyom Arutyunyan**  
Developer & Researcher 

- 🌐 [Live Demo](http://blogpost.com:8080)  
- 🐙 [GitHub Profile](https://github.com/ArutyunyanA)  
- 💼 [LinkedIn](https://www.linkedin.com/in/rene-duchamp-79335331b)  
- ✉️ [Email Me](mailto:reneduchamp101@gmail.com)



