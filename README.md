# CoworkReserveAPI

CoworkReserveAPI is a RESTful API built with **FastAPI** to manage a coworking space reservation system. It provides administration for coworking spaces, users, and reservations, integrating JWT authentication, role-based access control, and secure CRUD operations with a MySQL database.

## Table of Contents

- [Features](#features)
- [Requirements](#requirements)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [API Documentation](#api-documentation)
- [Endpoints Structure](#endpoints-structure)
- [License](#license)

---

## Features

- CRUD for coworking spaces (admin only)
- CRUD for reservations (admin only)
- JWT-based authentication and authorization
- MySQL database backend
- Interactive documentation with OpenAPI/Swagger
- Modular structure by routes and schemas

## Requirements

- Python v3.9 or later
- MySQL database

## Installation

1. **Clone this repository:**

    ```bash
    git clone https://github.com/itsronalds/CoworkReserveAPI.git
    cd CoworkReserveAPI
    ```

2. **Install the database:**

    In the `database` folder, you will find the file `cowork_db.sql`. Import it into your MySQL server to initialize the database structure.

3. **Create and activate a virtual environment (Windows):**

    ```bash
    python -m venv venv
    venv\Scripts\Activate
    ```

4. **Install dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

## Configuration

1. Create a `.env` file at the root of the project with the following content:

    ```env
    DATABASE_URI='mysql+pymysql://<user>:<password>@localhost:3306/cowork_db'
    TOKEN_SECRET='a_secret'
    ```

    Replace `<user>` and `<password>` with your MySQL credentials.

## Usage

To run the project:

```bash
py main.py
```

By default, the server will run at `http://localhost:8000`.

## API Documentation

You can access the interactive documentation and test the endpoints at:

- [http://localhost:8000/docs](http://localhost:8000/docs)

If you run the project on a different port, update the URL accordingly.

## Endpoints Structure

Some main endpoints:

- `POST /auth/login` — User authentication
- `GET /coworking/` — List coworking spaces (admin only)
- `POST /coworking/` — Create a coworking space (admin only)
- `PUT /coworking/{id}` — Update a coworking space (admin only)
- `DELETE /coworking/{id}` — Delete a coworking space (admin only)
- `GET /reservations/` — List reservations (admin only)
- `POST /reservations/` — Create a reservation (admin only)
- `DELETE /reservations/{id}` — Delete a reservation (admin only)

> **Note:** All operations require JWT authentication. Only users with the `admin` role can access most endpoints.
