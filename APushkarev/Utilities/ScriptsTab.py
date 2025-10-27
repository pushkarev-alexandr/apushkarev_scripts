# Allows you to execute scripts from the top menu using Tab, similar to how nodes are added via Tab


# v1.0.1
# created by: Pushkarev Aleksandr

# Changelog
# v1.0.0 initial release
# v1.0.1 added execution by double-click

# TODO
# - Add selection with mouse and then Enter, not working yet

# Installation:
# Add this line to menu.py:
# nuke.menu('Nuke').addCommand('Scripts Tab', 'import ScriptsTab; ScriptsTab.runScriptsTab()', 'Ctrl+Tab')

import nuke
try:
    from PySide2.QtWidgets import QWidget, QVBoxLayout, QLineEdit, QListWidget, QListWidgetItem
    from PySide2.QtCore import Qt, QEvent, QPoint
    from PySide2 import QtGui
except ImportError:
    from PySide6.QtWidgets import QWidget, QVBoxLayout, QLineEdit, QListWidget, QListWidgetItem
    from PySide6.QtCore import Qt, QEvent, QPoint
    from PySide6 import QtGui

def getMenuItems(menu, items):
    for item in menu.items():
        if isinstance(item, nuke.Menu):
            getMenuItems(item, items)
        elif item.name():
            try:
                item.script()
                if not item.name().startswith('@;'):
                    items[f'{item.name()} [{menu.name()}]'] = item
            except:
                pass

class ScriptsTab(QWidget):
    def __init__(self):
        super().__init__()
        
        self.placed = False
        
        self.resize(500, 150)  # sets the desired widget size
        
        # Main UI elements
        self.layout = QVBoxLayout(self)  # vertical layout
        self.search_box = QLineEdit(self)  # search and text input field
        self.list_widget = QListWidget(self)  # list of available scripts

        # Add items to the list
        self.items = {}
        getMenuItems(nuke.menu('Nuke'), self.items)
        
        for item in self.items:
            QListWidgetItem(item, self.list_widget)

        # Set up filtering
        self.search_box.textChanged.connect(self.filter_list)
        
        # Intercept key events
        self.search_box.installEventFilter(self)

        # Handle double-click
        self.list_widget.itemDoubleClicked.connect(self.execute_selected_item)

        # Add widgets to the main layout
        self.layout.addWidget(self.search_box)
        self.layout.addWidget(self.list_widget)

        # Remove window borders and make background transparent
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        
        self.installEventFilter(self)

    def resizeEvent(self, event):
        """Gui size is now known, so let's position it beneath the Mouse Cursor."""
        super(ScriptsTab, self).resizeEvent(event)
        if not self.placed:  # set position only once in the beginning
            geo = self.frameGeometry()
            centerTo = QtGui.QCursor.pos()
            centerTo -= QPoint(-int(geo.width() * 0.2), -int(geo.height() * 0.36))
            geo.moveCenter(centerTo)
            self.move(geo.topLeft())
            self.placed = True

    def filter_list(self, text):
        for i in range(self.list_widget.count()):
            item = self.list_widget.item(i)
            item.setHidden(text.lower() not in item.text().lower())

    def eventFilter(self, source, event):
        if source == self and event.type() in [QEvent.WindowDeactivate, QEvent.FocusOut]:
            self.close()
            return True
        if source == self.search_box and event.type() == QEvent.KeyPress:
            if event.key() == Qt.Key_Escape:
                self.close()  # Close window on Esc
                return True
            if event.key() in (Qt.Key_Up, Qt.Key_Down):
                current_row = self.list_widget.currentRow()
                direction = -1 if event.key() == Qt.Key_Up else 1
                # Find the next visible item
                next_row = current_row
                while True:
                    next_row += direction
                    if next_row < 0 or next_row >= self.list_widget.count():
                        break  # Out of list bounds
                    if not self.list_widget.item(next_row).isHidden():
                        self.list_widget.setCurrentRow(next_row)
                        break
                return True
            elif event.key() in (Qt.Key_Return, Qt.Key_Enter):
                self.execute_selected_item()
                return True
        return super().eventFilter(source, event)

    def execute_selected_item(self):
        # Get the currently selected item
        current_item = self.list_widget.currentItem()
        if current_item:
            self.items[current_item.text()].invoke()
        self.close()  # Close window

scriptsTabInstance = None

def runScriptsTab():
    global scriptsTabInstance
    scriptsTabInstance = ScriptsTab()
    scriptsTabInstance.show()
