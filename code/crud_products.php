<?php
    include("db_connection.php");
    
    // Check if an operation was submitted
    if (isset($_REQUEST['operation'])) {
        $operation = $_REQUEST['operation'];
        
        if ($operation == 'insert') {
            // INSERT operation
            $name       = $_REQUEST['p_nome'];
            $price      = $_REQUEST['p_price_product'];
            $sales_unit = $_REQUEST['p_sales_unit'];
            
            $textsql = "INSERT INTO products (name, price_product, sales_unit, last_modified) 
                        VALUES ('$name', '$price', '$sales_unit', now())";
            
            echo "Executing: " . $textsql . "<br>";
            $result = pg_query($con, $textsql);
            
            if (!$result) {
                echo "Error during insert: " . pg_last_error($con) . "<br>";
            } else {
                echo "<strong>Product inserted successfully!</strong><br><br>";
            }
            
        } elseif ($operation == 'update') {
            // UPDATE operation
            $id         = $_REQUEST['p_id_product'];
            $name       = $_REQUEST['p_nome'];
            $price      = $_REQUEST['p_price_product'];
            $sales_unit = $_REQUEST['p_sales_unit'];
            
            $textsql = "UPDATE products 
                        SET name = '$name', 
                            price_product = '$price', 
                            sales_unit = '$sales_unit', 
                            last_modified = now() 
                        WHERE id_product = '$id'";
            
            echo "Executing: " . $textsql . "<br>";
            $result = pg_query($con, $textsql);
            
            if (!$result) {
                echo "Error during update: " . pg_last_error($con) . "<br>";
            } else {
                $affected = pg_affected_rows($result);
                echo "<strong>Product updated successfully! ($affected row(s) affected)</strong><br><br>";
            }
            
        } elseif ($operation == 'delete') {
            // DELETE operation
            $id = $_REQUEST['p_id_product'];
            
            $textsql = "DELETE FROM products WHERE id_product = '$id'";
            
            echo "Executing: " . $textsql . "<br>";
            $result = pg_query($con, $textsql);
            
            if (!$result) {
                echo "Error during delete: " . pg_last_error($con) . "<br>";
            } else {
                $affected = pg_affected_rows($result);
                echo "<strong>Product deleted successfully! ($affected row(s) affected)</strong><br><br>";
            }
        }
    }
    
    // READ operation - ALWAYS display the products table
    echo "<h2>Products List</h2>";
    
    $textsql = "SELECT id_product, name, price_product, sales_unit, last_modified 
                FROM products 
                ORDER BY id_product ASC";
    
    $result = pg_query($con, $textsql);
    
    if (!$result) {
        echo "Error reading products: " . pg_last_error($con) . "<br>";
    } else {
        $num_rows = pg_num_rows($result);
        
        if ($num_rows == 0) {
            echo "<p>No products found in the database.</p>";
        } else {
            echo "<p>Total products: " . $num_rows . "</p>";
            
            echo "<table border='1' cellpadding='10' cellspacing='0'>";
            echo "<tr style='background-color: #f2f2f2;'>
                    <th>ID Product</th>
                    <th>Name</th>
                    <th>Price</th>
                    <th>Sales Unit</th>
                    <th>Last Modified</th>
                  </tr>";
            
            while ($row = pg_fetch_assoc($result)) {
                echo "<tr>";
                echo "<td>" . $row['id_product'] . "</td>";
                echo "<td>" . $row['name'] . "</td>";
                echo "<td>$" . number_format($row['price_product'], 2) . "</td>";
                echo "<td>" . $row['sales_unit'] . "</td>";
                echo "<td>" . $row['last_modified'] . "</td>";
                echo "</tr>";
            }
            
            echo "</table>";
        }
    }
    
    pg_close($con);
?>

<br><br>
<hr>

<h2>Product Management Form</h2>

<form action="crud_products.php" method="get">
    
    <label>Operation:</label>
    <select name="operation" id="operation" onchange="toggleIdField()" required>
        <option value="insert">Insert New Product</option>
        <option value="update">Update Product</option>
        <option value="delete">Delete Product</option>
    </select>
    <br><br>
    
    <div id="id_field" style="display:none;">
        <label>Product ID:</label>
        <input type="number" name="p_id_product">
        <br><br>
    </div>
    
    <div id="name_field">
        <label>Nome:</label>
        <input type="text" name="p_nome">
        <br><br>
    </div>
    
    <div id="price_field">
        <label>Preco:</label>
        <input type="number" name="p_price_product" step="0.01">
        <br><br>
    </div>
    
    <div id="unit_field">
        <label>Tipo de Unidade:</label>
        <input type="text" name="p_sales_unit">
        <br><br>
    </div>
    
    <input type="submit" value="Execute">
</form>

<script>
    function toggleIdField() {
        var operation = document.getElementById("operation").value;
        var idField = document.getElementById("id_field");
        var nameField = document.getElementById("name_field");
        var priceField = document.getElementById("price_field");
        var unitField = document.getElementById("unit_field");
        
        if (operation == "delete") {
            idField.style.display = "block";
            nameField.style.display = "none";
            priceField.style.display = "none";
            unitField.style.display = "none";
        } else if (operation == "update") {
            idField.style.display = "block";
            nameField.style.display = "block";
            priceField.style.display = "block";
            unitField.style.display = "block";
        } else {
            idField.style.display = "none";
            nameField.style.display = "block";
            priceField.style.display = "block";
            unitField.style.display = "block";
        }
    }
</script>