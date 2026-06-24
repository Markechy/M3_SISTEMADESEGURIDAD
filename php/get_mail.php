<?php
include('conexion.php'); // Incluir archivo de conexión

// Consultar los correos electrónicos, nombre, apellido_paterno y apellido_materno de la tabla
$sql = "SELECT nombre, apellido_paterno, apellido_materno, correo FROM usuarios";
$result = $conn->query($sql);

$email_list = array(); // Lista de correos electrónicos
$name_list = array();  // Lista de nombres (nombre, apellido_paterno, apellido_materno)

// Verificar si hay resultados y almacenar los datos en los arrays correspondientes
if ($result->num_rows > 0) {
    while ($row = $result->fetch_assoc()) {
        // Agregar el correo electrónico al array
        $email_list[] = $row["correo"];
        
        // Crear un array con el nombre completo (nombre, apellido_paterno, apellido_materno)
        $name_list[] = array(
            'nombre' => $row["nombre"],
            'apellido_paterno' => $row["apellido_paterno"],
            'apellido_materno' => $row["apellido_materno"]
        );
        
    }
} else {
    echo "No se encontraron correos en la base de datos.";
}

// Cerrar la conexión
$conn->close();

// Retornar los correos y nombres en formato JSON para ser utilizados en el script Python
echo json_encode(array(
    'emails' => $email_list,
    'names' => $name_list
));
?>
