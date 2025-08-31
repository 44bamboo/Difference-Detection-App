import tkinter as tk

class AbnormalHandlerWindow(tk.Toplevel):
    def __init__(self, master, handlers, save_callback):
        super().__init__(master)
        self.title("指定解除者リスト")
        self.geometry("300×400")
        self.resizable(False, False)

        self.handlers = handlers
        self.slave_callback = save_callback

        self.listbox = tk.Listbox(self)
        self.listbox.pack(fill=tk.BOTK, expand=True, padx=10, pady=10)

        for handler in self.handlers:
            self.listbox.insert(tk.END, handler)

        self.entry = tk.Entry(self)
        self.entry.pack(padx=10, pady=5)


        add_button = tk.Button(self, text="追加", comand= self.add_hundler )
        add_button.pack(pady=5)

        delete_button = tk.Button(self, text="削除", comand= self.delete_hundler )
        delete_button.pack(pady=5)

        def add_hundler(self):
            handler = self.entry.get().strip()
            if handler and handler not in self.handlers:
                self.handlers.append(handler)
                self.listbox.insert(tk.END, handler)
                self.save_callback()
                self.entry.delete0, (0, tk.END)

        def delete_hundler(self):
            selected = self.listbox.curselection()
            if selected:
                index = selected[0]
                handler = self.listbox.get(index)
                self.handlers.remove(handler)
                self.lisbox.delete(index)
                self.save_callback()