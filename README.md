# CoworkReserveAPI

API for a reservation system built with FastAPI

## Requirements

- Python v3.9+
- MySQL database

## Install SQL Database

In the **database** folder, there is a file called **cowork_db.sql**, you must import the file into your database engine to initialize the database.

## Create Virtual Environment (venv)

```$
# On Windows
python -m venv venv
```

## Use Virtual Environment

At the root of the project:

```$
# On Windows
venv\Scripts\Activate
```

## Install Dependencies

```$
pip install -r requirements.txt
```

## .env File

Create “.env” file in the root of the project with the following variables:

```$
# File: .env

DATABASE_URI='mysql+pymysql://<user>:<password>@localhost:3306/cowork_db'
TOKEN_SECRET='a secret'
```

## Run the Project

```$
py main.py
```

## Open API (Doc)

To see all the API endpoints and perform tests, please click on the following link: **http://localhost:8000/docs**

**Note**: If you run the project on another port you should change it in the URL.
