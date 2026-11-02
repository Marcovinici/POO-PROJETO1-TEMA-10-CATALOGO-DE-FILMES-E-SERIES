import argparse
import sqlite3
from domain.excecoes import DadosInvalidosError, CatalogoError
from repositories.sessao import Sessao
from domain.usuario import Usuario
from repositories.usuario_repository import UsuarioRepository
from domain.midias import Filme, Serie, Temporada, Episodio
from repositories.filme_repository import FilmeRepository
from repositories.serie_repository import SerieRepository
from domain.listas import ListaPersonalizada
from repositories.listas_repository import ListasRepository
from repositories.historico_repository import HistoricoRepository
from repositories.relatorios_repository import RelatorioRepository
from domain.avaliacao import Avaliacao
from repositories.avaliacao_repository import AvaliacaoRepository
from repositories.config_repository import ConfigRepository


# Instanciando os repositórios
repo_usuario = UsuarioRepository("src/database/banco.db")
sessao = Sessao("src/database/banco.db")
repo_filme = FilmeRepository("src/database/banco.db")
repo_serie = SerieRepository("src/database/banco.db")
repo_listas = ListasRepository("src/database/banco.db")
repo_historico = HistoricoRepository("src/database/banco.db")
repo_relatorios = RelatorioRepository("src/database/banco.db")
repo_avaliacoes = AvaliacaoRepository("src/database/banco.db")
repo_config = ConfigRepository("src/database/config.json")

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
        if args.acao == "alter-senha":
            if not args.nova_senha:
                print("Informe a nova senha")
                return
            try:
                print(repo_usuario.alterar_senha(usuario, args.nova_senha))
            except ValueError as erro:
                print(f"Erro ao alterar senha: {erro}")
            return
        print(f"Usuário: {usuario.nome_de_usuario}; nome: {usuario.nome}; tipo: {usuario.tipo}")
    else:
        print("Nenhum usuário logado")


def logout(args):
    usuario = sessao.obter_usuario_logado()
    if usuario:
        sessao.encerrar_sessao()
    else:
        print("Não há usuário logado")


def assistir_filme(args):
    usuario = sessao.obter_usuario_logado()
    if not usuario:
        print("Não há usuário logado")
        return
    filmes = repo_filme.listar_filmes()
    filme = next(
        (
            item for item in filmes
            if item.titulo == args.titulo
            and (args.ano is None or item.ano == args.ano)
        ),
        None,
    )
    if filme is None:
        print("Filme não encontrado")
        return
    try:
        repo_historico.registrar_conclusao(usuario.nome_de_usuario, filme)
        print(f"Filme '{filme.titulo}' registrado como assistido")
    except (ValueError, DadosInvalidosError) as erro:
        print(f"Erro ao registrar filme assistido: {erro}")


def assistir_episodio(args):
    usuario = sessao.obter_usuario_logado()
    if not usuario:
        print("Não há usuário logado")
        return
    series = repo_serie.listar_series()
    episodio = None
    for serie in series:
        if serie.titulo == args.serie and (
            args.ano is None or serie.ano == args.ano
        ):
            for temporada in serie.temporadas:
                if temporada.numero == args.temporada:
                    episodio = next(
                        (
                            item for item in temporada.episodios
                            if item.numero == args.episodio
                        ),
                        None,
                    )
                    break
            break
    if episodio is None:
        print("Episódio não encontrado")
        return
    try:
        repo_historico.registrar_conclusao(usuario.nome_de_usuario, episodio)
        print(f"Episódio '{episodio.titulo}' registrado como assistido")
    except (ValueError, DadosInvalidosError) as erro:
        print(f"Erro ao registrar episódio assistido: {erro}")


def listar_filmes_assistidos(args):
    usuario = sessao.obter_usuario_logado()
    if not usuario:
        print("Não há usuário logado")
        return
    registros = repo_historico.listar_filmes_assistidos(usuario.nome_de_usuario)
    for registro in registros:
        print(f"{registro.midia.titulo} - {registro.data_assistido:%d/%m/%Y %H:%M}")


