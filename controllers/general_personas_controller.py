import pandas as pd
import os
class GeneralPersonasController:
    _instance = None
    _initialized = False

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
        response = {"regional":self.dataFrame["nacional"].to_dict(orient="records"),
                    "regional_doencas":self.dataFrame["nacional_doencas"].to_dict(orient="records"),
                    "regional_ocupacional":self.dataFrame["nacional_ocupacional"].to_dict(orient="records")}
        
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
                database_regional["Masculino"],
                database_regional_doencas["Masculino"],
                database_regional_ocupacional["Masculino"]
            ],
            "Feminino": [
                database_regional["Feminino"],
                database_regional_doencas["Feminino"],
                database_regional_ocupacional["Feminino"]
            ]
        }

        return response
