# Tasks

## 1. Biblioteka PptxGenJS

- [ ] 1.1 Dodać tag `<script src="https://cdn.jsdelivr.net/npm/pptxgenjs@3/dist/pptxgen.bundle.js"></script>` w `<head>` pliku `static/index.html` — weryfikacja: otworzenie strony i sprawdzenie w konsoli przeglądarki że `window.PptxGenJS` jest zdefiniowany

## 2. Przycisk PPTX w kartach

- [ ] 2.1 W funkcji `renderDocs()` w `static/index.html` dodać przycisk `📎 PPTX` wyświetlany warunkowo tylko gdy `type === 'presentation'` z atrybutem `onclick="exportPptx('${eA(d.id)}')"` — weryfikacja: w widoku listy karta prezentacji ma przycisk PPTX, karta infografiki i cheatsheeту — nie

## 3. Funkcja exportPptx

- [ ] 3.1 Zaimplementować `async function exportPptx(id)` w sekcji `<script>` pliku `static/index.html`:
  - pobrać dokument przez `await api.get(id)`
  - stworzyć `new PptxGenJS()` i ustawić wymiary slajdu (10×7.5 cala)
  - na podstawie `data.theme` wybrać kolory `bgColor` i `textColor`
  - iterować po `data.slides` i dla każdego wywołać pomocniczą funkcję `addPptxSlide(pptx, slide, colors)`
  - wywołać `pptx.writeFile({ fileName: sanitizedTitle + '.pptx' })`
  - obsłużyć wyjątek: `catch(e) { alert('Błąd eksportu PPTX: ' + e.message); }`
  - weryfikacja: kliknięcie przycisku PPTX inicjuje pobieranie pliku `.pptx`

- [ ] 3.2 Zaimplementować `function addPptxSlide(pptx, slide, colors)` obsługującą 4 typy (`title`, `content`, `code`, `two-column`) zgodnie z pozycjonowaniem z `design.md` — weryfikacja: otworzyć wygenerowany plik PPTX w LibreOffice Impress i sprawdzić obecność wszystkich typów slajdów z poprawną treścią

## 4. Weryfikacja motywu i integracja

- [ ] 4.1 Sprawdzić że prezentacja z `theme: "dark"` generuje PPTX z ciemnym tłem, a `theme: "light"` z białym — weryfikacja wizualna w LibreOffice Impress

- [ ] 4.2 Sprawdzić pełny happy path: wybór prezentacji przykładowej → klik „📎 PPTX" → plik pobierany → otwarcie w Impress → slajdy wyglądają poprawnie
