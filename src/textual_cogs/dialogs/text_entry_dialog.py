# text_entry_dialog

from textual import on
from textual.app import ComposeResult
from textual.containers import Center, Horizontal, Vertical
from textual.screen import ModalScreen
from textual.widgets import Button, Header, Input, Label


class TextEntryDialog(ModalScreen):
    """
    Display a dialog that allows the user to enter some text and return it
    """

    DEFAULT_CSS = """
    TextEntryDialog {
        align: center middle;
        background: $primary-lighten-1 30%;
    }

    #text-entry-dlg {
        width: 80;
        height: 14;
        border: thick $background 70%;
        content-align: center middle;
        margin: 1;
    }

    #text-entry-label {
        margin: 1;
    }

    Button {
        width: 50%;
        margin: 1;
    }
    """

    def __init__(
        self,
        message: str,
        title: str,
        name: str | None = None,
        id: str | None = None,
        classes: str | None = None,
    ) -> None:
        super().__init__(name, id, classes)
        self.message = message
        self.title = title

    def compose(self) -> ComposeResult:
        """
        Create the widgets for the TextEntryDialog's user interface
        """
        yield Vertical(
            Header(),
            Center(Label(self.message, id="text-entry-label")),
            Input(placeholder="", id="answer"),
            Center(
                Horizontal(
                    Button("OK", variant="primary", id="text-entry-ok"),
                    Button("Cancel", variant="error", id="text-entry-cancel"),
                )
            ),
            id="text-entry-dlg",
        )

    def on_mount(self) -> None:
        """
        Set the focus on the input widget by default when the dialog is loaded
        """
        self.query_one("#answer").focus()

    @on(Button.Pressed, "#text-entry-ok")
    def on_ok(self, event: Button.Pressed) -> None:
        """
        Return the user's entry back to the calling application and dismiss the dialog
        """
        answer = self.query_one("#answer").value
        self.dismiss(answer)

    @on(Button.Pressed, "#text-entry-cancel")
    def on_cancel(self, event: Button.Pressed) -> None:
        """
        Returns False to the calling application and dismisses the dialog
        """
        self.dismiss(False)
