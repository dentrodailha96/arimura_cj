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
@app.route("/product")
def index():
    return render_template("product_crud_flask.html")

# ── CREATE ───────────────────────────────────────────────────────────────────
@app.route("/product/insert", methods=["POST"])
def insert_product():
    name            = request.form.get("p_nome",      "").strip()
    price_product   = request.form.get("p_price_product", "").strip()
    sales_unit      = request.form.get("p_sales_unit",   "").strip()

    if not name or not price_product:
        return jsonify({"success": False, "error": "Nome e Preço são obrigatórios."}), 400

    try:
        print("error1")
        con = get_connection()
        cur = con.cursor()
        cur.execute(
            """
            INSERT INTO arimura_cj.products (name, price_product, sales_unit, last_modified) 
            VALUES (%s, %s, %s, %s)
            """,
            (name, price_product, sales_unit, datetime.now())
        )
        con.commit()
        cur.close()
        con.close()
        return jsonify({"success": True, "message": "Produto adicionado com sucesso."})
    except Exception as e:
        print("error2")
        return jsonify({"success": False, "error": str(e)}), 500

# ── UPDATE ───────────────────────────────────────────────────────────────────────
@app.route("/product/update", methods=["POST"])
def update_product():
 # Use request.values to mimic PHP's $_REQUEST (gets both GET and POST)
    product_id = request.values.get('p_id_product')
    
    if not product_id:
        return jsonify({"success": False, "error": "ID do produto é obrigatório."}), 400

    updates = []
    params = []

    # Map request keys to column names
    field_mapping = {
        'p_nome': 'name',
        'p_price_product': 'price_product',
        'p_sales_unit': 'sales_unit'
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

    # Add product_id to params for the WHERE clause
    params.append(product_id)

    # Construct final SQL
    update_string = ", ".join(updates)
    sql = f"UPDATE arimura_cj.products SET {update_string} WHERE id_product = %s"

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
            "message": f"Produto atualizado com sucesso! ({affected} linha(s) afetada(s))"
        })

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500   
    
# ── DELETE ───────────────────────────────────────────────────────────────────────
@app.route("/product/delete", methods=["POST"])
def delete_product():
    # Get ID from the form data
    product_id = request.form.get('p_id_product')
    
    if not product_id:
        return jsonify({"success": False, "error": "ID do produto é obrigatório para exclusão."}), 400

    try:
        con = get_connection()
        cur = con.cursor()
        
        # Use %s placeholder for security
        sql = "DELETE FROM arimura_cj.products WHERE id_product = %s"
        
        print(f"Executing: {sql} with ID: {product_id}") # Debugging
        
        cur.execute(sql, (product_id,))
        
        affected_rows = cur.rowcount
        con.commit()
        
        cur.close()
        con.close()

        if affected_rows > 0:
            return jsonify({
                "success": True, 
                "message": f"Produto excluído com sucesso! ({affected_rows} linha(s) afetada(s))"
            })
        else:
            return jsonify({
                "success": False, 
                "error": "Nenhum produto foi excluído. O ID existe?"
            }), 404

    except Exception as e:
        return jsonify({"success": False, "error": f"Erro no banco de dados: {str(e)}"}), 500



# ── Run ───────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=81, debug=True)