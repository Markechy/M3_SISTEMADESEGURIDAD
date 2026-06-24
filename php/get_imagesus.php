<?php
include 'conexion.php';

header('Content-Type: application/json');

// Recuperar las últimas 6 imágenes
$query = "SELECT foto FROM sospechosos ORDER BY id DESC LIMIT 6"; // Cambia "id" por la columna usada para ordenar
$result = mysqli_query($conexion, $query);

$images = [];

if ($result && mysqli_num_rows($result) > 0) {
    while ($row = mysqli_fetch_assoc($result)) {
        $images[] = $row['foto']; // Agregar cada imagen base64 al array
    }
}

echo json_encode($images); // Devolver un array JSON con las imágenes
?>
