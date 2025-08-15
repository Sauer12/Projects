# Knižničná konzolová aplikácia (CLI)
Jednoduchá konzolová aplikácia pre správu malej knižnice. Umožňuje pridávať knihy, vyhľadávať, prezerať ich zoznam, označiť požičanie/vrátenie a uložiť stav do JSON súboru.
## Funkcionalita
- Pridanie novej knihy (s kontrolou duplicity podľa názvu, autora a roku vydania)
- Výpis všetkých kníh v knižnici
- Vyhľadávanie podľa názvu alebo autora (bez ohľadu na veľkosť písmen, čiastočná zhoda)
- Označenie knihy ako požičanej alebo vrátenej
- Uloženie/načítanie zoznamu kníh do/z JSON súboru
- Automatické nahratie ukážkových dát pri prvom spustení (ak neexistuje súbor s knihami)

## Požiadavky
- Python 3.13+
- Prostredie: odporúčaný virtuálny environment (virtualenv alebo venv)
- Externé balíčky: žiadne

## Inštalácia
1. Naklonuj repozitár:
    - git clone <url_tvojho_repa>
    - cd <adresár_repa>

2. Vytvor a aktivuj virtuálne prostredie:
    - Windows:
        - python -m venv .venv
        - .venv\Scripts\activate

    - macOS/Linux:
        - python3 -m venv .venv
        - source .venv/bin/activate

3. (Voliteľné) Over verziu Pythonu:
    - python --version

Nie sú potrebné žiadne ďalšie balíčky.
## Spustenie
- python main.py

Pri prvom spustení sa načítajú ukážkové knihy. Po uložení sa dáta používajú zo súboru books.json v koreňovom adresári projektu.
## Použitie (menu)
V aplikácii sa zobrazí menu s týmito voľbami:
1. Pridať novú knihu
2. Vypísať všetky knihy
3. Vyhľadať knihu podľa názvu alebo autora
4. Označiť knihu ako požičanú alebo vrátenú
5. Uložiť zoznam kníh do JSON súboru Q. Koniec (s voľbou uloženia zmien)

Poznámky:
- Pri pridávaní sa vyžaduje názov, autor a rok (rok musí byť číslo).
- Vyhľadávanie je „fulltext“ v rámci názvu a autora (bez ohľadu na veľkosť písmen).
- Pri označovaní požičania/vrátenia najprv vyberieš knihu zo zoznamu nájdených výsledkov.

## Formát uloženia (books.json)
Dáta sa ukladajú do JSON súboru v tvare:
- title: názov knihy (string)
- author: autor (string)
- year: rok vydania (number)
- is_available: dostupnosť (boolean)

Príklad jednej položky:
``` json
{
  "title": "1984",
  "author": "George Orwell",
  "year": 1949,
  "is_available": true
}
```
## Seed (ukážkové dáta)
Ak súbor books.json neexistuje, aplikácia automaticky naplní knižnicu ukážkovými titulmi (klasická beletria). Dostupnosť je pre každý titul náhodne nastavená.
## Typické scenáre
- Rýchla evidencia domácej knižnice
- Testovanie práce so súbormi JSON a jednoduchou persistenciou
- Ukážka práce s CLI menu a validáciou vstupov

## Roadmap / možné vylepšenia
- Trvalé logovanie operácií (audit)
- Pokročilé filtrovanie (rokové rozpätie, presná zhoda, triedenie)
- Export do CSV
- Jednotkové testy
- Lokalizácia textov (i18n)


## Kontakt
- GitHub: Sauer12
- E-mail: lsauerwork@gmail.com

Ak máš nápady na vylepšenia alebo našiel/-la si bug, otvor prosím issue alebo pošli PR.
