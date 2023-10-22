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
Kloonaa repositorio koneellesi ja siirry juurikansioon. Luo kansioon .env-tiedosto ja määritä sisältö seuraavanlaiseksi:
```
DATABASE_URL=<tietokannan-paikallinen-osoite> (esim DATABASE_URL=postgresql:///user)
SECRET_KEY=<salainen-avain>
```
Aktivoi virtuaaliympäristö ja asenna sovelluksen riippuvuudet komennoilla
```
python3 -m venv venv
source venv/bin/activate (source venv\Scripts\activate Windowsilla)
pip install -r ./requirements.txt
```
Käynnistä postgersql tietokanta ja määritä tietokannan skeema komennolla
```
psql < schema.sql
```
Voit lisätä artisteja ja albumeita joko itse tai ajaa testausta varten (lisääminen saattaa kestää hetken)
```
psql < example.sql
```
Tarvittaessa koko tietokannan voi tyhjentää ja alustaa komennoilla psql:llä
```
DROP SCHEMA public CASCADE;
CREATE SCHEMA public;
```
käynnistä sovellus komennolla
```
flask run
```
