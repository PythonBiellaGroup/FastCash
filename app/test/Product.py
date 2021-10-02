from fastapi.testclient import TestClient
from .main import api

client = TestClient(api)


def test_index():
    response = client.get("/")
    assert response.status_code == 200


def test_default():
    response = client.get("/default")
    assert response.status_code == 200
    assert response.json() == {"messaggio": "PythonBiellaGroup!"}


def test_test_noparameter():
    x = 20
    response = client.get(f"/api/test/{x}")
    assert response.status_code == 400
    assert response.json() == {"Errore": "Z non è valorizzato"}


def test_test_allparameters():
    x = 20
    y = 50
    z = 10

    response = client.get(f"/api/test/{x}?y={y}&z={z}")

    assert response.status_code == 200

    somma = x + y
    divisione = somma / z

    assert response.json() == {
        "x": x,
        "y": y,
        "z": z,
        "somma": somma,
        "divisione": divisione,
    }
