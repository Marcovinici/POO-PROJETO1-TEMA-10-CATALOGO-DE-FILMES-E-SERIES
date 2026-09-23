# POO-PROJETO1-TEMA-10-CATALOGO-DE-FILMES-E-SERIES
Repositório destinado ao primeiro projeto da cadeira de POO

## Descrição do Projeto e Objetivos
Desenvolver um sistema de linha de comando (CLI) ou API mínima (FastAPI/Flask, opcional) para gerenciar um catálogo pessoal de filmes e séries, com avaliações, status de visualização, temporadas/episódios, histórico e relatórios de consumo de mídia. O sistema deve permitir acompanhar o progresso de séries e comparar avaliações entre mídias. A persistência deve ser simples (em JSON ou SQLite) e a modelagem orientada a objetos deve enfatizar herança, encapsulamento, validações e composição.

## Requisitos Funcionais
### - Cadastro de mídias
Campos: título, tipo (FILME ou SERIE), gênero, ano, duração (minutos), classificação indicativa, elenco (lista), e status (NÃO ASSISTIDO, ASSISTINDO, ASSISTIDO).
Impedir duplicidade de títulos com mesmo tipo e ano.
### - Séries e episódios
- Para SERIE, registrar temporadas e episódios:
Campos: nº temporada, nº episódio, título, duração, data de lançamento, status de visualização, nota (opcional).
- Marcar série como “ASSISTIDA” quando todos os episódios estiverem concluídos.
- Avaliações
- Permitir ao usuário avaliar filmes e episódios (nota de 0 a 10).
- Calcular automaticamente a nota média da série e nota geral do catálogo.

## Estrutura de Classes
```mermaid
classDiagram
    %% Classes-base
    class Midia {
        %%---Atributos---
        +str titulo
        +str genero
        +int ano
        +int duracao
        +str classificacao
        +str status
        +List~str~ elenco
        +List~str~ diretor
        +List~str~ roteirista
        %%---Métodos---
        +exibir_detalhes()
        +alterar_status()
    }
    
    class Listas {

    }

    class Relatorios {

    }

    class Historico{

    }

    class Configuracoes{

    }

    %% Heranças de Midia 
    class Filme {
        +int nota
        +List~Avaliacao~avaliacoes
        +avaliar_filme()
    }

    class Serie {
        +List~Temporada~ temporadas
        +int nota_media
        +int total_temporadas
        +int total_episodios
        +List~Avaliacao~avaliacoes
        +media_avaliacao_temporadas()
        +avaliar_serie()
    }

    %% Serie Subclasses
    class Temporada {
        +int numero
        +List~Episodio~ episodios
        +int total_episodios
        +int nota_media
        +int nota
        +List~Avaliacao~avaliacoes
        +media_avaliacao_episodios()
        +avaliar_temporada()
        +
    }

    class Episodio {
        +int numero
        +str titulo
        +int duracao
        +float nota
        +str status
        +int nota
        +List~Avaliacao~avaliacoes
        +avaliar_episodio()
        +reproduzir()
        +ver_avaliacoes()
    }

    %% Avaliações
    class Avaliacao{
        +str comentario
        +int nota
        +adicionar_nota()
        +adicionar_comentario()
    }

    %% Relacionamentos
    Midia <|-- Filme : herda
    Midia <|-- Serie : herda
    Serie "1" *-- "many" Temporada : contem
    Serie "1" *-- "many" Avaliacao : contem
    Temporada "1" *-- "many" Episodio : contem
    Temporada "1" *-- "many" Avaliacao : contem
    Episodio "1" *-- "many" Avaliacao : contem
    Filme "1" *-- "many" Avaliacao : contem
```
