# Spec Delta

## Purpose

Umożliwia użytkownikom eksport dowolnego dokumentu (prezentacji, infografiki, cheatsheet) do pliku PDF bezpośrednio z poziomu listy dokumentów, z podglądem przed zapisem opartym na natywnym mechanizmie druku przeglądarki.

## ADDED Requirements

### Requirement: Przycisk PDF na karcie dokumentu

Każda karta dokumentu w widoku listy SHALL zawierać przycisk eksportu PDF widoczny obok istniejących przycisków akcji.

#### Scenario: Widoczność przycisku PDF

- **WHEN** użytkownik otwiera stronę główną z listą dokumentów
- **THEN** każda karta dokumentu wyświetla przycisk "📄 PDF" w sekcji akcji

#### Scenario: Przycisk PDF dla każdego typu dokumentu

- **WHEN** lista dokumentów zawiera prezentacje, infografiki i cheatsheets
- **THEN** przycisk PDF jest widoczny na kartach wszystkich trzech typów

### Requirement: Otwarcie widoku w trybie druku

Po kliknięciu przycisku PDF system SHALL otworzyć widok dokumentu w nowej karcie przeglądarki z aktywnym trybem druku.

#### Scenario: Nowa karta z trybem PDF

- **WHEN** użytkownik klika przycisk "📄 PDF" na karcie dokumentu
- **THEN** przeglądarka otwiera nową kartę z odpowiednim viewerem i parametrem `?pdf=1` w URL

#### Scenario: Viewer nie zmienia zachowania bez parametru

- **WHEN** użytkownik otwiera viewer bez parametru `?pdf=1` (zwykły podgląd)
- **THEN** viewer działa tak jak dotychczas — bez automatycznego uruchomienia druku

### Requirement: Podgląd przed zapisem

System SHALL wyświetlić natywne okno podglądu wydruku przeglądarki przed umożliwieniem zapisu PDF.

#### Scenario: Automatyczny podgląd po załadowaniu

- **WHEN** viewer załaduje się z parametrem `?pdf=1`
- **THEN** przeglądarka automatycznie otwiera okno podglądu druku/PDF

#### Scenario: Użytkownik może anulować

- **WHEN** użytkownik otwiera podgląd i klika "Anuluj" w oknie druku
- **THEN** okno druku zamknięcie bez zapisu pliku; karta przeglądarki pozostaje otwarta

#### Scenario: Zapis PDF

- **WHEN** użytkownik wybiera "Zapisz jako PDF" lub "Drukuj do PDF" w oknie podglądu
- **THEN** przeglądarka zapisuje dokument jako plik PDF

### Requirement: Ukrycie elementów nawigacyjnych w druku

Widok druku SHALL ukrywać elementy interfejsu nawigacyjnego (przyciski, skróty klawiszowe, pasek postępu), które nie należą do treści dokumentu.

#### Scenario: Elementy UI niewidoczne w PDF

- **WHEN** dokument jest wyświetlany w podglądzie druku
- **THEN** przyciski nawigacji, wskazówki klawiaturowe i inne elementy UI są niewidoczne w wydruku

#### Scenario: Treść dokumentu widoczna w PDF

- **WHEN** dokument jest wyświetlany w podglądzie druku
- **THEN** wszystkie slajdy / sekcje infografiki / kategorie cheatsheet są widoczne w wydruku
