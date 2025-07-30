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
        print(f"\033[92mIniciando o controller de relatório de saúde\033[m")
        self.dataFrame = pd.read_excel("./db/Perfis_SEST_SENAT_2025.xlsx", sheet_name=["nacional", "regional",
                                                                                       "nacional_doencas", "regional_doencas",
                                                                                       "nacional_ocupacional", "regional_ocupacional",])
        print(f"\033[92mDataFrame carregado com {len(self.dataFrame)} tabelas de personas\033[m")
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
        Return datas of regional personas based on the region provided
        """
        database_regional = {
            "Masculino": self.dataFrame["regional"][self.dataFrame["regional"]["Regiao"] == regiao.upper()].to_dict(orient="records"),
            "Feminino": self.dataFrame["regional"][self.dataFrame["regional"]["Regiao"] == regiao.upper()].to_dict(orient="records")
        }

        database_regional_doencas = {
            "Masculino": self.dataFrame["regional_doencas"][self.dataFrame["regional_doencas"]["Regiao"] == regiao].to_dict(orient="records"),
            "Feminino": self.dataFrame["regional_doencas"][self.dataFrame["regional_doencas"]["Regiao"] == regiao].to_dict(orient="records")
        }

        database_regional_ocupacional = {
            "Masculino": self.dataFrame["regional_ocupacional"][self.dataFrame["regional_ocupacional"]["Regiao"] == regiao].to_dict(orient="records"),
            "Feminino": self.dataFrame["regional_ocupacional"][self.dataFrame["regional_ocupacional"]["Regiao"] == regiao].to_dict(orient="records")
        }

        response = {
            "Image_Masculino": f'{os.getenv("BACKEND_URL")}/db/PERSONAS/{database_regional["Masculino"][0]["Nome"]}.jpg',
            "Image_Feminino": f'{os.getenv("BACKEND_URL")}/db/PERSONAS/{database_regional["Feminino"][0]["Nome"]}.jpg',
            "Masculino": [
                database_regional["Masculino"][0],
                database_regional_doencas["Masculino"][1],
                database_regional_ocupacional["Masculino"][1]
            ],
            "Feminino": [
                database_regional["Feminino"][1],
                database_regional_doencas["Feminino"][0],
                database_regional_ocupacional["Feminino"][0]
            ]
        }
        # Formata as chaves internas dos dicionários de cada gênero
        for genero in ["Masculino", "Feminino"]:
            response[genero] = [self.formatter.format_keys(d) for d in response[genero]]

        return response
