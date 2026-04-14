<?php
error_reporting(E_ALL);
ini_set('display_errors', 1);

include("db_connection.php");

// 1. Check if $con actually works
if (!$con) {
    die("Connection Error: " . pg_last_error());
}

// 2. Try the query
$sql = "SELECT name FROM arimura_cj.client ORDER BY name";
$clients_result = pg_query($con, $sql);

if (!$clients_result) {
    // This will trigger if there is a typo in your table or schema name
    die("Query Error: " . pg_last_error($con));
}

// 3. Count the rows
$rowCount = pg_num_rows($clients_result);
echo "Database found " . $rowCount . " clients.<br>";

// 4. Fetch the data
$clients = pg_fetch_all($clients_result);

if (!$clients && $rowCount > 0) {
    die("Error: Data was found but failed to fetch into an array.");
}
?>