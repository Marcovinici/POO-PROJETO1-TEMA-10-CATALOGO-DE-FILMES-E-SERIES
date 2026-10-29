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
        +List~str~elenco
        +List~str~diretor
        +List~str~roteirista
        +List~Avaliacao~avaliacoes
        +int nota_media
        %%---Métodos---
        +exibir_detalhes()
        +avaliar()
        +ver_avaliacoes()
    }


    class ListaPersonalizada{
        +int id
        +str nome
        +str usuario
        +List~Midia~midias
    }


    class Relatorio {
        +media_de_notas_por_genero()
        +tempo_total_assistido_por_tipo()
        +top10_bem_avaliados()
        +series_mais_assistidas_por_ep()

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
        +str metrica_duracao
        +cria_json_settings()
        +conversor_de_duracao()
        +mudar_nota_minima_de_recomendados()
        +mudar_limite_de_listas_recomendadas()
    }



    %% Heranças de Midia 
    class Filme {
        +int duracao
        +float nota
    }

    class Serie {
        +List~Temporada~ temporadas
        +float nota_media
        +float nota_media_temporadas
        +int total_temporadas
        +int total_episodios
        +ver_temporadas()
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
        +media_avaliacao_episodios()
        +avaliar_temporada()
        +ver_avaliacoes()
    }

    class Episodio {
        +int duracao
        +int numero
        +float nota_media
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

    Usuario "1" *-- "1" Configuracoes : contem
    Usuario "1" *-- "1" Historico : contem
```
