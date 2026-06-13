# Markdown Converter Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a local split-workbench Markdown converter powered by MarkItDown.

**Architecture:** A Python standard-library HTTP server serves a static frontend and exposes `POST /api/convert`. Conversion logic lives in a small testable module that imports MarkItDown lazily and returns Markdown text plus a safe download filename.

**Tech Stack:** Python 3, standard-library `http.server`, browser HTML/CSS/JS, Microsoft `markitdown`, `unittest`.

---

## File Structure

- `app/converter.py`: conversion wrapper, filename helpers, MarkItDown dependency handling.
- `app/server.py`: local HTTP server, static file serving, upload endpoint.
- `static/index.html`: split workbench UI.
- `static/styles.css`: pragmatic polished interface styling.
- `static/app.js`: upload, convert, preview, copy, and download behavior.
- `tests/test_converter.py`: unit tests for converter behavior.
- `requirements.txt`: MarkItDown dependency.
- `README.md`: setup and run instructions.

## Tasks

- [ ] Add failing converter unit tests for safe filenames, missing dependency errors, and fake conversion.
- [ ] Implement `app/converter.py` until tests pass.
- [ ] Add the HTTP server with `/api/convert` and static file handling.
- [ ] Add the split-workbench frontend with upload, convert, preview, copy, and download.
- [ ] Add README, requirements, and `.gitignore`.
- [ ] Run unit tests and a syntax check.
- [ ] Start the local server and verify the UI loads.

## Self-Review

The plan covers all requested v1 behavior, including the middle split-workbench layout and the added download button. No placeholders or deferred behavior remain.
