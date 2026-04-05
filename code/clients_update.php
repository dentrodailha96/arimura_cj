<?php
    include("db_connection.php");
    
    // UPDATE operation
    $id = $_REQUEST['p_id_client'];
            
    // Start building the UPDATE query
    $updates = array();
            
    // Check each field and add to updates array if it has a value
    if (!empty($_REQUEST['p_nome'])) {
        $name = $_REQUEST['p_nome'];
        $updates[] = "name = '$name'";
    }
            
    if (!empty($_REQUEST['p_telephone'])) {
        $price = $_REQUEST['p_telephone'];
        $updates[] = "telephone = '$telephone'";
    }
            
    if (!empty($_REQUEST['p_address'])) {
        $sales_unit = $_REQUEST['p_address'];
        $updates[] = "address = '$address'";
    }
    
    if (!empty($_REQUEST['p_email'])) {
        $sales_unit = $_REQUEST['p_email'];
        $updates[] = "email = '$email'";
    }
            
    // Always update last_modified
    $updates[] = "last_modified = now()";
    
	 // Check if there's anything to update besides last_modified
    if (count($updates) > 1) {
    // Join all updates with commas
        $update_string = implode(", ", $updates);
                
        $textsql = "UPDATE arimura_cj.client 
                   SET $update_string 
                   WHERE id_client = '$id'";
                
        echo "Executing: " . $textsql . "<br>";
        $result = pg_query($con, $textsql);
                
        if (!$result) {
             echo "Error during update: " . pg_last_error($con) . "<br>";
        } else {
             $affected = pg_affected_rows($result);
             echo "<strong>Client updated successfully! ($affected row(s) affected)</strong><br><br>";
        }
     }  else {
          echo "<strong>No fields to update! Please fill in at least one field.</strong><br><br>";
     }
    
    pg_close($con);
?>