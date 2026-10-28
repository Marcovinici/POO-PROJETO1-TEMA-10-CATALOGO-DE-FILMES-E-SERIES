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
cursor.executescript("""
DROP TABLE IF EXISTS lista_midia;

CREATE TABLE lista_midia (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    lista_id INTEGER NOT NULL,
    filme_titulo TEXT,
    serie_titulo TEXT,
    FOREIGN KEY (lista_id) REFERENCES listas(id) ON DELETE CASCADE,
    FOREIGN KEY (filme_titulo) REFERENCES filmes(titulo) ON DELETE CASCADE,
    FOREIGN KEY (serie_titulo) REFERENCES series(titulo) ON DELETE CASCADE,
    CHECK (
        (filme_titulo IS NOT NULL AND serie_titulo IS NULL) OR
        (filme_titulo IS NULL AND serie_titulo IS NOT NULL)
    ),
    UNIQUE(lista_id, filme_titulo, serie_titulo)
);
""")
conexao.commit()
cursor.close()
conexao.close()