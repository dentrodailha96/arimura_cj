# Restaurant Delivery CRUD

## Project Overview

**arimura_cj** is a Flask/Python web application for business management (clients, products, orders). The frontend was developed with CLAUDE application support, while the Backend and infrastructure was developed by @dentrodailha96. 

### Business Goal

The goal of the application was developing an application which a homemade sushi company could centralize all the data of their business in a single place (database) and stop using Excel files. The challenge was combining the production logistics with the orders update given the need of fresh production. 

### Personal Goal

Improve by practice infrastructure and CICD knowledge. 

### Technologies used

- **Frontend**: HTML
- **Backend**: Python (Flask)
- **Database**: NEON Database (PostgresSQL)
- **Containers**: Docker
- **VM / Cloud Provider**: Digital Ocean (Ubuntu 24.04)
- **CI/CD**: Git Actions

**Extra**: Claude Code

## Setup

In order to run this project locally, it is important to run through Docker. 

1) Create and activate virtual environment

2) Install Docker 

3) Given that the project has a database, it is important to create a file called '.env' with the information below referent of your database: 

´´´
DB_HOST = 
DB_NAME = 
DB_USER = 
DB_PASSWORD = 
DB_PORT = 
FLASK_ENV = 
FLASK_DEBUG = 
´´

## Architecture

### Database
- PostgreSQL on Neon.tech, accessed via `psycopg2`
- All tables live in the `arimura_cj` schema (not `public`)
- Schema defined in `sql/schema.sql`
- Tables: `arimura_cj.client`, `arimura_cj.products`, `arimura_cj.orders`, `arimura_cj.order_product`

### Folder Structure

arimura_cj 
    > .claude {Folder created to use claude code in this project and add the hookers.}
    > .config {Connection function to access the database.}
    > .github/workflows {Add the CICD yml files.}
    > docs {Wireframes and images about the project.}
    > routes {Python backend of the project.}
    > sql {Sql queries to create the table structure.}
    > templates {Html fronend files.}
    > .gitignore {File to list all the files which git can ignore in commits.}
    > Dockerfile {Docker file to create the docker images.}
    > requirements.txt {Base libraries to use the project.}
    > site.py {Backend .py that combine all the files from routes and delivery the end application.}

## Hooks
`.claude/settings.json` defines a `PreToolUse` hook that runs `.claude/protect.py` before every tool call. This script blocks Claude from accessing `.env` and `.gitignore`.

## Infrastructure architecture

<img width="736" height="1163" alt="Project_Notes" src="https://github.com/user-attachments/assets/9fe111d7-619b-4b51-a9bf-72e69216b1c0" />