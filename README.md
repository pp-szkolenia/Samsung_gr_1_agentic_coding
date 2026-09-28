# Slides Generator

Narzędzie webowe do tworzenia i przeglądania **prezentacji**, **infografik** i **cheatsheetów**.

## Uruchomienie

```bash
python3 server.py
```

Otwórz przeglądarkę: **http://localhost:8080**

> Opcjonalnie: `python3 server.py 3000` — inny port

Przy pierwszym uruchomieniu serwer automatycznie wczyta trzy przykładowe dokumenty.

## Użycie

| Akcja | Jak |
|-------|-----|
| Nowy dokument | Przycisk **+ Nowy dokument** → wybierz typ → wypełnij formularz |
| Podgląd | Przycisk **👁 Podgląd** na karcie dokumentu |
| Edycja | Przycisk **✏️ Edytuj** |
| Usunięcie | Przycisk **🗑** z potwierdzeniem |
| Nawigacja w prezentacji | Strzałki ←/→ lub klawiatura |

## Typy dokumentów

- **Prezentacja** — slajdy (tytułowy, treść, kod, dwie kolumny), nawigacja klawiaturą
- **Infografika** — kafelki statystyk, wykres (słupkowy/kołowy/pierścieniowy), sekcje tekstowe
- **Cheatsheet** — kategorie z komendami, wyszukiwarka, kopiowanie do schowka

## Struktura

```
server.py          # serwer HTTP (Python stdlib, bez pip)
static/
  index.html       # aplikacja główna
  viewer/          # przeglądarki dla każdego typu
documents/         # dokumenty użytkownika (pliki JSON)
examples/          # przykładowe dokumenty (presentation / infographic / cheatsheet)
```

## API

```
GET    /api/documents        # lista dokumentów
GET    /api/documents/{id}   # pobierz dokument
POST   /api/documents        # utwórz dokument
PUT    /api/documents/{id}   # zaktualizuj
DELETE /api/documents/{id}   # usuń
```
