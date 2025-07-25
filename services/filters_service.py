class FiltersService:

    async def get_region_and_filters_hearth_report(self, regiao: str, filters: dict):
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

    async def get_region_and_filters_panoramic_analyse(self, regiao: str, filters: dict):
        query_parts = []

        if regiao != "all":
            query_parts.append({"Região": regiao})

        if filters:
            if filters.get("unidade"):
                query_parts.append({"UnidadeAtendimento": filters["unidade"][0]})
            if filters.get("ano"):
                query_parts.append({"Ano": filters["ano"][0]})
            if filters.get("idade"):
                query_parts.append({"FaixaEtaria": filters["idade"][0]})
            if filters.get("genero"):
                query_parts.append({"Genero": filters["genero"][0]})
            if filters.get("conselho"):
                query_parts.append({"ConselhoRegional": filters["conselho"][0]})
            if filters.get("estado"):
                query_parts.append({"UF": filters["estado"][0]})
            if filters.get("modal"):
                query_parts.append({"Modal": filters["modal"][0]})
            if filters.get("cnpj"):
                query_parts.append({"CNPJ": str(filters["cnpj"][0]).zfill(14)})
            if filters.get("nome_empresa"):
                query_parts.append({"NomeEmpresa": filters["nome_empresa"][0]})

        return query_parts