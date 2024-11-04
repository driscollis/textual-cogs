# save_dialog.py

from textual.app import ComposeResult
from textual.containers import Grid
from textual.screen import ModalScreen
from textual.widgets import Button, DirectoryTree, Header, Input, Label

class SaveFileDialog(ModalScreen):
    DEFAULT_CSS = """
    SaveFileDialog {
    align: center middle;
    background: $primary 30%;
    }

    #save_dialog{
        grid-size: 1 5;
        grid-gutter: 1 2;
        grid-rows: 5% 55% 15% 20%;
        padding: 0 1;
        width: 100;
        height: 25;
        border: thick $background 70%;
        background: $surface-lighten-1;
    }

    #save_file {
        background: green;
    }
    """

    class Selected(Message):
        """
        File selected message
        """

        def __init__(self, filename: str) -> None:
            self.filename = filename
            super().__init__()

    def __init__(self) -> None:
        super().__init__()
        self.title = "Save File"
        self.root = "/"

    def compose(self) -> ComposeResult:
        """
        Create the widgets for the SaveFileDialog's user interface
        """
        yield Grid(
            Header(),
            Label(f"Folder name: {self.root}", id="folder"),
            DirectoryTree(self.root, id="directory"),
            Input(placeholder="filename.txt", id="filename"),
            Button("Save File", variant="primary", id="save_file"),
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
        filename = self.query_one("#filename").value
        self.post_message(self.Selected(filename))

    @on(DirectoryTree.DirectorySelected)
    def on_directory_selection(self, event: DirectoryTree.DirectorySelected) -> None:
        """
        Called when the DirectorySelected message is emitted from the DirectoryTree
        """
        self.query_one("#folder").update(f"Folder name: {event.path}")