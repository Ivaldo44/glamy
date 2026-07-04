"""
Modelos leves de dados do Glamy Lite.

Hoje o restante do app trabalha diretamente com tuplas retornadas pelo
sqlite3 (por simplicidade e performance). Estas dataclasses existem para
facilitar uma migração futura, deixando explícito o "formato" de cada
tabela e servindo como referência de campos.
"""

from dataclasses import dataclass
from typing import Optional


@dataclass
class Cliente:
    id: Optional[int]
    nome: str
    telefone: Optional[str] = None
    instagram: Optional[str] = None
    observacoes: Optional[str] = None

    @classmethod
    def from_row(cls, row):
        return cls(id=row[0], nome=row[1], telefone=row[2], instagram=row[3], observacoes=row[4])


@dataclass
class Servico:
    id: Optional[int]
    nome: str
    valor: float
    duracao_minutos: int

    @classmethod
    def from_row(cls, row):
        return cls(id=row[0], nome=row[1], valor=row[2], duracao_minutos=row[3])


@dataclass
class Agendamento:
    id: Optional[int]
    cliente_id: int
    servico_id: int
    data: str
    hora_inicio: str
    hora_fim: str
    valor: float
    status: str = "Agendado"
    observacoes: Optional[str] = None

    @classmethod
    def from_row(cls, row):
        return cls(
            id=row[0],
            cliente_id=row[1],
            servico_id=row[2],
            data=row[3],
            hora_inicio=row[4],
            hora_fim=row[5],
            valor=row[6],
            status=row[7] if len(row) > 7 else "Agendado",
            observacoes=row[8] if len(row) > 8 else None
        )


@dataclass
class Expediente:
    id: Optional[int]
    dia_semana: int
    hora_inicio: Optional[str]
    hora_fim: Optional[str]
    ativo: bool

    @classmethod
    def from_row(cls, row):
        return cls(
            id=row[0],
            dia_semana=row[1],
            hora_inicio=row[2],
            hora_fim=row[3],
            ativo=bool(row[4])
        )
