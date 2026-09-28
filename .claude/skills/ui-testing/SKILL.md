---
name: ui-testing
description: Dokładne testowanie UI Slides Generator — widoczność wszystkich elementów HTML, screenshoty, responsywność i scenariusze regresji
triggers:
  - test
  - testowanie
  - playwright
  - regresja
  - sprawdź
  - weryfikacja
  - screenshot
  - przeglądarka
  - ui
author: patryk@palej.email
version: 2.0.0
---

# Skill: ui-testing — Slides Generator

Metodologia dokładnego testowania UI: weryfikacja widoczności **każdego** elementu obecnego w kodzie HTML.

---

## Krok 0 — Przygotowanie

1. Ustaw rozdzielczość: `browser_resize` → `1920x1080`
2. Otwórz stronę: `browser_navigate` → `http://localhost:8080`
3. Zrób screenshot startowy i zapisz do `.playwright-mcp/`

---

## Krok 1 — Weryfikacja elementów przez `browser_snapshot`

Zamiast zgadywać co jest na stronie, **najpierw pobierz snapshot DOM** przez `browser_snapshot`. Snapshot zwraca accessibility tree — listę wszystkich widocznych elementów z ich rolami i etykietami. Porównaj go z kodem HTML strony.

Elementy które pojawiają się w HTML ale **nie ma ich w snapsocie** = niewidoczne lub ukryte.

---

## Krok 2 — Checklist elementów per widok

### 2.1 Strona główna (`/`)

Elementy do weryfikacji (selektory CSS):

| Element | Selektor | Co sprawdzić |
|---------|----------|--------------|
| Header | `.hdr` | Widoczny, nie ucięty |
| Logo | `.logo` | Tekst "SlidesGenerator" z akcentem |
| Przycisk nowego dok. | `.btn-primary` | Widoczny, kolor accent `#c96442` |
| Pasek filtrów | `.filters` | Wszystkie 4 przyciski: Wszystkie / Prezentacje / Infografiki / Cheatsheets |
| Aktywny filtr | `.flt-btn.on` | Ma tło accent |
| Siatka dokumentów | `.grid` | Nie pusta gdy są dokumenty |
| Karta dokumentu | `.card` | Pasek koloru na górze (niebieski/zielony/pomarańczowy wg typu) |
| Odznaka typu | `.badge` | Tekst i kolor zgodny z typem |
| Data aktualizacji | `.card-meta` | Widoczna, czytelna |
| Przyciski akcji | `.card-actions .btn` | Widoczne: 👁 Podgląd, ✏️ Edytuj, 🗑 Usuń |
| Przycisk PPTX | `.btn[data-action="pptx"]` | Widoczny tylko dla prezentacji |

**Jak sprawdzać visibility elementów:**

```js
// Przez browser_find lub browser_snapshot — szukaj elementu w accessibility tree
// Jeśli element jest w HTML ale nie ma go w tree → prawdopodobnie hidden/display:none

// Sprawdź konkretny element przez browser_evaluate:
// document.querySelector('.card-actions').getBoundingClientRect()
// Zwraca {x, y, width, height} — jeśli width=0 lub height=0 → niewidoczny
```

### 2.2 Widok prezentacji (`/static/viewer/presentation.html?id=<id>`)

| Element | Selektor | Co sprawdzić |
|---------|----------|--------------|
| Pasek nawigacji | `.nav` / `#nav` | Widoczny na górze/dole |
| Przycisk Wstecz | `button` z tekstem "Wstecz" lub "←" | Widoczny |
| Licznik slajdów | `#counter` / `.counter` | Format "X / N" |
| Przycisk Dalej | `button` z "Dalej" lub "→" | Widoczny |
| Przycisk motywu | `button` z "◐" | Widoczny |
| Slajd | `.slide` / `[class*="slide"]` | Wypełnia viewport |
| Tytuł slajdu | `h1`, `h2` na slajdzie | Czytelny, nie ucięty |
| Nawigacja klawiaturą | — | Sprawdź `browser_press_key` → ArrowRight |

### 2.3 Widok infografiki (`/static/viewer/infographic.html?id=<id>`)

| Element | Selektor | Co sprawdzić |
|---------|----------|--------------|
| Nagłówek | `h1` / `.title` | Tytuł widoczny |
| Podtytuł | `.subtitle` | Widoczny |
| Kafelki statystyk | `.stat` / `[class*="stat"]` | Wszystkie 4 widoczne, ikona + wartość + label |
| Kontener wykresu | `canvas` / `#chart` | Wyrenderowany (nie pusty canvas) |
| Tytuł wykresu | `.chart-title` | Widoczny |
| Sekcje tekstowe | `.section` / `[class*="section"]` | Tytuł + lista punktów |
| Brak poziomego scrolla | `body` | `scrollWidth <= window.innerWidth` |

