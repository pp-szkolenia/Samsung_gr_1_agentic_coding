---
name: ui-design
description: Zasady wizualne, paleta kolorów, layout i szablony komponentów HTML/CSS dla Slides Generator
triggers:
  - design
  - css
  - layout
  - komponent
  - slajd
  - kolor
  - wygląd
  - styl
  - interfejs
author: patryk@palej.email
version: 1.0.0
---

# Skill: ui-design

Skill do projektowania interfejsu w Slides Generator — zasady wizualne, layout i komponenty HTML/CSS.

## Zasady ogólne

- **Mobile-first** — layout działa od 320px wzwyż
- **16px** — minimalny gutter boczny na każdej stronie
- Brak poziomowego scrolla strony
- Ciemny i jasny motyw wspierane przez `@media (prefers-color-scheme: dark)`

## Paleta kolorów (tokeny CSS)

```css
:root {
  --color-bg:        #ffffff;
  --color-surface:   #f5f5f5;
  --color-border:    #e0e0e0;
  --color-text:      #1a1a1a;
  --color-muted:     #6b7280;
  --color-accent:    #2563eb;
  --color-accent-h:  #1d4ed8;  /* hover */
  --color-success:   #16a34a;
  --color-warning:   #d97706;
  --color-error:     #dc2626;
}

@media (prefers-color-scheme: dark) {
  :root:not([data-theme="light"]) {
    --color-bg:      #0f172a;
    --color-surface: #1e293b;
    --color-border:  #334155;
    --color-text:    #f1f5f9;
    --color-muted:   #94a3b8;
  }
}
```

## Typografia

- Nagłówki: `font-weight: 700`, skala 1.25x (h1→h2→h3)
- Body: `font-size: 16px`, `line-height: 1.6`
- Kod: `font-family: 'Courier New', monospace`, tło `--color-surface`

## Typy dokumentów — wytyczne layoutu

### Prezentacja (slides)
- Pełnoekranowy widok: `100vw × 100vh` per slajd
- Nawigacja strzałkami (←/→), wskaźnik slajdów na dole
- Jedno główne przesłanie per slajd

### Infografika
- Układ scrollowalny, max-width `900px`, wyśrodkowany
- Sekcje oddzielone `<hr>` lub spacing `2rem`
- Wykresy i statystyki w siatce (grid 2–3 kolumny na desktop)

### Cheatsheet
- Gęsty layout: 2–3 kolumny pojęć na desktop, 1 na mobile
- Każde pojęcie: `<dt>` bold + `<dd>` wyjaśnienie
- Możliwość druku (`@media print`)

## Komponenty — szablony

### Karta pojęcia (cheatsheet)
```html
<div class="card">
  <h3 class="card__title">Nazwa pojęcia</h3>
  <p class="card__body">Wyjaśnienie</p>
  <code class="card__example">przykład kodu</code>
</div>
```

### Slajd (prezentacja)
```html
<section class="slide">
  <h2 class="slide__title">Tytuł slajdu</h2>
  <div class="slide__content"><!-- treść --></div>
</section>
```

### Stat tile (infografika)
```html
<div class="stat">
  <span class="stat__value">42%</span>
  <span class="stat__label">Opis metryki</span>
</div>
```
