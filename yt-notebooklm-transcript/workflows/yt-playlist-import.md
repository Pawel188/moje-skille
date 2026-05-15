---
description: Import filmów z playlisty YouTube do NotebookLM z automatycznym śledzeniem
---

# YouTube Playlist → NotebookLM Import

## Kiedy użyć

Gdy użytkownik chce zaimportować filmy z playlisty YouTube jako źródła do NotebookLM.

## Wymagania

- `yt-dlp` zainstalowane (`which yt-dlp`)
- `notebooklm` zalogowane (`notebooklm auth check --test`)
- Aktywny notatnik ustawiony (`notebooklm use <id>`) lub podany jako parametr

## Workflow

### 1. Przygotowanie notatnika

Jeśli użytkownik nie podał notatnika, sprawdź aktualny:
```bash
/home/pawel/projekty/notebooklm-py/.venv/bin/notebooklm status
```

Jeśli trzeba stworzyć nowy:
```bash
/home/pawel/projekty/notebooklm-py/.venv/bin/notebooklm create "<tytuł>"
/home/pawel/projekty/notebooklm-py/.venv/bin/notebooklm use <id>
```

### 2. Dry-run (podgląd)

Najpierw pokaż co zostanie zaimportowane:
```bash
// turbo
/home/pawel/projekty/notebooklm-py/.venv/bin/python3 \
    ~/.gemini/antigravity/skills/notebooklm-py/scripts/yt_playlist_import.py \
    --playlist "<URL_PLAYLISTY>" \
    --notebooklm /home/pawel/projekty/notebooklm-py/.venv/bin/notebooklm \
    --yt-dlp /home/pawel/projekty/notebooklm-py/.venv/bin/yt-dlp \
    --cookies-from-browser chrome \
    --dry-run
```

### 3. Import

Po zatwierdzeniu przez użytkownika, uruchom import:
```bash
/home/pawel/projekty/notebooklm-py/.venv/bin/python3 \
    ~/.gemini/antigravity/skills/notebooklm-py/scripts/yt_playlist_import.py \
    --playlist "<URL_PLAYLISTY>" \
    --notebooklm /home/pawel/projekty/notebooklm-py/.venv/bin/notebooklm \
    --yt-dlp /home/pawel/projekty/notebooklm-py/.venv/bin/yt-dlp \
    --cookies-from-browser chrome \
    --delay 3
```

**Opcjonalnie z konkretnym notatnikiem:**
```bash
/home/pawel/projekty/notebooklm-py/.venv/bin/python3 \
    ~/.gemini/antigravity/skills/notebooklm-py/scripts/yt_playlist_import.py \
    --playlist "<URL_PLAYLISTY>" \
    --notebook "<NOTEBOOK_ID>" \
    --notebooklm /home/pawel/projekty/notebooklm-py/.venv/bin/notebooklm \
    --yt-dlp /home/pawel/projekty/notebooklm-py/.venv/bin/yt-dlp \
    --cookies-from-browser chrome \
    --delay 3
```

### 4. Sprawdzenie bazy importów

Baza śledzenia jest w `~/.notebooklm/yt_imports.json`. Aby sprawdzić:
```bash
// turbo
cat ~/.notebooklm/yt_imports.json | python3 -m json.tool
```

## Ważne informacje

- Skrypt **automatycznie pomija** filmy, które zostały już zaimportowane
- Baza **zapisuje się po każdym filmie** — bezpieczne w razie przerwania
- **Rate limiting**: domyślnie 3s między importami, aby nie obciążać API
- Baza śledzi: playlistę źródłową, indeks w playliście, datę importu, source_id
- Przy ponownym uruchomieniu z tą samą playlistą, zaimportowane zostaną **tylko nowe filmy**
