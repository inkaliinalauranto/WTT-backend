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

## Rajapinnan käyttö
Suurinta osaa rajapintametodeista voi käyttää ainoastaan sisäänkirjautuneena käyttäjänä. Eri roolin käyttäjiä voi luoda ainoastaan admin-käyttäjä. Admin-käyttäjän voit luoda tekemällä FastAPI-dokumentaation kautta pyynnön /api/auth/register/admin-POST-routeen. Sen jälkeen voit kirjautua sisään /api/auth/login-POST-routen kautta. Kirjoita request bodyn käyttäjänimeksi "admin" ja salasanaksi .env-tiedostossa ADMIN_PW-attribuutille antamasi arvo. Tämän jälkeen käyttäjien luonti sekä sen myötä myös muiden API-pyyntöjen toteuttaminen onnistuvat.

## Testit
- Muuta .env-tiedoston TEST-ympäristömuuttuja arvoon "on": `TEST=on`. Tallenna muutokset.
- Nyt testit voidaan ajaa paikallisesti syöttämällä terminaaliin seuraava komentoketju:
```
pytest tests.py --doctest-modules --junitxml=junit/test-results.xml --cov=. --cov-report=xml --cov-report=html
```
- Tämän jälkeen projektikansion juureen ilmestyy htmlcov-kansio, jonka sisällä olevaa index.html-tiedostoa klikkaamalla pääsee tarkastelemaan testiraportteja.
- Jos tämän jälkeen buildaat backendin Dockerissa uudestaan tai jatkat backendin käyttöä paikallisesti Uvicornilla, **muista vaihtaa TEST-ympäristömuuttujan arvo takaisin tai poistaa tämä ympäristömuuttuja kokonaan**.

## Rahti

Backend on buildattu myös Rahti-palveluun, ja rajapintadokumentaatio löytyy osoitteesta **https://wtt-backend-stacked-wtt.2.rahtiapp.fi/docs**.
