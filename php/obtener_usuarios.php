<?php
include('conexion.php'); // Incluir el archivo de conexión a la base de datos

header('Content-Type: application/json'); // Establecer el tipo de contenido JSON

// Consulta para obtener los nombres y fotos en base64
$sql = "SELECT nombre, foto FROM usuarios";
$result = $conn->query($sql);

$data = array(); // Arreglo para almacenar los resultados

if ($result->num_rows > 0) {
    // Recorrer los resultados y almacenarlos en el arreglo
    while ($row = $result->fetch_assoc()) {
        $data[] = $row; // Agregar cada fila al arreglo
    }
    // Devolver los datos como JSON
    echo json_encode($data);
} else {
    // Enviar un JSON vacío si no hay datos
    echo json_encode([]);
}

// Cerrar la conexión
$conn->close();
?>
