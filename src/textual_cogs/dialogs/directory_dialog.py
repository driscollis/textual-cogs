import platform

from textual import on
from textual.app import ComposeResult
from textual.containers import Horizontal, Vertical
from textual.screen import ModalScreen
from textual.widgets import Button, Header, DirectoryTree, Label, Tree


class DirectoryOnlyTree(DirectoryTree):
    """
    Subclass of DirectoryTree that only shows directories.
    """

    def filter_paths(self, paths):
        return [path for path in paths if path.is_dir()]


class DirectoryDialog(ModalScreen[str | bool]):
    # DEFAULT_CSS = """
    # DirectoryDialog {
    #     align: center middle;
    #     background: $primary-lighten-1 30%;
    # }
    # """
    CSS_PATH = "directory_dialog.tcss"

    def __init__(self, root_dir: str = "/", *args: tuple, **kwargs: dict):
        super().__init__(*args, **kwargs)
        self.root_dir = root_dir
        self.folder = root_dir

    def compose(self) -> ComposeResult:
        if "Windows" in platform.platform():
            path_label = "C:\\"
        else:
            path_label = "/"

        yield Vertical(
            Header(),
            DirectoryOnlyTree(self.root_dir, id="directory-tree"),
            Label(f"Folder: {path_label}", id="directory-label"),
            Horizontal(
                Button("Make New Folder", id="make-new-folder", variant="warning"),
                Button("OK", variant="primary", id="directory-ok"),
                Button("Cancel", variant="error", id="directory-cancel"),
                id="directory-buttons",
            ),
            id="directory-dialog",
        )

    def on_mount(self) -> None:
        self.title = "Choose a directory:"

    def _set_folder(self, path: str) -> None:
        """Keep selected folder and label in sync."""
        if path == "/" and "Windows" in platform.platform():
            path = "C:\\"
        else:
            path = str(path)

        self.folder = path
        self.query_one("#directory-label", Label).update(f"Folder: {self.folder}")

    @on(DirectoryTree.DirectorySelected)
    def on_directory_selected(self, event: DirectoryTree.DirectorySelected) -> None:
        """
        Event handler for when a directory is selected in the DirectoryTree.
        """
        self._set_folder(str(event.path))

    @on(Tree.NodeHighlighted, "#directory-tree")
    def on_tree_node_highlighted(self, event: Tree.NodeHighlighted) -> None:
        """DirectoryTree doesn't emit DirectorySelected for the root node (data is None)."""
        if event.node.is_root:
            self._set_folder(self.root_dir)

    @on(Button.Pressed, "#directory-ok")
    def on_ok_button(self, event: Button.Pressed) -> None:
        """
        Event handler for when the OK button is pressed. Dismisses the dialog and returns the selected directory.
        """
        event.stop()
        tree = self.query_one("#directory-tree", DirectoryOnlyTree)
        if tree.cursor_node is not None and tree.cursor_node.is_root:
            self._set_folder(self.root_dir)
        self.dismiss(self.folder)

    @on(Button.Pressed, "#directory-cancel")
    def on_cancel_button(self, event: Button.Pressed) -> None:
        """
        Event handler for when the Cancel button is pressed. Dismisses the dialog and returns False.
        """
        event.stop()
        self.dismiss(False)
