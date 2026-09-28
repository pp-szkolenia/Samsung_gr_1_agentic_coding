# Proposal

## Why

Użytkownicy nie mają możliwości eksportu dokumentów (prezentacji, infografik, cheatsheetów) do pliku PDF bez ręcznego otwierania widoku i korzystania z funkcji drukowania przeglądarki. Dodanie dedykowanego przycisku PDF z podglądem przed zapisem usprawni ten przepływ i zrobi go discoverable.

## What Changes

- Nowy przycisk "📄 PDF" na każdej karcie dokumentu w widoku listy (`index.html`)
- Otwarcie widoku danego dokumentu w nowej karcie z parametrem `?pdf=1`
- Każdy z trzech plików przeglądarki (`presentation.html`, `infographic.html`, `cheatsheet.html`) wykrywa parametr `?pdf=1` i po pełnym załadowaniu treści wywołuje `window.print()`
- Przeglądarka pokazuje wbudowany podgląd wydruku/PDF — użytkownik widzi dokument przed zapisem i decyduje czy zapisać
- Style `@media print` w każdym viewerze — ukrycie elementów nawigacyjnych, dostosowanie układu do strony A4

## Capabilities

### New Capabilities

- `pdf-export`: Eksport dokumentu do PDF z podglądem — przycisk na karcie, otwarcie viewera w trybie druku, wywołanie natywnego okna druku przeglądarki

### Modified Capabilities

_(brak — istniejące zachowanie viewerów nie zmienia się; tryb PDF to addytywne rozszerzenie)_

## Impact

- **`static/index.html`**: dodanie przycisku PDF i funkcji `exportPdf(id, type)` w sekcji card-actions
- **`static/viewer/presentation.html`**: detekcja `?pdf=1`, `@media print` styles, wywołanie `window.print()`
- **`static/viewer/infographic.html`**: j.w. + obsługa wyrenderowania Chart.js przed drukiem
- **`static/viewer/cheatsheet.html`**: j.w.
- **Zależności**: bez nowych bibliotek — używamy natywnego browser print API
- **Kompatybilność**: wstecznie kompatybilne — viewery bez parametru działają jak dotychczas
