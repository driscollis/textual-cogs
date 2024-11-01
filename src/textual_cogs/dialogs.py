# dialogs.py

from . import labels

from textual import on
from textual.app import ComposeResult
from textual.containers import Grid, Center, Vertical, Horizontal
from textual.message import Message
from textual.screen import ModalScreen
from textual.widgets import Button, DirectoryTree, Header, Footer, Input, Label


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


class MessageDialog(ModalScreen):
    DEFAULT_CSS = """
    MessageDialog {
        align: center middle;
        background: $primary-lighten-1 30%;
    }

    #msg-dlg {
        width: 80;
        height: 12;
        border: thick $background 70%;
        content-align: center middle;
    }

    #message-lbl {
        margin-top: 1;
    }

    #msg-dlg-buttons{
        align: center middle;
    }

    Button {
        margin: 1;
        margin-top: 0
    }
    """

    def __init__(
        self, message: str, title: str = "", flags: list | None = None, icon: str = ""
    ) -> None:
        super().__init__()
        self.message = message
        self.title = title
        if flags is None:
            self.flags = []
        else:
            self.flags = flags
        self.buttons = None
        self.icon = icon

        self.verify_flags()

    def compose(self) -> ComposeResult:
        """
        Create the widgets for the MessageDialog's user interface
        """
        buttons = []
        if self.icon:
            message_label = Label(f"{self.icon} {self.message}", id="message-lbl")
        else:
            message_label = Label(self.message, id="message-lbl")
        if "OK" in self.buttons:
            buttons.append(Button("OK", id="ok-btn", variant="primary"))
        if "Cancel" in self.buttons:
            buttons.append(Button("Cancel", id="cancel-btn", variant="error"))
        if "Yes" in self.buttons:
            buttons.append(Button("Yes", id="yes-btn", variant="primary"))
        if "No" in self.buttons:
            buttons.append(Button("No", id="no-btn", variant="error"))

        yield Vertical(
            Header(),
            Center(message_label),
            Center(Horizontal(*buttons, id="msg-dlg-buttons")),
            id="msg-dlg",
        )

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """
        Called when the user presses one of the buttons.

        OK - Returns None (via dismiss callback)
        Cancel and No - Returns False (via dismiss callback)
        Yes - Returns True (via dismiss callback)
        """
        if event.button.id == "ok-btn":
            self.dismiss(None)
        elif event.button.id in ["cancel-btn", "no-btn"]:
            self.dismiss(False)
        else:
            self.dismiss(True)

    def verify_flags(self) -> None:
        """
        Basic verification of the button flags the user sent to create the dialog
        """
        self.buttons = [btn for btn in self.flags]
        button_count = len(self.buttons)

        # Verify buttons
        if button_count > 2:
            raise ValueError(
                f"You cannot have more than two buttons! Found {button_count}"
            )
        elif "OK" in self.buttons and button_count == 2:
            if "Cancel" not in self.buttons:
                raise ValueError(
                    f"OK button can only be paired with Cancel button. Found: {self.buttons}"
                )
        elif "Yes" in self.buttons and button_count == 2:
            if "No" not in self.buttons:
                raise ValueError(
                    f"Yes button can only be paired with No button. Found: {self.buttons}"
                )
        elif button_count == 0:
            # No buttons found, so default to OK button
            self.buttons.append(labels.OK)


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

    def __init__(self, message: str, title: str) -> None:
        super().__init__()
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
