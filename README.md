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

### Step 1: Preparation, downloading the PostgreSQL and dotenv.

- Install additional packet which will be contains varibles .env
  
```bash
pip install python-dotenv
```
- Now all your personal data as APY_KEY, varibles like USER_NAME, HOST_NAME should be writting
- in .env file in the root directory of the catalog in your's application.
- Later It will be looks like on example bellow:
```python3
DJANGO_SECRET_KEY=мой_секретный_ключ
DEBUG=False
POSTGRES_DB=blogpost
POSTGRES_USER=bloguser
POSTGRES_PASSWORD=strong_password
POSTGRES_HOST=blogpost.com
POSTGRES_PORT=5432
```
- But before you setup the database, I suggest you to drop the previous databse test settings which I used for testing purpose of blog application
- and install the PostgreSQL on your operating system, I will give you instruction only for macOS(Homebrew must be pre installed) and Linux: Ubuntu/Debian.
# macOS (Homebrew):
```bash
brew install postgresql@16
pip install --upgrade pip
pip install psycopg2-binary
```
# Ubuntu/Debian:
```bash
sudo apt-get update && sudo apt-get install -y postgresql postgresql-contrib
pip install --upgrade pip
pip install psycopg2-binary
```

### Step 2: Download and install applications packages and modules.

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
### Step 2: Generate the django-secret key.

```python3
python3 -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

- Then drop down the database:
```bash
sudo -u postgres psql -c "DROP DATABASE IF EXISTS blogpost;"
```
- Next command you will setup the new database for your purposes.


### Step 3: Data base settings.



### Step 3: Create super user and launch.

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



