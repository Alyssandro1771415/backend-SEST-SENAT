from models.patient_model import Patient
from beanie.operators import And

def calc_media(valores: list):

    for index, valor in enumerate(valores):
        if valor is None:
            valores[index] = 0

    if not valores:
        return 0

    return sum(valores) / len(valores)

def calc_all_average(valores: list):
    averages_datas = {
        "mediaIMC": round(calc_media([p['imc'] for p in valores]), 2),
        "percGordura": round(calc_media([p['percentual_gordura'] for p in valores]), 2),
        "mme": round(calc_media([p['mme'] for p in valores]), 2),
        "gorduraVisceral": round(calc_media([p['gordura_visceral'] for p in valores]), 2),
        "rmssd": round(calc_media([p['rmssd'] for p in valores]), 2),
        "pnni_50": round(calc_media([p['pnni_50'] for p in valores]), 2),
        "sdnn": round(calc_media([p['sdnn'] for p in valores]), 2),
        "minutos_atividades_diarios_media": round(calc_media([p['minutos_atividades_diarios_media'] for p in valores]), 2),
        "passos_med": round(calc_media([p['passos_med'] for p in valores]), 2),
        "minutos_diarios_atividades_intensa": round(calc_media([p['minutos_diarios_atividades_intensa'] for p in valores]), 2),
        "minutos_diarios_atividades_moderada": round(calc_media([p['minutos_diarios_atividades_moderada'] for p in valores]), 2),
        "eficiencia_sono": round(calc_media([p['eficiencia_sono'] for p in valores]), 2),
        "duracao_sono_horas": round(calc_media([p['duracao_sono_minutos'] for p in valores]) / 60, 2),
    }

    minutos_diarios_atividades_intensa_moderada = round(averages_datas["minutos_diarios_atividades_intensa"] + averages_datas["minutos_diarios_atividades_moderada"], 2)

    averages_datas["minutos_diarios_atividades_intensa_moderada"] = minutos_diarios_atividades_intensa_moderada

    return averages_datas

def calc_avaliation_life_style():
    return

def calc_avaliation_health():
    return