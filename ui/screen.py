import tkinter as tk
from tkinter import ttk

from .view_model import IngredientLinkingViewModel

class IngredientLinkingScreen(ttk.Frame):
    def __init__(self, parent, db):
        super().__init__(parent)
        self.vm = IngredientLinkingViewModel(db)

        self.vendor_items = []
        self.selected_vendor_item = None
        self.suggestions = []

        self._build_ui()
        self._load_vendor_items()

    def _build_ui(self):
        self.pack(fill="both", expand=True)

        self.left = ttk.Frame(self)
        self.left.pack(side="left", fill="y")

        self.right = ttk.Frame(self)
        self.right.pack(side="right", fill="both", expand=True)

        self.vendor_list = tk.Listbox(self.left, width=40)
        self.vendor_list.pack(fill="y", expand=True)
        self.vendor_list.bind("<<ListboxSelect>>", self.on_vendor_select)

        self.match_list = tk.Listbox(self.right)
        self.match_list.pack(fill="both", expand=True)

        self.link_btn = ttk.Button(
            self.right,
            text="Link Selected",
            command=self.link_selected
        )
        self.link_btn.pack(pady=10)

    def _load_vendor_items(self):
        self.vendor_items = self.vm.load_unlinked_items()
        self.vendor_list.delete(0, tk.END)

        for item in self.vendor_items:
            label = f"{item.vendor_sku} - {item.vendor_description}"
            self.vendor_list.insert(tk.END, label)
        
    def on_vendor_select(self, event):
        index = self.vendor_list.curselection()
        if not index:
            return
        
        self.selected_vendor_item = self.vendor_items[index[0]]
        self._load_suggestions()

    def _load_suggestions(self):
        self.match_list.delete(0, tk.END)
        self.suggestions = self.vm.get_suggestions(self.selected_vendor_item)

        for match in self.suggestions:
            ingredient = match["ingredient"]
            score = match["score"]
            self.match_list.insert(
                tk.END,
                f"{ingredient.name} (score {score})"
            )
    
    def link_selected(self):
        index = self.match_list.curselection()
        if not index:
            return
        
        match = self.suggestions[index[0]]
        ingredient = match["ingredient"]
        confidence = match["score"]

        self.vm.link(
            self.selected_vendor_item,
            ingredient,
            confidence
        )

        self._load_vendor_items()
        self.match_list.delete(0, tk.END)