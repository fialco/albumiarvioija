# Albmiarvioija
## TKT20019 - Tietokannat ja web-ohjelmointi projekti
* Käyttäjä voi kirjautua sisään ja ulos sekä luoda uuden tunnuksen.
* Käyttäjä näkee etusivulla viimeisimpiä annettuja arvosteluja albumeille ja arvion lähetysajan.
* Käyttäjä voi etsiä artistia tai albumia hakupalkilla ja selata niitä listoittain.
* Artisteilla on omat sivunsa josta löytyy lista albumeista ja yleistä infoa (kotimaa, perustusvuosi/aktiivisena, genre yms).
* Albumeilla on omat sivunsa jossa lista kaikista arvosteluista, arvioiden keskiarvo ja yleistä infoa.
* Käyttäjä voi lisätä, muokata ja poistaa omia arvioitaan albumista.
* Luotettu käyttäjä voi lisätä sekä muokata artistien ja albumien tietoja. 
* Ylläpitäjä voi lisätä sekä muokata artistien ja albumien tietoja
* Ylläpitäjä voi poistaa käyttäjien arvosteluja.
## Tulossa
* Ohjelman ulkoasun parannus
* Mahdollisien bugien liiskaus ja koodin siivous
## Kuinka käyttää ohjelmaa
Kloonaa repositorio koneellesi ja siirry juurikansioon. Luo kansioon .env-tiedosto ja määritä sisältö seuraavanlaiseksi:
```
DATABASE_URL=<tietokannan-paikallinen-osoite> (esim DATABASE_URL=postgresql:///user)
SECRET_KEY=<salainen-avain>
```
Aktivoi virtuaaliympäristö ja asenna sovelluksen riippuvuudet komennoilla
```
python3 -m venv venv
source venv/bin/activate
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
