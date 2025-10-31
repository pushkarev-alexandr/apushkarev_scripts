# Displays the script string associated with the selected Nuke menu item, if available.

# v1.0.0
# created by: Pushkarev Aleksandr

import nuke
from PySide2.QtWidgets import QWidget, QVBoxLayout, QComboBox, QTextEdit

class MenuScriptsViewer(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Menu Scripts Viewer")
        self.setMinimumSize(500, 300)
        
        # Create layout
        self.layout = QVBoxLayout(self)
        
        # List of all comboboxes
        self.comboboxes = []
        
        # Create text field for displaying script
        self.script_text = QTextEdit()
        self.script_text.setReadOnly(True)
        self.script_text.setPlaceholderText("Script will be displayed here...")
        self.layout.addWidget(self.script_text)
        
        # Create the first ComboBox
        base_menus = {n: nuke.menu(n) for n in ["Nuke", "Nodes"]}
        self.create_combobox(base_menus, 0)
        
    def create_combobox(self, items_dict, level):
        """Creates a combobox for the specified level"""
        combobox = QComboBox()
        self.layout.addWidget(combobox)
        self.comboboxes.append(combobox)
        
        # Fill combobox
        for name, item_obj in items_dict.items():
            combobox.addItem(name, item_obj)
        
        # Connect selection change handler
        combobox.currentIndexChanged.connect(lambda: self.on_selection_changed(level))
        
        # If there are items, process the first one immediately
        if combobox.count() > 0:
            self.on_selection_changed(level)
    
    def on_selection_changed(self, level):
        """Handler for combobox selection change"""
        # Remove all comboboxes after the current level
        while len(self.comboboxes) > level + 1:
            cb = self.comboboxes.pop()
            self.layout.removeWidget(cb)
            cb.deleteLater()
        
        # Get the selected item
        current_combobox = self.comboboxes[level]
        selected_item = current_combobox.currentData()
        
        # Check if the item is of type nuke.Menu
        if isinstance(selected_item, nuke.Menu):
            try:
                # Get submenu
                sub_items = selected_item.items()
                if sub_items:
                    sub_items_dict = {i.name(): i for i in sub_items}  # Create dictionary for the next level
                    self.create_combobox(sub_items_dict, level + 1)  # Create new combobox for the next level
                else:
                    self.script_text.clear()  # Empty menu - clear the text field
            except:  # If failed to get items, then it's a final element
                pass
        else:
            self.display_script(selected_item)  # This is nuke.MenuItem - show the script
    
    def display_script(self, menu_item):
        """Displays the result of script() for the menu item"""
        try:
            script_content = menu_item.script()
            if script_content:
                self.script_text.setPlainText(script_content)
            else:
                self.script_text.setPlainText("(empty script)")
        except Exception as e:
            self.script_text.setPlainText(f"Error getting script: {str(e)}")
    
    def get_selected_item(self):
        """Returns the selected object from the last combobox"""
        if self.comboboxes:
            return self.comboboxes[-1].currentData()
        return None

def main():
    window = MenuScriptsViewer()
    window.show()
