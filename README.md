# PipoCLI 🍿
 Esse projeto faz parte da disciplina de Programação Orientada a Objetos (ES0008), feito para trabalhar os conhecimentos adquiridos ao longo da cadeira e nas disciplinas anteriores.

## Descrição  do Projeto

Sistema de linha de comando (CLI) ou API mínima (FastAPI/Flask, opcional) para gerenciar um catálogo pessoal de filmes e séries, com avaliações, status de visualização, temporadas/episódios, histórico e relatórios de consumo de mídia.

## Objetivos

O sistema deve permitir acompanhar o progresso de séries e comparar avaliações entre mídias, gerenciar o perfil do usuário e configurações.

## Estrutura de Pastas
```text
POO-PROJETO1-TEMA-10-CATALOGO-DE-FILMES-E-SERIES/
├── README.md
├── LICENSE
├── pyproject.toml
├── src/
│   ├── app/
│   │   ├── __init__.py
│   │   └── cli.py
│   ├── domain/
│   │   ├── __init__.py
│   │   ├── avaliacao.py
│   │   ├── catalogo.py
│   │   ├── config.py
│   │   ├── historico.py
│   │   ├── listas.py
│   │   ├── midia_assistida.py
│   │   ├── midias.py
│   │   ├── relatorios.py
│   │   └── usuario.py
│   ├── repositories/
│   │   ├── __init__.py
│   │   ├── avaliacao_repository.py
│   │   ├── catalogo_repository.py
│   │   ├── filme_repository.py
│   │   ├── historico_repository.py
│   │   ├── listas_repository.py
│   │   ├── relatorios_repository.py
│   │   ├── serie_repository.py
│   │   ├── sessao.py
│   │   └── usuario_repository.py
│   └── database/
│       └── banco.db
└── tests/
    └── test_01.py
```

## Estrutura de Classes
```mermaid
classDiagram
    %%----USUARIO----
    class Usuario {
        +str nome
        +str nome_de_usuario
        +str senha
        +mudar_nome_de_usuario()
        +mudar_senha()
    }



    %% Classes-base
    class Midia {
        %%---Atributos---
        +str titulo
        +str genero
        +int ano
        +str classificacao
        +List~str~ elenco
        +List~str~ diretor
        +List~str~ roteirista
        %%---Métodos---
        +exibir_detalhes()
    }

    class Catalogo {
        +List~Filme~filmes
        +List~Serie~series
        +List~Lista~listas
        +procurar_midia()
        +adicionar_midia()
    }
    
    class Lista {
        +str nome_da_lista
        +List~Midia~midias
        +adicionar_na_lista()
        +remover_da_lista()
    }

    class ListaPersonalizada{
        +str nome_usuario
    }

    class Relatorio {
        +str nome_do_usuario
        +str nome_do_relatorio
        +criar_relatorio()
        +atualizar_relatorio()
        +mostrar_relatorio()
    }

    %% Status por Usuário e Histórico

    class MidiaAssistida {
        +Midia midia
        +str data_ultima_visualizacacao
    }

    class Historico {
        +List~MidiaAssistida~midias_assistidas
        +adicionar_visualizacao()
        +mostrar_relatorio()

    }

    class Configuracoes {
        +float nota_minima_de_recomendados
        +int limite_de_listas_personalizadas
        +conversor_de_duracao()
        +mudar_nota_minima_de_recomendados()
        +mudar_limite_de_listas_recomendadas()
    }



    %% Heranças de Midia 
    class Filme {
        +int duracao
        +float nota
        +List~Avaliacao~avaliacoes
        +avaliar_filme()
        +ver_avaliacoes()
    }

    class Serie {
        +List~Temporada~ temporadas
        +float nota_media
        +float nota_serie
        +int total_temporadas
        +int total_episodios
        +List~Avaliacao~avaliacoes
        +media_avaliacao_temporadas()
        +avaliar_serie()
        +ver_temporadas()
        +ver_avaliacoes()
    }

    %% Serie Subclasses
    class Temporada {
        +int numero
        +List~Episodio~ episodios
        +int total_episodios
        +float nota_media
        +float nota_temporada
        +List~Avaliacao~avaliacoes
        +media_avaliacao_episodios()
        +avaliar_temporada()
        +mostrar_episodios()
        +ver_avaliacoes()
    }

    class Episodio {
        +int duracao
        +int numero
        +float nota
        +List~Avaliacao~avaliacoes
        +avaliar_episodio()
        +ver_avaliacoes()
    }



    %% Avaliações
    class Avaliacao {
        +str tipo
        +str usuario
        +str comentario
        +float nota
        +alterar_nota()
        +alterar_comentario()
    }



    %% Heranças de Relatorio
    class RelatorioGeral {
        +float media_notas_por_genero
        +float tempo_total_assistido
        +List top10_bem_avaliados
        +List series_mais_eps_assistidos
        +List filmes_mais_assistidos
        +List series_mais_assistidas
    }

    class RelatorioHistorico {
        +float tempo_total_dia
        +float tempo_total_semana
        +float tempo_total_mes
    }



    %% Relacionamentos
    Midia <|-- Filme : herda
    Midia <|-- Serie : herda
    Midia <|-- Episodio : herda
    Lista <|-- ListaPersonalizada : herda

    Serie "1" *-- "many" Temporada : contem
    Serie "1" *-- "many" Avaliacao : contem
    Temporada "1" *-- "many" Episodio : contem
    Temporada "1" *-- "many" Avaliacao : contem
    Episodio "1" *-- "many" Avaliacao : contem
    Filme "1" *-- "many" Avaliacao : contem

    Catalogo "1" *-- "many" Midia : contem
    Catalogo "1" *-- "many" Lista : contem
    Lista "1" o-- "many" Midia : agrega

    Relatorio <|-- RelatorioGeral : herda
    Relatorio <|-- RelatorioHistorico : herda
    Historico "1" *-- "1" RelatorioHistorico : contem
    Historico "1" *-- "many" MidiaAssistida : contem
    MidiaAssistida "many" --> "1" Midia : refere-se

    Usuario "many" --> "1" Catalogo : consulta/gerencia
    Usuario "1" *-- "1" Configuracoes : contem
    Usuario "1" *-- "1" RelatorioGeral : contem
    Usuario "1" *-- "1" Historico : contem
```
