from pathlib import Path
import json
from domain.excecoes import DadosInvalidosError

class ConfigRepository:
    """Representa as configurações pessoais do usuário

    Esta classe guarda os limites e preferências do catálogo e permite
    convertê-los ou alterá-los.

    Attributes:
    nota_minima_de_recomendados (float): Nota mínima para uma mídia ser recomendada
    limite_de_listas_personalizadas (int): Número máximo de listas personalizadas
    multiplicador_de_duracao (float): Valor que multiplica as durações das mídias
    """
    def __init__(self, caminho_json):
        self.caminho = Path(caminho_json)
        self._config = {} # Inicializa config como um dicionário vazio antes de carregá-lo
        self.carregar_config()


    def carregar_config(self) -> dict:
        """
        Acessa e devolve o dicionário de configurações

        Método usado para carregar as configurações: acessa o arquivo .json, se ele conter um dicionário de configurações,
        guarda o mesmo em '_config', se não, cria o dicionário de configurações com dados padrão e o guarda em '_config'  
        """
        if self.caminho.exists():
            with self.caminho.open("r", encoding="utf-8") as arquivo:
                self._config = json.load(arquivo)
        else:
            self._config = {
                "nota_minima_de_recomendados": 7.0,
                "limite_de_listas_personalizadas": 10,
                "multiplicador_de_duracao": 1,
            }

    # Getter e setter de nota_minima_de_recomendados
    @property
    def nota_minima_de_recomendados(self):
        return self._config["nota_minima_de_recomendados"]
    @nota_minima_de_recomendados.setter
    def nota_minima_de_recomendados(self, novo_valor: float):
        if 0 <= novo_valor <= 10 and (isinstance(novo_valor, float) or isinstance(novo_valor, int)):
            self._config["nota_minima_de_recomendados"] = novo_valor
        else:
            raise DadosInvalidosError("A nota mínima de um recomendado deve ser do tipo 'float'")

    # Getter e setter de limite_de_listas_personalizadas
    @property
    def limite_de_listas_personalizadas(self):
        return self._config["limite_de_listas_personalizadas"]
    @limite_de_listas_personalizadas.setter
    def limite_de_listas_personalizadas(self, novo_valor: int):
        if 0 < novo_valor and isinstance(novo_valor, int):
            self._config["limite_de_listas_personalizadas"] = novo_valor
        else:
            raise DadosInvalidosError("O valor que representa o limite de listas personalizadas de ser maior que 0 e do tipo 'int'")

    # Getter e setter de multiplicador_de_duracao
    @property
    def multiplicador_de_duracao(self):
        return self._config["multiplicador_de_duracao"]
    @multiplicador_de_duracao.setter
    def multiplicador_de_duracao(self, novo_valor):
        if (novo_valor == 1 or  novo_valor == 0.016666666) and (isinstance(novo_valor, float) or isinstance(novo_valor, int)):
            self._config["multiplicador_de_duracao"] = novo_valor
        else:
            raise DadosInvalidosError("O valor do multiplicador deve ser ou '1' ou '1/60'")

    def altera_multiplicador(self, metrica: str):
        """
        Altera o multiplicador de duração seguindo a métrica passada como argumento: horas ou minutos
        """
        if metrica is None:
            raise DadosInvalidosError("A metrica não pode receber valor 'None'")
        elif metrica.lower() in ["horas", "minutos"]:
            metrica = metrica.lower()
            if metrica == "horas":
                self.multiplicador_de_duracao = 0.016666666
            else:
                self.multiplicador_de_duracao = 1
        else:
            raise DadosInvalidosError("A metrica deve ser um dos seguintes valores: 'horas', 'minutos'")

    def atualizar_config(self):
        """
        Atualiza o arquivo json com a '_config' atual
        """
        with self.caminho.open("w", encoding="utf-8") as arquivo:
            json.dump(self._config, arquivo, ensure_ascii=False, indent=4)
