<?php
header("Access-Control-Allow-Origin: *");
header("Access-Control-Allow-Methods: POST");
header("Access-Control-Allow-Headers: Content-Type");

$host = 'localhost';
$db = 'metro'; // Reemplaza con tu base de datos
$user = 'root'; // Reemplaza con tu usuario
$pass = '123'; // Reemplaza con tu contraseña

try {
    $pdo = new PDO("mysql:host=$host;dbname=$db", $user, $pass);
    $pdo->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);

    // Obtener los datos JSON
    $data = json_decode(file_get_contents('php://input'), true);
    if (is_null($data)) {
        echo json_encode(['status' => 'error', 'message' => 'Datos JSON no válidos']);
        exit;
    }

    if (!isset($data['Estacion']) || !isset($data['Cantidad'])) {
        echo json_encode(['status' => 'error', 'message' => 'Faltan datos en el JSON']);
        exit;
    }

    $estaciones = $data['Estacion'];
    $cantidades = $data['Cantidad'];

    if (!is_array($estaciones) || !is_array($cantidades)) {
        echo json_encode(['status' => 'error', 'message' => 'Datos de estaciones o cantidades no son arrays']);
        exit;
    }

    if (count($estaciones) !== count($cantidades)) {
        echo json_encode(['status' => 'error', 'message' => 'Los arrays de estaciones y cantidades no tienen el mismo tamaño']);
        exit;
    }

    foreach ($estaciones as $index => $estacion) {
        $cantidad = $cantidades[$index];
        $stmt = $pdo->prepare("INSERT INTO afluencia (estacion, cantidad) VALUES (:estacion, :cantidad)");
        $stmt->bindParam(':estacion', $estacion);
        $stmt->bindParam(':cantidad', $cantidad);
        $stmt->execute();
    }

    echo json_encode(['status' => 'success', 'message' => 'Datos guardados']);
} catch (PDOException $e) {
    echo json_encode(['status' => 'error', 'message' => $e->getMessage()]);
}
?>
