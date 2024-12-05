## Projektin lataaminen ja konfigurointi Windows-käyttöjärjestelmällä
1. Kloonaa repositorio:
```
git clone https://github.com/Anttiom1/WTT-backend.git
```
2. Avaa projekti esim. *Visual Studio Codella*:
```
code WTT-backend
```
3. Tee projektin juureen .env-tiedosto ja aseta sinne .env_example.txt-tiedostossa olevan esimerkin mukaiset muuttujat. Tallenna muutokset.
4. Avaa terminaali, navigoi projektin juureen ja luo virtuaaliympäristö:
```
python -m venv venv
```
5. Käynnistä virtuaaliympäristö:
```
venv\Scripts\activate
```
6. Asenna riippuvuudet:
```
python -m pip install -r requirements.txt
```
7. Buildaa docker:
```
docker compose up --build 
```
- Vaihtoehtoisesti käynnistä refreshaava ympäristö
```
docker compose -f compose-dev.yaml up 
```
8. FastApi, PhpMyadmin ja db pyörivät nyt localhostissa asettamissasi porteissa

9. Jos haluat luoda taulukot tietokantaan, lisää alla oleva enviin, ja buildaa docker uudestaan.
```
CREATE_DB_TABLES="true"
```
10. Kun taulut on luotu Dockerin tietokantaan, suorita prepopulate insertit phpmyadminissa (löytyy sql/sql_prepopulate.txt). 
Mikäli käytät paikallista tietokantaa, käytä create_local_database.sql-MySQL-tietokantadumppia, joka sisältää myös tarvittavat insertit.

## Testit
- Vaihda .env-tiedoston TEST-attribuutti arvoon True, ja tallenna muutokset.
- Nyt testit voidaan ajaa paikallisesti syöttämällä terminaaliin seuraava komentoketju:
```
pytest tests.py --doctest-modules --junitxml=junit/test-results.xml --cov=. --cov-report=xml --cov-report=html
```
- Tämän jälkeen projektikansion juureen ilmestyy htmlcov-kansio, jonka sisällä olevaa index.html-tiedostoa klikkaamalla pääsee tarkastelemaan testiraportteja.

## Rahti

Backend on buildattu myös Rahti-palveluun, ja rajapintadokumentaatio löytyy osoitteesta **https://wtt-backend-stacked-wtt.2.rahtiapp.fi/docs**.
