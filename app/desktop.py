from pathlib import Path
from typing import Optional

from app.converter import ConverterDependencyError, convert_file_to_markdown, markdown_download_name


tk = None
filedialog = None
messagebox = None
ttk = None

SUPPORTED_FILE_TYPES = (
    ("Documents", "*.pdf *.docx *.pptx *.xlsx *.xls *.csv *.txt *.html *.htm *.md"),
    ("All files", "*.*"),
)

APP_ROOT = Path(__file__).resolve().parent.parent
HEADER_ICON_DISPLAY_SIZE = 64


def default_output_path(source_path: Path) -> Path:
    return source_path.with_name(markdown_download_name(source_path.name))


def write_markdown_file(destination: Path, markdown: str) -> None:
    destination.write_text(markdown, encoding="utf-8")


def app_icon_path() -> Path:
    return APP_ROOT / "assets" / "markdown-converter-icon.png"


def header_icon_subsample_factor(source_size: int) -> int:
    return max(1, source_size // HEADER_ICON_DISPLAY_SIZE)


def load_tkinter():
    global filedialog, messagebox, tk, ttk

    if tk is not None:
        return

    try:
        import tkinter as loaded_tk
        from tkinter import filedialog as loaded_filedialog
        from tkinter import messagebox as loaded_messagebox
        from tkinter import ttk as loaded_ttk
    except ImportError as exc:
        raise RuntimeError(
            "Tkinter is not available for this Python. Install a Python build with Tk support, "
            "then recreate .venv and reinstall requirements."
        ) from exc

    tk = loaded_tk
    filedialog = loaded_filedialog
    messagebox = loaded_messagebox
    ttk = loaded_ttk


class MarkdownConverterApp:
    def __init__(self, root):
        load_tkinter()
        self.root = root
        self.source_path: Optional[Path] = None
        self.markdown = ""
        self.output_path: Optional[Path] = None

        self.source_var = tk.StringVar(value="No file selected")
        self.status_var = tk.StringVar(value="Choose a document to convert.")

        self._configure_root()
        self._build_ui()

    def _configure_root(self) -> None:
        self.root.title("Markdown Converter")
        self.root.geometry("980x680")
        self.root.minsize(760, 520)
        self._set_window_icon()

        style = ttk.Style()
        if "aqua" in style.theme_names():
            style.theme_use("aqua")
        style.configure("Primary.TButton", padding=(14, 8))
        style.configure("Toolbar.TButton", padding=(10, 7))
        style.configure("Status.TLabel", foreground="#52606d")

    def _set_window_icon(self) -> None:
        icon_path = app_icon_path()
        if not icon_path.is_file():
            return

        try:
            self.icon_image = tk.PhotoImage(file=str(icon_path))
            self.root.iconphoto(True, self.icon_image)
        except tk.TclError:
            self.icon_image = None

    def _header_icon(self):
        icon_path = app_icon_path()
        if not icon_path.is_file():
            return None

        try:
            icon = tk.PhotoImage(file=str(icon_path))
            factor = header_icon_subsample_factor(icon.width())
            self.header_icon_image = icon.subsample(factor, factor)
        except tk.TclError:
            self.header_icon_image = None
        return self.header_icon_image

    def _build_ui(self) -> None:
        container = ttk.Frame(self.root, padding=20)
        container.grid(row=0, column=0, sticky="nsew")
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)

        container.columnconfigure(0, weight=1)
        container.rowconfigure(2, weight=1)

        title_bar = ttk.Frame(container)
        title_bar.grid(row=0, column=0, sticky="w")

        header_icon = self._header_icon()
        if header_icon is not None:
            icon_label = ttk.Label(title_bar, image=header_icon)
            icon_label.grid(row=0, column=0, sticky="w", padx=(0, 12))

        title = ttk.Label(title_bar, text="Markdown Converter", font=("Helvetica Neue", 22, "bold"))
        title.grid(row=0, column=1, sticky="w")

        file_bar = ttk.Frame(container)
        file_bar.grid(row=1, column=0, sticky="ew", pady=(16, 12))
        file_bar.columnconfigure(1, weight=1)

        choose_button = ttk.Button(file_bar, text="Choose File", command=self.choose_file, style="Primary.TButton")
        choose_button.grid(row=0, column=0, sticky="w")

        source_label = ttk.Label(file_bar, textvariable=self.source_var)
        source_label.grid(row=0, column=1, sticky="ew", padx=(12, 12))

        self.convert_button = ttk.Button(
            file_bar,
            text="Convert",
            command=self.convert_selected_file,
            style="Primary.TButton",
        )
        self.convert_button.grid(row=0, column=2, sticky="e")

        preview_frame = ttk.Frame(container)
        preview_frame.grid(row=2, column=0, sticky="nsew")
        preview_frame.columnconfigure(0, weight=1)
        preview_frame.rowconfigure(0, weight=1)

        self.preview = tk.Text(
            preview_frame,
            wrap="word",
            undo=True,
            font=("Menlo", 13),
            padx=14,
            pady=14,
            borderwidth=1,
            relief="solid",
        )
        self.preview.grid(row=0, column=0, sticky="nsew")

        scrollbar = ttk.Scrollbar(preview_frame, orient="vertical", command=self.preview.yview)
        scrollbar.grid(row=0, column=1, sticky="ns")
        self.preview.configure(yscrollcommand=scrollbar.set)

        footer = ttk.Frame(container)
        footer.grid(row=3, column=0, sticky="ew", pady=(12, 0))
        footer.columnconfigure(0, weight=1)

        status = ttk.Label(footer, textvariable=self.status_var, style="Status.TLabel")
        status.grid(row=0, column=0, sticky="w")

        actions = ttk.Frame(footer)
        actions.grid(row=0, column=1, sticky="e")

        ttk.Button(actions, text="Copy", command=self.copy_markdown, style="Toolbar.TButton").grid(
            row=0, column=0, padx=(0, 8)
        )
        ttk.Button(actions, text="Save As", command=self.save_markdown, style="Toolbar.TButton").grid(
            row=0, column=1, padx=(0, 8)
        )
        ttk.Button(actions, text="Clear", command=self.clear, style="Toolbar.TButton").grid(row=0, column=2)

    def choose_file(self) -> None:
        selected = filedialog.askopenfilename(title="Choose a document", filetypes=SUPPORTED_FILE_TYPES)
        if not selected:
            return

        self.source_path = Path(selected)
        self.output_path = default_output_path(self.source_path)
        self.source_var.set(str(self.source_path))
        self.status_var.set("Ready to convert.")

    def convert_selected_file(self) -> None:
        if self.source_path is None:
            messagebox.showinfo("Choose a file", "Choose a document before converting.")
            return

        self._set_busy(True)
        self.status_var.set("Converting...")
        self.root.update_idletasks()

        try:
            markdown = convert_file_to_markdown(self.source_path)
        except ConverterDependencyError as exc:
            messagebox.showerror("Missing dependency", str(exc))
            self.status_var.set("Install dependencies and try again.")
        except Exception:
            messagebox.showerror(
                "Conversion failed",
                "The file could not be converted. Try another file or check the format.",
            )
            self.status_var.set("Conversion failed.")
        else:
            self._set_markdown(markdown)
            self.status_var.set(f"Converted {self.source_path.name}.")
        finally:
            self._set_busy(False)

    def copy_markdown(self) -> None:
        markdown = self._current_markdown()
        if not markdown:
            messagebox.showinfo("Nothing to copy", "Convert a document or enter Markdown before copying.")
            return

        self.root.clipboard_clear()
        self.root.clipboard_append(markdown)
        self.status_var.set("Markdown copied to the clipboard.")

    def save_markdown(self) -> None:
        markdown = self._current_markdown()
        if not markdown:
            messagebox.showinfo("Nothing to save", "Convert a document or enter Markdown before saving.")
            return

        initial_path = self.output_path or Path.home() / "converted.md"
        selected = filedialog.asksaveasfilename(
            title="Save Markdown",
            defaultextension=".md",
            filetypes=(("Markdown", "*.md"), ("Text", "*.txt"), ("All files", "*.*")),
            initialdir=str(initial_path.parent),
            initialfile=initial_path.name,
        )
        if not selected:
            return

        destination = Path(selected)
        write_markdown_file(destination, markdown)
        self.output_path = destination
        self.status_var.set(f"Saved {destination.name}.")

    def clear(self) -> None:
        self.source_path = None
        self.markdown = ""
        self.output_path = None
        self.source_var.set("No file selected")
        self.preview.delete("1.0", tk.END)
        self.status_var.set("Choose a document to convert.")

    def _set_markdown(self, markdown: str) -> None:
        self.markdown = markdown
        self.preview.delete("1.0", tk.END)
        self.preview.insert("1.0", markdown)

    def _current_markdown(self) -> str:
        return self.preview.get("1.0", tk.END).rstrip("\n")

    def _set_busy(self, busy: bool) -> None:
        state = "disabled" if busy else "normal"
        self.convert_button.configure(state=state)
        self.root.configure(cursor="watch" if busy else "")


def main() -> None:
    load_tkinter()
    root = tk.Tk()
    MarkdownConverterApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
