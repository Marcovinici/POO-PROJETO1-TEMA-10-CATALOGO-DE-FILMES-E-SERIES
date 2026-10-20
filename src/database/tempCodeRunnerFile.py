import sqlite3
from pathlib import Path

caminho_banco = Path("banco.db")
conexao = sqlite3.connect(caminho_banco)
cursor = conexao.cursor()

conexao.execute("""
    CREATE TABLE IF NOT EXISTS usuarios (
        nome_de_usuario VARCHAR(100) PRIMARY KEY,
        senha INT NOT NULL,
        nome TEXT NOT NULL,
        tipo TEXT NOT NULL
    )
""")

conexao.commit()
conexao.close()