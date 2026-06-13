# Markdown Converter

A local desktop app for converting documents to Markdown with Microsoft MarkItDown.

## Setup

```bash
python3 -c 'import tkinter'
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
```

Use a Python build with Tkinter support. On macOS, the Python installer from python.org includes Tkinter. If the first setup command fails, install a Tk-capable Python, remove the old `.venv`, and run the setup commands again.

## Run

Double-click:

```text
Markdown Converter.app
```

or:

```text
Start Markdown Converter.command
```

When using `Start Markdown Converter.command`, the desktop window opens directly. Close the Markdown Converter window to quit.

Command-line option:

```bash
.venv/bin/python -m app.desktop
```

## Use

Choose a supported document, convert it, preview or edit the Markdown, then copy it or save a `.md` file.
