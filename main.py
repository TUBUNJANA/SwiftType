# main.py
import tkinter as tk
from ui.gui import TypingTutorApp

if __name__ == "__main__":
    root = tk.Tk()
    app = TypingTutorApp(root)
    root.mainloop()