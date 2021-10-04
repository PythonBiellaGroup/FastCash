from fastapi.testclient import TestClient
from live.main import app
import pytest

client = TestClient(app)


@pytest.mark.api
def test_product_getall():
    response = client.get("/api/v1/products")
    assert response.status_code == 200
    assert len(response.json()) == 2


# def test_product_getone():
#     response = client.get("/products/1")
#     assert response.status_code == 200
#     assert response.json().get("name") == "kebab"


# def test_product_insert():
#     new_product = {
#         "id": 3,
#         "name": "hotdog",
#         "description": "ketchup",
#         "price": 1,
#         "available": True,
#     }
#     response = client.post("/products/", json=new_product)
#     assert response.status_code == 200
#     assert response.json() == new_product


# def test_product_delete():
#     product_id = 1
#     response = client.delete(f"/products/{product_id}")
#     assert response.status_code == 200


# def test_product_update():
#     product_id = 1
#     modify_product = {
#         "id": product_id,
#         "name": "kebab",
#         "description": "con piccante",
#         "price": 3.00,
#         "available": True,
#     }
#     response = client.put(f"/products/{product_id}", json=modify_product)
#     assert response.status_code == 200
