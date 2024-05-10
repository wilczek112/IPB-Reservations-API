from mockModel import *

def mock_event() -> Root:
    return Root(
        aula=Aula(
            activo=True,
            anoLectPeriodo=0,
            fim="string",
            id=0,
            idPeriodo=0,
            idSala=0,
            inicio="string",
            lastEditId=0,80
            manual=True
        ),
        disciplinas=[
            Disciplina(
                abrevCurso="string",
                abrevDisciplina="string",
                abrevTipoAula="string",
                ano=0,
                anoLect=0,
                codCurso=0,
                codEscola=0,
                id=0,
                idAula=0,
                nDisciplina=0,
                nOpcao=0,
                nPlano=0,
                nome="string",
                nomeCurso="string",
                nomeDisciplina="string",
                nomeTipoAula="string",
                semestre=0,
                turma="string"
            )
        ],
        docentes=[
            Docente(
                email="string",
                firstLast="string",
                login="string",
                nome="string",
                runas=True
            )
        ],
        idAula=0,
        sala=Sala(
            abrev="string",
            abrevEscola="string",
            codEscola=0,
            codSala="string",
            escola="string",
            id=0,
            ip=0,
            nome="string"
        ),
        sumarios=[
            Sumario(
                abrevTipoAula="string",
                bibliografia=[
                    "string"
                ],
                fim="string",
                id=0,
                idAula=0,
                idDetalhesAula=0,
                inicio="string",
                lastEdit=LastEdit(
                    data="string",
                    descricao="string",
                    id=0,
                    idSumario=0,
                    login="string",
                    nomeDocente="string"
                ),
                lastEditId=0,
                nomeTipoAula="string",
                sumario="string"
            )
        ]
    )

# Now you can use the mock data
data = mock_event()

# Extract the fields
aula = data.aula
fim = aula.fim
id = aula.id
idSala = aula.idSala
inicio = aula.inicio

# Now you can process these variables
print(f"fim: {fim}, id: {id}, idSala: {idSala}, inicio: {inicio}")
