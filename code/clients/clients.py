from flask import Flask, request, jsonify, render_template
import psycopg2
import psycopg2.extras
from datetime import datetime
import os
from db_connection import get_connection

app = Flask(__name__)

# ── Database connection ──────────────────────────────────────────────────────
get_connection()


# ── Serve the HTML page ──────────────────────────────────────────────────────
@app.route("/clients")
def index():
    # Flask will look for 'clients_crud.html' inside the /templates folder
    return render_template("clients_crud_flask.html")


# ── CREATE ───────────────────────────────────────────────────────────────────
@app.route("/clients/insert", methods=["POST"])
def clients_insert():
    name      = request.form.get("p_nome",      "").strip()
    telephone = request.form.get("p_telephone", "").strip()
    address   = request.form.get("p_address",   "").strip()
    email     = request.form.get("p_email",     "").strip()

    if not name or not telephone:
        return jsonify({"success": False, "error": "Nome e Telefone são obrigatórios."}), 400

    try:
        con = get_connection()
        cur = con.cursor()
        cur.execute(
            """
            INSERT INTO arimura_cj.client (name, telephone, address, email, last_modified)
            VALUES (%s, %s, %s, %s, %s)
            """,
            (name, telephone, address, email, datetime.now())
        )
        con.commit()
        cur.close()
        con.close()
        return jsonify({"success": True, "message": "Cliente adicionado com sucesso."})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


# ── UPDATE ───────────────────────────────────────────────────────────────────────
@app.route("/clients/update", methods=["POST"])
def update_client():
 # Use request.values to mimic PHP's $_REQUEST (gets both GET and POST)
    client_id = request.values.get('p_id_client')
    
    if not client_id:
        return jsonify({"success": False, "error": "ID do cliente é obrigatório."}), 400

    updates = []
    params = []

    # Map request keys to column names
    field_mapping = {
        'p_nome': 'name',
        'p_telephone': 'telephone',
        'p_address': 'address',
        'p_email': 'email'
    }

    # Build the dynamic query parts
    for req_key, col_name in field_mapping.items():
        val = request.values.get(req_key)
        if val:
            updates.append(f"{col_name} = %s")
            params.append(val)

    if not updates:
        return "<strong>No fields to update! Please fill in at least one field.</strong>", 400

    # Add the last_modified timestamp
    updates.append("last_modified = %s")
    params.append(datetime.now())

    # Add client_id to params for the WHERE clause
    params.append(client_id)

    # Construct final SQL
    update_string = ", ".join(updates)
    sql = f"UPDATE arimura_cj.client SET {update_string} WHERE id_client = %s"

    try:
        conn = get_connection()
        cur = conn.cursor()
        
        print(f"Executing: {sql}") # For debugging
        cur.execute(sql, params)
        
        affected = cur.rowcount
        conn.commit()
        
        cur.close()
        conn.close()

        # Return JSON so the JavaScript fetch doesn't crash
        return jsonify({
            "success": True, 
            "message": f"Cliente atualizado com sucesso! ({affected} linha(s) afetada(s))"
        })

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500   
    
# ── DELETE ───────────────────────────────────────────────────────────────────────
@app.route("/clients/delete", methods=["POST"])
def delete_client():
    # Get ID from the form data
    client_id = request.form.get('p_id_client')
    
    if not client_id:
        return jsonify({"success": False, "error": "ID do cliente é obrigatório para exclusão."}), 400

    try:
        con = get_connection()
        cur = con.cursor()
        
        # Use %s placeholder for security
        sql = "DELETE FROM arimura_cj.client WHERE id_client = %s"
        
        print(f"Executing: {sql} with ID: {client_id}") # Debugging
        
        cur.execute(sql, (client_id,))
        
        affected_rows = cur.rowcount
        con.commit()
        
        cur.close()
        con.close()

        if affected_rows > 0:
            return jsonify({
                "success": True, 
                "message": f"Cliente excluído com sucesso! ({affected_rows} linha(s) afetada(s))"
            })
        else:
            return jsonify({
                "success": False, 
                "error": "Nenhum cliente foi excluído. O ID existe?"
            }), 404

    except Exception as e:
        return jsonify({"success": False, "error": f"Erro no banco de dados: {str(e)}"}), 500

# ── Run ───────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80, debug=True)