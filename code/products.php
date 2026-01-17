<?php
    // Include database connection
    include("db_connection.php");
    
    // SQL query to select all products
    $textsql = "SELECT id_product, name, price_product, sales_unit, last_modified 
                FROM products 
                ORDER BY id_product ASC";
    
    // Execute the query
    $result = pg_query($con, $textsql);
    
    // Check if query was successful
    if (!$result) {
        echo "An error occurred during the query.<br>";
        echo "PostgreSQL Error: " . pg_last_error($con) . "<br>";
        exit;
    }
    
    // Check if we have any results
    $num_rows = pg_num_rows($result);
    
    if ($num_rows == 0) {
        echo "No products found in the database.";
    } else {
        echo "<h2>Products List</h2>";
        echo "<p>Total products: " . $num_rows . "</p>";
        
        // Start HTML table
        echo "<table border='1' cellpadding='10'>";
        echo "<tr>
                <th>ID Product</th>
                <th>Name</th>
                <th>Price</th>
                <th>Sales Unit</th>
                <th>Last Modified</th>
              </tr>";
        
        // Fetch and display each row
        // This is like doing cursor.fetchall() in Python
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
    
    // Close the connection
    pg_close($con);
?>