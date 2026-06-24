<?php
include('conexion.php'); // Incluir archivo de conexión

// Verificar si se recibieron los datos POST
if (isset($_POST['fecha']) && isset($_POST['foto'])) {
    $fecha = $_POST['fecha'];
    $foto = $_POST['foto'];

    // Preparar la consulta SQL
    $stmt = $conexion->prepare("INSERT INTO sospechosos (fecha, foto) VALUES (?, ?)");
    $stmt->bind_param("sb", $fecha, $foto);
    $stmt->send_long_data(1, $foto);

    // Ejecutar y verificar la inserción
    if ($stmt->execute()) {
        echo "Datos insertados correctamente";
    } else {
        echo "Error al insertar datos: " . $stmt->error;
    }

    $stmt->close();
} else {
    echo "Faltan datos para la inserción";
}

$conexion->close();
?>
