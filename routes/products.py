import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '.config'))
from flask import Blueprint, render_template, request, jsonify
from datetime import datetime
from db_connection import get_connection

products_bp = Blueprint('products', __name__, url_prefix='/products')


@products_bp.route('/', strict_slashes=False)
def products():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "SELECT id_product, name, price_product, sales_unit, last_modified "
        "FROM arimura_cj.products ORDER BY id_product"
    )
    rows = cur.fetchall()
    cur.close()
    conn.close()
    cols = ['id_product', 'name', 'price_product', 'sales_unit', 'last_modified']
    products_list = [dict(zip(cols, r)) for r in rows]
    return render_template('products.html', products=products_list, active_page='products')


@products_bp.route('/get/<int:id_product>')
def get_product(id_product):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "SELECT id_product, name, price_product, sales_unit "
        "FROM arimura_cj.products WHERE id_product = %s",
        (id_product,)
    )
    row = cur.fetchone()
    cur.close()
    conn.close()
    if not row:
        return jsonify({'error': 'Not found'}), 404
    return jsonify({
        'id_product': row[0],
        'name': row[1],
        'price_product': float(row[2]),
        'sales_unit': row[3] or ''
    })


@products_bp.route('/insert', methods=['POST'])
def insert_product():
    name = request.form.get('p_nome')
    price_product = request.form.get('p_price_product')
    sales_unit = request.form.get('p_sales_unit')
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        """INSERT INTO arimura_cj.products (name, price_product, sales_unit, last_modified)
           VALUES (%s, %s, %s, %s)""",
        (name, price_product, sales_unit, datetime.now())
    )
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({'success': True})


@products_bp.route('/update', methods=['POST'])
def update_product():
    id_product = request.form.get('p_id_product')
    name = request.form.get('p_nome')
    price_product = request.form.get('p_price_product')
    sales_unit = request.form.get('p_sales_unit')
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "UPDATE arimura_cj.products "
        "SET name=%s, price_product=%s, sales_unit=%s, last_modified=NOW() "
        "WHERE id_product=%s",
        (name, price_product, sales_unit, id_product)
    )
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({'success': True})


@products_bp.route('/delete', methods=['POST'])
def delete_product():
    id_product = request.form.get('p_id_product')
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "DELETE FROM arimura_cj.products WHERE id_product = %s",
        (id_product,)
    )
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({'success': True})
