# textual-cogs

A collection of Textual dialogs.

Dialogs included so far:

- Generic `MessageDialog` - shows messages to the user
- `SaveFileDialog` - gives the user a way to select a location to save a file
- `TextEntryDialog` - Ask the user a question and get their answer using an `Input` widget

## Installation

You can install `textual-cog` using pip:

```
python -m pip install textual-cog
```

You also need [Textual](https://github.com/Textualize/textual) to run these dialogs.

## Example Usage

Here is an example of creating a small application that opens the `MessageDialog` immediately. You would normally open the dialog in response to a message or event that has occurred, such as when the application has an error or you need to tell the user something.

```python
from textual.app import App
from textual.app import App, ComposeResult
from textual.widgets import Static

from textual_cogs.dialogs import MessageDialog
from textual_cogs import icons


class DialogApp(App):
    def on_mount(self) -> ComposeResult:
        def my_callback(value: None | bool) -> None:
            self.exit()

        self.push_screen(
            MessageDialog(
                "What is your favorite language?",
                icon=icons.ICON_QUESTION,
                title="Warning",
            ),
            my_callback,
        )


if __name__ == "__main__":
    app = DialogApp()
    app.run()
```