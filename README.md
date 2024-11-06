## Projektin lataaminen ja konfigurointi Windows-käyttöjärjestelmällä
1. Kloonaa repositorio:
```
git clone https://github.com/inkaliinalauranto/WTT-backend.git
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
6. Käynnistä sovellus:
```
uvicorn main:app --reload
```

build docker:
docker compose up --build

luo tietokanta Phpmyadminissa pohjana db.sql

syötä test tauluun uusi rivi

mene osoitteeseen localhost:8080/test tai localhost:8080/docs

tee testi kysely tietokantaan!