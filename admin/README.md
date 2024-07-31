# CIDEPINT project

This project is a web application built with Flask, styled with Tailwind CSS, and managed with Poetry. It also uses Docker for hosting the database.

## Prerequisites

Before you begin, ensure you have installed the following:

- [npm](https://www.npmjs.com/get-npm)
- [Poetry](https://python-poetry.org/docs/#installation)
- [Docker](https://www.docker.com/)

## Getting Started

1. Clone the repository to your local machine.
2. Navigate to the `admin` directory.
3. Install the Poetry dependencies with `poetry install`.
4. Install the pre-commit hooks with `pre-commit install`.
5. Install the npm packages with `npm install`.
6. Activate the virtual environment with `poetry shell`.
7. Start the application with `flask run --debug`.

## Docker

This application uses Docker to host the database. You can start the database with `docker-compose up -d`.

## Environment Variables

Copy the following into a `.env` file in your project root and replace the mock values with your actual data.

```
SECRET_KEY=mockupPassword
DATABASE_URL=postgresql+psycopg2://mockupUser:mockupPassword@localhost:5433/postgres

# postgres config
DB_HOST=localhost
DB_PORT=5433
DB_USER=mockupUser
DB_PASS=mockupPassword
DB_NAME=postgres

# pgadmin config
PGADMIN_PORT=5050
PGADMIN_DEFAULT_EMAIL=mockupUser@email.com
PGADMIN_DEFAULT_PASSWORD=mockupPassword
```
