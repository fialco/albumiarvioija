# Albmiarvioija
## TKT20019 - Tietokannat ja web-ohjelmointi projekti
Ohjelman ideana on sivusto jossa on tietoa artisteista, heidän albumeista ja kyseisten albumien arvostelusta.
* Yleistä
  * Artisteilla on omat sivunsa josta löytyy lista albumeista ja yleistä infoa (kotimaa, perustusvuosi/aktiivisena, genre yms).
  * Albumeilla on omat sivunsa jossa lista kaikista arvosteluista, arvioiden keskiarvo ja yleistä infoa.
  * Voi etsiä artistia tai albumia hakupalkilla ja selata niitä listoittain.
  * Etusivulla näkyy viimeisimpiä annettuja arvosteluja albumeille.
* Käyttäjät
  * Voi kirjautua sisään ja ulos sekä luoda uuden tunnuksen.
  * Voi lisätä ja poistaa oman arvion albumista
  * Luotettu käyttäjä ja ylläpitäjä voi lisätä, poistaa ja muokata artistien ja albumien tietoja.
  * Ylläpitäjä voi poistaa käyttäjien arvosteluja.
## Kuinka käyttää ohjelmaa
Varmista että sinulla on Docker asennettuna! 

Kloonaa repositorio koneellesi ja siirry juurikansioon. Luo kansioon .env-tiedosto ja määritä sisältö.
Käyttäjän nimen, salasanan ja tietokannan nimen voi valita itse. Luo SECRET_KEY esimerkiksi pythonin secrets moduulin token_hex(16):lla.
```
POSTGRES_USER=albumiarvioija
POSTGRES_PASSWORD=albums
POSTGRES_DB=albums-db
DATABASE_URL=postgresql://albumiarvioija:albums@db:5432/albums-db
SECRET_KEY=<salainen-avain>
```
Asenna ohjelma ajamalla:

```
docker compose build
```

Ohjelma käynnistettän ajamalla:
```
docker compose up
```
Ohjelmaa pääsee nyt käyttämään osoitteen http://localhost:5001 kautta.


Voit testausta varten täyttää tietokannan esimerkkidatalla. Psql parametrit
ovat samat mitä .env tiedostoon on määritelty (lisääminen kestää hetken).
```
psql -U albumiarvioija -h localhost -p 5432 -d albums-db < example.sql
```
