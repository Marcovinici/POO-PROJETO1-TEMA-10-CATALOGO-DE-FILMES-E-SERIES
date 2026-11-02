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

## Pipocli Comandos

### Comandos globais


| AÇÃO                                                                            | COMANDO                                         | DISPONÍVEL |
| ------------------------------------------------------------------------------- | ----------------------------------------------- | ---------- |
| Logar o usuário                                                                 | `pipocli logar <usuario> <senha>`               | SIM        |
| Cadastrar um novo usuário (para cadastrar usuario administrador usa-se --admin) | `pipocli cad-usuario <usuario> <senha> --admin` | SIM        |


### Comandos de Usuário

| AÇÃO                            | COMANDO                       | DISPONÍVEL |
| ------------------------------- | ----------------------------- | ---------- |
| Checar qual usuário está logado | `pipocli usuario`             | SIM        |
| Alterar senha                   | `pipocli usuario alter-senha <nova_senha>` | SIM |

#### Manipulação de conteúdos

| AÇÃO                                       | COMANDO                                                                                                                                                        | DISPONÍVEL |
| ------------------------------------------ | -------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------- |
| Listar todas as mídias do catálogo         | `pipocli listar midias`                                                                                                                                        | SIM |
| Adicionar filme ao catálogo                | `pipocli adicionar filme` + todos os argumentos  necessários e `--gen <genero>`  ,  `--elen <elenco>`, `--dir <diretor>`, ` --rot <roteirista>` como opcionais | SIM        |
| Listar todos os filmes disponíveis         | `pipocli listar filmes`                                                                                                                                        | SIM        |
| Adicionar série ao catálogo                | `pipocli adicionar serie`+ todos os argumentos  necessários e `--gen <genero>`  ,  `--elen <elenco>`, `--dir <diretor>`, ` --rot <roteirista>` como opcionais  | SIM        |
| Adicionar temporada a serie                | `pipocli adicionar temporada <serie> <ano> <numero> <titulo_ep> <duracao_ep> <ano_ep> <numero_ep> <classificacao>` | SIM |
| Adicionar episódio a temporada             | `pipocli adicionar episodio <serie> <ano> <temporada> <numero> <titulo> <duracao> <ano_ep> <classificacao>` | SIM |
| Listar temporadas de uma serie             | `pipocli listar temporadas <serie> [--ano ANO]` | SIM |
| Listar episódios de uma temporada          | `pipocli listar episodios <serie> <temporada> [--ano ANO]` | SIM |
| Listar todas as séries disponíveis         | `pipocli listar series`                                                                                                                                        | SIM        |
| Ver determinada lista de mídias disponível | `pipocli lista mostrar <nome_da_lista>`                                                                                                                        | SIM        |
| Ver listas de mídias disponíveis           | `pipocli listar listas`                                                                                                                                        | SIM        |
| Adicionar nova lista ao catálogo           | `pipocli adicionar lista`                                                                                                                                      | SIM        |
| Adicionar nova mídia a lista               | `pipocli lista <nome_da_lista> adicionar filme <nome_do_filme>` ou `pipocli lista <nome_da_lista> adicionar serie <nome_da_serie>`                             | SIM        |
| Ver lista de Recomendados                  | `pipocli recomendados` | SIM |
| Remover filme de uma lista                 | `pipocli lista <nome> remover-filme <filme>` | SIM |
| Remover série de uma lista                 | `pipocli lista <nome> remover-serie <serie>` | SIM |
| Remover filme do catálogo                  | `pipocli remover filme <titulo> [--ano ANO]` | SIM |
| Remover série do catálogo                  | `pipocli remover serie <titulo> [--ano ANO]` | SIM |
| Remover temporada de uma serie             | `pipocli remover temporada <serie> <temporada> [--ano ANO]` | SIM |
| Remover episodio de uma temporada          | `pipocli remover episodio <serie> <temporada> <episodio> [--ano ANO]` | SIM |
#### Visualização,  Avaliação, Histórico e Relatórios

| AÇÃO                                                  | COMANDO | DISPONÍVEL |
| ----------------------------------------------------- | ------- | ---------- |
| Assistir filme                                        | `pipocli assistir filme <titulo> [--ano ANO]` | SIM |
| Assistir episódio                                     | `pipocli assistir episodio <serie> <temporada> <episodio> [--ano ANO]` | SIM |
| Ver informações da série                              | `pipocli info serie <serie> [--ano ANO]` | SIM |
| Ver informações da temporada                          | `pipocli info temporada <serie> <temporada> [--ano ANO]` | SIM |
| Ver informações do episódio                           | `pipocli info episodio <serie> <temporada> <episodio> [--ano ANO]` | SIM |
| Ver informações do filme                              | `pipocli info filme <titulo> [--ano ANO]` | SIM |
| Avaliar filme                                         | `pipocli avaliar filme <titulo> <nota> [--comentario TEXTO]` | SIM |
| Avaliar episódio                                      | `pipocli avaliar episodio <serie> <temporada> <episodio> <nota> [--ano ANO]` | SIM |
| Avaliar temporada                                     | `pipocli avaliar temporada <serie> <temporada> <nota> [--ano ANO]` | SIM |
| Avaliar série                                         | `pipocli avaliar serie <serie> <nota> [--ano ANO]` | SIM |
| Ver avaliações de filme                               | `pipocli avaliacoes filme <titulo> [--ano ANO]` | SIM |
| Ver avaliações de episódio                            | `pipocli avaliacoes episodio <serie> <temporada> <episodio> [--ano ANO]` | SIM |
| Ver avaliações de temporada                           | `pipocli avaliacoes temporada <serie> <temporada> [--ano ANO]` | SIM |
| Ver avaliações de série                               | `pipocli avaliacoes serie <serie> [--ano ANO]` | SIM |
| Listar filmes assistidos                              | `pipocli listar filmes-assistidos` | SIM |
| Listar series assistidas e que estão sendo assistidas | `pipocli listar series-assistidas` | SIM |
| Listar últimas mídias assistidas                      | `pipocli listar ultimas-assistidas [--limite N]` | SIM |
| Relatório de média de notas por gênero                | `pipocli relatorio generos` | SIM |
| Relatório de tempo total assistido                    | `pipocli relatorio tempo` | SIM |
| Relatótio do Top10 filmes/series                      | `pipocli relatorio top10` | SIM |
| Relatório de séries com maior número de episódios     | `pipocli relatorio series-episodios` | SIM |
#### Configurações

| AÇÃO                                                | COMANDO | DISPONÍVEL |
| --------------------------------------------------- | ------- | ---------- |
| Ver configurações atuais                            | `pipocli config ver` | SIM |
| Alterar nota mínima para "recomendado"              | `pipocli config nota <valor>` | SIM |
| Alterar limite de listas personalizadas por usuário | `pipocli config listas <valor>` | SIM |
| Alterar métrica de duração                          | `pipocli config metrica horas\|minutos` | SIM |




### Comandos de Administrador

| AÇÃO                                 | COMANDO                   | DISPONÍVEL |
| ------------------------------------ | ------------------------- | ---------- |
| Listar todos os usuários do catálogo | `pipocli listar-usuarios` | SIM        |
