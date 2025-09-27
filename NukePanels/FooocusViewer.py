# Panel for Fooocus, displays images generated through Fooocus

# v1.0.0
# created by: Pushkarev Aleksandr

import nuke
if nuke.NUKE_VERSION_MAJOR < 16:
    from PySide2.QtWidgets import (
        QWidget,
        QLabel,
        QPushButton,
        QGridLayout,
        QScrollArea,
        QVBoxLayout,
        QComboBox,
        QHBoxLayout,
    )
    from PySide2.QtGui import QPixmap
    from PySide2.QtCore import Qt, Signal
else:
    from PySide6.QtWidgets import (
        QWidget,
        QLabel,
        QPushButton,
        QGridLayout,
        QScrollArea,
        QVBoxLayout,
        QComboBox,
        QHBoxLayout,
    )
    from PySide6.QtGui import QPixmap
    from PySide6.QtCore import Qt, Signal
import os

# Change this variable to the path where your Fooocus program stores outputs.
BASE_FOLDER_PATH = "Z:/Programs/ML/Fooocus/Fooocus/outputs"

class ClickableLabel(QLabel):
    """
    A QLabel class that can emit a signal on double-click.
    The signal sends the file path associated with this widget.
    """
    doubleClicked = Signal(str)

    def __init__(self, file_path, parent=None):
        super().__init__(parent)
        self.file_path = file_path

    def mouseDoubleClickEvent(self, event):
        """
        Overrides the mouse double-click event.
        """
        # Emit the signal if the click was with the left mouse button
        if event.button() == Qt.MouseButton.LeftButton:
            self.doubleClicked.emit(self.file_path)
        super().mouseDoubleClickEvent(event)

class ImageGallery(QWidget):
    """
    Widget for displaying an image gallery from a specified folder.
    """
    
    def __init__(self):
        super().__init__()
        self.base_folder = BASE_FOLDER_PATH
        self.init_ui()

    def init_ui(self):
        """
        Initializes the user interface.
        """
        self.setWindowTitle("Fooocus Image Gallery")
        self.setGeometry(100, 100, 1200, 800)

        main_layout = QVBoxLayout(self)

        top_layout = QHBoxLayout()

        # Create a dropdown list for selecting folders
        self.folder_combo = QComboBox(self)
        top_layout.addWidget(self.folder_combo)

        # Create the "Update" button
        self.refresh_button = QPushButton("Update", self)
        self.refresh_button.setToolTip("Update the list of images in the current folder")
        top_layout.addWidget(self.refresh_button)

        main_layout.addLayout(top_layout)

        scroll_area = QScrollArea(self)
        scroll_area.setWidgetResizable(True)
        main_layout.addWidget(scroll_area)

        scroll_content_widget = QWidget()
        scroll_area.setWidget(scroll_content_widget)

        self.grid_layout = QGridLayout(scroll_content_widget)

        self.folder_combo.currentTextChanged.connect(self.on_folder_changed)
        self.refresh_button.clicked.connect(self.refresh_current_folder)
        self.populate_folders()

    def refresh_current_folder(self):
        """
        Refreshes the contents of the currently selected folder,
        re-calling on_folder_changed.
        """
        self.on_folder_changed(self.folder_combo.currentText())

    def populate_folders(self):
        """
        Finds all subfolders in the base directory and adds them to the dropdown list.
        """
        self.folder_combo.blockSignals(True)  # Block signals to avoid triggering on_folder_changed
        self.folder_combo.clear()

        if not os.path.isdir(self.base_folder):
            print(f"Error: Base folder not found: {self.base_folder}")
            self.folder_combo.blockSignals(False)
            return

        try:
            # Get a list of all items in the folder and filter to keep only directories
            subfolders = [
                f for f in os.listdir(self.base_folder)
                if os.path.isdir(os.path.join(self.base_folder, f))
            ]
            # Sort folders in reverse order (newest first)
            subfolders.sort(reverse=True)

            if subfolders:
                self.folder_combo.addItems(subfolders)
            else:
                self.folder_combo.addItem("No folders found")
                self.folder_combo.setEnabled(False)

        except OSError as e:
            print(f"Error reading folder: {e}")
            self.folder_combo.addItem("Error reading folder")
            self.folder_combo.setEnabled(False)

        self.folder_combo.blockSignals(False)  # Unblock signals
        # Explicitly call the handler for the first folder in the list
        if self.folder_combo.count() > 0 and self.folder_combo.isEnabled():
            self.on_folder_changed(self.folder_combo.currentText())

    def on_folder_changed(self, folder_name):
        """
        Called when a new folder is selected in the QComboBox.
        Loads images from the selected folder.
        """
        if not folder_name or folder_name in ["No folders found", "Error reading folder"]:
            self.clear_grid_layout()
            return

        full_path = os.path.join(self.base_folder, folder_name)
        self.load_images(full_path)

    def clear_grid_layout(self):
        """
        Removes all widgets from the grid layout.
        """
        while self.grid_layout.count():
            child = self.grid_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

    def load_images(self, folder_path):
        """
        Loads and displays all PNG images from the specified folder.
        """
        self.clear_grid_layout()  # Clear the gallery before loading new images

        if not os.path.isdir(folder_path):
            error_label = QLabel(f"Error: Folder not found\n{folder_path}")
            error_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.grid_layout.addWidget(error_label, 0, 0)
            return

        try:
            image_files = [
                f
                for f in os.listdir(folder_path)
                if f.lower().endswith(".png")
            ]
        except OSError as e:
            error_label = QLabel(f"Error reading folder: {e}")
            error_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.grid_layout.addWidget(error_label, 0, 0)
            return

        if not image_files:
            no_files_label = QLabel(
                f"No images with .png extension found in folder\n{folder_path}"
            )
            no_files_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.grid_layout.addWidget(no_files_label, 0, 0)
            return

        columns = 3
        row, col = 0, 0

        for image_file in sorted(image_files, reverse=True):
            file_path = os.path.join(folder_path, image_file)
            pixmap = QPixmap(file_path)

            if pixmap.isNull():
                print(f"Failed to load: {file_path}")
                continue

            # Use our new ClickableLabel instead of a regular QLabel
            image_label = ClickableLabel(file_path)
            # Connect its signal to the handler function
            image_label.doubleClicked.connect(self.create_read)

            scaled_pixmap = pixmap.scaled(
                250, 250,
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation,
            )
            image_label.setPixmap(scaled_pixmap)
            image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            # Update the tooltip
            image_label.setToolTip(f"{image_file}\n(Double-click for full size)")

            self.grid_layout.addWidget(image_label, row, col)

            col += 1
            if col >= columns:
                col = 0
                row += 1

    def create_read(self, file_path):
        read = nuke.createNode("Read", inpanel=False)
        read["file"].fromUserText(file_path)
        read["colorspace"].setValue("Output - sRGB")
