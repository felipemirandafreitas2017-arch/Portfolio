<?php
require "conexao.php";

$stmt = $conexao->prepare(
    "INSERT INTO contato (nome, email, texto)
    VALUES (?, ?, ?)"
);
$stmt->execute([$_POST["nome"], $_POST["email"], $_POST["texto"]]);
?>