import tkinter as tk

import traceback
from functools import wraps

def show_on_error(function):
    "関数実行中に例外が発生したら、showerrorするデコレータ"
    @wraps(function)
    def show_error(*args,**kwargs):
        try:
            function(*args,**kwargs)
        except Exception as e:
            print(traceback.format_exc())
            title = e.__class__.__name__
            message = traceback.format_exc(limit=0)
            tk.messagebox.showerror(f"{title}",
                                 f"{message}")
    return show_error