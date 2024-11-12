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
pip install -r requirements.txt
```
6. Buildaa docker:
```
docker compose up --build
```
7. FastApi, PhpMyadmin ja db pyörivät nyt localhostissa asettamissasi porteissa

8. Jos haluat luoda taulukot tietokantaan, lisää allaoleva enviin, ja buildaa docker uudestaan.
```
CREATE_DB_TABLES="true"
```
9. Luo tietokantaan roolille tietueet "employee" ja "manager", sekä yksi organisaatio ja yksi team.

