from models.patient_model import Patient
from beanie.operators import And

async def get_region_health_datas_filters(regiao: str, filters: dict):

    query_parts = []

    if regiao != "all":
        query_parts.append(Patient.regiao == regiao)

    if filters:
        if filters.get("unidade"):
            query_parts.append(Patient.unidade == filters["unidade"][0])
        if filters.get("idade"):
            query_parts.append(Patient.faixa_etaria == filters["idade"][0])
        if filters.get("genero"):
            query_parts.append(Patient.sexo == filters["genero"][0])
        if filters.get("conselho"):
            query_parts.append(Patient.conselho == filters["conselho"][0])
        if filters.get("estado"):
            query_parts.append(Patient.estado == filters["estado"][0])
        if filters.get("modal"):
            query_parts.append(Patient.modal == filters["modal"][0])
        if filters.get("cnpj"):
            query_parts.append(Patient.cnpj == str(filters["cnpj"][0]).zfill(14))
        if filters.get("nome_empresa"):
            query_parts.append(Patient.nome_empresa == filters["nome_empresa"][0])


    if query_parts:
        query = And(*query_parts)
        patients_filtered_datas = await Patient.find(query).to_list()
    else:
        patients_filtered_datas = await Patient.find_all().to_list()

    all_datas = [p.model_dump(exclude={"id"}) for p in patients_filtered_datas]

    return all_datas