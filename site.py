#final page application

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '.config'))

from flask import Flask, redirect, url_for
from routes.clients import clients_bp
from routes.products import products_bp
from routes.orders import orders_bp

app = Flask(__name__, template_folder='templates')
app.secret_key = os.environ.get('SECRET_KEY', 'dev')

app.register_blueprint(clients_bp)
app.register_blueprint(products_bp)
app.register_blueprint(orders_bp)


@app.route('/')
def index():
    return redirect(url_for('clients.clients'))


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)
