import json
import pandas as pd
from itertools import product
import os

class CacheService:
    def __init__(self, PanoramicAnalysesController):
        self.cache = {}
        self.PanoramicAnalysesController = PanoramicAnalysesController
        self.cache_path = "./cache/cache_data.json"

        if os.path.exists(self.cache_path):
            try:
                with open(self.cache_path, "r") as file:
                    content = file.read().strip()
                    if content:
                        self.cache = json.loads(content)
            except json.JSONDecodeError:
                print("[WARN] Cache corrompido. Reiniciando com cache vazio.")

    def get(self, key):
        try:
            return self.cache[key]
        except KeyError:
            return None
    
    def set(self, filtros: dict):
        key = "_".join(str(filtros[k]) for k in sorted(filtros))

        if self.get(key) is not None:
            return

        filtros_completos = filtros
        if filtros.get("regiao") == "all":
            filtros_completos = {k: v for k, v in filtros.items() if k != "regiao"}

        resultado = self.PanoramicAnalysesController.painel_atendimentos([filtros_completos])
        self.cache[key] = resultado

        with open(self.cache_path, "w") as file:
            json.dump(self.cache, file, indent=2, ensure_ascii=False)
    
    def starter_set(self):

        print("\033[93m[INFO] Iniciando cache...\033[0m")

        regiao = ["all", "Nordeste", "Norte", "Centro-Oeste", "Sudeste", "Sul"]
        sexo = ["Masculino", "Feminino"]
        ano_atendimento = [2023, 2024, 2025]

        regiao_genero = [{"regiao": r, "genero": s} for r, s in product(regiao, sexo)]
        regiao_ano = [{"regiao": r, "ano": a} for r, a in product(regiao, ano_atendimento)]

        self.cache["all"] = self.PanoramicAnalysesController.painel_atendimentos([{}])

        for item in regiao_genero:
            key = f"{item['regiao']}_{item['genero']}"

            if self.get(key) is None:
                if item["regiao"] == "all":
                    item = [{"genero": item["genero"]}]
                    self.cache[key] = self.PanoramicAnalysesController.painel_atendimentos(item)
                else:
                    self.cache[key] = self.PanoramicAnalysesController.painel_atendimentos([item])

        for item in regiao_ano:
            key = f"{item['regiao']}_{item['ano']}"

            if self.get(key) is None:
                if item["regiao"] == "all":
                    item = [{"ano": item["ano"]}]
                    self.cache[key] = self.PanoramicAnalysesController.painel_atendimentos(item)
                else:
                    self.cache[key] = self.PanoramicAnalysesController.painel_atendimentos([item])

        with open(self.cache_path, "w") as file:
            json.dump(self.cache, file, indent=2, ensure_ascii=False)

        print("\033[92m[INFO] Cache iniciado com sucesso!\033[0m")