def listar_series_assistidas(args):
    usuario = sessao.obter_usuario_logado()
    if not usuario:
        print("Não há usuário logado")
        return
    series = repo_historico.listar_series_assistidas(usuario.nome_de_usuario)
    em_andamento = {
        (serie.titulo, serie.ano)
        for serie in repo_historico.listar_series_em_andamento(
            usuario.nome_de_usuario
        )
    }
    for serie in series:
        status = (
            "em andamento"
            if (serie.titulo, serie.ano) in em_andamento
            else "assistida"
        )
        print(f"{serie.titulo} - {status}")


def listar_series_em_andamento(args):
    usuario = sessao.obter_usuario_logado()
    if not usuario:
        print("Não há usuário logado")
        return
    series = repo_historico.listar_series_em_andamento(usuario.nome_de_usuario)
    for serie in series:
        print(serie.titulo)


def listar_ultimas_midias(args):
    usuario = sessao.obter_usuario_logado()
    if not usuario:
        print("Não há usuário logado")
        return
    registros = repo_historico.listar_ultimas(
        usuario.nome_de_usuario, args.limite
    )
    for registro in registros:
        print(f"{registro.midia.titulo} - {registro.data_assistido:%d/%m/%Y %H:%M}")


def relatorio(args):
    usuario = sessao.obter_usuario_logado()
    if not usuario:
        print("Não há usuário logado")
        return
    if args.tipo == "generos":
        print(repo_relatorios.media_de_notas_por_genero())
    elif args.tipo == "tempo":
        if ConfigRepository.multiplicador_de_duracao == 1:
            print(f"{repo_relatorios.tempo_total_assistido(usuario.nome_de_usuario)} minutos")
        else:
            print(f"{repo_relatorios.tempo_total_assistido(usuario.nome_de_usuario):.1f} horas")
    elif args.tipo == "top10":
        print(repo_relatorios.top_10())
    else:
        print(repo_relatorios.series_com_mais_eps())


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
                elenco=args.elenco or [], 
                diretor=args.diretor or [], 
                roteirista=args.roteirista or []
                )
        except (ValueError, DadosInvalidosError) as erro:
            print(f"Erro ao adicionar a filme: {erro}")
            return

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

    if not usuario:
        print("Não há usuário logado")
        return

    try:
        print("\nDados do primeiro episódio da primeira temporada")

        titulo_episodio = input("Título do episódio: ").strip()
        duracao_episodio = int(input("Duração do episódio: "))
        ano_episodio = int(input("Ano do episódio: "))
        numero_episodio = int(input("Número do episódio: "))

        classificacao_episodio = input(
            f"Classificação do episódio [{args.classificacao}]: "
        ).strip()

        if not classificacao_episodio:
            classificacao_episodio = args.classificacao

        episodio = Episodio(
            titulo=titulo_episodio,
            duracao=duracao_episodio,
            ano=ano_episodio,
            classificacao=classificacao_episodio,
            numero=numero_episodio,
            genero=args.genero,
            elenco=args.elenco or [],
            diretor=args.diretor or [],
            roteirista=args.roteirista or [],
        )

        primeira_temporada = Temporada(
            numero=1,
            episodios=[episodio],
        )

        serie = Serie(
            titulo=args.titulo,
            ano=args.ano,
            classificacao=args.classificacao,
            genero=args.genero,
            elenco=args.elenco or [],
            diretor=args.diretor or [],
            roteirista=args.roteirista or [],
            temporadas=[primeira_temporada],
        )

        print(repo_serie.adicionar_serie(serie))

    except (ValueError, DadosInvalidosError) as erro:
        print(f"Erro ao criar série: {erro}")


def _buscar_filme(titulo, ano=None):
    return next(
        (filme for filme in repo_filme.listar_filmes()
         if filme.titulo == titulo and (ano is None or filme.ano == ano)),
        None,
    )


def _buscar_serie(titulo, ano=None):
    return next(
        (serie for serie in repo_serie.listar_series()
         if serie.titulo == titulo and (ano is None or serie.ano == ano)),
        None,
    )


def _buscar_episodio(serie, numero_temporada, numero_episodio):
    for temporada in serie.temporadas:
        if temporada.numero == numero_temporada:
            return next(
                (ep for ep in temporada.episodios if ep.numero == numero_episodio),
                None,
            )
    return None


def listar_midias(args):
    listar_filmes(args)
    listar_series(args)


