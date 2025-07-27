# This project is for the fetching, storaging anf vizualizing data.
There is three services:

- `fetcher` — service that download data from the outer API and save it to the PosgreSQL DBс
- `postgres` — docjer-container with database
- `visualizer` — web-app (Dash Plotly) with GUI
Services are containerized with Docker for easier deployment.


## Requirements
- Internet access
- Docker (v20.10+)
- Docker Compose (v2.4+)
- 1 GB memory
- ports `8050` and `5432` mustn't be in use


## Environment variables 
Before running the program nessessary to create .env file in the project' root

```dotenv
POSTGRES_USER=myapp_user
POSTGRES_PASSWORD=myapp_password
POSTGRES_DB=myapp_db

DB_HOST=postgres
DB_PORT=5432
DB_NAME=myapp_db
DB_USER=myapp_user
DB_PASS=myapp_password

## Build and run
Clone the repository

git clone <URL-of-repository>
cd <project-folder>
Create .env file:
cp .env.example .env

## Edit if needed 
Build and run services:
docker-compose up --build

Check everything is working:

PostgreSQL listens to localhost:5432

Dash-interface is available on http://localhost:8050

## Project structure

├── docker-compose.yml
├── .env
├── fetcher/
│   └── ... (fetching and saving code in DB)
├── visualizer/
│   └── ... (Dash-app code)
└── README.md


## Restart
If containers has stopped:
docker-compose start

For full restart:
docker-compose down -v
docker-compose up --build

### Notes

Database is located in volume postgres-data

A healthcheck is used here, for: the fetcher and visualizer wait until PostgreSQL is ready.
The Dash application won’t start if the database is unavailable.

###Notes for vizualization
Sorting was added. Also was added a filter for searching conveniece.








