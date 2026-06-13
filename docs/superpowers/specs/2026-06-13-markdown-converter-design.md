# Markdown Converter Design

## Goal

Build a local web app that converts an uploaded document to Markdown using Microsoft MarkItDown, then lets the user preview, copy, and download the generated `.md` file.

## Product Shape

The app uses the selected split workbench layout:

- Left side: file drop/upload, selected file details, conversion button, and status.
- Right side: Markdown preview with copy and download buttons.
- The download button saves the latest converted Markdown as a `.md` file.

The visual style should be streamlined and pragmatic: dense enough to feel like a real tool, quiet in color, strong typography, visible states, and no marketing-style landing page.

## Architecture

The app is a local Python web server using only the standard library for HTTP routing, static file delivery, multipart upload parsing, and JSON responses. Conversion is isolated in `app/converter.py`, which wraps `markitdown.MarkItDown` behind a small function that can be tested independently.

The browser submits a file to `POST /api/convert`. The server writes the upload to a temporary file, converts it with MarkItDown, returns Markdown plus a safe suggested filename, and then removes the temporary file.

## Error Handling

If MarkItDown is not installed, the API returns a clear dependency error telling the user to install project requirements. Invalid or empty uploads return a user-facing error. Unexpected converter failures return a concise message without exposing stack traces in the UI.

## Testing

Unit tests cover filename sanitization, dependency-missing behavior, and conversion wrapper behavior with a fake MarkItDown class. This keeps the core behavior verified without requiring real document fixtures or network access.
