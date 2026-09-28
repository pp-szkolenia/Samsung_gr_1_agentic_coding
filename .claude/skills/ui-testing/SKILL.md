---
name: ui-testing
description: Checklist manualny, Playwright i scenariusze regresji dla testowania UI Slides Generator
triggers:
  - test
  - testowanie
  - playwright
  - regresja
  - sprawdź
  - weryfikacja
  - screenshot
  - przeglądarka
author: patryk@palej.email
version: 1.0.0
---

# Skill: ui-testing

Skill do testowania interfejsu Slides Generator w przeglądarce — checklist manualny, Playwright i scenariusze regresji.

## Wymagania przed zgłoszeniem gotowości

Przed napisaniem "gotowe" do każdej zmiany UI **musisz**:
1. Uruchomić serwer dev
2. Otworzyć stronę w przeglądarce (Playwright lub opis kroków)
3. Przejść golden path opisany poniżej
4. Sprawdzić brak błędów w konsoli

Jeśli nie możesz uruchomić przeglądarki — napisz to wprost, nie deklaruj sukcesu.

## Golden path — checklist manualny

### Aplikacja ogólna
- [ ] Strona główna ładuje się bez błędów JS w konsoli
- [ ] Lista dokumentów wyświetla się poprawnie
- [ ] Serwer Python odpowiada na `http://localhost:PORT`

### Prezentacja
- [ ] Slajdy wyświetlają się pełnoekranowo
- [ ] Nawigacja strzałkami (←/→) działa
- [ ] Wskaźnik slajdów pokazuje właściwy numer
- [ ] Pierwszy i ostatni slajd — brak out-of-bounds

### Infografika
- [ ] Wykresy/statystyki renderują się poprawnie
- [ ] Brak poziomowego scrolla
- [ ] Sekcje są czytelnie oddzielone

### Cheatsheet
- [ ] Wszystkie pojęcia są widoczne
- [ ] Layout 2–3 kolumnowy na szerokim ekranie
- [ ] Pojedyncza kolumna na mobile (≤768px)

## Scenariusze brzegowe

- Pusty dokument (0 slajdów / 0 pojęć) — brak błędów
- Bardzo długi tekst — nie wychodzi poza kontener
- Resize okna — layout nie łamie się w trakcie

## Testy responsywności

Sprawdź przy szerokościach: `320px`, `768px`, `1280px`

```js
// Playwright — przykład resize
await page.setViewportSize({ width: 320, height: 568 });
await page.screenshot({ path: 'mobile.png' });
```

## Playwright — szablon testu

```js
import { test, expect } from '@playwright/test';

test('golden path — [nazwa funkcji]', async ({ page }) => {
  await page.goto('http://localhost:PORT');

  // Asercja widoczności głównego elementu
  await expect(page.locator('h1')).toBeVisible();

  // TODO: dodaj kroki specyficzne dla testowanej funkcji

  // Brak błędów JS
  const errors = [];
  page.on('pageerror', e => errors.push(e.message));
  expect(errors).toHaveLength(0);
});
```

## Regresje po zmianach

Po każdej zmianie CSS/JS sprawdź, czy nadal działają:
- Pozostałe typy dokumentów (nie tylko zmieniony)
- Nawigacja między dokumentami
- Dark/light mode (jeśli zaimplementowany)
