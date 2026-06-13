import json
import mimetypes
import tempfile
from email import policy
from email.parser import BytesParser
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import unquote

from app.converter import ConverterDependencyError, convert_file_to_markdown, markdown_download_name


ROOT = Path(__file__).resolve().parent.parent
STATIC_DIR = ROOT / "static"


class MarkdownConverterHandler(BaseHTTPRequestHandler):
    server_version = "MarkdownConverter/1.0"

    def do_GET(self):
        if self.path == "/" or self.path.startswith("/?"):
            self._send_file(STATIC_DIR / "index.html")
            return

        requested = unquote(self.path.split("?", 1)[0]).lstrip("/")
        self._send_file(STATIC_DIR / requested)

    def do_HEAD(self):
        if self.path == "/" or self.path.startswith("/?"):
            self._send_file(STATIC_DIR / "index.html", include_body=False)
            return

        requested = unquote(self.path.split("?", 1)[0]).lstrip("/")
        self._send_file(STATIC_DIR / requested, include_body=False)

    def do_POST(self):
        if self.path != "/api/convert":
            self._send_json({"error": "Not found"}, HTTPStatus.NOT_FOUND)
            return

        try:
            result = self._handle_conversion()
        except ConverterDependencyError as exc:
            self._send_json({"error": str(exc)}, HTTPStatus.SERVICE_UNAVAILABLE)
            return
        except ValueError as exc:
            self._send_json({"error": str(exc)}, HTTPStatus.BAD_REQUEST)
            return
        except Exception:
            self._send_json(
                {"error": "The file could not be converted. Try another file or check the format."},
                HTTPStatus.INTERNAL_SERVER_ERROR,
            )
            return

        self._send_json(result)

    def _handle_conversion(self):
        content_type = self.headers.get("content-type", "")
        if not content_type.startswith("multipart/form-data"):
            raise ValueError("Upload a file before converting.")

        content_length = int(self.headers.get("content-length", "0"))
        body = self.rfile.read(content_length)
        message = BytesParser(policy=policy.default).parsebytes(
            f"Content-Type: {content_type}\r\nMIME-Version: 1.0\r\n\r\n".encode("utf-8") + body
        )
        upload = next(
            (
                part
                for part in message.iter_parts()
                if part.get_param("name", header="content-disposition") == "file"
            ),
            None,
        )
        if upload is None or not upload.get_filename():
            raise ValueError("Choose a file to convert.")

        original_name = Path(upload.get_filename()).name
        suffix = Path(original_name).suffix
        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as temp_file:
            temp_path = Path(temp_file.name)
            temp_file.write(upload.get_payload(decode=True) or b"")

        try:
            markdown = convert_file_to_markdown(temp_path)
        finally:
            temp_path.unlink(missing_ok=True)

        return {
            "markdown": markdown,
            "downloadName": markdown_download_name(original_name),
            "sourceName": original_name,
        }

    def _send_file(self, path, include_body=True):
        resolved = path.resolve()
        if not str(resolved).startswith(str(STATIC_DIR.resolve())) or not resolved.is_file():
            self._send_json({"error": "Not found"}, HTTPStatus.NOT_FOUND)
            return

        content_type = mimetypes.guess_type(resolved.name)[0] or "application/octet-stream"
        data = resolved.read_bytes()
        self.send_response(HTTPStatus.OK)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        if include_body:
            self.wfile.write(data)

    def _send_json(self, payload, status=HTTPStatus.OK):
        data = json.dumps(payload).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def log_message(self, format, *args):
        return


def run(host="127.0.0.1", port=8000):
    server = ThreadingHTTPServer((host, port), MarkdownConverterHandler)
    print(f"Markdown converter running at http://{host}:{port}")
    server.serve_forever()


if __name__ == "__main__":
    run()