def adicionar_temporada(args):
    usuario = sessao.obter_usuario_logado()
    if not usuario:
        print("Não há usuário logado")
        return
    serie_id = repo_serie.buscar_id_serie(args.serie, args.ano)
    if serie_id is None:
        print("Série não encontrada")
        return
    try:
        episodio = Episodio(
            args.titulo_episodio,
            args.duracao_episodio,
            args.ano_episodio,
            args.classificacao,
            args.numero_episodio,
            genero=args.genero,
        )
        temporada = Temporada(args.numero, [episodio])
        print(repo_serie.adicionar_temporada(temporada, serie_id))
    except (ValueError, DadosInvalidosError, CatalogoError) as erro:
        print(f"Erro ao adicionar temporada: {erro}")


def adicionar_episodio(args):
    usuario = sessao.obter_usuario_logado()
    if not usuario:
        print("Não há usuário logado")
        return
    serie_id = repo_serie.buscar_id_serie(args.serie, args.ano)
    if serie_id is None:
        print("Série não encontrada")
        return
    temporada_id = repo_serie.buscar_temporada_id(serie_id, args.temporada)
    if temporada_id is None:
        print("Temporada não encontrada")
        return
    try:
        episodio = Episodio(
            args.titulo,
            args.duracao,
            args.ano_episodio,
            args.classificacao,
            args.numero,
            genero=args.genero,
        )
        print(repo_serie.adicionar_episodio(episodio, temporada_id))
    except (ValueError, DadosInvalidosError, CatalogoError) as erro:
        print(f"Erro ao adicionar episódio: {erro}")


def listar_temporadas(args):
    serie = _buscar_serie(args.serie, args.ano)
    if serie is None:
        print("Série não encontrada")
        return
    for temporada in serie.temporadas:
        print(f"Temporada {temporada.numero}: {temporada.total_episodios} episódios")


def listar_episodios(args):
    serie = _buscar_serie(args.serie, args.ano)
    if serie is None:
        print("Série não encontrada")
        return
    temporada = next((t for t in serie.temporadas if t.numero == args.temporada), None)
    if temporada is None:
        print("Temporada não encontrada")
        return
    for episodio in temporada.episodios:
        print(f"{episodio.numero}. {episodio.titulo}")


def mostrar_recomendados(args):
    recomendados = repo_relatorios.recomendados(
        repo_config.nota_minima_de_recomendados,
        limite=10,
    )
    for midia in recomendados:
        print(f"{midia['titulo']} - nota {midia['nota_media']}")


def remover_filme(args):
    filme_id = repo_filme.buscar_filme_id(args.titulo, args.ano)
    if filme_id is None:
        print("Filme não encontrado")
        return
    print(repo_filme.remover_filme(filme_id))


def remover_serie(args):
    serie_id = repo_serie.buscar_id_serie(args.titulo, args.ano)
    if serie_id is None:
        print("Série não encontrada")
        return
    print(repo_serie.remover_serie(serie_id))


def remover_temporada(args):
    serie_id = repo_serie.buscar_id_serie(args.serie, args.ano)
    temporada_id = (
        repo_serie.buscar_temporada_id(serie_id, args.temporada)
        if serie_id is not None else None
    )
    if temporada_id is None:
        print("Temporada não encontrada")
        return
    print(repo_serie.remover_temporada(temporada_id))


def remover_episodio(args):
    serie_id = repo_serie.buscar_id_serie(args.serie, args.ano)
    temporada_id = (
        repo_serie.buscar_temporada_id(serie_id, args.temporada)
        if serie_id is not None else None
    )
    episodio_id = (
        repo_serie.buscar_episodio_id(temporada_id, args.episodio)
        if temporada_id is not None else None
    )
    if episodio_id is None:
        print("Episódio não encontrado")
        return
    try:
        print(repo_serie.remover_episodio(episodio_id))
    except CatalogoError as erro:
        print(f"Erro ao remover episódio: {erro}")


def _midia_para_avaliar(args):
    if args.tipo == "filme":
        return _buscar_filme(args.titulo, args.ano)
    serie = _buscar_serie(args.serie, args.ano)
    if serie is None:
        return None
    if args.tipo == "serie":
        return serie
    temporada = next((t for t in serie.temporadas if t.numero == args.temporada), None)
    if temporada is None:
        return None
    if args.tipo == "temporada":
        return temporada
    return _buscar_episodio(serie, args.temporada, args.episodio)


