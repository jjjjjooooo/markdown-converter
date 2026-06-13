import re
from pathlib import Path
from typing import Callable, Type


DEFAULT_MARKITDOWN = object()
IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png"}


class ConverterDependencyError(RuntimeError):
    """Raised when MarkItDown is not available in the runtime."""


def markdown_download_name(original_name: str) -> str:
    stem = Path(original_name).stem or "converted"
    safe_stem = re.sub(r"[^A-Za-z0-9]+", "-", stem).strip("-")
    return f"{safe_stem or 'converted'}.md"


def image_markdown_reference(path: Path) -> str:
    label = Path(path).stem or "image"
    return f"![{label}]({Path(path).resolve().as_uri()})\n"


def is_image_file(path: Path) -> bool:
    return Path(path).suffix.lower() in IMAGE_EXTENSIONS


def _load_markitdown_class():
    try:
        from markitdown import MarkItDown
    except ImportError as exc:
        raise ConverterDependencyError(
            "MarkItDown is not installed. Run `python3 -m pip install -r requirements.txt`."
        ) from exc

    return MarkItDown


def convert_file_to_markdown(
    path: Path,
    markitdown_cls: object = DEFAULT_MARKITDOWN,
    loader: Callable[[], Type] = _load_markitdown_class,
) -> str:
    if markitdown_cls is None:
        raise ConverterDependencyError(
            "MarkItDown is not installed. Run `python3 -m pip install -r requirements.txt`."
        )
    if markitdown_cls is DEFAULT_MARKITDOWN:
        markitdown_cls = loader()

    converter = markitdown_cls()
    result = converter.convert(str(path))
    markdown = getattr(result, "text_content", "")
    markdown = markdown if markdown is not None else ""
    if not markdown.strip() and is_image_file(path):
        return image_markdown_reference(path)
    return markdown
