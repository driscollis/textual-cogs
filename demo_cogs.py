# demo_cogs.py

import platform

from textual_cogs import icons, labels
from textual_cogs.dialogs import MessageDialog, SaveFileDialog
from textual_cogs.dialogs import SingleChoiceDialog, TextEntryDialog

from textual import on
from textual.app import App, ComposeResult
from textual.containers import Center, Vertical
from textual.widgets import Button, TabbedContent, TabPane


class DemoCogsApp(App):

    CSS_PATH = "demo_cogs.tcss"

    def compose(self) -> ComposeResult:
        with TabbedContent(initial="msg-dlgs", id="tabbed"):
            with TabPane("Message Dialogs", id="msg-dlgs"):
                yield Vertical(
                    Center(
                        Button("Info MessageDialog", id="info-msg"),
                        Button("Exclamation MessageDialog", id="exclamation-msg"),
                        Button("Question MessageDialog", id="question-msg"),
                        Button("Warning MessageDialog", id="warning-msg"),
                        Button("Regular MessageDialog", id="regular-msg"),
                    )
                )
            with TabPane("File Dialogs", id="file-dlgs"):
                yield Vertical(Center(Button("SaveFileDialog", id="save-file-dlg")))

            with TabPane("Choice Dialogs", id="choice-dlgs"):
                yield Vertical(
                    Center(
                        Button("SingleChoiceDialog", id="single-choice-dlg"),
                        Button("TextEntryDialog", id="text-entry-dlg"),
                    )
                )

    def msg_dialog_callback(self, button_choice: None | bool) -> None:
        choices = {
            None: "OK",
            True: "Yes",
            False: "No or Cancel",
        }
        self.notify(f"You pressed '{choices[button_choice]}'")

    def save_file_dialog_callback(self, file: str) -> None:
        self.notify(f"Saving file to: '{file}'")

    def single_choice_callback(self, choice: str) -> None:
        severity = "information" if choice == "Python" else "error"
        self.notify(f"You picked: '{choice}'", severity=severity)

    def text_entry_callback(self, entry: str) -> None:
        self.notify(f"You entered: '{entry}'")

    @on(Button.Pressed, "#info-msg")
    def on_info_msg(self, event: Button.Pressed) -> None:
        self.log.info("on_info_msg called!")
        self.push_screen(
            MessageDialog(
                "An informational message",
                title="Information",
                icon=icons.ICON_INFORMATION,
            ),
            self.msg_dialog_callback,
        )

    @on(Button.Pressed, "#exclamation-msg")
    def on_exclamation_msg(self, event: Button.Pressed) -> None:
        self.push_screen(
            MessageDialog("DANGER!", title="Exclamation", icon=icons.ICON_EXCLAMATION),
            self.msg_dialog_callback,
        )

    @on(Button.Pressed, "#question-msg")
    def on_question_msg(self, event: Button.Pressed) -> None:
        self.push_screen(
            MessageDialog(
                "Do you want to save your work?",
                title="Question",
                icon=icons.ICON_QUESTION,
                flags=[labels.YES, labels.NO],
            ),
            self.msg_dialog_callback,
        )

    @on(Button.Pressed, "#warning-msg")
    def on_warning_msg(self, event: Button.Pressed) -> None:
        self.push_screen(
            MessageDialog(
                "This is only a warning!", title="Warning", icon=icons.ICON_WARNING
            ),
            self.msg_dialog_callback,
        )

    @on(Button.Pressed, "#regular-msg")
    def on_regular_msg(self, event: Button.Pressed) -> None:
        self.push_screen(
            MessageDialog(
                "Do you want to continue?",
                title="Regular",
                flags=[labels.OK, labels.CANCEL],
            ),
            self.msg_dialog_callback,
        )

    @on(Button.Pressed, "#save-file-dlg")
    def on_save_file_dialog(self, event: Button.Pressed) -> None:
        if "Windows" in platform.platform():
            self.push_screen(SaveFileDialog(root="C:/"), self.save_file_dialog_callback)
        else:
            self.push_screen(SaveFileDialog(), self.save_file_dialog_callback)

    @on(Button.Pressed, "#single-choice-dlg")
    def on_single_choice_dialog(self, event: Button.Pressed) -> None:
        choices = ["Python", "PHP", "C++", "Ruby", "Lua"]
        self.push_screen(
            SingleChoiceDialog(
                "What is your favorite language?",
                title="Choose Language",
                choices=choices,
            ),
            self.single_choice_callback,
        )

    @on(Button.Pressed, "#text-entry-dlg")
    def on_text_entry_dialog(self, event: Button.Pressed) -> None:
        self.push_screen(
            TextEntryDialog("Enter your favorite food:", title="Question"),
            self.text_entry_callback,
        )


if __name__ == "__main__":
    app = DemoCogsApp()
    app.run()
