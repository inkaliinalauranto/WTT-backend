import pytest
from app.custom_exceptions.notfound import NotFoundException
from app.custom_exceptions.taken import TakenException
from app.db import session, engine
from app.models import Base
from app.services.sqlalchemy.organizations_sqlalchemy import OrganizationsServiceSqlAlchemy

# Luodaan tietokantataulut testejä varten. Vaikutteita tähän on otettu
# seuraavasta lähteestä:
# https://coderpad.io/blog/development/a-guide-to-database-unit-testing-with-pytest-and-sqlalchemy/
Base.metadata.create_all(engine)


# Luodaan testeille tarvittavat kontekstit pytestin
# fixture-riippuvuus-injektion avulla seuraavaa lähdettä mukaillen:
# https://pytest-with-eric.com/database-testing/pytest-sql-database-testing/#Testing-Database-Operations
@pytest.fixture
def organization_instance(scope="session"):
    # Luodaan db-instanssi kutsumalla db-tiedostossa määriteltyä sessionia,
    # koska OrganizationsServin käyttö aiheutti virheen. Virheen yhteydessä
    # on konsultoitu ChatGPT:n ilmaisversiota, joka ehdotti sessionin käyttöä
    # manuaalisesti, koska testiympäristö ei pysty ratkaisemaan
    # OrganizationsServiceen liittyvää annotoitua luonnetta/riippuvuuksia.
    db_session = session()
    organization_serv = OrganizationsServiceSqlAlchemy(db_session)

    yield organization_serv

    db_session.close()


# Kun testit tehdään tämän funktion yieldaamaa instanssia hyödyntämällä,
# organisaatiotaulun tietueet siivotaan/tyhjennetään sekä ennen testin ajoa
# että sen jälkeen seuraavaa lähdettä mukaillen:
# https://pytest-with-eric.com/database-testing/pytest-sql-database-testing/#Testing-Database-Operations
@pytest.fixture
def emptied_organization_instance(organization_instance, scope="session"):
    organization_instance.delete_all()
    yield organization_instance
    organization_instance.delete_all()


# Tehdään testi, joka testaa onnistunutta tietueen luomista ja luodun
# tietueen hakemista kuvaavaa skenaariota seuraavaa lähdettä mukaillen:
# https://pytest-with-eric.com/database-testing/pytest-sql-database-testing/#Testing-Database-Operations
def test_create_and_read_org(emptied_organization_instance):
    emptied_organization_instance.create_org_if_not_exist("Test organization")
    organization = emptied_organization_instance.get_by_id(1)
    assert organization.id == 1
    assert organization.name == "Test organization"


# Tehdään seuraavaa lähdettä mukaillen testi, jonka tarkoitus on testata
# tietueen luomisen epäonnistumista, eli luodaan kaksi kertaa organisaatio
# samalla nimellä:
# https://medium.com/@ramanish1992/pytest-assertions-and-test-discovery-python-24b4bcb468eb
def test_create_same_username(emptied_organization_instance):
    emptied_organization_instance.create_org_if_not_exist("Test organization")
    with pytest.raises(TakenException) as exc_info:
        emptied_organization_instance.create_org_if_not_exist("Test organization")
    assert str(exc_info.value) == "Organization already exists"


# Tehdään seuraavaa lähdettä mukaillen testi, jonka tarkoitus on testata
# tietueen hakemisen epäonnistumista, eli haetaan luotu tietue sellaisella
# id:llä, jollaista tietueella ei pitäisi olla:
# https://medium.com/@ramanish1992/pytest-assertions-and-test-discovery-python-24b4bcb468eb
def test_read_org_with_0_id(emptied_organization_instance):
    emptied_organization_instance.create_org_if_not_exist("Test organization")
    with pytest.raises(NotFoundException) as exc_info:
        emptied_organization_instance.get_by_id(0)
    assert str(exc_info.value) == "Organization not found"
