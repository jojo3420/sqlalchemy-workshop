from devtools import debug
from fastapi import Depends
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.main import app
from app import models, database

client = TestClient(app)


def test_conn_db():
    conn = next(database.get_conn())
    users = conn.query(models.User).all()
    assert conn is not None
    assert len(users) >= 0


def test_users():
    response = client.get('/users')
    assert response.status_code == 200
    assert len(response.json()) >= 0


