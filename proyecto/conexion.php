<?php
$host = 'localhost';
$db = 'metro'; // Reemplaza con tu base de datos
$user = 'root'; // Reemplaza con tu usuario
$pass = '123'; // Reemplaza con tu contraseña

try {
    $pdo = new PDO("mysql:host=$host;dbname=$db", $user, $pass);
    $pdo->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);

    // Obtener los datos JSON
    $data = json_decode(file_get_contents('php://input'), true);
    
    $estaciones = $data['Estacion'];
    $cantidades = $data['Cantidad'];

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
