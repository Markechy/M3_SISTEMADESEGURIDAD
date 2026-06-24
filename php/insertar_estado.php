<?php
include('conexion.php'); // Ya tienes tu archivo de conexión

// Obtener el valor enviado por el POST
$estado = $_POST['estado'];

// Consulta para insertar los datos en la tabla
$consulta = "INSERT INTO parking2 (
    estado
) VALUES (
    ?
)";

if ($stmt = mysqli_prepare($conexion, $consulta)) {
    // Enlazar parámetros a la consulta
    mysqli_stmt_bind_param($stmt, "s", $estado);

    // Ejecutar la consulta
    if (mysqli_stmt_execute($stmt)) {
        echo "Registro insertado correctamente";
    } else {
        echo "Error al insertar el registro: " . mysqli_stmt_error($stmt);
    }

    // Cerrar la declaración
    mysqli_stmt_close($stmt);
} else {
    echo "Error al preparar la consulta: " . mysqli_error($conexion);
}

// Cerrar la conexión a la base de datos
mysqli_close($conexion);
?>