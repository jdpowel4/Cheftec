import tkinter as tk
from tkinter import ttk
import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), 'Cheftec_0_3.db')

# --------------------
# GUI
# --------------------
class Cheftec(tk.Tk):
	def __init__(self):
		super().__init__()
		self.title("Cheftec 0.3")
		self.geometry('600x800')
		self.state('zoomed')

		menu = MenuBar(self)
		self.config(menu = menu)

		self.create_widget()

	def  create_widget(self):
		notebook = ttk.Notebook(self)
		notebook.pack(fill = 'both', expand = True)

		self.inventory_frame = InventoryFrame(notebook)

		notebook.add(self.inventory_frame, text = "Inventory")

# --------------------
# Menu Setup
# --------------------
class MenuBar(tk.Menu):
	def __init__(self, parent):
		super().__init__(parent)

		# Initalize Menu Bar
		menu_main = tk.Menu(self, tearoff = False)
		menu_main_new = tk.Menu(self, tearoff = False)
		menu_main_open = tk.Menu(self, tearoff = False)
		menu_view = tk.Menu(self, tearoff = False)
		self.add_cascade(label = "Cheftec", menu = menu_main)
		self.add_cascade(label = "View", menu = menu_view)

		# Adding Sub-Menus to Main Menu
		menu_main.add_cascade(label = "New", menu = menu_main_new)
		menu_main.add_cascade(label = "Open", menu = menu_main_open)

		# Adding Menu Items
		menu_main_new.add_command(label = "Inventory Item")
		menu_main_new.add_command(label = "Invoice")
		menu_main_new.add_command(label = "Recipe")
		menu_main_new.add_command(label = "Menu")
		menu_main_new.add_separator()
		menu_main_new.add_command(label = "Vendor")
		menu_main_new.add_command(label = "Unit")
		menu_main_open.add_command(label = "Inventory")
		menu_main_open.add_command(label = "Inventory Locations")
		menu_main_open.add_command(label = "Invoices")
		menu_main_open.add_command(label = "Par Levels")
		menu_main_open.add_command(label = "Conversions")
		menu_main_open.add_command(label = "Global Conversions")
		menu_main_open.add_separator()
		menu_main_open.add_command(label = "Recipes")
		menu_view.add_command(label = "Restore", command = lambda: parent.state('normal'))
		menu_view.add_command(label = "Minimize", command = lambda: parent.state('iconic'))
		menu_view.add_command(label = "Maximize", command = lambda: parent.state('zoomed'))
		menu_view.add_command(label = "Close", command = parent.destroy)

# --------------------
# Inventory Frame
# --------------------
class InventoryFrame(ttk.Frame):
	def __init__(self, parent):
		super().__init__(parent)
		self.build_ui()

	def build_ui(self):
		toolbar = ttk.Frame(self)
		toolbar.pack(fill = 'x', padx = 5, pady = 5)
		ttk.Button(toolbar, text = "New Inventory Item", command = self.add_ingredent).pack(side = 'left')
		ttk.Button(toolbar, text = "Edit Inventory Item", command = self.edit_ingredent).pack(side = 'left')
		ttk.Button(toolbar, text = "Delete Inventory Item", command = self.delete_ingredent).pack(side = 'left')
		ttk.Button(toolbar, text = "Take Inventory", command = self.take_inventory).pack(side = 'left')
		ttk.Button(toolbar, text = "Add Item Sales", command = self.add_sales).pack(side = 'left')

		sidebar = tk.Frame(self, width = 150, bg = 'white', relief = 'groove', borderwidth = 2)
		sidebar.pack(fill = 'y', side = 'left', padx = 5, pady = 5)

		columns = ("Location", "Name", "QOH", "Unit", "Cost", "Par")
		self.tree = ttk.Treeview(self, columns = columns, show = 'headings')
		for col in columns:
			self.tree.heading(col, text = col.title())
			self.tree.column(col, anchor = 'center', width = 150)
		self.tree.pack(fill = 'both', expand = True, padx = 5, pady = 5)

	def load_ingredents(self):
		return

	def add_ingredent(self):
		ingredent = IngredentEditor(self)
		self.wait_window(ingredent)
		return

	def edit_ingredent(self):
		return

	def delete_ingredent(self):
		return

	def take_inventory(self):
		return

	def add_sales(self):
		return


class IngredentEditor(tk.Toplevel):
	def __init__(self, parent, item = None):
		super().__init__(parent)
		self.title(f"Ingredent Editor: {item}")
		self.build_ui(item)

	def build_ui(self, item):
		s = ttk.Style()
		s.configure("TNotebook", tabposition='s')

		name = ttk.Frame(self)
		name.pack(fill = 'y', expand = True, padx = 5, pady = 5)
		ttk.Label(name, text = "Name: ").pack(side = 'left')
		self.name = ttk.Entry(name, width = 30)
		self.name.pack(side = 'left', padx = 5, pady = 5)
		notebook = ttk.Notebook(self, style = "TNotebook")
		notebook.pack(fill = 'both', expand = True, side = 'bottom')

		self.item_info = IngEdtGen(notebook)
		notebook.add(self.item_info, text = "General")

class IngEdtGen(ttk.Frame):
	def __init__(self, parent):
		super().__init__(parent)

		
		

# --------------------
# Main Program
# --------------------
def main():
	app = Cheftec()
	app.mainloop()

if __name__ == "__main__":
	main()
