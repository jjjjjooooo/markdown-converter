import tempfile
import unittest
from pathlib import Path

from app.desktop import default_output_path, write_markdown_file


class DesktopHelperTests(unittest.TestCase):
    def test_default_output_path_uses_source_folder_and_markdown_name(self):
        source = Path("/tmp/Quarterly deck v1.2.pptx")

        self.assertEqual(default_output_path(source), Path("/tmp/Quarterly-deck-v1-2.md"))

    def test_write_markdown_file_writes_utf8_text(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            destination = Path(temp_dir) / "converted.md"

            write_markdown_file(destination, "# Title\n\nConverted text.")

            self.assertEqual(destination.read_text(encoding="utf-8"), "# Title\n\nConverted text.")


if __name__ == "__main__":
    unittest.main()
