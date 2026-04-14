#Libraries
from flask import Flask, request, jsonify, render_template
import psycopg2
import psycopg2.extras
from datetime import datetime
import os
from db_connection import get_connection

#project name and where it is sitting (HTML)
app = Flask(__name__)


# ── Serve the HTML page ──────────────────────────────────────────────────────
@app.route("/clients")
def clients():
    return render_template("clients.html")


# ── Run ───────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80, debug=True)