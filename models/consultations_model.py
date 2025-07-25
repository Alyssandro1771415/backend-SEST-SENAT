from pydantic import Field
from typing import Optional
from beanie import Document

class Consultation(Document):
    id_historico_saude: Optional[int] = Field(default=None, alias="IdHistoricoSaude")
    ano: Optional[int] = Field(default=None, alias="Ano_Atendimento")
    genero: Optional[str] = Field(default=None, alias="Genero")
    grau_instrucao: Optional[str] = Field(default=None, alias="GrauInstrucao")
    estado_civil: Optional[str] = Field(default=None, alias="EstadoCivil")
    renda: Optional[float] = Field(default=None, alias="Renda")
    idade: Optional[int] = Field(default=None, alias="Idade")
    classificacao_transporte_ou_comunidade: Optional[str] = Field(default=None, alias="Classificacao_Transporte_ou_Comunidade")
    categoria_dependente_ou_titular: Optional[str] = Field(default=None, alias="Categoria_Dependente_ou_Titular_da_Classificação")
    bairro: Optional[str] = Field(default=None, alias="Bairro")
    cidade: Optional[str] = Field(default=None, alias="Cidade")
    ocupacao: Optional[str] = Field(default=None, alias="Ocupação")
    area_saude: Optional[str] = Field(default=None, alias="AreaSaude")
    status_atendimento: Optional[str] = Field(default=None, alias="Status_Atendimento")
    data_atendimento: Optional[str] = Field(default=None, alias="Data_Atendimento")
    unidade_atendimento: Optional[str] = Field(default=None, alias="Unidade_Atendimento")
    conselho_regional: Optional[str] = Field(default=None, alias="Conselho_Regional")
    cep_unidade: Optional[int] = Field(default=None, alias="CEP_da_Unidade")
    codigo_ibge_unidade_operacional: int = Field(..., alias="CodigoIBGE_UnidadeOperacional")
    cnpj: Optional[str] = Field(default=None, alias="CNPJ")
    modal: Optional[str] = Field(default=None, alias="Modal")
    codigo_municipal_completo: int = Field(..., alias="Código Município Completo")
    nome_municipio: Optional[str] = Field(default=None, alias="Nome_Município")
    nome_empresa: Optional[str] = Field(default=None, alias="Nome_Empresa")
    ano_atendimento: Optional[int] = Field(default=None, alias="Ano_Atendimento")
    mes_atendimento: Optional[int] = Field(default=None, alias="Mes_Atendimento")
    uf: Optional[str] = Field(default=None, alias="UF")
    regiao: Optional[str] = Field(default=None, alias="Região")
    faixa_etaria: Optional[str] = Field(default=None, alias="Faixa_Etaria")
    monitorado: Optional[bool] = Field(default=None, alias="Monitorado")

    class Settings:
        name = "consultations"
