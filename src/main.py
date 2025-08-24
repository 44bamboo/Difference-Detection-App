from Window.inspection_window import  InspectionWindow

import tkinter as tk
import traceback

# アプリケーションの起動
if __name__ == "__main__":
    root = tk.Tk()
    app = InspectionWindow(root)
    root.mainloop()