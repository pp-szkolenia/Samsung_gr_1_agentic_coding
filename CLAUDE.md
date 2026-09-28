# Nazwa projektu: Slides Generator

Narzędzie webowe do tworzenia i przeglądania prezentacji, infografik oraz cheatsheetów.
Działa jako aplikacja w przeglądarce — uruchomienie przez `python3 server.py`.

## Git
Rób commita po każdej większej zmianie.

## Uruchamianie

```bash
python3 server.py          # domyślnie port 8080
python3 server.py 3000     # inny port
```

Przy pierwszym uruchomieniu serwer automatycznie importuje przykłady z `examples/` do `documents/`.

## Architektura

```
slidesGenerator/
├── server.py              # Minimalny serwer HTTP Python (bez zależności zewnętrznych)
├── static/
│   ├── index.html         # Główna aplikacja SPA (lista dokumentów, edytor)
│   └── viewer/
│       ├── presentation.html  # Przeglądarka prezentacji (slajdy, klawiatura)
│       ├── infographic.html   # Przeglądarka infografik (Chart.js)
│       └── cheatsheet.html    # Przeglądarka cheatsheetów (wyszukiwanie)
├── documents/             # Dokumenty użytkownika (pliki JSON)
└── examples/              # Przykładowe dokumenty (po jednym z każdego typu)
    ├── presentation/data.json
    ├── infographic/data.json
    └── cheatsheet/data.json
```

## Warstwa danych — JSON

Każdy dokument jest przechowywany jako plik `.json` w folderze `documents/`.
Serwer udostępnia REST API do zarządzania dokumentami.

### API

| Metoda | Endpoint                  | Opis                        |
|--------|---------------------------|-----------------------------|
| GET    | `/api/documents`          | Lista wszystkich dokumentów |
| GET    | `/api/documents/{id}`     | Pobierz dokument            |
| POST   | `/api/documents`          | Utwórz dokument             |
| PUT    | `/api/documents/{id}`     | Zaktualizuj dokument        |
| DELETE | `/api/documents/{id}`     | Usuń dokument               |

### Schemat JSON — Prezentacja

```json
{
  "type": "presentation",
  "title": "Tytuł",
  "author": "Autor",
  "theme": "dark",
  "slides": [
    { "type": "title",      "title": "...", "subtitle": "..." },
    { "type": "content",    "title": "...", "content": "...", "bullets": ["punkt 1"] },
    { "type": "code",       "title": "...", "language": "python", "code": "..." },
    { "type": "two-column", "title": "...", "left": "...", "right": "..." }
  ]
}
```

### Schemat JSON — Infografika

```json
{
  "type": "infographic",
  "title": "Tytuł",
  "subtitle": "Podtytuł",
  "accent": "#3776ab",
  "stats": [
    { "icon": "📊", "value": "42%", "label": "Opis metryki" }
  ],
  "chart": {
    "type": "bar",
    "title": "Tytuł wykresu",
    "data": [{ "label": "Element", "value": 42, "color": "#3776ab" }]
  },
  "sections": [
    { "title": "Sekcja", "items": ["punkt 1", "punkt 2"] }
  ]
}
```

### Schemat JSON — Cheatsheet

```json
{
  "type": "cheatsheet",
  "title": "Tytuł",
  "subtitle": "Podtytuł",
  "categories": [
    {
      "id": "cat-id",
      "name": "Nazwa kategorii",
      "icon": "📦",
      "commands": [
        { "cmd": "komenda", "desc": "Opis", "example": "przykład", "tip": "wskazówka" }
      ]
    }
  ]
}
```

## Opis typów dokumentów

1. **Prezentacja** — zestaw slajdów w pliku .html z nawigacją strzałkami.
   Typy slajdów: tytułowy, treść z punktami, kod, dwie kolumny.

2. **Infografika** — plik HTML z kafelkami statystyk, wykresem (bar/pie/donut) i sekcjami tekstowymi.

3. **Cheatsheet** — przeglądalna lista komend/pojęć z kategoriami, wyszukiwarką i przyciskiem kopiuj.

## Forma projektu

Aplikacja webowa uruchamiana w przeglądarce. Minimalny serwer w Pythonie (stdlib only, brak pip).
Frontend: vanilla JS + HTML/CSS, Chart.js z CDN (tylko w widoku infografiki).


## OpenSpec

Kiedy implementujesz jakiś większy feature albo inne zmiany w kodzie automatycznie (bez pytania o zgodę) twórz najpierw specyfikację. Potem pytaj o akceptację i po zaimplemnetowaniu automatycznie archiwizuj zmiany bez kolejnego pytania mnie o to
