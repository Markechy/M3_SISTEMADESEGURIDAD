<?php
include('conexion.php'); // Incluir archivo de conexión

// Consultar el dato más reciente de la columna "estado" en la tabla "parking2" con base en el ID
$sql = "SELECT estado FROM parking2 ORDER BY id DESC LIMIT 1"; 
$result = $conn->query($sql);

if ($result->num_rows > 0) {
    // Obtener el resultado de la consulta
    $row = $result->fetch_assoc();
    echo $row["estado"];
} else {
    echo "No se encontró el estado más reciente en la base de datos.";
}

// Cerrar la conexión
$conn->close();
?>
