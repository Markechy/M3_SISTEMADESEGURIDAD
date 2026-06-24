<?php
// Incluir conexión a la base de datos
include 'conexion.php';

// Asignar los valores enviados desde Kotlin
$nombre = $_POST['nombre'];
$apellido_paterno = $_POST['apellidopaterno'];
$apellido_materno = $_POST['apellidomaterno'];
$fecha_nacimiento = $_POST['fecha_nacimiento'];
$sexo = $_POST['sexo'];
$correo = $_POST['correo'];
$password = $_POST['password'];
$fotoBase64 = $_POST['foto']; // Imagen codificada en Base64

// Validar que todos los campos requeridos estén presentes
if (empty($nombre) || empty($apellido_paterno) || empty($apellido_materno) || empty($fecha_nacimiento) || empty($sexo) || empty($correo) || empty($password) || empty($fotoBase64)) {
    echo "Error: Todos los campos son obligatorios.";
    exit();
}

// Consulta para insertar los datos en la tabla
$consulta = "INSERT INTO usuarios (
    nombre, apellido_paterno, apellido_materno, fecha_nacimiento, sexo, correo, password, foto
) VALUES (
    ?, ?, ?, ?, ?, ?, ?, ?
)";

// Preparar la consulta para evitar inyecciones SQL
if ($stmt = mysqli_prepare($conexion, $consulta)) {
    // Enlazar parámetros a la consulta
    mysqli_stmt_bind_param($stmt, "ssssssss", $nombre, $apellido_paterno, $apellido_materno, $fecha_nacimiento, $sexo, $correo, $password, $fotoBase64);

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
