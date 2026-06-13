# Markdown Converter

A local split-workbench web app for converting documents to Markdown with Microsoft MarkItDown.

## Setup

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
```

## Run

Double-click:

```text
Markdown Converter.app
```

or:

```text
Start Markdown Converter.command
```

When using `Start Markdown Converter.command`, leave the Terminal window open while you use the converter. Close that window or press Control-C to stop the server.

To stop a server that is already running on port 8000, double-click:

```text
Stop Markdown Converter.command
```

Command-line option:

```bash
.venv/bin/python -m app.server
```

Then open:

```text
http://127.0.0.1:8000
```

## Use

Drop or choose a supported document, convert it, preview the Markdown, then copy or download the `.md` file.
