import pandas as pd
import os

from services.formatation_service import FormatationService

class GeneralPersonasController:
    _instance = None
    _initialized = False
    formatter = FormatationService()

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(GeneralPersonasController, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        if self._initialized:
            return
        print(f"\033[91mIniciando o controller de personas\033[m")
        self.dataFrame = pd.read_excel("./db/Perfis_SEST_SENAT_2025.xlsx", sheet_name=["nacional", "regional",
                                                                                       "nacional_doencas", "regional_doencas",
                                                                                       "nacional_ocupacional", "regional_ocupacional",])
        print(f"\033[91mDataFrame carregado com {len(self.dataFrame)} tabelas de personas\033[m")
        GeneralPersonasController._initialized = True

    def get_datas_personas_nacional(self):
        """
        Return datas of national personas
        """
        database_nacional = self.dataFrame["nacional"].to_dict(orient="records")

        database_nacional = {"Masculino": self.dataFrame["nacional"].to_dict(orient="records")[0],
                             "Feminino": self.dataFrame["nacional"].to_dict(orient="records")[1]}
        
        database_nacional_doencas = {"Masculino": self.dataFrame["nacional_doencas"].to_dict(orient="records")[1],
                                     "Feminino": self.dataFrame["nacional_doencas"].to_dict(orient="records")[0]}
        
        database_nacional_ocupacional = {"Masculino": self.dataFrame["nacional_ocupacional"].to_dict(orient="records")[1],
                                         "Feminino": self.dataFrame["nacional_ocupacional"].to_dict(orient="records")[0]}

        response = {"Image_Masculino": f'{os.getenv("BACKEND_URL")}/db/PERSONAS/{database_nacional["Masculino"]["Nome"]}.jpg',
                   "Image_Feminino": f'{os.getenv("BACKEND_URL")}/db/PERSONAS/{database_nacional["Feminino"]["Nome"]}.jpg',
                   "Masculino": [
                       database_nacional["Masculino"],
                       database_nacional_doencas["Masculino"],
                       database_nacional_ocupacional["Masculino"]
                   ],
                   "Feminino": [
                       database_nacional["Feminino"],
                       database_nacional_doencas["Feminino"],
                       database_nacional_ocupacional["Feminino"]
                   ]}
        
        for genero in ["Masculino", "Feminino"]:
            response[genero] = [self.formatter.format_keys(d) for d in response[genero]]

        return response
    
    def get_datas_personas_regional(self, regiao: str):
        """
        Return datas of regional personas based on the region provided.
        Caso a região seja 'Centro-Oeste', os dados femininos não são retornados.
        """
        regiao_upper = regiao.upper()

        df_regional = self.dataFrame["regional"]
        df_doencas = self.dataFrame["regional_doencas"]
        df_ocupacional = self.dataFrame["regional_ocupacional"]

        regional_data = df_regional[df_regional["Regiao"] == regiao_upper].to_dict(orient="records")
        doencas_data = df_doencas[df_doencas["Regiao"] == regiao].to_dict(orient="records")
        ocupacional_data = df_ocupacional[df_ocupacional["Regiao"] == regiao].to_dict(orient="records")

        print(ocupacional_data)

        response = {}

        response["Image_Masculino"] = f'{os.getenv("BACKEND_URL")}/db/PERSONAS/{regional_data[0]["Nome"]}.jpg' \
            if "Masculino" in regional_data[0].get("Nome", "") else \
            f'{os.getenv("BACKEND_URL")}/db/PERSONAS/{regional_data[1]["Nome"]}.jpg'

        masculino_index = 0 if "Masculino" in regional_data[0].get("Nome", "") else 1

        if regiao_upper != "CENTRO-OESTE":
            response["Masculino"] = [
                self.formatter.format_keys(regional_data[masculino_index]),
                self.formatter.format_keys(doencas_data[1]) if len(doencas_data) > 1 else {},
                self.formatter.format_keys(ocupacional_data[1]) if len(ocupacional_data) > 1 else {},
            ]
        else:
            response["Masculino"] = [
                self.formatter.format_keys(regional_data[masculino_index]),
                self.formatter.format_keys(doencas_data[1]) if len(doencas_data) > 1 else {},
                self.formatter.format_keys(ocupacional_data[1]) if len(ocupacional_data) > 1 else self.formatter.format_keys(ocupacional_data[0]),
            ]

        if regiao_upper != "CENTRO-OESTE":
            feminino_index = 1 - masculino_index
            response["Image_Feminino"] = f'{os.getenv("BACKEND_URL")}/db/PERSONAS/{regional_data[feminino_index]["Nome"]}.jpg'
            response["Feminino"] = [
                self.formatter.format_keys(regional_data[feminino_index]),
                self.formatter.format_keys(doencas_data[0]) if len(doencas_data) > 0 else {},
                self.formatter.format_keys(ocupacional_data[0]) if len(ocupacional_data) > 0 else {},
            ]

        return response
