# demo_cogs.py

import platform

from textual_cogs import icons, labels
from textual_cogs.dialogs import MessageDialog,  SaveFileDialog

from textual import on
from textual.app import App, ComposeResult
from textual.containers import Center, Vertical
from textual.widgets import Button, TabbedContent, TabPane


class DemoCogsApp(App):
    def compose(self) -> ComposeResult:
        with TabbedContent(initial="msg-dlgs"):
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
                yield Vertical(
                    Center(
                        Button("SaveFileDialog", id="save-file-dlg")
                    )
                )

    def msg_dialog_callback(self, button_choice):
        choices = {
            None: "OK",
            True: "Yes",
            False: "No or Cancel",
        }
        self.notify(f"You pressed '{choices[button_choice]}'")

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
        self.push_screen(SaveFileDialog())
        #if "Windows" in platform.platform():
            #self.push_screen(SaveFileDialog(root="C:"))
        #else:
            #self.push_screen(SaveFileDialog())


if __name__ == "__main__":
    app = DemoCogsApp()
    app.run()