def avaliar(args):
    usuario = sessao.obter_usuario_logado()
    if not usuario:
        print("Não há usuário logado")
        return
    midia = _midia_para_avaliar(args)
    if midia is None:
        print("Mídia não encontrada")
        return
    try:
        avaliacao = Avaliacao(args.tipo.capitalize(), usuario.nome_de_usuario, args.nota, args.comentario)
        repo_avaliacoes.adicionar_avaliacao(avaliacao, midia)
        print("Avaliação registrada com sucesso")
    except (ValueError, DadosInvalidosError) as erro:
        print(f"Erro ao avaliar mídia: {erro}")


def listar_avaliacoes(args):
    midia = _midia_para_avaliar(args)
    if midia is None:
        print("Mídia não encontrada")
        return
    for avaliacao in repo_avaliacoes.listar_por_midia(midia):
        comentario = f" - {avaliacao.comentario}" if avaliacao.comentario else ""
        print(f"{avaliacao.usuario}: {avaliacao.nota}{comentario}")


def mostrar_informacoes(args):
    midia = _midia_para_avaliar(args)
    if midia is None:
        print("Mídia não encontrada")
        return
    if hasattr(midia, "exibir_detalhes"):
        midia.exibir_detalhes()
    else:
        print(midia)


def mostrar_configuracoes(args):
    print(repo_config.obter_configuracoes())


def alterar_configuracao(args):
    try:
        if args.configuracao == "nota":
            repo_config.nota_minima_de_recomendados = args.valor
        elif args.configuracao == "listas":
            repo_config.limite_de_listas_personalizadas = args.valor
        else:
            repo_config.altera_multiplicador(args.valor)
        repo_config.atualizar_config()
        print("Configuração atualizada com sucesso")
    except (ValueError, DadosInvalidosError) as erro:
        print(f"Erro ao alterar configuração: {erro}")


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
        listas = repo_listas.listar_listas_por_usuario(usuario.nome_de_usuario)
        if len(listas) >= repo_config.limite_de_listas_personalizadas:
            print(
                "Limite de listas personalizadas atingido: "
                f"{repo_config.limite_de_listas_personalizadas}"
            )
            return
        try:
            repo_listas.criar_lista(args.nome_da_lista, usuario.nome_de_usuario)
            print("Lista criada com sucesso")
        except (sqlite3.IntegrityError, ValueError) as erro:
            print(f"Erro ao criar lista: {erro}")
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
        id_lista = repo_listas.buscar_id_por_nome(args.nome_da_lista, usuario.nome_de_usuario)
        if id_lista is None:
            print("Lista não encontrada")
            return
        id_filme = repo_filme.buscar_filme_id(args.nome_do_filme)
        if id_filme is None:
            print("Filme não encontrado")
            return
        repo_listas.adicionar_filme_na_lista(id_lista, id_filme)
    else:
        print("Não há usuário logado")


def adicionar_serie_na_lista(args):
    usuario = sessao.obter_usuario_logado()
    if usuario:
        id_lista = repo_listas.buscar_id_por_nome(args.nome_da_lista, usuario.nome_de_usuario)
        if id_lista is None:
            print("Lista não encontrada")
            return
        id_serie = repo_serie.buscar_id_por_titulo(args.nome_da_serie)
        if id_serie is None:
            print("Serie não encontrada")
            return
        repo_listas.adicionar_serie_na_lista(id_lista, id_serie)
    else:
        print("Não há usuário logado") 


def remover_filme_da_lista(args):
    usuario = sessao.obter_usuario_logado()
    if not usuario:
        print("Não há usuário logado")
        return
    lista_id = repo_listas.buscar_id_por_nome(args.nome_da_lista, usuario.nome_de_usuario)
    filme_id = repo_filme.buscar_filme_id(args.nome_do_filme)
    if lista_id is None or filme_id is None:
        print("Lista ou filme não encontrado")
        return
    print(repo_listas.remover_filme_da_lista(lista_id, filme_id))


def remover_serie_da_lista(args):
    usuario = sessao.obter_usuario_logado()
    if not usuario:
        print("Não há usuário logado")
        return
    lista_id = repo_listas.buscar_id_por_nome(args.nome_da_lista, usuario.nome_de_usuario)
    serie_id = repo_serie.buscar_id_serie(args.nome_da_serie)
    if lista_id is None or serie_id is None:
        print("Lista ou série não encontrada")
        return
    print(repo_listas.remover_serie_da_lista(lista_id, serie_id))


