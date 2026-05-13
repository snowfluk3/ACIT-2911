import importlib
import sys
from pathlib import Path

import pytest


PROJECT_ROOT = Path(__file__).resolve().parents[1]


def reset_app_modules():
    for module_name in list(sys.modules):
        if module_name == "app" or module_name.startswith("app."):
            sys.modules.pop(module_name, None)


@pytest.fixture()
def client(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    monkeypatch.syspath_prepend(str(PROJECT_ROOT))
    (tmp_path / "database").mkdir()

    reset_app_modules()

    flask_app = importlib.import_module("app").create_app()
    db = importlib.import_module("app.extensions.extensions").db
    importlib.import_module("app.models.model").init_db()
    flask_app.config.update(TESTING=True)

    with flask_app.test_client() as test_client:
        yield test_client

    if not db.is_closed():
        db.close()


def create_ingredient(client, **overrides):
    payload = {
        "name": "Milk",
        "quantity": 2,
        "unit": "L",
        "category": "Dairy",
        "expiry_date": None,
        "notes": "Opened carton",
    }
    payload.update(overrides)

    response = client.post("/ingredients", json=payload)
    assert response.status_code == 201
    return response.get_json()

def register_and_login(client):
    client.post("/register", data={
        "username": "Fossil",
        "email": "test_user@example.com",
        "password": "password"
    })

def test_create_ingredient(client):
    register_and_login(client)
    ingredient = create_ingredient(client)

    assert ingredient["name"] == "Milk"
    assert ingredient["quantity"] == 2
    assert ingredient["unit"] == "L"
    assert ingredient["category"] == "Dairy"
    assert ingredient["notes"] == "Opened carton"



def test_get_ingredient(client):
    register_and_login(client)
    created = create_ingredient(client, name="Eggs", quantity=12, unit="pcs", category="Protein")

    response = client.get(f"/ingredients/{created['id']}")

    assert response.status_code == 200
    assert response.get_json()["name"] == "Eggs"


def test_update_ingredient(client):
    register_and_login(client)
    created = create_ingredient(client, name="Rice", quantity=5, unit="kg", category="Grain")

    response = client.put(
        f"/ingredients/{created['id']}",
        json={"quantity": 4.5, "notes": "Stored in pantry"},
    )

    assert response.status_code == 200
    ingredient = response.get_json()
    assert ingredient["quantity"] == 4.5
    assert ingredient["notes"] == "Stored in pantry"


def test_delete_ingredient(client):
    register_and_login(client)
    created = create_ingredient(client, name="Bread", quantity=1, unit="loaf", category="Bakery")

    delete_response = client.delete(f"/ingredients/{created['id']}")
    get_response = client.get(f"/ingredients/{created['id']}")

    assert delete_response.status_code == 204
    assert get_response.status_code == 404
    assert get_response.get_json() == {"error": f"Ingredient {created['id']} not found"}
