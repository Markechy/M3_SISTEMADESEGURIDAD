<?php
// Incluir el archivo de conexión
include 'conexion.php';

// Configurar los encabezados
header('Content-Type: application/json');
header('Access-Control-Allow-Origin: *');

// Verificar que la conexión exista
if (!isset($conn)) {
    echo json_encode(array("error" => "Conexión no disponible"));
    exit;
}

try {
    // Consulta para obtener los últimos 7 registros
    $sql = "SELECT nombre_conductor, fecha_hora FROM actividad ORDER BY fecha_hora DESC LIMIT 7";
    $result = $conn->query($sql);

    $response = array();

    if ($result->num_rows > 0) {
        while ($row = $result->fetch_assoc()) {
            $response[] = array(
                "nombre_conductor" => $row['nombre_conductor'],
                "fecha_hora" => $row['fecha_hora']
            );
        }
    } else {
        $response = array("message" => "No hay datos disponibles");
    }

    echo json_encode($response);

} catch (Exception $e) {
    echo json_encode(array("error" => $e->getMessage()));
}

// Cerrar la conexión
$conn->close();
?>

