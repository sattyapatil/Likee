from fastapi.testclient import TestClient

from Application.app import app

client = TestClient(app)


def test_add_person():
    response = client.post(
        "/person/",
        json={
              "name": "Test",
              "first_name": "test_first_name",
              "last_name": "test_last_name"
            },
    )
    assert response.status_code == 200
    assert response.json() == {
      "message": "Test added successfully"
    }


def test_add_person_already_exist():
    """test person is already exit"""
    response = client.post(
        "/person/",
        json={
              "name": "Test",
              "first_name": "test_first_name",
              "last_name": "test_last_name"
            },
    )
    assert response.status_code == 200
    assert response.json() == {
      "message": "Test already exist"
    }


def test_get_peoples():
    response = client.get("/peoples")
    assert response.status_code == 200
    assert response.json() == [
        {
            "name": "Test",
           "first_name": "test_first_name",
            "last_name": "test_last_name",
            "peoples_liked_by_me": [],
            "peoples_who_like_me": [],
            "likes": []
        }
    ]


def test_delete_peoples():
    response = client.delete("/peoples/")
    assert response.status_code == 200
    assert response.json() == {
            "message": "Deleted peoples successfully"
        }
