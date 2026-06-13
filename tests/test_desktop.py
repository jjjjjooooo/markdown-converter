import tempfile
import unittest
from pathlib import Path
from PIL import Image

from app.desktop import default_output_path, write_markdown_file
from app.desktop import app_icon_path


class DesktopHelperTests(unittest.TestCase):
    def test_default_output_path_uses_source_folder_and_markdown_name(self):
        source = Path("/tmp/Quarterly deck v1.2.pptx")

        self.assertEqual(default_output_path(source), Path("/tmp/Quarterly-deck-v1-2.md"))

    def test_write_markdown_file_writes_utf8_text(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            destination = Path(temp_dir) / "converted.md"

            write_markdown_file(destination, "# Title\n\nConverted text.")

            self.assertEqual(destination.read_text(encoding="utf-8"), "# Title\n\nConverted text.")

    def test_app_icon_path_points_to_png_asset(self):
        icon_path = app_icon_path()

        self.assertEqual(icon_path.name, "markdown-converter-icon.png")
        self.assertTrue(icon_path.is_file())

    def test_app_icon_source_is_4k_square(self):
        with Image.open(app_icon_path()) as icon:
            self.assertEqual(icon.size, (4096, 4096))


if __name__ == "__main__":
    unittest.main()
