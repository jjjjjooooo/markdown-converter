import tempfile
import unittest
from pathlib import Path

from app.converter import (
    DEFAULT_MARKITDOWN,
    ConverterDependencyError,
    convert_file_to_markdown,
    markdown_download_name,
)


class FakeResult:
    def __init__(self, text):
        self.text_content = text


class FakeMarkItDown:
    def convert(self, path):
        return FakeResult(f"converted:{Path(path).name}")


class LoaderBackedMarkItDown:
    def __call__(self):
        return FakeMarkItDown()


class ConverterTests(unittest.TestCase):
    def test_markdown_download_name_replaces_extension_and_unsafe_characters(self):
        self.assertEqual(markdown_download_name("Quarterly deck v1.2.pptx"), "Quarterly-deck-v1-2.md")

    def test_convert_file_to_markdown_uses_supplied_markitdown_class(self):
        with tempfile.NamedTemporaryFile(suffix=".txt") as source:
            markdown = convert_file_to_markdown(Path(source.name), markitdown_cls=FakeMarkItDown)

        self.assertEqual(markdown, f"converted:{Path(source.name).name}")

    def test_convert_file_to_markdown_reports_missing_dependency(self):
        with tempfile.NamedTemporaryFile(suffix=".txt") as source:
            with self.assertRaises(ConverterDependencyError) as error:
                convert_file_to_markdown(Path(source.name), markitdown_cls=None)

        self.assertIn("markitdown", str(error.exception).lower())

    def test_convert_file_to_markdown_calls_default_loader_before_converting(self):
        def fake_loader():
            return FakeMarkItDown

        with tempfile.NamedTemporaryFile(suffix=".txt") as source:
            markdown = convert_file_to_markdown(
                Path(source.name),
                markitdown_cls=DEFAULT_MARKITDOWN,
                loader=fake_loader,
            )

        self.assertEqual(markdown, f"converted:{Path(source.name).name}")


if __name__ == "__main__":
    unittest.main()
