# single_choice_dialog.py

from textual import on
from textual.app import ComposeResult
from textual.containers import Center, Horizontal, Vertical
from textual.screen import ModalScreen
from textual.widgets import Button, Header, Label, OptionList


class SingleChoiceDialog(ModalScreen):
    DEFAULT_CSS = """
    SingleChoiceDialog {
        align: center middle;
        background: $primary 30%;

        #single-choice-dlg {
            width: 85;
            height: 18;
            border: thick $background 70%;
            content-align: center middle;
            margin: 1;
        }

        #single-choice-label {
            margin: 1;
        }

        Button {
            width: 50%;
            margin: 1;
        }
    }
    """

    def __init__(
        self,
        message: str,
        title: str,
        choices: list[str],
        name: str | None = None,
        id: str | None = None,
        classes: str | None = None,
    ) -> None:
        super().__init__(name, id, classes)
        self.message = message
        self.title = title
        self.choices = choices
        self.current_option = None

    def compose(self) -> ComposeResult:
        """
        Create the widgets for the SingleChoiceDialog's user interface
        """
        yield Vertical(
            Header(),
            Center(Label(self.message, id="single-choice-label")),
            OptionList(*self.choices, id="single-choice-answer"),
            Center(
                Horizontal(
                    Button("OK", variant="primary", id="single-choice-ok"),
                    Button("Cancel", variant="error", id="single-choice-cancel"),
                )
            ),
            id="single-choice-dlg",
        )

    @on(OptionList.OptionHighlighted)
    @on(OptionList.OptionSelected)
    def on_option_selected(
        self, event: OptionList.OptionHighlighted | OptionList.OptionSelected
    ) -> None:
        """
        Update the currently selected option when the user highlights or selects
        an item in the OptionList
        """
        self.current_option = event.option.prompt

    @on(Button.Pressed, "#single-choice-ok")
    def on_ok(self, event: Button.Pressed) -> None:
        """
        Return the user's choice back to the calling application and dismiss the dialog
        """
        self.dismiss(self.current_option)

    @on(Button.Pressed, "#single-choice-cancel")
    def on_cancel(self, event: Button.Pressed) -> None:
        """
        Returns False to the calling application and dismisses the dialog
        """
        self.dismiss(False)
