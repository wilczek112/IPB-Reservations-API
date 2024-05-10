from typing import List
from pydantic import BaseModel

class Aula(BaseModel):
    activo: bool
    anoLectPeriodo: int
    fim: str
    id: int
    idPeriodo: int
    idSala: int
    inicio: str
    lastEditId: int
    manual: bool

class Disciplina(BaseModel):
    abrevCurso: str
    abrevDisciplina: str
    abrevTipoAula: str
    ano: int
    anoLect: int
    codCurso: int
    codEscola: int
    id: int
    idAula: int
    nDisciplina: int
    nOpcao: int
    nPlano: int
    nome: str
    nomeCurso: str
    nomeDisciplina: str
    nomeTipoAula: str
    semestre: int
    turma: str

class Docente(BaseModel):
    email: str
    firstLast: str
    login: str
    nome: str
    runas: bool

class Sala(BaseModel):
    abrev: str
    abrevEscola: str
    codEscola: int
    codSala: str
    escola: str
    id: int
    ip: int
    nome: str

class LastEdit(BaseModel):
    data: str
    descricao: str
    id: int
    idSumario: int
    login: str
    nomeDocente: str

class Sumario(BaseModel):
    abrevTipoAula: str
    bibliografia: List[str]
    fim: str
    id: int
    idAula: int
    idDetalhesAula: int
    inicio: str
    lastEdit: LastEdit
    lastEditId: int
    nomeTipoAula: str
    sumario: str

class Root(BaseModel):
    aula: Aula
    disciplinas: List[Disciplina]
    docentes: List[Docente]
    idAula: int
    sala: Sala
    sumarios: List[Sumario]