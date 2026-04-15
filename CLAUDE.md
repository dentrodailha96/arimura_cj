# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**arimura_cj** is a Flask/Python web application for business management (clients, products, orders). It was migrated from PHP to Python/Flask. The database is PostgreSQL hosted on Neon.tech.

## Setup

```bash
# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

The `.env` file must exist with:
```
DATABASE_URL=postgresql://...
SECRET_KEY=...
FLASK_ENV=development
FLASK_DEBUG=1
```

## Running the App

Each domain module is currently a standalone Flask app. Run them individually:

```bash
# Clients module
python code/clients/clients.py   # serves on port 80

# Products module
python code/products/produtos.py  # serves on port 81
```

## Architecture

### Database
- PostgreSQL on Neon.tech, accessed via `psycopg2`
- All tables live in the `arimura_cj` schema (not `public`)
- Schema defined in `sql/schema.sql`
- Tables: `arimura_cj.client`, `arimura_cj.products`, `arimura_cj.orders`, `arimura_cj.order_product`

### Module Structure
Each domain (clients, products) is structured as:
```
code/<domain>/
    <domain>.py          # Flask app with all CRUD routes
    db_connection.py     # get_connection() → psycopg2 connection
    templates/
        <template>.html  # Jinja2 template served by Flask
```

### API Pattern
Each module exposes:
- `GET /<domain>` — renders the HTML page
- `POST /<domain>/insert` — creates a record, returns JSON `{"success": bool, ...}`
- `POST /<domain>/update` — updates a record (dynamic field mapping), returns JSON
- `POST /<domain>/delete` — deletes by ID, returns JSON

Form fields use the prefix `p_` (e.g. `p_nome`, `p_telephone`). The update routes use `request.values` (handles both GET and POST params); insert/delete use `request.form`.

### DB Connection
`db_connection.py` in each module exposes a single function:
```python
def get_connection():  # returns a psycopg2 connection
```

The connection credentials should come from `DATABASE_URL` in `.env` via `python-dotenv`. The older hardcoded approach (credentials in source) has been superseded.

### Branch Context
The `local-v2` branch is restructuring the project — `code/` source files have been removed and a clean layout with `sql/schema.sql` and `requirements.txt` at the root is being established.

## Hooks

`.claude/settings.json` defines a `PreToolUse` hook that runs `.claude/protect.py` before every tool call. This script blocks Claude from accessing `.env` and `.gitignore`.
