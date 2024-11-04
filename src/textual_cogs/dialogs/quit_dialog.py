# quit_dialog.py

from textual.app import ComposeResult
from textual.screen import ModalScreen
from textual.widgets import Button


class QuitDialog(ModalScreen[bool]):
    """Screen with a dialog to quit."""

    DEFAULT_CSS = """
    QuitDialog {
    align: center middle;
    }

    #dialog {
        grid-size: 2;
        grid-gutter: 1 2;
        grid-rows: 1fr 3;
        padding: 0 1;
        width: 60;
        height: 11;
        border: thick $background 80%;
        background: $surface-lighten-1;
    }

    #question {
        column-span: 2;
        height: 1fr;
        width: 1fr;
        content-align: center middle;
    }

    Button {
        width: 100%;
    }
    """

    def compose(self) -> ComposeResult:
        yield Grid(
            Label("Are you sure you want to quit?", id="question"),
            Button("Quit", variant="error", id="quit"),
            Button("Cancel", variant="primary", id="cancel"),
            id="dialog",
        )

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """
        Called when the user presses a button in the QuitDialog
        """
        if event.button.id == "quit":
            self.dismiss(True)
        else:
            self.dismiss(False)