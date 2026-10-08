<?php
$conexao = new PDO(
    "mysql:host=localhost;dbname=banco",
    "root", ""
);
$conexao->setAttribute(
    PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION
);
?>