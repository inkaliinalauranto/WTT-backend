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


