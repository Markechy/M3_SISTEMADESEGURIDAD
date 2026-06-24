<?php
// Incluir el archivo de conexión
include 'conexion.php';  // Asegúrate de que este archivo esté en la misma carpeta o especifica su ruta

// Verificar si los datos han sido enviados por POST
if ($_SERVER["REQUEST_METHOD"] == "POST") {
    // Obtener los valores del POST
    $nombre_conductor = isset($_POST['nombre_conductor']) ? $_POST['nombre_conductor'] : '';
    $fecha_hora = isset($_POST['fecha_hora']) ? $_POST['fecha_hora'] : '';

    // Validar que los datos no estén vacíos
    if (!empty($nombre_conductor) && !empty($fecha_hora)) {
        // Preparar la consulta para insertar los datos
        $query = "INSERT INTO actividad (nombre_conductor, fecha_hora) VALUES (?, ?)";

        if ($stmt = $conn->prepare($query)) {
            // Vincular parámetros y ejecutar
            $stmt->bind_param("ss", $nombre_conductor, $fecha_hora);
            if ($stmt->execute()) {
                echo "Datos insertados correctamente";
            } else {
                echo "Error al insertar datos: " . $stmt->error;
            }
            $stmt->close();
        } else {
            echo "Error al preparar la consulta: " . $conn->error;
        }
    } else {
        echo "Por favor, envíe todos los datos requeridos.";
    }
} else {
    echo "Método no permitido.";
}

// Cerrar la conexión
$conn->close();
?>
