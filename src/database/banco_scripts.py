import sqlite3

conexao = sqlite3.connect("src/database/banco.db")
cursor = conexao.cursor()
'''
conexao.executescript("""
    CREATE TABLE IF NOT EXISTS usuarios (
        nome_de_usuario VARCHAR(100) PRIMARY KEY,
        senha INTEGER NOT NULL,
        nome TEXT NOT NULL,
        tipo TEXT NOT NULL
    );

    CREATE TABLE IF NOT EXISTS filmes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        titulo TEXT NOT NULL,
        duracao INT NOT NULL,
        ano INTEGER NOT NULL,
        classificacao TEXT NOT NULL,
        genero TEXT,
        elenco TEXT,
        diretor TEXT,
        roteirista TEXT
    );

    CREATE TABLE IF NOT EXISTS avaliacoes(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        usuario_id VARCHAR(100) NOT NULL,
        nota INTEGER NOT NULL,
        comentario TEXT NOT NULL,
        midia_id INTEGER NOT NULL,
        tipo_midia TEXT NOT NULL,
        
        FOREIGN KEY (usuario_id) REFERENCES usuarios(nome_de_usuario) ON DELETE CASCADE,

        UNIQUE(usuario_id, midia_id, tipo_midia)

    );
""")
'''
'''
cursor.execute(
    "DELETE FROM usuarios WHERE nome_de_usuario == 'adm'"
)
'''
'''
cursor.execute(
    "DROP TABLE IF EXISTS filmes"
)
'''
cursor.execute("""
    DELETE FROM usuarios WHERE nome_de_usuario == 'adm'
""")

conexao.commit()
cursor.close()
conexao.close()