# Tasks

## 1. Przycisk PDF w widoku listy (index.html)

- [x] 1.1 Dodać przycisk `📄 PDF` w sekcji `.card-actions` w szablonie karty (funkcja `renderGrid`) w `static/index.html` — przycisk wywołuje `exportPdf(id, type)`; zweryfikować że przycisk jest widoczny na każdej karcie po odświeżeniu strony
- [x] 1.2 Dodać funkcję `exportPdf(id, type)` w `static/index.html`, która wywołuje `window.open('/viewer/${type}.html?id=${id}&pdf=1', '_blank')`; zweryfikować w devtools że URL zawiera `?pdf=1`

## 2. Tryb PDF w presentation.html

- [x] 2.1 Dodać detekcję parametru `?pdf=1` w `static/viewer/presentation.html` — po `DOMContentLoaded`, gdy parametr obecny, wywołać `window.print()`; zweryfikować że okno druku otwiera się automatycznie po załadowaniu URL z `?pdf=1`
- [x] 2.2 Dodać style `@media print` w `static/viewer/presentation.html`: ukryć `.nav` i `.progress`, ustawić `background: white`, dodać `page-break-after: always` na kontenerze każdego slajdu; zweryfikować w podglądzie druku że nawigacja jest niewidoczna i każdy slajd zaczyna się na nowej stronie

## 3. Tryb PDF w infographic.html

- [x] 3.1 Dodać detekcję parametru `?pdf=1` w `static/viewer/infographic.html` — wywołać `window.print()` PO renderowaniu Chart.js (po `new Chart(...)` lub w callbacku `animation.onComplete`); zweryfikować że wykres jest widoczny w podglądzie druku
- [x] 3.2 Dodać style `@media print` w `static/viewer/infographic.html`: ustawić `background: white`, `canvas { max-width: 100%; }`; zweryfikować że layout infografiki i wykres wyświetlają się poprawnie w podglądzie druku

## 4. Tryb PDF w cheatsheet.html

- [x] 4.1 Dodać detekcję parametru `?pdf=1` w `static/viewer/cheatsheet.html` — po `DOMContentLoaded`, gdy parametr obecny, wywołać `window.print()`; zweryfikować że okno druku otwiera się automatycznie po załadowaniu URL z `?pdf=1`
- [x] 4.2 Dodać style `@media print` w `static/viewer/cheatsheet.html`: ukryć pasek wyszukiwania (`input[type=search]`) i przyciski kopiuj, ustawić `background: white`; zweryfikować w podglądzie druku że wyszukiwarka i copy-buttony są niewidoczne, a wszystkie kategorie i komendy są widoczne

## 5. Weryfikacja integracyjna

- [x] 5.1 Przetestować eksport PDF dla dokumentu każdego typu (prezentacja, infografika, cheatsheet): kliknąć przycisk PDF na karcie → sprawdzić że otwiera się nowa karta z viewerem → sprawdzić że okno druku otwiera się automatycznie → sprawdzić że elementy nawigacyjne są ukryte w podglądzie
- [x] 5.2 Zweryfikować że zwykły podgląd (przycisk "👁 Podgląd") nadal działa bez zmian — URL bez `?pdf=1` nie uruchamia okna druku
