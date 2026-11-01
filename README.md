# PipoCLI 🍿
 Esse projeto faz parte da disciplina de Programação Orientada a Objetos (ES0008), feito para trabalhar os conhecimentos adquiridos ao longo da cadeira e nas disciplinas anteriores.

## Descrição  do Projeto

Sistema de linha de comando (CLI) ou API mínima (FastAPI/Flask, opcional) para gerenciar um catálogo pessoal de filmes e séries, com avaliações, status de visualização, temporadas/episódios, histórico e relatórios de consumo de mídia.

## Objetivos

O sistema deve permitir acompanhar o progresso de séries e comparar avaliações entre mídias, gerenciar o perfil do usuário e configurações.

## Estrutura de Pastas
```text
POO-PROJETO1-TEMA-10-CATALOGO-DE-FILMES-E-SERIES/
├── .gitignore
├── LICENSE
├── README.md
├── pyproject.toml
├── src/
│   ├── app/
│   │   ├── __init__.py
│   │   └── cli.py
│   ├── database/
│   │   ├── banco.db
│   │   └── banco_scripts.py
│   ├── domain/
│   │   ├── __init__.py
│   │   ├── avaliacao.py
│   │   ├── config.py
│   │   ├── excecoes.py
│   │   ├── historico.py
│   │   ├── listas.py
│   │   ├── midia_assistida.py
│   │   ├── midias.py
│   │   ├── mixins.py
│   │   ├── relatorios.py
│   │   └── usuario.py
│   └── repositories/
│       ├── __init__.py
│       ├── avaliacao_repository.py
│       ├── config_repository.py
│       ├── filme_repository.py
│       ├── historico_repository.py
│       ├── listas_repository.py
│       ├── midia_assistida_repository.py
│       ├── relatorios_repository.py
│       ├── serie_repository.py
│       ├── sessao.py
│       └── usuario_repository.py
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
        +str tipo
        +Historico historico
        +mudar_senha()
    }


    %% Classes-base
    class Midia {
        %%---Atributos---
        +str titulo
        +str genero
        +int ano
        +str classificacao
        +List~str~elenco
        +List~str~diretor
        +List~str~roteirista
        %%---Métodos---
        +exibir_detalhes()
    }


    class ListaPersonalizada{
        +int id
        +str nome
        +str usuario
        +List~Midia~midias
        +adicionar_na_lista()
        +remover_da_lista()
    }


    class Relatorio {
        +List~Filme~filmes
        +List~Serir~series
        +Historico historico
        +tempo_total_assistido()
        +media_de_notas_por_genero()
        +top_10()
        +series_com_mais_eps()
    }

    %% Status por Usuário e Histórico

    class MidiaAssistida {
        +Midia midia
        +int usuario_id
        +str data_assistido

    }

    class Historico {
        +List~MidiaAssistida~registros
        +int usuario_id
        +registrar_conclusao()
        +soma_tempo_no_periodo()
        +gerar_relatorio()
        +mostrar_relatorio()

    }


    %% Heranças de Midia 
    class Filme {
        +int duracao
        +float nota
        +List~Avaliacao~avaliacoes
        +float nota_media
        + avaliar()
    }

    class Serie {
        +List~Temporada~ temporadas
        +float nota_media
        +float nota_media_temporadas
        +int total_temporadas
        +int total_episodios
        +List~Avaliacao~avaliacoes
        +ver_temporadas()
        +avaliar()
    }

    %% Serie Subclasses
    class Temporada {
        +int numero
        +List~Episodio~ episodios
        +int total_episodios
        +float nota_media
        +float nota_temporada
        +List~Avaliacao~avaliacoes
        +mostrar_episodios()
        +avaliar()
    }

    class Episodio {
        +int duracao
        +int numero
        +float nota_media
        +List~Avaliacao~ avaliacoes
        +avaliar()
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



    %% Relacionamentos
    Midia <|-- Filme : herda
    Midia <|-- Serie : herda
    Midia <|-- Episodio : herda

    Serie "1" *-- "many" Temporada : contem
    Serie "1" *-- "many" Avaliacao : contem
    Temporada "1" *-- "many" Episodio : contem
    Temporada "1" *-- "many" Avaliacao : contem
    Episodio "1" *-- "many" Avaliacao : contem
    Filme "1" *-- "many" Avaliacao : contem

    ListaPersonalizada "1" o-- "many" Midia : agrega

    Historico "1" *-- "many" MidiaAssistida : contem
    MidiaAssistida "many" --> "1" Midia : refere-se

    Usuario "1" *-- "1" Historico : contem
    Relatorio "1" *-- "1" Historico : contem
```
