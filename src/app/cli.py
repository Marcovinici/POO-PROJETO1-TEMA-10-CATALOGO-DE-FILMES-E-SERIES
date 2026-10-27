import argparse
from repositories.sessao import Sessao
from domain.usuario import Usuario
from repositories.usuario_repository import UsuarioRepository
from domain.midias import Filme, Serie
from repositories.filme_repository import FilmeRepository
from repositories.serie_repository import SerieRepository
from domain.listas import ListaPersonalizada
from repositories.listas_repository import ListasRepository


# Instanciando os repositórios
repo_usuario = UsuarioRepository("src/database/banco.db")
sessao = Sessao("src/database/banco.db")
repo_filme = FilmeRepository("src/database/banco.db")
repo_serie = SerieRepository("src/database/banco.db")
repo_listas = ListasRepository("src/database/banco.db")

# --------------------FUNÇÕES-----------------------
def logar(args):
    if repo_usuario.login(args.nome_de_usuario, args.senha):
        sessao.registrar_login(args.nome_de_usuario)
        print(f"O usuario {args.nome_de_usuario} foi logado com sucesso!")
    else:
        print("Nome de usuário ou senha inválidas")
    
def cad_usuario(args):
    if args.admin :
        novo_usuario = Usuario(args.nome_de_usuario, args.senha, args.nome, "ADMIN")
    else:
        novo_usuario = Usuario(args.nome_de_usuario, args.senha, args.nome)
    print(repo_usuario.cadastrar(novo_usuario))

# ----> FUNÇOES DE USUÁRIO PADRAO
def usuario(args):
    usuario = sessao.obter_usuario_logado()
    if usuario:
        print(f"Usuário: {usuario.nome_de_usuario}; nome: {usuario.nome}; tipo: {usuario.tipo}")
    else:
        print("Nenhum usuário logado")

def logout(args):
    usuario = sessao.obter_usuario_logado()
    if usuario:
        sessao.encerrar_sessao()
    else:
        print("Não há usuário logado")

def adicionar_filme(args):
    usuario = sessao.obter_usuario_logado()
    if usuario:
        try:
            filme = Filme(
                titulo=args.titulo,
                duracao=args.duracao, 
                ano=args.ano, 
                classificacao=args.classificacao, 
                genero=args.genero, 
                elenco=args.elenco, 
                diretor=args.diretor, 
                roteirista=args.roteirista
                )
        except:
            filme = None
            print("Erro ao criar objeto filme")

        if filme:
            print(repo_filme.adicionar_filme(filme))
    else:
        print("Não há usuário logado")

def listar_filmes(args):
    usuario = sessao.obter_usuario_logado()
    if usuario:
        filmes = repo_filme.listar_filmes()
        print("FILMES DO CATÁLOGO: ")
        print("-"*30)
        for filme in filmes:
            print(filme.titulo)
    else:
        print("Não há usuário logado")

def adicionar_serie(args):
    usuario = sessao.obter_usuario_logado()
    if usuario:
        try:
            serie = Serie(
                titulo=args.titulo, 
                ano=args.ano, 
                classificacao=args.classificacao, 
                genero=args.genero, 
                elenco=args.elenco, 
                diretor=args.diretor, 
                roteirista=args.roteirista
                )
        except:
            serie = None
            print("Erro ao criar objeto serie")

        if serie:
            print(repo_serie.adicionar_serie(serie))
    else:
        print("Não há usuário logado")

def listar_series(args):
    usuario = sessao.obter_usuario_logado()
    if usuario:
        series = repo_serie.listar_series()
        print("SÉRIES DO CATÁLOGO: ")
        print("-"*30)
        for serie in series:
            print(serie.titulo)
    else:
        print("Não há usuário logado")

def adicionar_lista(args):
    usuario = sessao.obter_usuario_logado()
    if usuario:
        repo_listas.criar_lista(args.nome_da_lista, usuario.nome_de_usuario)
    else:
        print("Não há usuário logado")

def listar_listas(args):
    usuario = sessao.obter_usuario_logado()
    if usuario:
        listas = repo_listas.listar_listas_por_usuario(usuario.nome_de_usuario)
        print("SUAS LISTAS:")
        print("-"*30)
        for lista in listas:
            print(lista.nome)
    else:
        print("Não há usuário logado")
    
def adicionar_filme_na_lista(args):
    usuario = sessao.obter_usuario_logado()
    if usuario:
        id_lista = repo_listas.buscar_id_por_nome(args.nome_da_lista)
        repo_listas.adicionar_filme_na_lista(id_lista, args.titulo)
    else:
        print("Não há usuário logado")

def adicionar_serie_na_lista(args):
    usuario = sessao.obter_usuario_logado()
    if usuario:
        id_lista = repo_listas.buscar_id_por_nome(args.nome_da_lista)
        repo_listas.adicionar_serie_na_lista(id_lista, args.titulo)
    else:
        print("Não há usuário logado") 

def mostrar_lista(args):
    usuario = sessao.obter_usuario_logado()
    if usuario:
        id_lista = repo_listas.buscar_id_por_nome(args.nome_da_lista)
        repo_listas.obter_lista_com_midias(id_lista)
    else:
        print("Não há usuário logado") 

# ----> FUNÇÕES DE ADMIN
def listar_usuarios(args):
    usuario = sessao.obter_usuario_logado()
    if usuario:
        if usuario.tipo == "ADMIN":
            linhas = repo_usuario.listar()
            for linha in linhas:
                print(linha)
        else:
            print(f"O usuário '{usuario.nome_de_usuario}' não tem permissão de administrador")
    else:
        print("O usuário não está logado")



