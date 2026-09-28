# Spec: pptx-export

## Purpose

Umożliwia użytkownikom pobranie prezentacji jako pliku `.pptx` gotowego do edycji w PowerPoint lub LibreOffice Impress, bezpośrednio z listy dokumentów w aplikacji.

## Requirements

### Requirement: Przycisk eksportu PPTX dla prezentacji

Aplikacja SHALL wyświetlać przycisk „📎 PPTX" w sekcji akcji każdej karty dokumentu o typie `presentation`. Przyciski eksportu PDF i PPTX SHALL być dostępne równolegle. Karty dokumentów o typach `infographic` i `cheatsheet` NIE SHALL wyświetlać przycisku PPTX.

#### Scenario: Przycisk widoczny tylko dla prezentacji

- **WHEN** lista dokumentów zawiera dokument o typie `presentation`
- **THEN** karta tego dokumentu wyświetla przycisk „📎 PPTX"

#### Scenario: Brak przycisku dla innych typów

- **WHEN** lista dokumentów zawiera dokument o typie `infographic` lub `cheatsheet`
- **THEN** karta tego dokumentu NIE wyświetla przycisku „📎 PPTX"

### Requirement: Generowanie pliku PPTX po stronie klienta

Po kliknięciu przycisku „📎 PPTX" aplikacja SHALL pobrać dane prezentacji z API i wygenerować plik `.pptx` bezpośrednio w przeglądarce (bez udziału serwera). Plik SHALL zostać automatycznie pobrany przez przeglądarkę.

#### Scenario: Pobranie pliku PPTX

- **WHEN** użytkownik klika „📎 PPTX" na karcie prezentacji
- **THEN** przeglądarka pobiera plik o nazwie `<tytuł_prezentacji>.pptx`

#### Scenario: Błąd sieci podczas pobierania danych

- **WHEN** żądanie do API podczas eksportu zwróci błąd
- **THEN** aplikacja wyświetla alert z komunikatem błędu i nie inicjuje pobierania

### Requirement: Mapowanie slajdów na slajdy PPTX

Każdy slajd w prezentacji SHALL być odwzorowany na oddzielny slajd PPTX zgodnie z jego typem:

- `title` → tytuł wyśrodkowany (duży) + podtytuł poniżej
- `content` → tytuł slajdu + treść tekstowa + lista punktowana (każdy punkt zaczyna się od „•")
- `code` → tytuł slajdu + blok kodu w czcionce monospace
- `two-column` → tytuł slajdu + dwa obszary tekstu obok siebie (lewa i prawa kolumna)

#### Scenario: Slajd tytułowy

- **WHEN** slajd ma `type: "title"`
- **THEN** slajd PPTX zawiera pole z tytułem i pole z podtytułem

#### Scenario: Slajd z treścią i punktami

- **WHEN** slajd ma `type: "content"` z wypełnionym `bullets`
- **THEN** slajd PPTX zawiera tytuł oraz listę punktów; każdy punkt zaczyna się od „•"

#### Scenario: Slajd z kodem

- **WHEN** slajd ma `type: "code"`
- **THEN** slajd PPTX zawiera tytuł oraz blok kodu w czcionce monospace

#### Scenario: Slajd dwukolumnowy

- **WHEN** slajd ma `type: "two-column"`
- **THEN** slajd PPTX zawiera tytuł oraz dwa oddzielne obszary tekstowe obok siebie

### Requirement: Obsługa motywu kolorystycznego

Wygenerowany PPTX SHALL uwzględniać motyw prezentacji (`dark` lub `light`) wpływający na kolor tła slajdów i kolor tekstu.

#### Scenario: Motyw ciemny

- **WHEN** prezentacja ma `theme: "dark"`
- **THEN** slajdy PPTX mają ciemne tło i jasny tekst

#### Scenario: Motyw jasny

- **WHEN** prezentacja ma `theme: "light"` lub brak pola `theme`
- **THEN** slajdy PPTX mają białe tło i ciemny tekst
