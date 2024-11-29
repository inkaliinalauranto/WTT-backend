from unittest.mock import patch
import pytest

"""Testien luomisessa on hyödynnetty ChatGPT:tä"""


@pytest.fixture(autouse=True)
def mock_env_vars(monkeypatch):
    # Simuloidaan tietokannan muodostavan URL:n ympäristömuuttujia
    # arvoilla, jotka asetetaan setenv-metodikutsun toisiksi parametreiksi:
    monkeypatch.setenv("MYSQL_USER", "testuser")
    monkeypatch.setenv("MYSQL_PASSWORD", "testpassword")
    monkeypatch.setenv("MYSQL_DATABASE", "localhost")
    monkeypatch.setenv("MYSQL_DATABASE_NAME", "testdb")
    yield


@pytest.fixture(autouse=True)
def mock_dotenv_load(monkeypatch):
    with patch("dotenv.load_dotenv") as mock_load_dotenv:
        # Varmistetaan, ettei load_dotenv lataa .env-tiedoston oikeita arvoja:
        mock_load_dotenv.return_value = None
        yield mock_load_dotenv


def test_env_variables():
    from app.db import DB_USER, DB_PASSWORD, DB_HOST, DB_NAME
    # Testataan, että ympäristömuuttujat on asetettu oikein:
    assert DB_USER == "testuser"
    assert DB_PASSWORD == "testpassword"
    assert DB_HOST == "localhost"
    assert DB_NAME == "testdb"


def test_database_url():
    from app.db import DATABASE_URL
    # Testataan, että tietokantayhteyden URL on oikein muodostettu:
    expected_url = "mysql+pymysql://testuser:testpassword@localhost/testdb"
    assert DATABASE_URL == expected_url
