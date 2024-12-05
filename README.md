## Projektin lataaminen ja konfigurointi Windows-käyttöjärjestelmällä
1. Kloonaa repositorio:
```
git clone https://github.com/Anttiom1/WTT-backend.git
```
2. Avaa projekti esim. *Visual Studio Codella*:
```
code WTT-backend
```
3. Avaa terminaali, navigoi projektin juureen ja luo virtuaaliympäristö:
```
python -m venv venv
```
4. Käynnistä virtuaaliympäristö:
```
venv\Scripts\activate
```
5. Asenna riippuvuudet:
```
python -m pip install -r requirements.txt
```
6. Buildaa docker:
```
docker compose up --build 
```
- Vaihtoehtoisesti käynnistä refreshaava ympäristö
```
docker compose -f compose-dev.yaml up 
```
7. FastApi, PhpMyadmin ja db pyörivät nyt localhostissa asettamissasi porteissa

8. Jos haluat luoda taulukot tietokantaan, lisää alla oleva enviin, ja buildaa docker uudestaan.
```
CREATE_DB_TABLES="true"
```
9. Kun taulut on luotu dockerin tietokantaan, suorita prepopulate insertit phpmyadminissa (löytyy sql/sql_prepopulate.txt). 
Mikäli käytät paikallista tietokantaa, käytä create_local_database.sql mysql tietokanta dumppia, joka sisältää myös tarvittavat insertit.

## Testit
- Jos haluat ajaa testit, syötä terminaaliin seuraava komentoketju:
```
pytest tests.py --doctest-modules --junitxml=junit/test-results.xml --cov=. --cov-report=xml --cov-report=html
```
- Tämän jälkeen projektikansion juureen ilmestyy htmlcov-kansio, jonka sisällä olevaa index.html-tiedostoa klikkaamalla pääsee tarkastelemaan testiraportteja. 
