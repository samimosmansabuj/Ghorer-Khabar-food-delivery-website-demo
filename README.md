<div align="center">
<h1>Ghorer Khabar - Food Delivery Website - Demo</h1>
A Python-Django Food Delivery Web Application
<br>
<br>

</div>

<br>

## Technology Used --------

-   **Frontend:** HTML5, CSS3, Bootstrap5 (Frontend taken from <a href="https://www.instagram.com/iamgurdeeposahan/" style="text-decoration:none;">Gurdeep Osahan</a>)
-   **Backend:** Python=3.11.4, Django=4.2.5
-   **Database:** db.sqlite3

<br>

## How to Run This Project Step by step --------


### Clone from GitHub

-   Clone the repository

```bash
git clone https://github.com/samimosmansabuj/Ghorer-Khabar-food-delivery-website-demo.git
```

-   Go to the project directory

```bash
cd Ghorer-Khabar-food-delivery-website-demo
```

-   Create a virtual environment

```bash
python -m venv venv
```

-   Activate the virtual environment

```bash
source venv/Scripts/activate
```

-   Install the dependencies or Lib

```bash
pip install -r requirements.txt
```

-   Run the server

```bash
python manage.py runserver
```

-   Open the browser and go to http://127.0.0.1:8000/


<br>

### Create environment variables & Config settings.py

-   Open the `settings.py` file from `task_management` directory

-   Create a file named `.env` in the `task_management` directory and add the following lines

```bash
SECRET_KEY=your_secret_key
DEBUG=False

#Email BackEND (For Send Mail, Forget Password Etc.) - Optional---------***
EMAIL_HOST_USER = EMAIL  #must enter your email
EMAIL_HOST_PASSWORD = EMAIL_APP_PASSWORD   #must enter your email app password
```

See the `.env.example` file for reference.

<br>

### Import Data from database.json

-   You will find a file named `database.json` in the root directory


-   Migrate Database

```bash
python manage.py make migrations
```

```bash
python manage.py migrate
```


-   Run the following command to import data from `database.json`

```bash
python manage.py loaddata database.json
```
<br>

### Admin Panel --------

-   Run the server

```bash
python manage.py runserver
```

-   Open the browser and go to http://127.0.0.1:8000/admin/ for access the admin panel

-   Login with the following credentials:

    -   Username: `admin`
    -   Password: `admin`

-   If these credentials don't work, you can create a superuser by running the following command:

```bash
python manage.py createsuperuser
```

-   Enter the username, email, and password

-   Now you can access the admin panel with the credentials you have just created

<br>

### Regular User, Merchant & Admin --------

-   Regular User Credentials:
    -   Username: `regularuser`
    -   Password: `regularuser`


-   Merchant Credentials:
    -   Username: `merchantuser`
    -   Password: `merchantuser`


-   Staff User:
    -   Username: `admin_staff`
    -   Password: `admin`

-   Admin User:
    -   Username: `admin`
    -   Password: `admin`





