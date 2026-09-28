# Design

## Context

`server.py` używa wyłącznie Python stdlib — brak zewnętrznych zależności jest twardym ograniczeniem (patrz proposal.md — Why). Istniejący eksport PDF działa przez `window.print()` w viewer. Aplikacja to SPA z vanilla JS ładowanym z jednego pliku `static/index.html`.

## Goals / Non-Goals

**Goals:**
- Wygenerowanie poprawnego `.pptx` bez zmian po stronie serwera
- Obsługa wszystkich 4 typów slajdów i 2 motywów

**Non-Goals:**
- Eksport PPTX dla infografik i cheatsheetów
- Zachowanie stylów CSS (cienie, gradienty) w PPTX
- Generowanie po stronie serwera

## Decisions

### 1. Generowanie po stronie klienta (PptxGenJS)

**Wybór:** PptxGenJS v3 z CDN `cdn.jsdelivr.net/npm/pptxgenjs@3/dist/pptxgen.bundle.js`.

**Dlaczego nie generowanie serwer-side?** Wymagałoby `python-pptx` (pip), co łamie ograniczenie stdlib-only.

**Dlaczego nie ręczna konstrukcja XML/ZIP?** Format OOXML jest złożony; biblioteka JS produkuje poprawne PPTX bez ryzyka błędów struktury.

**Alternatywa odrzucona:** jsPDF — generuje tylko PDF, nie PPTX.

### 2. Tylko jeden plik do zmiany (`index.html`)

Cała logika eksportu trafia do funkcji `exportPptx(id)` inline w `<script>` w `index.html`. Brak nowych plików statycznych. Biblioteka ładowana z CDN.

### 3. Mapowanie typów slajdów na TextBox'y PptxGenJS

PptxGenJS nie ma wbudowanych layoutów tytułowych — używamy API `slide.addText()` z jawnie podanymi wymiarami i pozycjami (w calach, siatka 10×7.5). Decyzja pozycjonowania:

| Typ      | Elementy na slajdzie                                  |
|----------|-------------------------------------------------------|
| `title`  | Tytuł wyśrodkowany (y=2.5, h=1.5) + podtytuł (y=4.2)|
| `content`| Tytuł (y=0.3, h=0.8) + treść+bullets (y=1.4, h=5.5)|
| `code`   | Tytuł (y=0.3, h=0.8) + kod monospace (y=1.4, h=5.5) |
|`two-column`| Tytuł (y=0.3) + lewa (x=0.3, w=4.6) + prawa (x=5.2, w=4.6)|

### 4. Kolory motywu

- `dark`: bg=`#1a1a2e`, text=`#e8e8e8`, accent=`#4f8ef7`
- `light` (domyślny): bg=`#ffffff`, text=`#1f1e1c`, accent=`#c96442`

## Risks / Trade-offs

- **[Ryzyko] CDN niedostępne** → PptxGenJS nie załaduje się, przycisk wywołuje błąd `PptxGenJS is not defined`. Mitigacja: alert z komunikatem „Brak połączenia z CDN".
- **[Trade-off] Emoji w tekście** → PptxGenJS obsługuje Unicode, emoji mogą jednak nie renderować się identycznie w każdej wersji Office. Akceptowalne.
- **[Trade-off] Brak zachowania stylów CSS** → Kolory z motywu są uproszczone (brak gradientów). PPTX jest edytowalny — użytkownik może dostosować styl.

## Migration Plan

Zmiana jest addytywna — brak migracji. Cofnięcie: usunięcie skryptu CDN i funkcji `exportPptx` z `index.html`.

## Open Questions

*(brak)*
