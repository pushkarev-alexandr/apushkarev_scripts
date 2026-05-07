# Shows the recent projects in a list and allows to open them by clicking on the item or using the number shortcut

# v1.0.0
# created by: Pushkarev Aleksandr

import os
from pathlib import Path

from PySide6 import QtCore, QtGui, QtWidgets
import nuke


RECENT_FILES_PATH = Path.home() / ".nuke" / "recent_files"
MAX_ITEMS = 9
FOLDERS_TO_SHOW_IN_LIST = 2
WINDOW_STYLE = """
    QDialog {
        background-color: #2b2b2b;
        border: 1px solid #3a3a3a;
        border-radius: 8px;
    }
    QListWidget {
        background-color: #232323;
        border: 1px solid #3a3a3a;
        border-radius: 6px;
        padding: 6px;
        outline: none;
        color: #d8d8d8;
    }
    QListWidget::item {
        height: 28px;
        padding: 4px 8px;
        border-radius: 4px;
    }
    QListWidget::item:hover {
        background: #3a3a3a;
    }
    QListWidget::item:selected {
        background: #505050;
        color: #ffffff;
    }
    QToolTip {
        background-color: #1d1d1d;
        color: #efefef;
        border: 1px solid #5a5a5a;
        padding: 4px 6px;
    }
"""


class ProjectItemDelegate(QtWidgets.QStyledItemDelegate):
    def paint(self, painter, option, index):
        painter.save()

        style = option.widget.style() if option.widget else QtWidgets.QApplication.style()
        style.drawPrimitive(QtWidgets.QStyle.PrimitiveElement.PE_PanelItemViewItem, option, painter, option.widget)

        number = str(index.data(QtCore.Qt.ItemDataRole.UserRole + 1) or "")
        label = str(index.data(QtCore.Qt.ItemDataRole.UserRole + 2) or "")

        number_rect = QtCore.QRect(option.rect)
        number_rect.setLeft(option.rect.left() + 10)
        number_rect.setWidth(22)

        text_rect = QtCore.QRect(option.rect)
        text_rect.setLeft(number_rect.right() + 8)
        text_rect.setRight(option.rect.right() - 8)

        number_color = QtGui.QColor("#9ea3aa") if not (option.state & QtWidgets.QStyle.StateFlag.State_Selected) else QtGui.QColor("#d3d7de")
        path_color = QtGui.QColor("#bcc1c8") if not (option.state & QtWidgets.QStyle.StateFlag.State_Selected) else QtGui.QColor("#e7eaef")
        file_color = QtGui.QColor("#dee2e8") if not (option.state & QtWidgets.QStyle.StateFlag.State_Selected) else QtGui.QColor("#f7f8fb")

        number_font = QtGui.QFont(option.font)
        number_font.setBold(False)
        painter.setFont(number_font)
        painter.setPen(number_color)
        painter.drawText(number_rect, QtCore.Qt.AlignmentFlag.AlignVCenter | QtCore.Qt.AlignmentFlag.AlignLeft, number)

        folder_prefix, sep, file_name = label.rpartition("/")

        text_font = QtGui.QFont(option.font)
        text_font.setBold(False)
        metrics = QtGui.QFontMetrics(text_font)

        x = text_rect.left()
        y = text_rect.top()
        h = text_rect.height()

        if sep:
            folder_text = f"{folder_prefix}/"
            painter.setFont(text_font)
            painter.setPen(path_color)
            painter.drawText(
                QtCore.QRect(x, y, text_rect.width(), h),
                QtCore.Qt.AlignmentFlag.AlignVCenter | QtCore.Qt.AlignmentFlag.AlignLeft,
                folder_text,
            )
            x += metrics.horizontalAdvance(folder_text)
        else:
            file_name = label

        file_font = QtGui.QFont(option.font)
        file_font.setBold(False)
        file_font.setWeight(QtGui.QFont.Weight.DemiBold)
        painter.setFont(file_font)
        painter.setPen(file_color)
        painter.drawText(
            QtCore.QRect(x, y, max(0, text_rect.right() - x), h),
            QtCore.Qt.AlignmentFlag.AlignVCenter | QtCore.Qt.AlignmentFlag.AlignLeft,
            file_name,
        )

        painter.restore()

    def sizeHint(self, option, index):
        size = super().sizeHint(option, index)
        size.setHeight(max(size.height(), 30))
        return size


