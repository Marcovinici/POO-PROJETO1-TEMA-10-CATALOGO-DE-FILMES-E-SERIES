import sqlite3

conexao = sqlite3.connect("src/database/banco.db")
cursor = conexao.cursor()

cursor.executescript("""
 Digite o script
""")
conexao.commit()
cursor.close()
conexao.close()