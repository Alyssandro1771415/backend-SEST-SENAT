async def get_region_and_filters(regiao: str, filters: dict):
    query_parts = []

    if regiao != "all":
        query_parts.append({"regiao": regiao})

    if filters:
        if filters.get("unidade"):
            query_parts.append({"unidade": filters["unidade"][0]})
        if filters.get("ano"):
            query_parts.append({"ano": filters["ano"][0]})
        if filters.get("idade"):
            query_parts.append({"faixa_etaria": filters["idade"][0]})
        if filters.get("sexo"):
            query_parts.append({"sexo": filters["sexo"][0]})
        if filters.get("conselho"):
            query_parts.append({"conselho": filters["conselho"][0]})
        if filters.get("estado"):
            query_parts.append({"estado": filters["estado"][0]})
        if filters.get("modal"):
            query_parts.append({"modal": filters["modal"][0]})
        if filters.get("cnpj"):
            query_parts.append({"cnpj": str(filters["cnpj"][0]).zfill(14)})
        if filters.get("nome_empresa"):
            query_parts.append({"nome_empresa": filters["nome_empresa"][0]})

    return query_parts