class RecentProjectsWindow(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Recent Nuke Projects")
        self.resize(420, 360)
        self.setWindowFlag(QtCore.Qt.WindowType.FramelessWindowHint, True)
        self.setWindowFlag(QtCore.Qt.WindowType.Tool, True)
        self.setStyleSheet(WINDOW_STYLE)

        self.list_widget = QtWidgets.QListWidget()
        self.list_widget.itemClicked.connect(self.open_selected_project)
        self.list_widget.setSpacing(3)
        self.list_widget.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.list_widget.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.list_widget.setItemDelegate(ProjectItemDelegate(self.list_widget))

        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.addWidget(self.list_widget)

        self._number_shortcuts = []
        self._setup_number_shortcuts()
        self._populate_recent_projects()

    def focusOutEvent(self, event):
        super().focusOutEvent(event)
        self.close()

    def _setup_number_shortcuts(self):
        for index in range(MAX_ITEMS):
            shortcut = QtGui.QShortcut(QtGui.QKeySequence(str(index + 1)), self)
            shortcut.activated.connect(lambda idx=index: self.open_project_by_index(idx))
            self._number_shortcuts.append(shortcut)

    def _populate_recent_projects(self):
        self.list_widget.clear()

        if not RECENT_FILES_PATH.exists():
            QtWidgets.QMessageBox.warning(
                self,
                "File not found",
                f"Recent files list not found:\n{RECENT_FILES_PATH}",
            )
            return

        with RECENT_FILES_PATH.open("r", encoding="utf-8") as file:
            recent_paths = [line.strip() for line in file if line.strip()]

        for index, project_path in enumerate(recent_paths[:MAX_ITEMS], start=1):
            project_label = self._format_project_label(project_path)
            item = QtWidgets.QListWidgetItem("")
            item.setData(QtCore.Qt.ItemDataRole.UserRole, project_path)
            item.setData(QtCore.Qt.ItemDataRole.UserRole + 1, str(index))
            item.setData(QtCore.Qt.ItemDataRole.UserRole + 2, project_label)
            item.setToolTip(project_path)
            self.list_widget.addItem(item)

        self._fit_window_to_items()

    def _format_project_label(self, project_path):
        file_name = Path(project_path).name
        folders_count = max(0, FOLDERS_TO_SHOW_IN_LIST)
        if folders_count == 0:
            return file_name

        parent_parts = list(Path(project_path).parts[:-1])
        tail_folders = parent_parts[-folders_count:] if parent_parts else []
        if not tail_folders:
            return file_name

        folders_path = "/".join(tail_folders)
        return f"{folders_path}/{file_name}"

    def _fit_window_to_items(self):
        row_count = max(self.list_widget.count(), MAX_ITEMS)
        row_height = max(self.list_widget.sizeHintForRow(0), 28)
        spacing_height = max(0, row_count - 1) * self.list_widget.spacing()

        contents_margins = self.list_widget.contentsMargins()
        margins_height = contents_margins.top() + contents_margins.bottom()
        frame_height = self.list_widget.frameWidth() * 2
        # Extra safety for DPI/style rounding so the last row is never clipped.
        safety_padding = 18

        list_height = (
            (row_count * row_height)
            + spacing_height
            + margins_height
            + frame_height
            + safety_padding
        )

        self.list_widget.setFixedHeight(list_height)
        self.setFixedSize(420, list_height + 24)

    def open_project_by_index(self, index):
        if index < 0 or index >= self.list_widget.count():
            return
        item = self.list_widget.item(index)
        self.open_selected_project(item)

    def open_selected_project(self, item=None):
        if item is None:
            item = self.list_widget.currentItem()
        if item is None:
            return

        project_path = item.data(QtCore.Qt.ItemDataRole.UserRole)

        if not os.path.exists(project_path):
            QtWidgets.QMessageBox.warning(
                self,
                "Missing file",
                f"File does not exist:\n{project_path}",
            )
            return

        nuke.scriptOpen(project_path)
        self.accept()


def openRecentProject():
    window = RecentProjectsWindow()
    window.show()
    window.raise_()
    window.activateWindow()
    window.setFocus(QtCore.Qt.FocusReason.ActiveWindowFocusReason)
    return window
