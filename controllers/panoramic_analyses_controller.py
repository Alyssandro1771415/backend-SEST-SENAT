import numpy as np
import pandas as pd
from tqdm import tqdm

from services.cache_service import CacheService

class PanoramicAnalysesController:
    _instance = None
    _initialized = False

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if not self.__class__._initialized:
            print(f"\033[94mIniciando o controller de análises panorâmicas\033[m")

            file_path = "./db/Atendimentos_SEST_SENAT.csv"

            # Contar linhas (descontando header)
            total_rows = sum(1 for _ in open(file_path, encoding="utf-8")) - 1

            # Ler em chunks e mostrar progresso
            chunks = []
            for chunk in tqdm(pd.read_csv(file_path, sep="|", encoding="utf-8", chunksize=50_000),
                              total=(total_rows // 50_000) + 1,
                              desc="Carregando CSV"):
                chunks.append(chunk)

            self.dataFrame = pd.concat(chunks, ignore_index=True)

            print(f"\033[94mDataFrame carregado com {self.dataFrame.shape[0]} linhas e {self.dataFrame.shape[1]} colunas\033[m")

            # Ajustes no CNPJ
            self.dataFrame['CNPJ'] = self.dataFrame['CNPJ'].astype(str).str.zfill(14)
            self.dataFrame['CNPJ'] = self.dataFrame['CNPJ'].str.replace('.0', '', regex=False)
            self.dataFrame['CNPJ'] = self.dataFrame['CNPJ'].astype(str).str.zfill(14)
            self.dataFrame.loc[self.dataFrame['CNPJ'] == '00000000000nan', 'CNPJ'] = np.nan

            self.__class__._initialized = True

    def get_total_atendimentos_2024(self, df: pd.DataFrame, categoria: str) -> int:
        return int((df['AreaSaude'] == categoria).sum())

    def get_variacao_2023(self, df: pd.DataFrame, categoria: str, total_2024: int) -> int:
        total_2023 = int((df['AreaSaude'] == categoria).sum())
        return round(((total_2024 - total_2023) / total_2023) * 100, 2) if total_2023 != 0 else 0

    def get_atendimentos_genero(self, df: pd.DataFrame, categoria: str) -> int:
        df = df[(df['AreaSaude'] == categoria)]
        total_masculino = int((df['Genero'] == "Masculino").sum())
        total_feminino = int((df['Genero'] == "Feminino").sum())

        total_masculino = round((total_masculino / (total_masculino + total_feminino)) * 100, 2) if (total_masculino + total_feminino) != 0 else 0
        total_feminino = round(100 - total_masculino, 2)

        return total_masculino, total_feminino

    def get_tendencia_atendimentos(self, atendimentos, categoria):
        # Verificação inicial para DataFrame vazio ou sem dados após filtro
        if len(atendimentos) == 0:
            return 0, 0.0

        if categoria:
            atendimentos = atendimentos[atendimentos['AreaSaude'] == categoria]
            atendimentos.reset_index(drop=True, inplace=True)
            # Verificar novamente após o filtro
            if len(atendimentos) == 0:
                return 0, 0.0

        # 1. Processamento inicial do DataFrame
        try:
            novo_df = atendimentos.groupby(['Ano_Atendimento', 'Mes_Atendimento']).size().reset_index(name='Total_Atendimentos')
            novo_df = novo_df.sort_values(['Ano_Atendimento', 'Mes_Atendimento']).reset_index(drop=True)

            # Remover as duas últimas linhas (se necessário)
            if len(novo_df) > 2:
                novo_df = novo_df.iloc[:-2]
        except:
            return 0, 0.0

        # 2. Completar meses faltantes
        try:
            ultimo_ano = novo_df['Ano_Atendimento'].max()
            ultimo_mes = novo_df.loc[novo_df['Ano_Atendimento'] == ultimo_ano, 'Mes_Atendimento'].max()

            anos = novo_df['Ano_Atendimento'].unique()
            todas_combinacoes = []

            for ano in anos:
                meses = range(1, 13) if ano < ultimo_ano else range(1, ultimo_mes + 1)
                todas_combinacoes.extend([{'Ano_Atendimento': ano, 'Mes_Atendimento': mes} for mes in meses])

            df_completo = pd.merge(
                pd.DataFrame(todas_combinacoes),
                novo_df,
                on=['Ano_Atendimento', 'Mes_Atendimento'],
                how='left'
            ).fillna(0)

            df_completo = df_completo.sort_values(['Ano_Atendimento', 'Mes_Atendimento']).reset_index(drop=True)
        except:
            return 0, 0.0

        # 3. Previsão para meses restantes do último ano (COM ROLLING WINDOW = 12)
        try:
            ultimo_ano = df_completo['Ano_Atendimento'].max()
            ultimo_mes = df_completo[df_completo['Ano_Atendimento'] == ultimo_ano]['Mes_Atendimento'].max()

            # CALCULAR MÉDIA MENSAL COM ROLLING WINDOW
            # Primeiro calculamos a média histórica normal
            media_mensal = (
                df_completo[df_completo['Ano_Atendimento'] < ultimo_ano]
                .groupby('Mes_Atendimento')['Total_Atendimentos']
                .mean()
            )

            # Aplicamos rolling average na série temporal completa
            df_rolling = df_completo.copy()
            df_rolling['Data'] = pd.to_datetime(df_rolling['Ano_Atendimento'].astype(str) + '-' +
                                            df_rolling['Mes_Atendimento'].astype(str), format='%Y-%m')
            df_rolling.set_index('Data', inplace=True)
            df_rolling['Total_Atendimentos_rolling'] = df_rolling['Total_Atendimentos'].rolling(window=9, min_periods=1).mean()

            # Pegamos a média rolling para os meses do último ano
            dados_ultimo_ano_rolling = (
                df_rolling[(df_rolling['Ano_Atendimento'] == ultimo_ano) &
                        (df_rolling['Mes_Atendimento'] <= ultimo_mes)]
                .set_index('Mes_Atendimento')['Total_Atendimentos_rolling']
            )

            # Preencher meses faltantes na média mensal com a média global rolling
            media_global_rolling = df_rolling['Total_Atendimentos_rolling'].mean()
            media_mensal = media_mensal.reindex(range(1, 13), fill_value=media_global_rolling)
            media_mensal = media_mensal.replace(0, media_global_rolling)

            # CALCULAR CRESCIMENTO RECENTE USANDO ROLLING
            try:
                crescimento_recente = (dados_ultimo_ano_rolling / media_mensal).mean()
            except:
                crescimento_recente = 1  # Fallback seguro

            # GERAR PREVISÕES (garantindo valores não-negativos)
            meses_restantes = range(ultimo_mes + 1, 13)
            previsoes = [{
                'Ano_Atendimento': ultimo_ano,
                'Mes_Atendimento': mes,
                'Total_Atendimentos': max(0, media_mensal.get(mes, media_global_rolling) * crescimento_recente)
            } for mes in meses_restantes]

            df_previsao = pd.concat([df_completo, pd.DataFrame(previsoes)], ignore_index=True)
        except:
            return 0, 0.0

        # 4. Cálculo das métricas anuais
        try:
            anos_disponiveis = sorted(df_previsao['Ano_Atendimento'].unique(), reverse=True)[:2]

            if len(anos_disponiveis) >= 2:
                ano_anterior, ano_atual = anos_disponiveis[1], anos_disponiveis[0]
            else:
                ano_anterior, ano_atual = None, anos_disponiveis[0]

            atendimentos_ano_anterior = df_previsao[df_previsao['Ano_Atendimento'] == ano_anterior]['Total_Atendimentos'].sum() if ano_anterior else 0
            atendimentos_ano_atual = df_previsao[df_previsao['Ano_Atendimento'] == ano_atual]['Total_Atendimentos'].sum()

            if ano_anterior and atendimentos_ano_anterior > 0:
                variacao_percentual = ((atendimentos_ano_atual - atendimentos_ano_anterior) / atendimentos_ano_anterior) * 100
            else:
                variacao_percentual = 0.0

            return int(round(atendimentos_ano_atual)), float(round(variacao_percentual, 2))
        except:
            return 0, 0.0

    def painel_atendimentos(self, filters: list) -> dict:

        cache_service = CacheService()

        cache_key = "all" if cache_service.generate_key(filters) == "" else cache_service.generate_key(filters)

        if (cached := cache_service.get(cache_key)) is not None:
            return cached

        df = self.dataFrame.copy()
        
        # Aplica filtros uma única vez (otimização crítica)
        mask = True
        
        genero = None
        faixa_etaria = None
        modal = None
        regiao = None
        estado = None
        municipio = None
        conselho = None
        cnpj = None
        nome_empresa = None
        unidade = None
        ano = None

        for filter in filters:
            if filter.get('Genero') != None:
                genero = filter.get('Genero')
            if filter.get('FaixaEtaria') != None:
                faixa_etaria = filter.get('FaixaEtaria')
            if filter.get('Modal') != None:
                modal = filter.get('Modal')
            if filter.get('Região') != None:
                regiao = filter.get('Região')
            if filter.get('UF') != None:
                estado = filter.get('UF')
            if filter.get('Municipio') != None:
                municipio = filter.get('Municipio')
            if filter.get('ConselhoRegional') != None:
                conselho = filter.get('ConselhoRegional')
            if filter.get('CNPJ') != None:
                cnpj = filter.get('CNPJ')
            if filter.get('NomeEmpresa') != None:
                nome_empresa = filter.get('NomeEmpresa')
            if filter.get('UnidadeAtendimento') != None:
                unidade = filter.get('UnidadeAtendimento')
            if filter.get('Ano') != None:
                ano = int(filter.get('Ano'))

        if genero:
            mask &= (df['Genero'] == genero)
        if faixa_etaria:
            mask &= (df['Faixa_Etaria'] == faixa_etaria)
        if modal:
            mask &= (df['Modal'] == modal)
        if regiao:
            mask &= (df['Região'] == regiao)
        if estado:
            mask &= (df['UF'] == estado)
        if municipio:
            mask &= (df['Nome_Município'] == municipio)
        if conselho:
            mask &= (df['Conselho_Regional'] == conselho)
        if cnpj:
            mask &= (df['CNPJ'] == cnpj)
        if nome_empresa:
            mask &= (df['Nome_Empresa'] == nome_empresa)
        if unidade:
            mask &= (df['Unidade_Atendimento'] == unidade)
        if ano:
            mask &= (df['Ano_Atendimento'] == ano)

        # Aplica todos os filtros de uma vez
        df_filtrado = df[mask] if any([genero, faixa_etaria, modal, regiao, estado,
                                        municipio, conselho, cnpj, nome_empresa, unidade]) else df

        # Filtrando conjuntos de dados por ano
        df_filtrado_2025 = df_filtrado[df_filtrado['Ano_Atendimento'] == 2025]
        df_filtrado_2024 = df_filtrado[df_filtrado['Ano_Atendimento'] == 2024]
        df_filtrado_2023 = df_filtrado[df_filtrado['Ano_Atendimento'] == 2023]

        # Adicionando filtro do ano
        if ano:
            if ano == 2023:
                df_filtrado_ano = df_filtrado_2023
            elif ano == 2024:
                df_filtrado_ano = df_filtrado_2024
            elif ano == 2025:
                df_filtrado_ano = df_filtrado_2025

            numero_atendimentos = df_filtrado_ano.shape[0]
            clientes_atendidos = df_filtrado_ano["IdCliente"].nunique()
            prontuarios_preenchidos = float(round(df_filtrado_ano['IdHistoricoSaude'].isna().sum() / df_filtrado_ano.shape[0] * 100,2)) if df_filtrado_ano.shape[0] != 0 else 0
            clientes_monitorados = df_filtrado_ano[df_filtrado_ano['Monitorado'] == True]['IdCliente'].nunique()
        else:
            numero_atendimentos = df_filtrado.shape[0]
            clientes_atendidos = df_filtrado["IdCliente"].nunique()
            prontuarios_preenchidos = float(round(df_filtrado['IdHistoricoSaude'].isna().sum() / df_filtrado.shape[0] * 100,2)) if df_filtrado.shape[0] != 0 else 0
            clientes_monitorados = df_filtrado[df_filtrado['Monitorado'] == True]['IdCliente'].nunique()

        # PAINEL SUPERIOR
        referencia_atendimento = round(numero_atendimentos/clientes_atendidos, 2) if clientes_atendidos != 0 else 0
        atendimentos_esperados_2025, tendencia_atendimentos_2025 = self.get_tendencia_atendimentos(df_filtrado, None) # A tendencia é calculada considerando todos os anos e nao apenas o ano selecionado no filtro
        
        # PAINEL INFERIOR
        # total_atendimentos_2024

        odontologia_total_atendimentos_2024 = self.get_total_atendimentos_2024(df_filtrado_2024, "Odontologia")
        fisioterapia_total_atendimentos_2024 = self.get_total_atendimentos_2024(df_filtrado_2024, "Fisioterapia")
        psicologia_total_atendimentos_2024 = self.get_total_atendimentos_2024(df_filtrado_2024, "Psicologia")
        nutricao_total_atendimentos_2024 = self.get_total_atendimentos_2024(df_filtrado_2024, "Nutrição")
        radiologia_total_atendimentos_2024 = self.get_total_atendimentos_2024(df_filtrado_2024, "Radiologia")
        educacao_fisica_total_atendimentos_2024 = self.get_total_atendimentos_2024(df_filtrado_2024, "Educação Física")

        # variacao_2023
        odontologia_variacao_2023 = self.get_variacao_2023(df_filtrado_2023, "Odontologia", odontologia_total_atendimentos_2024)
        fisioterapia_variacao_2023 = self.get_variacao_2023(df_filtrado_2023, "Fisioterapia", fisioterapia_total_atendimentos_2024)
        psicologia_variacao_2023 = self.get_variacao_2023(df_filtrado_2023, "Psicologia", psicologia_total_atendimentos_2024)
        nutricao_variacao_2023 = self.get_variacao_2023(df_filtrado_2023, "Nutrição", nutricao_total_atendimentos_2024)
        radiologia_variacao_2023 = self.get_variacao_2023(df_filtrado_2023, "Radiologia", radiologia_total_atendimentos_2024)
        educacao_fisica_variacao_2023 = self.get_variacao_2023(df_filtrado_2023, "Educação Física", educacao_fisica_total_atendimentos_2024)

        # tendencia_2025
        odontologia_atendimentos_esperados_2025, odontologia_tendencia_2025 = self.get_tendencia_atendimentos(df_filtrado, "Odontologia")
        fisioterapia_atendimentos_esperados_2025, fisioterapia_tendencia_2025 = self.get_tendencia_atendimentos(df_filtrado, "Fisioterapia")
        psicologia_atendimentos_esperados_2025, psicologia_tendencia_2025 = self.get_tendencia_atendimentos(df_filtrado, "Psicologia")
        nutricao_atendimentos_esperados_2025, nutricao_tendencia_2025 = self.get_tendencia_atendimentos(df_filtrado, "Nutrição")
        radiologia_atendimentos_esperados_2025, radiologia_tendencia_2025 = self.get_tendencia_atendimentos(df_filtrado, "Radiologia")
        educacao_fisica_atendimentos_esperados_2025, educacao_fisica_tendencia_2025 = self.get_tendencia_atendimentos(df_filtrado, "Educação Física")

        # porcentagem_atendimentos_masculino e porcentagem_atendimentos_feminino
        odontologia_atendimentos_masculino, odontologia_atendimentos_feminino = self.get_atendimentos_genero(df_filtrado, "Odontologia")
        fisioterapia_atendimentos_masculino, fisioterapia_atendimentos_feminino = self.get_atendimentos_genero(df_filtrado, "Fisioterapia")
        psicologia_atendimentos_masculino, psicologia_atendimentos_feminino = self.get_atendimentos_genero(df_filtrado, "Psicologia")
        nutricao_atendimentos_masculino, nutricao_atendimentos_feminino = self.get_atendimentos_genero(df_filtrado, "Nutrição")
        radiologia_atendimentos_masculino, radiologia_atendimentos_feminino = self.get_atendimentos_genero(df_filtrado, "Radiologia")
        educacao_fisica_atendimentos_masculino, educacao_fisica_atendimentos_feminino = self.get_atendimentos_genero(df_filtrado, "Educação Física")

        # Montando a response
        response = {
            "numero_atendimentos": numero_atendimentos,
            "clientes_atendidos": clientes_atendidos,
            "referencia_atendimento": referencia_atendimento,
            "prontuarios_preenchidos": prontuarios_preenchidos,
            "clientes_monitorados": clientes_monitorados,
            "atendimentos_esperados_2025": atendimentos_esperados_2025,
            "tendencia_atendimentos": tendencia_atendimentos_2025,
            "categorias": {
            "odontologia": {
                "total_atendimentos_2024": odontologia_total_atendimentos_2024,
                "variacao_2023": odontologia_variacao_2023,
                "atendimentos_esperados_2025": odontologia_atendimentos_esperados_2025,
                "tendencia_2025": odontologia_tendencia_2025,
                "porcentagem_atendimentos_masculino": odontologia_atendimentos_masculino,
                "porcentagem_atendimentos_feminino": odontologia_atendimentos_feminino
            },
            "fisioterapia": {
                "total_atendimentos_2024": fisioterapia_total_atendimentos_2024,
                "variacao_2023": fisioterapia_variacao_2023,
                "atendimentos_esperados_2025": fisioterapia_atendimentos_esperados_2025,
                "tendencia_2025": fisioterapia_tendencia_2025,
                "porcentagem_atendimentos_masculino": fisioterapia_atendimentos_masculino,
                "porcentagem_atendimentos_feminino": fisioterapia_atendimentos_feminino
            },
            "psicologia": {
                "total_atendimentos_2024": psicologia_total_atendimentos_2024,
                "variacao_2023": psicologia_variacao_2023,
                "atendimentos_esperados_2025": psicologia_atendimentos_esperados_2025,
                "tendencia_2025": psicologia_tendencia_2025,
                "porcentagem_atendimentos_masculino": psicologia_atendimentos_masculino,
                "porcentagem_atendimentos_feminino": psicologia_atendimentos_feminino
            },
            "nutricao": {
                "total_atendimentos_2024": nutricao_total_atendimentos_2024,
                "variacao_2023": nutricao_variacao_2023,
                "atendimentos_esperados_2025": nutricao_atendimentos_esperados_2025,
                "tendencia_2025": nutricao_tendencia_2025,
                "porcentagem_atendimentos_masculino": nutricao_atendimentos_masculino,
                "porcentagem_atendimentos_feminino": nutricao_atendimentos_feminino
            },
            "radiologia": {
                "total_atendimentos_2024": radiologia_total_atendimentos_2024,
                "variacao_2023": radiologia_variacao_2023,
                "atendimentos_esperados_2025": radiologia_atendimentos_esperados_2025,
                "tendencia_2025": radiologia_tendencia_2025,
                "porcentagem_atendimentos_masculino": radiologia_atendimentos_masculino,
                "porcentagem_atendimentos_feminino": radiologia_atendimentos_feminino
            },
            "educacao_fisica": {
                "total_atendimentos_2024": educacao_fisica_total_atendimentos_2024,
                "variacao_2023": educacao_fisica_variacao_2023,
                "atendimentos_esperados_2025": educacao_fisica_atendimentos_esperados_2025,
                "tendencia_2025": educacao_fisica_tendencia_2025,
                "porcentagem_atendimentos_masculino": educacao_fisica_atendimentos_masculino,
                "porcentagem_atendimentos_feminino": educacao_fisica_atendimentos_feminino
            }
            }
        }

        cache_service.set(cache_key, response)

        return response
