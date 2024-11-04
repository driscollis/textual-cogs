# message_dialog.py

from textual_cogs import labels

from textual.app import ComposeResult
from textual.containers import Center, Horizontal, Vertical
from textual.screen import ModalScreen
from textual.widgets import Button, Header, Label


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
