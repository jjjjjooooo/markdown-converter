# Markdown Converter

A local desktop app for converting documents to Markdown with Microsoft MarkItDown.

## Setup

```bash
brew install python-tk@3.13
python3.13 -c 'import tkinter'
python3.13 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
```

Use Python 3.10 or newer with Tkinter support. MarkItDown requires Python 3.10+, and on Homebrew Python the Tkinter extension is installed separately with `python-tk@3.13`. If the Tkinter check fails, install a Tk-capable Python, remove the old `.venv`, and run the setup commands again.

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
