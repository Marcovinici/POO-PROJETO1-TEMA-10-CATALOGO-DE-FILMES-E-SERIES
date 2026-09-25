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
        +criar_lista()
        +adicionar_na_lista()
        +remover_da_lista()
    }

    class Relatorio {
        +str nome_do_usuario
        +str nome_do_relatorio
        +criar_relatorio()
        +atualizar_relatorio()
        +mostrar_relatorio()
    }

    class Historico {
        +List~Midia~midias_assistidas
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
        +float nota
        +List~Avaliacao~avaliacoes
        +avaliar_filme()
        +marcar_concluido()
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
        +int numero
        +str titulo
        +int duracao
        +float nota
        +str status
        +List~Avaliacao~avaliacoes
        +avaliar_episodio()
        +marcar_concluido()
        +ver_avaliacoes()
    }



    %% Avaliações
    class Avaliacao {
        +str tipo
        +str comentario
        +float nota
        +adicionar_nota()
        +adicionar_comentario()
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
    Serie "1" *-- "many" Temporada : contem
    Serie "1" *-- "many" Avaliacao : contem
    Temporada "1" *-- "many" Episodio : contem
    Temporada "1" *-- "many" Avaliacao : contem
    Episodio "1" *-- "many" Avaliacao : contem
    Filme "1" *-- "many" Avaliacao : contem
    Catalogo "1" *-- "many" Filme : contem
    Catalogo "1" *-- "many" Serie : contem
    Catalogo "1" *-- "many" Lista : contem
    Lista "1" o-- "many" Filme : agrega
    Lista "1" o-- "many" Serie : agrega
    Relatorio <|-- RelatorioGeral : herda
    Relatorio <|-- RelatorioHistorico : herda
    Historico "1" *-- "1" RelatorioHistorico : contem
    Usuario "1" *-- "1" Catalogo : contem
    Usuario "1" *-- "1" Configuracoes : contem
    Usuario "1" *-- "1" RelatorioGeral : contem
    Usuario "1" *-- "1" Historico : contem
```
