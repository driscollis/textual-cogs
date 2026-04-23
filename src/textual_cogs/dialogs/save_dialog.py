# save_dialog.py

import os
from pathlib import Path

from textual import on
from textual.app import ComposeResult
from textual.containers import Horizontal, Vertical
from textual.screen import ModalScreen
from textual.widgets import Button, DirectoryTree, Header, Input, Label


class SaveFileDialog(ModalScreen[str | bool]):
    DEFAULT_CSS = """
    SaveFileDialog {
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

    DirectoryTree {
        margin: 1;
    }

    Input {
        margin: 1;
    }

    #save_file {
        background: green;
    }
    """

    def __init__(
        self,
        root: Path = Path("/"),
        name: str | None = None,
        id: str | None = None,
        classes: str | None = None,
    ) -> None:
        super().__init__(name, id, classes)
        self.title = "Save File"
        self.root = root
        self.folder = root

    def compose(self) -> ComposeResult:
        """
        Create the widgets for the SaveFileDialog's user interface
        """
        yield Header()
        yield Vertical(
            Label(f"Folder name: {self.root}", id="folder"),
            DirectoryTree(self.root, id="directory"),
            Input(placeholder="filename.txt", id="filename"),
            Horizontal(
                Button("Save File", variant="primary", id="save_file"),
                Button("Cancel", variant="error", id="cancel_file"),
                id="save_btn_row",
            ),
            id="save_dialog",
        )

    def on_mount(self) -> None:
        """
        Focus the input widget so the user can name the file
        """
        self.query_one("#filename", Input).focus()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """
        Event handler for when the load file button is pressed
        """
        event.stop()
        if event.button.id == "save_file":
            filename = self.query_one("#filename", Input).value
            full_path = os.path.join(self.folder, filename)
            self.dismiss(full_path)
        else:
            self.dismiss(False)

    @on(DirectoryTree.DirectorySelected)
    def on_directory_selection(self, event: DirectoryTree.DirectorySelected) -> None:
        """
        Called when the DirectorySelected message is emitted from the DirectoryTree
        """
        self.folder = event.path
        self.query_one("#folder", Label).update(f"Folder name: {self.folder}")