### 2.4 Widok cheatsheet (`/static/viewer/cheatsheet.html?id=<id>`)

| Element | Selektor | Co sprawdzić |
|---------|----------|--------------|
| Nagłówek | `h1` | Tytuł widoczny |
| Pole wyszukiwania | `input[type="search"]` / `#search` | Widoczne, placeholder czytelny |
| Selektor motywu | `select` / `.theme-select` | Widoczny |
| Przyciski kategorii | `.category-btn` / `nav button` | Wszystkie widoczne |
| Komendy | `.command` / `[class*="cmd"]` | Tekst komendy, opis, przykład |
| Przyciski kopiuj | `button` z "kopiuj" / "📋" | Przy każdej komendzie |
| Footer statystyki | `footer` / `.footer` | "X kategorii · Y pozycji" |

### 2.5 Modal edycji / tworzenia (na stronie głównej)

| Element | Selektor | Co sprawdzić |
|---------|----------|--------------|
| Overlay | `.overlay` | Zasłania resztę strony |
| Box modalny | `.mbox` | Wycentrowany, nie wychodzi poza ekran |
| Pole Tytuł | `input[name="title"]` / `#doc-title` | Widoczne |
| Pole Autor | `input[name="author"]` | Widoczne |
| Dropdown Motyw | `select[name="theme"]` | Widoczny |
| Przyciski Anuluj/Zapisz | `.btn` w modalu | Oba widoczne |
| Sekcja slajdów | `.slides-editor` / `[id*="slides"]` | Widoczna dla prezentacji |

---

## Krok 3 — Jak sprawdzić widoczność przez Playwright MCP

### 3.1 `browser_snapshot`
Pobiera accessibility tree. Jeśli elementu nie ma w tree — jest niewidoczny lub ma `display:none` / `visibility:hidden` / `aria-hidden`.

### 3.2 `browser_find`
Szuka elementu po tekście lub roli. Jeśli nie znajdzie → element niewidoczny lub nie istnieje.

### 3.3 `browser_evaluate`
Uruchom JS bezpośrednio:
```js
// Sprawdź czy element jest widoczny i ma rozmiar
const el = document.querySelector('.card-actions');
const rect = el?.getBoundingClientRect();
// rect.width > 0 && rect.height > 0 && rect.top < window.innerHeight → widoczny
```

### 3.4 `browser_take_screenshot`
Rób screenshoty **przed i po** każdej interakcji. Zapisuj do `.playwright-mcp/` z numerowaną nazwą: `01_main.png`, `02_modal.png` itp.

---

## Krok 4 — Weryfikacja responsywności

Sprawdź każdy widok przy 3 szerokościach przez `browser_resize`:

| Szerokość | Wysokość | Scenariusz |
|-----------|----------|------------|
| 375px | 667px | Mobile (iPhone SE) |
| 768px | 1024px | Tablet |
| 1920px | 1080px | Desktop |

Na mobile (375px) sprawdź:
- Brak poziomego scrolla (`scrollWidth <= clientWidth`)
- Elementy nie nakładają się
- Tekst czytelny (min 13px)

---

## Krok 5 — Sprawdzenie błędów JS

Po każdym widoku: `browser_console_messages`. Błędy (level `error`) są niedopuszczalne. Warnings traktuj jako opcjonalne do sprawdzenia.

---

## Krok 6 — Scenariusze interaktywne

### Filtrowanie dokumentów
1. Kliknij przycisk "Prezentacje" → karty innego typu znikają
2. Kliknij "Wszystkie" → wracają wszystkie karty

### Nawigacja w prezentacji
1. Kliknij "Dalej" kilka razy → licznik rośnie, nie przekracza max
2. Kliknij "Wstecz" na pierwszym slajdzie → nic złego się nie dzieje
3. `browser_press_key` → ArrowRight → slajd się zmienia

### Wyszukiwanie w cheatsheet
1. Wpisz tekst w pole wyszukiwania
2. Sprawdź czy komendy filtrują się poprawnie

### Modal tworzenia nowego dokumentu
1. Kliknij "+ Nowy dokument"
2. Sprawdź że modal się otwiera
3. Kliknij "Anuluj" → modal znika

---

## Krok 7 — Output i raportowanie

Format raportu:

```
### [Nazwa widoku]
- Status: ✅ OK / ❌ Problem
- Niewidoczne elementy: [lista lub "brak"]
- Błędy JS: [liczba lub "brak"]
- Screenshot: .playwright-mcp/NN_nazwa.png
- Opis problemu (jeśli jest): [szczegóły]
```

Zawsze kończ podsumowaniem:
- Łączna liczba sprawdzonych widoków
- Czy zmiana jest OK (TAK/NIE)
- Lista elementów do naprawy (jeśli są)