def mostrar_lista(args):
    usuario = sessao.obter_usuario_logado()
    if usuario:
        id_lista = repo_listas.buscar_id_por_nome(args.nome_da_lista, usuario.nome_de_usuario)
        lista = repo_listas.obter_lista_com_midias(id_lista)
        print("MÍDIAS PRESENTES NA LISTA")
        print("-"*30)
        for midia in lista.midias:
            print(midia.titulo)
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
    prog= "pipocli",
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

    # -> Comando usuario
    cmd_usuario = subparsers.add_parser(
        "usuario", help="Imprime informações sobre o usuario que está logado no momento"
    )
    cmd_usuario.add_argument("acao", nargs="?", choices=["alter-senha"])
    cmd_usuario.add_argument("nova_senha", nargs="?")

    cmd_usuario.set_defaults(func=usuario)

    # -> Comando logout
    cmd_logout = subparsers.add_parser(
        "logout", help="Desloga o usuario"
    )

    cmd_logout.set_defaults(func=logout)

    # -> Comando assistir e seus subcomandos
    cmd_assistir = subparsers.add_parser(
        "assistir", help="Registra uma mídia concluída pelo usuário logado"
    )
    subparsers_assistir = cmd_assistir.add_subparsers(
        dest="subcomando_assistir", required=True
    )
    # assistir filme
    assistir_filme_cmd = subparsers_assistir.add_parser("filme")
    assistir_filme_cmd.add_argument("titulo", type=str)
    assistir_filme_cmd.add_argument("--ano", type=int)

    assistir_filme_cmd.set_defaults(func=assistir_filme)

    # assistir episodio
    assistir_episodio_cmd = subparsers_assistir.add_parser("episodio")
    assistir_episodio_cmd.add_argument("serie", type=str)
    assistir_episodio_cmd.add_argument("temporada", type=int)
    assistir_episodio_cmd.add_argument("episodio", type=int)
    assistir_episodio_cmd.add_argument("--ano", type=int)

    assistir_episodio_cmd.set_defaults(func=assistir_episodio)

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

    # adicionar temporada
    addcmd_temporada = subparsers_adicionar.add_parser("temporada")
    addcmd_temporada.add_argument("serie")
    addcmd_temporada.add_argument("ano", type=int)
    addcmd_temporada.add_argument("numero", type=int)
    addcmd_temporada.add_argument("titulo_episodio")
    addcmd_temporada.add_argument("duracao_episodio", type=int)
    addcmd_temporada.add_argument("ano_episodio", type=int)
    addcmd_temporada.add_argument("numero_episodio", type=int)
    addcmd_temporada.add_argument("classificacao")
    addcmd_temporada.add_argument("--gen", dest="genero")

    addcmd_temporada.set_defaults(func=adicionar_temporada)

    # adicionar episodio
    addcmd_episodio = subparsers_adicionar.add_parser("episodio")
    addcmd_episodio.add_argument("serie")
    addcmd_episodio.add_argument("ano", type=int)
    addcmd_episodio.add_argument("temporada", type=int)
    addcmd_episodio.add_argument("numero", type=int)
    addcmd_episodio.add_argument("titulo")
    addcmd_episodio.add_argument("duracao", type=int)
    addcmd_episodio.add_argument("ano_episodio", type=int)
    addcmd_episodio.add_argument("classificacao")
    addcmd_episodio.add_argument("--gen", dest="genero")
    addcmd_episodio.set_defaults(func=adicionar_episodio)

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
    # listar midias
    listcmd_midias = subparsers_listar.add_parser("midias")
    listcmd_midias.set_defaults(func=listar_midias)
    listcmd_temporadas = subparsers_listar.add_parser("temporadas")
    listcmd_temporadas.add_argument("serie")
    listcmd_temporadas.add_argument("--ano", type=int)

    listcmd_temporadas.set_defaults(func=listar_temporadas)
    # listar episodios
    listcmd_episodios = subparsers_listar.add_parser("episodios")
    listcmd_episodios.add_argument("serie")
    listcmd_episodios.add_argument("temporada", type=int)
    listcmd_episodios.add_argument("--ano", type=int)

    listcmd_episodios.set_defaults(func=listar_episodios)
    # listar listas
    listcmd_listas = subparsers_listar.add_parser(
        "listas", help="Utilizando o subcomando listas em listar, o programa imprimirá todas as listas do catálogo"
    )

    listcmd_listas.set_defaults(func=listar_listas)
    # listar filmes-assistidos
    listcmd_filmes_assistidos = subparsers_listar.add_parser(
        "filmes-assistidos", help="Utilizando o subcomando 'filmes-assistidos' em listar, o programa imprimirá os filmes assistidos"
    )

    listcmd_filmes_assistidos.set_defaults(func=listar_filmes_assistidos)
    # listar series-assistidas
    listcmd_series_assistidas = subparsers_listar.add_parser(
        "series-assistidas", help="Utilizando o subcomando 'series-assistidas' em listar, o programa imprimirá as séries assistidas"
    )

    listcmd_series_assistidas.set_defaults(func=listar_series_assistidas)
    # listar series-assistindo
    listcmd_series_andamento = subparsers_listar.add_parser(
        "series-assistindo", help="Utilizando o subcomando 'series-assistindo' em listar, o programa imprimirá as séries que não foram assistidas por completo"
    )

    listcmd_series_andamento.set_defaults(func=listar_series_em_andamento)
    # listar ultimas-assistidas
    listcmd_ultimas = subparsers_listar.add_parser(
        "ultimas-assistidas", help="Utilizando o subcomando 'ultima-assistidas' em listar, o programa imprimirá as últimas mídias assistidas"
    )
    listcmd_ultimas.add_argument("--limite", type=int, default=10)

    listcmd_ultimas.set_defaults(func=listar_ultimas_midias)

    # -> Comando recomendados
    cmd_recomendados = subparsers.add_parser(
        "recomendados", help="Imprimi a lista de recomendados"
    )
    cmd_recomendados.set_defaults(func=mostrar_recomendados)

    # -> Comando remover e seus subcomandos
    cmd_remover = subparsers.add_parser("remover")
    subparsers_remover = cmd_remover.add_subparsers(dest="tipo", required=True)
    # remover filme
    remover_filme_cmd = subparsers_remover.add_parser("filme")
    remover_filme_cmd.add_argument("titulo")
    remover_filme_cmd.add_argument("--ano", type=int)

    remover_filme_cmd.set_defaults(func=remover_filme)
    # remover serie
    remover_serie_cmd = subparsers_remover.add_parser("serie")
    remover_serie_cmd.add_argument("titulo")
    remover_serie_cmd.add_argument("--ano", type=int)

    remover_serie_cmd.set_defaults(func=remover_serie)
    # remover temporada
    remover_temp_cmd = subparsers_remover.add_parser("temporada")
    remover_temp_cmd.add_argument("serie")
    remover_temp_cmd.add_argument("temporada", type=int)
    remover_temp_cmd.add_argument("--ano", type=int)

    remover_temp_cmd.set_defaults(func=remover_temporada)
    # remover episodio
    remover_ep_cmd = subparsers_remover.add_parser("episodio")
    remover_ep_cmd.add_argument("serie")
    remover_ep_cmd.add_argument("temporada", type=int)
    remover_ep_cmd.add_argument("episodio", type=int)
    remover_ep_cmd.add_argument("--ano", type=int)

    remover_ep_cmd.set_defaults(func=remover_episodio)

    # -> Comando info e seus subcomandos
    cmd_info = subparsers.add_parser("info")
    subparsers_info = cmd_info.add_subparsers(dest="tipo", required=True)
    # Adicionando todos os subcomandos:
    # remover filme, remover serie, remover temporada e remover episodio
    for nome in ("filme", "serie", "temporada", "episodio"):
        info_cmd = subparsers_info.add_parser(nome)
        info_cmd.add_argument("titulo" if nome == "filme" else "serie")
        if nome == "filme":
            info_cmd.add_argument("--ano", type=int)
        else:
            info_cmd.add_argument("--ano", type=int)
        if nome in ("temporada", "episodio"):
            info_cmd.add_argument("temporada", type=int)
        if nome == "episodio":
            info_cmd.add_argument("episodio", type=int)
        info_cmd.set_defaults(func=mostrar_informacoes)

    # -> Comandos avaliar e avaliacoes e seus subcomandos
    # Adicionando todos os subcomandos:
    # avaliar filme, avaliar serie, avaliar temporada, avaliar episodio, avaliacoes filme, avaliacoes serie, avaliacoes temporada, avaliacoes episodios
    for acao in ("avaliar", "avaliacoes"):
        cmd = subparsers.add_parser(acao)
        sub = cmd.add_subparsers(dest="tipo", required=True)
        for nome in ("filme", "serie", "temporada", "episodio"):
            item = sub.add_parser(nome)
            item.add_argument("titulo" if nome == "filme" else "serie")
            item.add_argument("--ano", type=int)
            if nome in ("temporada", "episodio"):
                item.add_argument("temporada", type=int)
            if nome == "episodio":
                item.add_argument("episodio", type=int)
            if acao == "avaliar":
                item.add_argument("nota", type=float)
                item.add_argument("--comentario")
                item.set_defaults(func=avaliar)
            else:
                item.set_defaults(func=listar_avaliacoes)

    # -> Comandos config e configuracao 
    cmd_config = subparsers.add_parser("config")
    sub_config = cmd_config.add_subparsers(dest="configuracao", required=True)
    # config mostrar
    sub_config.add_parser("mostrar").set_defaults(func=mostrar_configuracoes)
    # config recomendadosmin
    nota_cmd = sub_config.add_parser("recomendadosmin")
    nota_cmd.add_argument("valor", type=float)

    nota_cmd.set_defaults(func=alterar_configuracao)
    # config listasmax
    listas_cmd = sub_config.add_parser("listasmax")
    listas_cmd.add_argument("valor", type=int)

    listas_cmd.set_defaults(func=alterar_configuracao)
    # config metrica
    metrica_cmd = sub_config.add_parser("metrica")
    metrica_cmd.add_argument("valor", choices=["horas", "minutos"])

    metrica_cmd.set_defaults(func=alterar_configuracao)

    # -> Comando relatorio
    cmd_relatorio = subparsers.add_parser(
        "relatorio", help="Exibe relatórios do catálogo e do histórico."
    )
    cmd_relatorio.add_argument(
        "tipo",
        choices=["generos", "tempo", "top10", "series-episodios"],
    )
    cmd_relatorio.set_defaults(func=relatorio)

    # -> Comando de listas
    # Subcomando principal
    cmd_lista = subparsers.add_parser(
        "lista", help="Gerencia as listas personalizadas"
    )

    cmd_lista.add_argument("nome_da_lista", type=str, help="Nome da lista")

    subparsers_lista = cmd_lista.add_subparsers(
        dest="subcomando_lista", required=True
    )
    # lista adicionar
    listacmd_adicionar = subparsers_lista.add_parser(
        "adicionar", help="Adiciona uma mídia à lista"
    )

    subparsers_lista_adicionar = listacmd_adicionar.add_subparsers(
        dest="subcomando_lista_adicionar", required=True
    )
    # lista adicionar filme
    listacmd_adicionar_filme = subparsers_lista_adicionar.add_parser(
        "filme", help="Adiciona um filme à lista"
    )
    listacmd_adicionar_filme.add_argument(
        "nome_do_filme", type=str
    )

    listacmd_adicionar_filme.set_defaults(func=adicionar_filme_na_lista)
    # lista adicionar serie
    listacmd_adicionar_serie = subparsers_lista_adicionar.add_parser(
        "serie", help="Adiciona uma série à lista"
    )
    listacmd_adicionar_serie.add_argument(
        "nome_da_serie", type=str
    )

    listacmd_adicionar_serie.set_defaults(func=adicionar_serie_na_lista)
    # lista remover filme
    listacmd_remover_filme = subparsers_lista.add_parser(
        "remover-filme", help="Remove um filme da lista"
    )
    listacmd_remover_filme.add_argument("nome_do_filme")

    listacmd_remover_filme.set_defaults(func=remover_filme_da_lista)
    # lista remover serie
    listacmd_remover_serie = subparsers_lista.add_parser(
        "remover-serie", help="Remove uma série da lista"
    )
    listacmd_remover_serie.add_argument("nome_da_serie")
    listacmd_remover_serie.set_defaults(func=remover_serie_da_lista)
    # lista mostrar
    listacmd_mostrar = subparsers_lista.add_parser(
        "mostrar", help="Imprimi as midias da lista"
    )

    listacmd_mostrar.set_defaults(func=mostrar_lista)

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