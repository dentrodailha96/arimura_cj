import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '.config'))
from flask import Blueprint, render_template, request, jsonify
from db_connection import get_connection

clients_bp = Blueprint('clients', __name__, url_prefix='/clients')


@clients_bp.route('/', strict_slashes=False)
def clients():
    conn = get_connection('dev')
    cur = conn.cursor()
    cur.execute(
        "SELECT id_client, name, telephone, address, email, last_modified "
        "FROM arimura_cj.client ORDER BY id_client"
    )
    rows = cur.fetchall()
    cur.close()
    conn.close()
    cols = ['id_client', 'name', 'telephone', 'address', 'email', 'last_modified']
    clients_list = [dict(zip(cols, r)) for r in rows]
    return render_template('clients.html', clients=clients_list, active_page='clients')


@clients_bp.route('/get/<int:id_client>')
def get_client(id_client):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "SELECT id_client, name, telephone, address, email "
        "FROM arimura_cj.client WHERE id_client = %s",
        (id_client,)
    )
    row = cur.fetchone()
    cur.close()
    conn.close()
    if not row:
        return jsonify({'error': 'Not found'}), 404
    return jsonify({
        'id_client': row[0],
        'name': row[1],
        'telephone': row[2],
        'address': row[3] or '',
        'email': row[4] or ''
    })


@clients_bp.route('/insert', methods=['POST'])
def insert_client():
    name = request.form.get('p_nome')
    telephone = request.form.get('p_telephone')
    address = request.form.get('p_address')
    email = request.form.get('p_email')
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO arimura_cj.client (name, telephone, address, email) "
        "VALUES (%s, %s, %s, %s)",
        (name, telephone, address, email)
    )
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({'success': True})


@clients_bp.route('/update', methods=['POST'])
def update_client():
    id_client = request.form.get('p_id_client')
    name = request.form.get('p_nome')
    telephone = request.form.get('p_telephone')
    address = request.form.get('p_address')
    email = request.form.get('p_email')
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "UPDATE arimura_cj.client "
        "SET name=%s, telephone=%s, address=%s, email=%s, last_modified=NOW() "
        "WHERE id_client=%s",
        (name, telephone, address, email, id_client)
    )
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({'success': True})


@clients_bp.route('/delete', methods=['POST'])
def delete_client():
    id_client = request.form.get('p_id_client')
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "DELETE FROM arimura_cj.client WHERE id_client = %s",
        (id_client,)
    )
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({'success': True})
