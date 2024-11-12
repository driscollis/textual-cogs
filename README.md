# textual-cogs

A collection of Textual dialogs.

![screenshot](https://github.com/driscollis/textual-cogs/blob/main/images/cog_demo.gif)

Dialogs included so far:

- Generic `MessageDialog` - shows messages to the user
- `SaveFileDialog` - gives the user a way to select a location to save a file
- `SingleChoiceDialog` - gives the user a series of choices to pick from
- `TextEntryDialog` - ask the user a question and get their answer using an `Input` widget

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

When you run this code, you will get something like the following:

![screenshot](https://github.com/driscollis/textual-cogs/blob/main/images/message_dialog.jpg)

### Creating a TextEntryDialog

Here is how you would create a `TextEntryDialog`:

```python
from textual.app import App
from textual.app import App, ComposeResult

from textual_cogs.dialogs import TextEntryDialog


class DialogApp(App):
    def on_mount(self) -> ComposeResult:
        def my_callback(value: str | bool) -> None:
            self.exit()

        self.push_screen(
            TextEntryDialog("What is your name?", "Information"), my_callback
        )


if __name__ == "__main__":
    app = DialogApp()
    app.run()
```

When you run this code, you will see the following:

![screenshot](https://github.com/driscollis/textual-cogs/blob/main/images/text_entry_dialog.jpg)

### Creating a SaveFileDialog

The following code demonstrates how to create a `SaveFileDialog`:

```python
from textual.app import App
from textual.app import App, ComposeResult

from textual_cogs.dialogs import SaveFileDialog


class DialogApp(App):
    def on_mount(self) -> ComposeResult:        
        self.push_screen(SaveFileDialog())

if __name__ == "__main__":
    app = DialogApp()
    app.run()
```

When you run this code, you will see the following:

![screenshot](https://github.com/driscollis/textual-cogs/blob/main/images/save_file_dialog.jpg)
