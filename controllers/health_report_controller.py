import pandas as pd
import math

class HealthReportController:
    _instance = None
    _initialized = False

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(HealthReportController, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        if self._initialized:
            return
        print(f"\033[92mIniciando o controller de relatório de saúde\033[m")
        self.dataFrame = pd.read_csv("./db/Relatorio_de_saude.csv", sep="|", encoding="utf-8")
        print(f"\033[92mDataFrame carregado com {self.dataFrame.shape[0]} linhas e {self.dataFrame.shape[1]} colunas\033[m")
        HealthReportController._initialized = True

    def get_datas_by_filters(self, filters: list):
        if not filters:
            return self.dataFrame.to_dict(orient="records")

        filtered_data = self.dataFrame

        for filter in filters:
            for key, value in filter.items():
                filtered_data = filtered_data[filtered_data[key] == value]

        return filtered_data.to_dict(orient="records")

    def calc_media(self, valores: list):
        # Filtra valores numéricos válidos (não None, não NaN)
        valores_validos = [v for v in valores if isinstance(v, (int, float)) and not math.isnan(v)]

        if not valores_validos:
            return 0

        return sum(valores_validos) / len(valores_validos)

    def calc_all_average(self, valores: list):
        averages_datas = {
            "mediaIMC": round(self.calc_media([p['imc'] for p in valores]), 2),
            "percGordura": round(self.calc_media([p['percentual_gordura'] for p in valores]), 2),
            "mme": round(self.calc_media([p['mme'] for p in valores]), 2),
            "gorduraVisceral": round(self.calc_media([p['gordura_visceral'] for p in valores]), 2),
            "rmssd": round(self.calc_media([p['rmssd'] for p in valores]), 2),
            "pnni_50": round(self.calc_media([p['pnni_50'] for p in valores]), 2),
            "sdnn": round(self.calc_media([p['sdnn'] for p in valores]), 2),
            "minutos_atividades_diarios_media": round(self.calc_media([p['minutos_atividades_diarios_media'] for p in valores]), 2),
            "passos_med": round(self.calc_media([p['passos_med'] for p in valores]), 2),
            "minutos_diarios_atividades_intensa": round(self.calc_media([p['minutos_diarios_atividades_intensa'] for p in valores]), 2),
            "minutos_diarios_atividades_moderada": round(self.calc_media([p['minutos_diarios_atividades_moderada'] for p in valores]), 2),
            "eficiencia_sono": round(self.calc_media([p['eficiencia_sono'] for p in valores]), 2),
            "duracao_sono_horas": round(self.calc_media([p['duracao_sono_minutos'] for p in valores]) / 60, 2),
        }

        minutos_diarios_atividades_intensa_moderada = round(
            averages_datas["minutos_diarios_atividades_intensa"] +
            averages_datas["minutos_diarios_atividades_moderada"], 2)

        averages_datas["minutos_diarios_atividades_intensa_moderada"] = minutos_diarios_atividades_intensa_moderada

        return averages_datas

    def calc_avaliation_life_style():
        return

    def calc_avaliation_health():
        return