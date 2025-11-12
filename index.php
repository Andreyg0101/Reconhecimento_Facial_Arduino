<?php
include('conexao.php');

// Conexão ao banco
$host = "localhost";
$usuario = "root";
$senha = "";
$banco = "controle_acesso";

$conexao = new mysqli($host, $usuario, $senha, $banco);
if ($conexao->connect_error) {
    die("Erro de conexão: " . $conexao->connect_error);
}

// Verifica quantidade de registros
$sql_count = "SELECT COUNT(*) as total FROM alunos";
$result_count = $conexao->query($sql_count);
$row_count = $result_count->fetch_assoc();
$total_registros = $row_count['total'];

// Limpa a tabela se tiver 5 ou mais registros
if ($total_registros >= 5) {
    $conexao->query("TRUNCATE TABLE alunos");
}

// Busca registros
$sql = "SELECT * FROM alunos ORDER BY ultimo_acesso DESC";
$resultado = $conexao->query($sql);
?>
<!DOCTYPE html>
<html lang="pt-br">
<head>
    <meta charset="UTF-8">
    <title>📸 Sistema de Reconhecimento Facial</title>
    <meta http-equiv="refresh" content="5">
    <style>
        body {
            font-family: 'Segoe UI', sans-serif;
            background-color: #0b0c10;
            color: #c5c6c7;
            margin: 0;
            padding: 0;
        }

        .container {
            width: 95%;
            max-width: 1000px;
            margin: 50px auto;
            background-color: #1f2833;
            padding: 20px;
            border-radius: 15px;
            box-shadow: 0 0 15px #45a29e;
        }

        h1 {
            text-align: center;
            color: #66fcf1;
            font-size: 26px;
            margin-bottom: 25px;
        }

        table {
            width: 100%;
            border-collapse: collapse;
            overflow: hidden;
            border-radius: 10px;
        }

        th {
            background-color: #0b0c10;
            color: #45a29e;
            padding: 12px;
            text-align: center;
        }

        td {
            text-align: center;
            padding: 10px;
            color: #c5c6c7;
            border-bottom: 1px solid #45a29e;
        }

        tr:hover {
            background-color: #16222a;
        }

        .ok {
            color: #4caf50;
            font-weight: bold;
        }

        .no {
            color: #e74c3c;
            font-weight: bold;
        }

        footer {
            text-align: center;
            color: #777;
            font-size: 14px;
            margin-top: 20px;
        }

        @media (max-width: 700px) {
            h1 { font-size: 22px; }
            th, td { font-size: 14px; padding: 8px; }
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>📸 Sistema de Reconhecimento Facial</h1>
        <table>
            <thead>
                <tr>
                    <th>ID</th>
                    <th>Nome</th>
                    <th>Matrícula</th>
                    <th>Autorizado</th>
                    <th>Último Acesso</th>
                    <th>Resultado</th>
                </tr>
            </thead>
            <tbody>
                <?php
                if ($resultado->num_rows > 0) {
                    while ($linha = $resultado->fetch_assoc()) {
                        echo "<tr>";
                        echo "<td>" . $linha['id'] . "</td>";
                        echo "<td>" . htmlspecialchars($linha['nome']) . "</td>";
                        echo "<td>" . htmlspecialchars($linha['matricula']) . "</td>";
                        echo "<td>" . ($linha['autorizado'] ? "<span class='ok'>✅ Sim</span>" : "<span class='no'>❌ Não</span>") . "</td>";
                        echo "<td>" . $linha['ultimo_acesso'] . "</td>";
                        echo "<td>" . htmlspecialchars($linha['resultado']) . "</td>";
                        echo "</tr>";
                    }
                } else {
                    echo "<tr><td colspan='6'>Nenhum registro encontrado</td></tr>";
                }
                ?>
            </tbody>
        </table>

        <footer>Projeto IoT - Reconhecimento Facial | UNIMES</footer>
    </div>
</body>
</html>
