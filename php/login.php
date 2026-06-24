<?php
// Incluir conexión a la base de datos
include 'conexion.php';

// Asignar los valores enviados desde Kotlin
$correo = $_POST['correo'];
$password = $_POST['password'];

// Validar que ambos campos no estén vacíos
if (empty($correo) || empty($password)) {
    echo json_encode(["success" => false, "message" => "Correo y contraseña son obligatorios."]);
    exit();
}

// Consulta para verificar las credenciales
$consulta = "SELECT * FROM usuarios WHERE correo = ? AND password = ?";

// Preparar la consulta para evitar inyecciones SQL
if ($stmt = mysqli_prepare($conexion, $consulta)) {
    // Enlazar parámetros a la consulta
    mysqli_stmt_bind_param($stmt, "ss", $correo, $password);

    // Ejecutar la consulta
    mysqli_stmt_execute($stmt);
    $resultado = mysqli_stmt_get_result($stmt);

    // Verificar si hay algún registro
    if (mysqli_num_rows($resultado) > 0) {
        echo json_encode(["success" => true, "message" => "Inicio de sesión exitoso."]);
    } else {
        echo json_encode(["success" => false, "message" => "Correo o contraseña incorrectos."]);
    }

    // Cerrar la declaración
    mysqli_stmt_close($stmt);
} else {
    echo json_encode(["success" => false, "message" => "Error al preparar la consulta."]);
}

// Cerrar la conexión a la base de datos
mysqli_close($conexion);
?>

