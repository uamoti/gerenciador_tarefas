from fastapi import status
from fastapi.testclient import TestClient

from gerenciador_tarefas.gerenciador import TAREFAS, app


def test_listar_tarefas_retorna_status_200():

    cliente = TestClient(app)
    resposta = cliente.get("/tarefas")
    assert resposta.status_code == status.HTTP_200_OK


def test_listar_tarefas_retorna_json():

    cliente = TestClient(app)
    resposta = cliente.get("/tarefas")
    assert resposta.headers["Content-Type"] == "application/json"


def test_listar_tarefas_retorna_lista():

    cliente = TestClient(app)
    resposta = cliente.get("/tarefas")
    assert isinstance(resposta.json(), list)


def test_tarefa_retornada_deve_possuir_id():

    TAREFAS.append(
        {
            "id_num": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
            "titulo": "tarefa1",
            "descricao": "descricao 1",
            "estado": "finalizado",
        }
    )
    cliente = TestClient(app)
    resposta = cliente.get("/tarefas")
    assert "id_num" in resposta.json().pop()
    TAREFAS.clear()


def test_tarefa_retornada_deve_possuir_titulo():

    TAREFAS.append(
        {
            "id_num": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
            "titulo": "tarefa1",
            "descricao": "descricao 1",
            "estado": "finalizado",
        }
    )
    cliente = TestClient(app)
    resposta = cliente.get("/tarefas")
    assert "titulo" in resposta.json().pop()
    TAREFAS.clear()


def test_tarefa_retornada_deve_possuir_descricao():

    TAREFAS.append(
        {
            "id_num": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
            "titulo": "tarefa1",
            "descricao": "descricao 1",
            "estado": "finalizado",
        }
    )
    cliente = TestClient(app)
    resposta = cliente.get("/tarefas")
    assert "descricao" in resposta.json().pop()
    TAREFAS.clear()


def test_tarefa_retornada_deve_possuir_estado():

    TAREFAS.append(
        {
            "id_num": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
            "titulo": "tarefa1",
            "descricao": "descricao 1",
            "estado": "finalizado",
        }
    )
    cliente = TestClient(app)
    resposta = cliente.get("/tarefas")
    assert "estado" in resposta.json().pop()
    TAREFAS.clear()


def test_tarefas_deve_aceitar_post():

    cliente = TestClient(app)
    resposta = cliente.post("/tarefas")
    assert resposta.status_code != status.HTTP_405_METHOD_NOT_ALLOWED


def test_tarefa_submetida_deve_possuir_titulo():

    cliente = TestClient(app)
    resposta = cliente.post("/tarefas", json={})
    assert resposta.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_titulo_entre_3_e_50_chars():

    cliente = TestClient(app)
    resposta = cliente.post("/tarefas", json={"titulo": "**"})
    assert resposta.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    resposta = cliente.post("/tarefas", json={"titulo": 51 * "*"})
    assert resposta.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_tarefa_deve_possuir_descricao():

    cliente = TestClient(app)
    resposta = cliente.post("/tarefas", json={"titulo": "titulo"})
    assert resposta.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_descricao_possui_max_140_chars():

    cliente = TestClient(app)
    resposta = cliente.post(
        "/tarefas", json={"titulo": "titulo", "descricao": 141 * "*"}
    )
    assert resposta.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_criacao_de_tarefa_deve_retornar_a_mesma():

    cliente = TestClient(app)
    tarefa_esperada = {"titulo": "titulo", "descricao": "descricao"}
    resposta = cliente.post("/tarefas", json=tarefa_esperada)
    tarefa_criada = resposta.json()
    assert tarefa_criada["titulo"] == tarefa_esperada["titulo"]
    assert tarefa_criada["descricao"] == tarefa_esperada["descricao"]
    TAREFAS.clear()


def test_id_da_tarefa_deve_ser_unico():

    cliente = TestClient(app)
    tarefa1 = {"titulo": "titulo1", "descricao": "descricao1"}
    tarefa2 = {"titulo": "titulo2", "descricao": "descricao1"}
    resposta1 = cliente.post("/tarefas", json=tarefa1)
    resposta2 = cliente.post("/tarefas", json=tarefa2)
    assert resposta1.json()["id_num"] != resposta2.json()["id_num"]
    TAREFAS.clear()


def test_estado_padrao_tarefa_nao_finalizado():

    cliente = TestClient(app)
    tarefa = {"titulo": "titulo", "descricao": "descricao"}
    resposta = cliente.post("/tarefas", json=tarefa)
    assert resposta.json()["estado"] == "nao finalizado"
    TAREFAS.clear()


def test_criar_tarefa_retorna_codigo_201():

    cliente = TestClient(app)
    tarefa = {"titulo": "titulo", "descricao": "descricao"}
    resposta = cliente.post("/tarefas", json=tarefa)
    assert resposta.status_code == status.HTTP_201_CREATED
    TAREFAS.clear()


def test_tarefa_criada_deve_ser_salva():

    cliente = TestClient(app)
    tarefa = {"titulo": "titulo", "descricao": "descricao"}
    cliente.post("/tarefas", json=tarefa)
    assert len(TAREFAS) == 1
    TAREFAS.clear()


def test_remover_tarefa_existente():

    TAREFAS.append(
        {
            "id_num": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
            "titulo": "tarefa",
            "descricao": "descricao",
            "estado": "finalizado",
        }
    )
    cliente = TestClient(app)
    resposta = cliente.delete("/tarefas/3fa85f64-5717-4562-b3fc-2c963f66afa6")
    assert resposta.status_code == status.HTTP_204_NO_CONTENT
    TAREFAS.clear()
    
    
def test_remover_tarefa_inexistente():

    TAREFAS.append(
        {
            "id_num": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
            "titulo": "tarefa",
            "descricao": "descricao",
            "estado": "nao finalizado",
        }
    )
    cliente = TestClient(app)
    resposta = cliente.delete("/tarefas/3fa85f64-5717-4562-b3fc-2c963f66af")
    assert resposta.status_code == status.HTTP_404_NOT_FOUND
    TAREFAS.clear()

