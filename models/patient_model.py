from beanie import Document
from pydantic import Field
from typing import Optional
from bson import ObjectId


class Patient(Document):
    patient_id: str
    nome: str
    sexo: str
    idade: int
    altura: int
    peso: Optional[float] = None
    imc: float
    estado_civil: Optional[str] = None
    profissao: Optional[str] = None
    cidade: str
    sigop: int
    unidade: str
    faixa_etaria: str
    estado: str
    regiao: str

    percentual_gordura: Optional[float] = None
    mme: Optional[float] = None
    gordura_visceral: Optional[float] = None
    fc_max: Optional[float] = None
    fc_med: Optional[float] = None
    fc_min: Optional[float] = None
    rmssd: Optional[float] = None
    pnni_50: Optional[float] = None
    sdnn: Optional[float] = None

    minutos_diarios_atividades_intensa: Optional[float] = None
    minutos_diarios_atividades_leve: Optional[float] = None
    minutos_diarios_atividades_moderada: Optional[float] = None
    minutos_atividades_diarios_media: Optional[float] = None

    calorias_med: Optional[float] = None
    distancia_med: Optional[float] = None
    passos_med: Optional[float] = None

    sono_leve_pct: Optional[float] = None
    sono_rem_pct: Optional[float] = None
    sono_profundo_pct: Optional[float] = None
    eficiencia_sono: Optional[float] = None
    duracao_sono_minutos: Optional[float] = None
    duracao_sono_horas: Optional[float] = None

    class Settings:
        name = "patients"
