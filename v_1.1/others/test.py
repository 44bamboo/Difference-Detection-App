# import tkinter as tk

# def on_modified(e):
#     print(e)
#     e.widget.edit_modified(False)  # フラグをオフにする事で、毎回呼ばれるようにする。

# root = tk.Tk()
# text = tk.Text(root)
# text.bind("<<Modified>>", on_modified)
# text.pack()
# root.mainloop()







# import tkinter as tk

# def is_number(s):
#     return s.isdigit()

# root = tk.Tk()
# validate_command = root.register(is_number)
# entry = tk.Entry(root, validate="key", validatecommand=(validate_command, '%P'))
# entry.pack()
# root.mainloop()

# import tkinter as tk

# # Create the main window
# root = tk.Tk()
# root.geometry("300x200")

# # Configure row behavior
# root.grid_rowconfigure(0, weight=1)  # Row 0 grows proportionally
# root.grid_rowconfigure(1, weight=2)  # Row 1 grows twice as much as Row 0
# root.grid_rowconfigure(2, weight=1, minsize=50)  # Row 2 has a minimum height of 50px

# # Add widgets
# tk.Label(root, text="Row 0").grid(row=0, column=0, sticky="nsew")
# tk.Label(root, text="Row 1").grid(row=1, column=0, sticky="nsew")
# tk.Label(root, text="Row 2").grid(row=2, column=0, sticky="nsew")

# # Configure column behavior (optional)
# root.grid_columnconfigure(0, weight=2)

# # Run the application
# root.mainloop()



import cv2

cap = cv2.VideoCapture(1, cv2.CAP_DSHOW)


cap.set(cv2.CAP_PROP_SETTINGS, 1)

while True:
   ret, img = cap.read()
   cv2.imshow('video image', img)
   key = cv2.waitKey(10)
   if key == 27:
       break

cap.release()
cv2.destroyAllWindows()