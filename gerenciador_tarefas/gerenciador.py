from enum import Enum
from uuid import UUID, uuid4

from fastapi import FastAPI, status, Response
from pydantic import BaseModel, constr


class EstadosPossiveis(str, Enum):

    finalizado = "finalizado"
    nao_finalizado = "nao finalizado"


class TarefaEntrada(BaseModel):

    titulo: constr(min_length=3, max_length=50)
    descricao: constr(max_length=140)
    estado: EstadosPossiveis = EstadosPossiveis.nao_finalizado


class Tarefa(TarefaEntrada):

    id_num: UUID


TAREFAS = [
    {
        "id_num": "1",
        "titulo": "fazer compras",
        "descricao": "comprar leite e ovos",
        "estado": "nao finalizado",
    },
    {
        "id_num": "2",
        "titulo": "levar o cachorro para tosar",
        "descricao": "está muito peludo",
        "estado": "nao finalizado",
    },
    {
        "id_num": "3",
        "titulo": "lavar roupas",
        "descricao": "estão sujas",
        "estado": "nao finalizado",
    },
]

app = FastAPI()


@app.get("/tarefas")
def listar():

    return TAREFAS


@app.post(
    "/tarefas", response_model=Tarefa, status_code=status.HTTP_201_CREATED
)
def criar(tarefa: TarefaEntrada):

    nova_tarefa = tarefa.dict()
    nova_tarefa.update({"id_num": uuid4()})
    TAREFAS.append(nova_tarefa)

    return nova_tarefa


@app.delete("/tarefas/{id_num}")
def remover(id_num):

    for i in range(len(TAREFAS)):
        if TAREFAS[i]['id_num'] == id_num:
            TAREFAS.pop(i)
            #break
            return Response(status_code=status.HTTP_204_NO_CONTENT)
    else:
        return Response(status_code=status.HTTP_404_NOT_FOUND)



