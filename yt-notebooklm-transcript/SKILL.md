---
name: yt-notebooklm-transcript
description: "Use when extracting YouTube video transcripts via NotebookLM — creates a temporary notebook, imports the video, retrieves the full transcript, saves as markdown, and cleans up."
---

# YouTube Transcript via NotebookLM

## Overview

Extract full transcripts from YouTube videos using Google NotebookLM as the processing engine. Creates a temporary notebook, imports the video, retrieves the indexed transcript, saves it as markdown, and deletes the temporary notebook. NotebookLM handles transcript extraction automatically, including for videos where standard transcript APIs may fail.

## When to Use

- User provides a YouTube link and asks for a transcript, summary, or analysis
- User wants to extract text content from a YouTube video
- Standard transcript APIs fail (private/unlisted videos, missing captions)
- User wants the NotebookLM-processed version of the transcript

## Workflow

### Step 1: Create temporary notebook

```bash
// turbo
/home/pawel/projekty/notebooklm-py/.venv/bin/notebooklm create "YT Temp - <video title or ID>"
```

Save the notebook ID from output (format: `Created notebook: <ID> - <title>`).

### Step 2: Add YouTube video as source

```bash
/home/pawel/projekty/notebooklm-py/.venv/bin/notebooklm source add "<YOUTUBE_URL>" -n <NOTEBOOK_ID>
```

Save the source ID from output (format: `Added source: <ID>`).

### Step 3: Wait for processing

NotebookLM needs a moment to process the video. Wait for the source to be ready:

```bash
// turbo
/home/pawel/projekty/notebooklm-py/.venv/bin/notebooklm source wait <SOURCE_ID> -n <NOTEBOOK_ID> --timeout 120
```

### Step 4: Get transcript

```bash
// turbo
/home/pawel/projekty/notebooklm-py/.venv/bin/notebooklm source fulltext <SOURCE_ID> -n <NOTEBOOK_ID> -o /tmp/yt_transcript.txt
```

### Step 5: Read and process the transcript

Read the transcript file and perform whatever the user asked for (summarize, analyze, translate, etc.):

```bash
// turbo
cat /tmp/yt_transcript.txt
```

If the user wants the transcript saved as markdown, create a properly formatted file:

```markdown
# <Video Title>

**Source:** <YouTube URL>
**Extracted:** <date>

---

<transcript content>
```

### Step 6: Cleanup — delete temporary notebook

```bash
/home/pawel/projekty/notebooklm-py/.venv/bin/notebooklm use <NOTEBOOK_ID>
/home/pawel/projekty/notebooklm-py/.venv/bin/notebooklm delete -y
```

And remove the temp file:
```bash
// turbo
rm -f /tmp/yt_transcript.txt
```

### Authentication (If Session Expires)

If the NotebookLM session expires (commands return auth errors), the user needs to re-authenticate manually since it requires a browser context:

```bash
/home/pawel/projekty/notebooklm-py/.venv/bin/notebooklm login
```
Ask the user to run this command in their terminal and follow the browser prompts.

## Important Notes

- **Temporary notebook**: Always delete after use to keep the account clean
- **Processing time**: YouTube sources take ~10-30 seconds to process
- **Transcript quality**: NotebookLM processes the audio track, so transcripts may differ from YouTube's auto-captions
- **If user wants to KEEP the notebook**: Skip step 6, inform the user about the notebook ID
- **Multiple videos**: If user provides multiple URLs, consider using the existing `notebooklm-py` skill's full workflow instead of creating/deleting temporary notebooks for each
