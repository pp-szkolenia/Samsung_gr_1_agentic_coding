# Design

## Context

Projekt to aplikacja SPA (vanilla JS) z trzema przeglądarkami dokumentów: `presentation.html`, `infographic.html`, `cheatsheet.html`. Serwer to minimalny Python HTTP server (stdlib only — brak możliwości dodania Puppeteer czy wDKHTMLtoPDF po stronie serwera). Chart.js jest jedyną zewnętrzną biblioteką, ładowaną z CDN tylko w `infographic.html`.

## Goals / Non-Goals

**Goals:**
- Eksport każdego typu dokumentu do PDF przez natywne okno druku przeglądarki
- Podgląd przed zapisem — użytkownik widzi jak będzie wyglądał PDF
- Ukrycie UI nawigacyjnego w wydruku (`@media print`)
- Zero nowych zależności zewnętrznych

**Non-Goals:**
- Generowanie PDF po stronie serwera
- Batchowy eksport wielu dokumentów naraz
- Kontrola nad ustawieniami strony (orientacja, marginesy) — to odpowiedzialność przeglądarki
- Eksport do formatów innych niż PDF

## Decisions

### D1: Browser Print API zamiast biblioteki PDF

**Decyzja**: Używamy `window.print()` + `@media print` CSS.

**Rationale**: Projekt ma zasadę zero zewnętrznych zależności po stronie serwera. Biblioteki jak jsPDF / html2canvas wymagają dodatkowych plików lub CDN i mają problemy z renderowaniem CSS (szczególnie Chart.js canvas). Natywny print daje dokładne odwzorowanie — przeglądarka wie jak renderować własne strony.

**Alternatywy**:
- `jsPDF` — wymaga ładowania biblioteki (~300KB), słabo renderuje custom fonts i Chart.js canvas
- `html2canvas + jsPDF` — generuje screenshot (bitmap), nie wektorowy PDF; niska jakość tekstu
- Puppeteer po stronie serwera — narusza zasadę "stdlib only Python"

### D2: Parametr URL `?pdf=1` zamiast osobnej strony

**Decyzja**: Każdy viewer wykrywa `?pdf=1` w `URLSearchParams` i wywołuje `window.print()` po załadowaniu.

**Rationale**: Nie trzeba duplikować plików viewer. Istniejące URL-e `viewDoc()` pozostają niezmienione — dodanie parametru to minimalna ingerencja.

**Timing dla `window.print()`**:
- `presentation.html` — po event `DOMContentLoaded` (treść synchroniczna)
- `infographic.html` — po `chart.update()` / callbacku Chart.js (canvas musi być wyrenderowany przed drukiem)
- `cheatsheet.html` — po `DOMContentLoaded` (treść synchroniczna)

### D3: `@media print` — co ukryć

Ukrywamy:
```css
@media print {
  .nav-hints, .slide-counter, .controls, .search-bar, .copy-btn { display: none; }
  body { background: white; }
}
```

Dla `presentation.html` — wszystkie slajdy drukowane na osobnych stronach przez `page-break-after: always`.

## Risks / Trade-offs

- **[Ryzyko] Chart.js canvas w PDF** → Chart.js renderuje do `<canvas>`. Większość przeglądarek (Chrome, Edge) poprawnie drukuje canvas jako obraz w PDF. Firefox może mieć niższą jakość. **Mitygacja**: dodanie `canvas { max-width: 100%; }` w `@media print`; nie jest to bloker.
- **[Ryzyko] Prezentacja wieloslajdowa — łamanie stron** → Domyślnie slajdy mogą się przycinać. **Mitygacja**: `page-break-after: always` na kontenerze slajdu.
- **[Trade-off] Użytkownik musi wybrać "Zapisz jako PDF"** → Nie ma auto-downloadu; system otwiera native print dialog. To zgodne z wymaganiem "podgląd przed zapisem" — celowe.
