---
name: git-usage
description:  Ten skill tłumaczy w jaki sposób pracować z gitem
---

# Skill: git-usage

Skill do obsługi git w projekcie Slides Generator — konwencje commitów, workflow i dobre praktyki.

Rób commita po każdym nowym featurze lub innej większej zmianie

## Konwencje commitów

Używaj formatu **Conventional Commits**:

```
<type>(<scope>): <short description>

[optional body]

Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>
```

### Typy commitów
| Typ | Kiedy używać |
|-----|-------------|
| `feat` | Nowa funkcjonalność |
| `fix` | Naprawa błędu |
| `style` | Zmiany CSS/wyglądu bez logiki |
| `refactor` | Refaktoryzacja bez zmiany zachowania |
| `docs` | Zmiany dokumentacji |
| `chore` | Konfiguracja, zależności, buildy |

### Scope'y projektu
- `slides` — funkcje związane z prezentacjami
- `infographic` — infografiki
- `cheatsheet` — cheatsheety
- `server` — serwer Python
- `ui` — ogólne zmiany interfejsu

## Workflow

1. `git status` — sprawdź co jest zmienione
2. Dodaj konkretne pliki (`git add <plik>`, nie `git add .`)
3. `git diff --staged` — przejrzyj zmiany przed commitem
4. Commit z opisową wiadomością
5. Nigdy nie pushuj bezpośrednio do `main` bez review

## Checklist przed commitem
- [ ] Nie ma plików z sekretami (.env, klucze API)
- [ ] Zmiany są logicznie powiązane (jeden temat per commit)
- [ ] Wiadomość commita opisuje *dlaczego*, nie tylko *co*
