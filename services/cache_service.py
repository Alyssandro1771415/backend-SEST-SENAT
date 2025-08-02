from itertools import product
import json
import os
import pandas as pd
import unicodedata

class CacheService:
    _instance = None
    _initialized = False

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if not self.__class__._initialized:
            self.cache = {}
            self.cache_path = "./cache/cache_data.json"
            self.PanoramicAnalysesController = None

            os.makedirs(os.path.dirname(self.cache_path), exist_ok=True)

            if not os.path.exists(self.cache_path):
                with open(self.cache_path, "w", encoding="utf-8") as file:
                    json.dump({}, file, indent=2, ensure_ascii=False)

            try:
                with open(self.cache_path, "r", encoding="utf-8") as file:
                    content = file.read().strip()
                    if content:
                        self.cache = json.loads(content)
            except json.JSONDecodeError:
                print("[WARN] Cache corrompido. Reiniciando com cache vazio.")

            self.__class__._initialized = True

    def set_controller(self, controller):
        self.PanoramicAnalysesController = controller

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def get(self, key):
        try:
            return self.cache[key]
        except KeyError:
            return None
    
    def generate_key(self, filtros: list[dict]) -> str:
            def remover_acentos(texto: str) -> str:
                return ''.join(
                    c for c in unicodedata.normalize('NFKD', texto)
                    if not unicodedata.combining(c)
                )

            filtros_processados = [
                {
                    remover_acentos(k.lower()): v
                    for k, v in filtro.items()
                    if not (remover_acentos(k.lower()) == "Regiao" and v == "all")
                }
                for filtro in filtros
            ]

            key_parts = []
            for f in filtros_processados:
                for k in sorted(f):
                    key_parts.append(f"{k}={f[k]}")
            return "|".join(key_parts)

    def set(self, key: str, data_response: dict):
        if self.get(key) is not None:
            return
        self.cache[key] = data_response

        with open(self.cache_path, "w", encoding="utf-8") as file:
            json.dump(self.cache, file, indent=2, ensure_ascii=False)
    
    def starter_set(self):

        print("\033[93m[INFO] Iniciando cache...\033[0m")

        regiao = ["all", "Nordeste", "Norte", "Centro-Oeste", "Sudeste", "Sul"]
        sexo = ["Masculino", "Feminino"]
        ano_atendimento = [2023, 2024, 2025]

        regioes = [{"Regiao": r} for r in regiao]
        regiao_genero = [{"Regiao": r, "Genero": s} for r, s in product(regiao, sexo)]
        regiao_ano = [{"Regiao": r, "ano": a} for r, a in product(regiao, ano_atendimento)]
    
        self.cache["all"] = self.PanoramicAnalysesController.painel_atendimentos([{}])

        for item in regioes:

            key = self.generate_key([item])

            if self.get(key) is None:
                if item["Regiao"] == "all":
                    pass
                else:
                    self.cache[key] = self.PanoramicAnalysesController.painel_atendimentos([item])

        for item in regiao_genero:
            original_item = item.copy()  # salvar para referência da Regiao e Genero

            if item["Regiao"] == "all":
                filtros = [{"Genero": item["Genero"]}]
            else:
                filtros = [item]

            key = self.generate_key(filtros)

            if self.get(key) is None:
                self.cache[key] = self.PanoramicAnalysesController.painel_atendimentos(filtros)

        for item in regiao_ano:
            original_item = item.copy()

            if item["Regiao"] == "all":
                filtros = [{"ano": item["ano"]}]
            else:
                filtros = [item]

            key = self.generate_key(filtros)

            if self.get(key) is None:
                self.cache[key] = self.PanoramicAnalysesController.painel_atendimentos(filtros)


        with open(self.cache_path, "w") as file:
            json.dump(self.cache, file, indent=2, ensure_ascii=False)

        print("\033[92m[INFO] Cache iniciado com sucesso!\033[0m")
