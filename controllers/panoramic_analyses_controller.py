from models.consultations_model import Consultation
from beanie.operators import And
from typing import Optional

# Como já filtra o ano e depois a categoria, OKAY
async def get_total_atendimentos_2024(categoria: str) -> int:
    pipeline = []

    match_stage = {"Ano_Atendimento": 2024}

    if categoria:
        match_stage["AreaSaude"] = categoria

    pipeline.append({"$match": match_stage})
    pipeline.append({"$count": "total"})

    result = await Consultation.aggregate(pipeline).to_list(length=1)

    if result:
        return result[0]["total"]
    return 0

# Como já filtra o ano e depois a categoria, OKAY
async def get_variacao_2023(categoria: str, total_2024: int) -> int:
    pipeline = []

    match_stage = {"Ano_Atendimento": 2023}

    if categoria:
        match_stage["AreaSaude"] = categoria

    pipeline.append({"$match": match_stage})
    pipeline.append({"$count": "total"})

    result = await Consultation.aggregate(pipeline).to_list(length=1)

    total_2023 = result[0]["total"]

    final_result = round(((total_2024 - total_2023) / total_2023) * 100, 2) if total_2023 != 0 else 0
    
    return final_result

# Recebe as partes da query referente aos filtros e a categoria
async def get_atendimentos_genero(categoria: str, query_parts: list):
    filtros_base = query_parts.copy()
    filtros_base.append({"AreaSaude": categoria})

    pipeline_masculino = [
        {
            "$match": {
                "$and": [{"Genero": "Masculino"}, *filtros_base]
            }
        },
        {"$count": "total"}
    ]

    pipeline_feminino = [
        {
            "$match": {
                "$and": [{"Genero": "Feminino"}, *filtros_base]
            }
        },
        {"$count": "total"}
    ]

    total_masculino = await Consultation.aggregate(pipeline_masculino).to_list(length=1)
    total_feminino = await Consultation.aggregate(pipeline_feminino).to_list(length=1)

    masculino = total_masculino[0]["total"] if total_masculino else 0
    feminino = total_feminino[0]["total"] if total_feminino else 0

    total_masculino_porcentagem = round((masculino / (masculino + feminino)) * 100, 2) if (masculino + feminino) != 0 else 0
    total_feminino_porcentagem = round(100 - total_masculino_porcentagem, 2)

    return total_masculino_porcentagem, total_feminino_porcentagem


