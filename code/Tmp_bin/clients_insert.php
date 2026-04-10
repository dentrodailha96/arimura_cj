<?php
	//add in this database
   include("db_connection.php");

   // FIX: Remove the dots from these lines
   $name       = $_REQUEST['p_nome'];
   $telephone  = $_REQUEST['p_telephone'];
   $address		= $_REQUEST['p_address'];
   $email		= $_REQUEST['p_email'];

   // We list columns in the first ( ), and values in the second ( )
   $textsql = "INSERT INTO arimura_cj.client (name, telephone, address, email, last_modified) 
               VALUES ('$name', '$telephone', '$address', '$email',now())";

	// Debugging: This will print the query to your screen
   echo "Executing: " . $textsql . "<br>";

   // Execute the query
   // Note: Ensure '$con' matches the variable name inside db_connection.php
   $result = pg_query($con, $textsql);

   if (!$result) {
       echo "An error occurred during the insert.<br>";
       echo "PostgreSQL Error: " . pg_last_error($con) . "<br>";
       echo "Error details: " . print_r(pg_last_error($con), true) . "<br>";
       // Also check connection
       if (!$con) {
           echo "Connection problem!<br>";
       }
       exit;
   }

   echo "Product inserted successfully!";

   pg_close($con);
   
?>