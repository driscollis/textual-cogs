# single_color_picker_dialog.py

from textual._color_constants import COLOR_NAME_TO_RGB
from textual import on
from textual.app import ComposeResult
from textual.containers import Center, Horizontal, Vertical
from textual.screen import ModalScreen
from textual.widgets import Button, Header, Placeholder, Select


class SimpleColorPickerDialog(ModalScreen):
    DEFAULT_CSS = """
    SimpleColorPickerDialog {
        align: center middle;
        background: $primary 30%;

        #simple-color-dlg {
            width: 85;
            height: 18;
            border: thick $background 70%;
            content-align: center middle;
            margin: 1;
        }

        Button {
            width: 50%;
            margin: 1;
        }

        Placeholder {
                    width: 100%;
                    height:5;
                    margin: 1
            }
    }
    """

    def __init__(self) -> None:
        super().__init__()
        self.title = "Color Picker"
        self.current_color = None

    def compose(self) -> ComposeResult:
        colors = list(COLOR_NAME_TO_RGB.keys())
        colors.sort()
        placeholder = Placeholder(
            label="No Color Selected", id="chosen-color", disabled=True
        )
        placeholder.styles.background = None

        yield Vertical(
            Header(),
            Center(Select.from_values(colors, id="simple-color-picker")),
            Center(placeholder),
            Center(
                Horizontal(
                    Button("OK", variant="primary", id="simple-color-ok"),
                    Button("Cancel", variant="error", id="simple-color-cancel"),
                )
            ),
            id="simple-color-dlg",
        )

    @on(Select.Changed, "#simple-color-picker")
    def on_selection_changed(self, event: Select.Changed):
        self.current_color = event.select.value
        self.log.info(f"Selection -> {event.select.value}")
        place = self.query_one("#chosen-color")
        place.styles.background = self.current_color
        place.value = self.current_color

    @on(Button.Pressed, "#simple-color-ok")
    def on_ok(self, event: Button.Pressed) -> None:
        """
        Return the user's choice back to the calling application and dismiss the dialog
        """
        self.dismiss(self.current_color)

    @on(Button.Pressed, "#simple-color-cancel")
    def on_cancel(self, event: Button.Pressed) -> None:
        """
        Returns False to the calling application and dismisses the dialog
        """
        self.dismiss(False)
