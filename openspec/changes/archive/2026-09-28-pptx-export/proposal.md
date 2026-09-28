# Proposal

## Why

Użytkownicy tworzący prezentacje w Slides Generator potrzebują możliwości eksportu do formatu `.pptx`, aby móc dalej edytować slajdy w PowerPoint lub Impress. Istniejący eksport PDF nie pozwala na dalszą edycję treści — PPTX wypełnia tę lukę bez naruszania ograniczenia stdlib-only serwera.

## What Changes

- Dodanie przycisku „📎 PPTX" w kartach dokumentów typu `presentation` na liście w `index.html`
- Dodanie funkcji `exportPptx(id)` generującej plik `.pptx` po stronie klienta z użyciem biblioteki PptxGenJS (CDN)
- Mapowanie czterech typów slajdów JSON (`title`, `content`, `code`, `two-column`) na odpowiednie układy slajdów PPTX
- Obsługa motywu (`dark`/`light`) wpływającego na kolory tła i tekstu w PPTX
- Dodanie skryptu PptxGenJS z CDN (`cdn.jsdelivr.net`) do `<head>` w `index.html`

## Capabilities

### New Capabilities

- `pptx-export`: Eksport dokumentu prezentacji do pliku `.pptx` bezpośrednio z przeglądarki, z zachowaniem struktury slajdów i motywu kolorystycznego.

### Modified Capabilities

*(brak — eksport PDF nie zmienia wymagań)*

## Impact

- **Plik zmieniony**: `static/index.html` (jedyna modyfikacja)
- **Nowa zależność JS**: PptxGenJS v3 z CDN `cdn.jsdelivr.net/npm/pptxgenjs@3` (bez zmian serwera)
- **Brak zmian**: `server.py` (stdlib-only pozostaje bez zmian), pliki viewer
- **Typy dokumentów**: eksport PPTX tylko dla `presentation`; `infographic` i `cheatsheet` pozostają z PDF
