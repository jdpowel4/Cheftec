import tkinter as tk
from sqlalchemy.orm import sessionmaker

from core.database import engine
from ui.screen import IngredientLinkingScreen

Session = sessionmaker(bind=engine)

def main():
    root = tk.Tk()
    root.title("Ingredient Linking")

    db = Session()

    screen = IngredientLinkingScreen(root, db)
    screen.pack(fill="both", expand=True)

    root.mainloop()

if __name__ == "__main__":
    main()
