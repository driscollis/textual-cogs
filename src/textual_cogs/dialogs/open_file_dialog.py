# open_file_dialog.py

import os
from fnmatch import fnmatch
from pathlib import Path
from collections.abc import Iterable

from textual import on
from textual.app import ComposeResult
from textual.containers import Horizontal, Vertical
from textual.screen import ModalScreen
from textual.widgets import Button, DirectoryTree, Header, Input, Label, Select


class FilterableDirectoryTree(DirectoryTree):
    def __init__(self, path: str, *, file_pattern: str = "*.*", **kwargs):
        super().__init__(path, **kwargs)
        self.file_pattern = file_pattern

    def set_filter(self, pattern: str) -> None:
        self.file_pattern = pattern or "*.*"
        self.reload()

    def filter_paths(self, paths: Iterable[Path]) -> Iterable[Path]:
        pattern = self.file_pattern.strip()

        # Treat *.* as "show everything"
        if pattern in {"", "*", "*.*"}:
            return paths

        # Accept ".py" as shorthand
        if pattern.startswith("."):
            pattern = f"*{pattern}"

        return [path for path in paths if path.is_dir() or fnmatch(path.name, pattern)]


class OpenFileDialog(ModalScreen):
    DEFAULT_CSS = """
    OpenFileDialog {
    align: center middle;
    background: $primary 30%;
    }

    #save_dialog{
        width: 50%;
        height: 25;
        border: thick $background 70%;
        background: $surface-lighten-1;
        Button {
            width: 50%;
            margin: 1;
        }
    }

    Horizontal {
        height: auto;
    }

    Label {
        margin: 1;
    }

    FilterableDirectoryTree {
        margin: 1;
    }

    Input {
        margin: 1;
    }

    #open_file {
        background: green;
    }
    """

    def __init__(
        self,
        root="/",
        name: str | None = None,
        file_types: list[tuple[str, str]] | None = None,
        id: str | None = None,
        classes: str | None = None,
    ) -> None:
        super().__init__(name, id, classes)
        self.title = "Choose a File"
        self.root = root
        self.folder = root
        if file_types is None:
            self.file_types = [
                ("Python source (*.py)", "*.py"),
                ("All files (*.*)", "*.*"),
            ]
        else:
            self.file_types = file_types

    def compose(self) -> ComposeResult:
        """
        Create the widgets for the SaveFileDialog's user interface
        """
        yield Header()
        yield Vertical(
            Label(f"Folder name: {self.root}", id="folder"),
            FilterableDirectoryTree(self.root, file_pattern="*.*", id="directory"),
            Input(placeholder="File name", id="filename"),
            Select(self.file_types, value="*.*", prompt="All files", id="file_filter"),
            Horizontal(
                Button("Open", variant="primary", id="open_file"),
                Button("Cancel", variant="error", id="cancel_file"),
                id="save_btn_row",
            ),
            id="save_dialog",
        )

    def on_mount(self) -> None:
        """
        Focus the input widget so the user can name the file
        """
        self.query_one("#filename").focus()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """
        Event handler for when the load file button is pressed
        """
        event.stop()
        if event.button.id == "open_file":
            filename = self.query_one("#filename").value
            full_path = os.path.join(self.folder, filename)
            self.dismiss(full_path)
        else:
            self.dismiss(False)

    @on(Select.Changed, "#file_filter")
    def on_filter_changed(self, event: Select.Changed) -> None:
        tree = self.query_one(FilterableDirectoryTree)
        value = event.value
        if not isinstance(value, str):
            value = "*.*"
        tree.set_filter(value)

    @on(DirectoryTree.DirectorySelected)
    def on_directory_selection(self, event: DirectoryTree.DirectorySelected) -> None:
        self.folder = str(event.path)
        self.query_one("#folder").update(f"Folder name: {self.folder}")

    @on(DirectoryTree.FileSelected)
    def on_file_selected(self, event: DirectoryTree.FileSelected) -> None:
        self.folder = str(event.path.parent)
        self.query_one("#folder").update(f"Folder name: {self.folder}")
        self.query_one("#filename", Input).value = event.path.name