# -------------------------------------MAIN---------------------------------------
def main():
    parser = argparse.ArgumentParser(
    prog= "Catalogo de Midias CLI",
    description= "Programa para manipular e gerenciar um catálogo de filmes e séries"
    )

    # CRIA O GESTOR DE SUBCOMANDOS
    subparsers = parser.add_subparsers(
        dest="comando",  # Guarda o nome do comando digitado em args.comando
        required=True,  # Obriga o utilizador ao escolher um comando
    )

    # ---> CRIA OS COMANDOS

    # Comando 'logar'
    cmd_logar = subparsers.add_parser(
        "logar", help="O usuário pode logar adicionando o 'nome de usuário' e a 'senha' como argumentos"
    )
    cmd_logar.add_argument("nome_de_usuario", type=str, help="Nome de usuário")
    cmd_logar.add_argument("senha", type=str, help="Senha do usuário")

    cmd_logar.set_defaults(func=logar)
    # Comando 'cadastrar'
    cmd_cad_usuario = subparsers.add_parser(
        "cad-usuario", help="O usuário pode cadastrar um nomvo usuario"
    )
    cmd_cad_usuario.add_argument("nome_de_usuario", type=str, help="Nome de usuário")
    cmd_cad_usuario.add_argument("senha", type=str, help="Senha do usuário")
    cmd_cad_usuario.add_argument("nome", type=str, help="Nome real do usuário")
    cmd_cad_usuario.add_argument("--admin", action="store_true", help="Define o usuário como Administrador")

    cmd_cad_usuario.set_defaults(func=cad_usuario)

    # --> COMANDOS DE USUÁRIO LOGADO

    # Comando usuario
    cmd_usuario = subparsers.add_parser(
        "usuario", help="Imprime informações sobre o usuario que está logado no momento"
    )

    cmd_usuario.set_defaults(func=usuario)

    # Comando logout
    cmd_logout = subparsers.add_parser(
        "logout", help="Desloga o usuario"
    )

    cmd_logout.set_defaults(func=logout)

    # -> comando adicionar e seus subcomandos
    cmd_adicionar = subparsers.add_parser(
        "adicionar", help="Permite adicionar determinado objeto ao catálogo (filme, serie, temporada, episodio ou lista)"
    )

    subparsers_adicionar = cmd_adicionar.add_subparsers(
        dest = "subcomando_adicionar", required=True
    )
    # adicionar filme
    addcmd_filme = subparsers_adicionar.add_parser(
        "filme", help="Utilizando o subcomando filme em adicionar, o usuário pode adicionar um filme no catálogo"
    )
    addcmd_filme.add_argument("titulo", type=str)
    addcmd_filme.add_argument("duracao", type=int)
    addcmd_filme.add_argument("ano", type=int)
    addcmd_filme.add_argument("classificacao", type=str)
    addcmd_filme.add_argument("--gen", dest="genero", type=str)
    addcmd_filme.add_argument("--elen", dest="elenco", nargs="+", type=str)
    addcmd_filme.add_argument("--dir", dest="diretor", nargs="+", type=str)
    addcmd_filme.add_argument("--rot", dest="roteirista", nargs="+", type=str)

    addcmd_filme.set_defaults(func=adicionar_filme)
    # adicionar serie
    addcmd_serie = subparsers_adicionar.add_parser(
        "serie", help="Utilizando o subcomando serie em adicionar, o usuário pode adicionar uma série ao catálogo"
    )
    addcmd_serie.add_argument("titulo", type=str)
    addcmd_serie.add_argument("ano", type=int)
    addcmd_serie.add_argument("classificacao", type=str)
    addcmd_serie.add_argument("--gen", dest="genero", type=str)
    addcmd_serie.add_argument("--elen", dest="elenco", nargs="+", type=str)
    addcmd_serie.add_argument("--dir", dest="diretor", nargs="+", type=str)
    addcmd_serie.add_argument("--rot", dest="roteirista", nargs="+", type=str)

    addcmd_serie.set_defaults(func=adicionar_serie)

    # adicionar lista
    addcmd_lista = subparsers_adicionar.add_parser(
        "lista", help="Utilizando o subcomando lista em adicionar, o usuário pode adicionar uma lista ao catálogo"
    )
    addcmd_lista.add_argument("nome_da_lista", type=str)

    addcmd_lista.set_defaults(func=adicionar_lista)

    # -> comando listar e seus subcomandos
    cmd_listar = subparsers.add_parser(
        "listar", help="Permite listar todos os objetos de determinado tipo do catálogo"
    )

    subparsers_listar = cmd_listar.add_subparsers(
        dest = "subcomando_listar", required=True
    )
    # listar filmes
    listcmd_filmes = subparsers_listar.add_parser(
        "filmes", help="Utilizando o subcomando filmes em listar, o programa imprimirá todos os filmes do catálogo"
    )

    listcmd_filmes.set_defaults(func=listar_filmes)
    # listar series
    listcmd_series = subparsers_listar.add_parser(
        "series", help="Utilizando o subcomando series em listar, o programa imprimirá todas as séries do catálogo"
    )

    listcmd_series.set_defaults(func=listar_series)

    listcmd_listas = subparsers_listar.add_parser(
        "listas", help="Utilizando o subcomando listas em listar, o programa imprimirá todas as listas do catálogo"
    )

    listcmd_listas.set_defaults(func=listar_listas)

    # --> COMANDOS DE USUÁRIO ADMINISTRADOR
    cmd_listar_usuarios = subparsers.add_parser(
        "listar-usuarios", help="O comando imprime todos os usuários cadastrados (esse comando só está disponível para administradores)"
    )

    cmd_listar_usuarios.set_defaults(func=listar_usuarios)

    # LENDO ARGS
    args = parser.parse_args()

    # LIGANDO ARGS A FUNÇOES
    args.func(args)

if __name__ == "__main__":
    main()