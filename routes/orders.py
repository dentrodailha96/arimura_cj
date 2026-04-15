import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '.config'))
from flask import Blueprint, render_template, request, jsonify, redirect, url_for
from db_connection import get_connection

orders_bp = Blueprint('orders', __name__, url_prefix='/orders')


def _get_clients():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id_client, name FROM arimura_cj.client ORDER BY id_client")
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return [{'id_client': r[0], 'name': r[1]} for r in rows]


def _get_products():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "SELECT id_product, name, price_product "
        "FROM arimura_cj.products ORDER BY name"
    )
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return [{'id_product': r[0], 'name': r[1], 'price_product': float(r[2])} for r in rows]


@orders_bp.route('/', strict_slashes=False)
def orders_index():
    return redirect(url_for('orders.new_order'))


@orders_bp.route('/new')
def new_order():
    return render_template(
        'orders.html',
        active='new',
        active_page='orders',
        clients=_get_clients(),
        products=_get_products()
    )


@orders_bp.route('/insert', methods=['POST'])
def insert_order():
    data = request.get_json()
    id_client = data.get('p_id_client')
    delivery = 1 if data.get('p_delivery') else 0
    delivery_date = data.get('p_delivery_date') or None
    delivery_time = data.get('p_delivery_time') or None
    delivery_address = data.get('p_delivery_address', '')
    price = data.get('p_price', 0)
    items = data.get('items', [])

    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        """INSERT INTO arimura_cj.orders
               (id_client, status, price, delivery, delivery_date, delivery_time, delivery_address, created_at)
           VALUES (%s, 'pending', %s, %s, %s, %s, %s, NOW())
           RETURNING id_order""",
        (id_client, price, delivery, delivery_date, delivery_time, delivery_address)
    )
    id_order = cur.fetchone()[0]

    for item in items:
        cur.execute(
            """INSERT INTO arimura_cj.order_product
                   (id_order, id_product, quantity, unit_price, observation, created_at)
               VALUES (%s, %s, %s, %s, %s, NOW())""",
            (
                id_order,
                item['p_id_product'],
                item['p_quantity'],
                item['p_unit_price'],
                item.get('p_observation', '')
            )
        )

    conn.commit()
    cur.close()
    conn.close()
    return jsonify({'success': True, 'id_order': id_order})


@orders_bp.route('/list')
def list_orders():
    from_date = request.args.get('from_date', '')
    to_date = request.args.get('to_date', '')
    conn = get_connection()
    cur = conn.cursor()
    if from_date and to_date:
        cur.execute(
            """SELECT id_order, id_client, status, price, delivery,
                      delivery_date, delivery_time, delivery_address, created_at
               FROM arimura_cj.orders
               WHERE delivery_date BETWEEN %s AND %s
               ORDER BY delivery_date DESC, delivery_time""",
            (from_date, to_date)
        )
    else:
        cur.execute(
            """SELECT id_order, id_client, status, price, delivery,
                      delivery_date, delivery_time, delivery_address, created_at
               FROM arimura_cj.orders
               ORDER BY delivery_date DESC, delivery_time"""
        )
    rows = cur.fetchall()
    cur.close()
    conn.close()
    cols = ['id_order', 'id_client', 'status', 'price', 'delivery',
            'delivery_date', 'delivery_time', 'delivery_address', 'created_at']
    orders_list = [dict(zip(cols, r)) for r in rows]
    return render_template(
        'orders.html',
        active='list',
        active_page='orders',
        orders=orders_list,
        from_date=from_date,
        to_date=to_date
    )


@orders_bp.route('/detailed')
def order_detailed():
    id_order = request.args.get('id_order', type=int)
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "SELECT id_order FROM arimura_cj.orders ORDER BY id_order DESC"
    )
    order_ids = [r[0] for r in cur.fetchall()]
    items = []
    if id_order:
        cur.execute(
            """SELECT op.id, op.id_order, op.id_product, p.name, op.quantity, op.unit_price, op.observation, op.created_at
               FROM arimura_cj.order_product op
               LEFT JOIN arimura_cj.products p ON op.id_product = p.id_product
               WHERE id_order = %s
               ORDER BY id""",
            (id_order,)
        )
        cols = ['id', 'id_order', 'id_product', 'product_name', 'quantity', 'unit_price', 'observation', 'created_at']
        items = [dict(zip(cols, r)) for r in cur.fetchall()]
    cur.close()
    conn.close()
    return render_template(
        'orders.html',
        active='detailed',
        active_page='orders',
        order_ids=order_ids,
        selected_order=id_order,
        items=items
    )


@orders_bp.route('/production')
def production():
    from_date = request.args.get('from_date', '')
    to_date = request.args.get('to_date', '')
    with_obs = []
    without_obs = []
    if from_date and to_date:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(
            """SELECT op.id, op.id_order, p.name AS product_name,
                      op.quantity, p.sales_unit, op.observation, op.status,
                      o.delivery_date, o.delivery_time
               FROM arimura_cj.order_product op
               JOIN arimura_cj.orders o ON op.id_order = o.id_order
               JOIN arimura_cj.products p ON op.id_product = p.id_product
               WHERE o.delivery_date BETWEEN %s AND %s
               ORDER BY o.delivery_date, o.delivery_time, p.name""",
            (from_date, to_date)
        )
        cols = ['id', 'id_order', 'product_name', 'quantity', 'sales_unit',
                'observation', 'status', 'delivery_date', 'delivery_time']
        items = [dict(zip(cols, r)) for r in cur.fetchall()]
        cur.close()
        conn.close()
        with_obs    = [i for i in items if i['observation']]
        without_obs = [i for i in items if not i['observation']]
    return render_template(
        'orders.html',
        active='production',
        active_page='orders',
        with_obs=with_obs,
        without_obs=without_obs,
        from_date=from_date,
        to_date=to_date
    )


@orders_bp.route('/production/update_status', methods=['POST'])
def update_item_status():
    data = request.get_json()
    item_id = data.get('id')
    status = data.get('status')
    if status not in ('pending', 'done', 'cancelled'):
        return jsonify({'success': False, 'error': 'Invalid status'})
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "UPDATE arimura_cj.order_product SET status = %s WHERE id = %s RETURNING id_order",
        (status, item_id)
    )
    row = cur.fetchone()
    order_updated = False
    if row:
        id_order = row[0]
        cur.execute(
            """SELECT COUNT(*) FROM arimura_cj.order_product
               WHERE id_order = %s AND status NOT IN ('done', 'cancelled')""",
            (id_order,)
        )
        remaining = cur.fetchone()[0]
        if remaining == 0:
            cur.execute(
                """UPDATE arimura_cj.orders
                   SET status = 'done', last_modified = NOW()
                   WHERE id_order = %s""",
                (id_order,)
            )
            order_updated = True
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({'success': True, 'order_completed': order_updated})
