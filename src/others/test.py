# # import tkinter as tk

# # def on_modified(e):
# #     print(e)
# #     e.widget.edit_modified(False)  # フラグをオフにする事で、毎回呼ばれるようにする。

# # root = tk.Tk()
# # text = tk.Text(root)
# # text.bind("<<Modified>>", on_modified)
# # text.pack()
# # root.mainloop()







# # import tkinter as tk

# # def is_number(s):
# #     return s.isdigit()

# # root = tk.Tk()
# # validate_command = root.register(is_number)
# # entry = tk.Entry(root, validate="key", validatecommand=(validate_command, '%P'))
# # entry.pack()
# # root.mainloop()

# # import tkinter as tk

# # # Create the main window
# # root = tk.Tk()
# # root.geometry("300x200")

# # # Configure row behavior
# # root.grid_rowconfigure(0, weight=1)  # Row 0 grows proportionally
# # root.grid_rowconfigure(1, weight=2)  # Row 1 grows twice as much as Row 0
# # root.grid_rowconfigure(2, weight=1, minsize=50)  # Row 2 has a minimum height of 50px

# # # Add widgets
# # tk.Label(root, text="Row 0").grid(row=0, column=0, sticky="nsew")
# # tk.Label(root, text="Row 1").grid(row=1, column=0, sticky="nsew")
# # tk.Label(root, text="Row 2").grid(row=2, column=0, sticky="nsew")

# # # Configure column behavior (optional)
# # root.grid_columnconfigure(0, weight=2)

# # # Run the application
# # root.mainloop()



# # import cv2

# # cap = cv2.VideoCapture(1, cv2.CAP_DSHOW)


# # cap.set(cv2.CAP_PROP_SETTINGS, 1)

# # while True:
# #    ret, img = cap.read()
# #    cv2.imshow('video image', img)
# #    key = cv2.waitKey(10)
# #    if key == 27:
# #        break

# # cap.release()
# # cv2.destroyAllWindows()

# import tkinter as tk
# from tkinter import simpledialog

# def open_subwindow():
#     # サブウィンドウを作成
#     def submit_value():
#         nonlocal return_value
#         return_value = entry.get()  # 入力値を取得
#         subwindow.destroy()  # サブウィンドウを閉じる

#     return_value = None
#     subwindow = tk.Toplevel(root)
#     subwindow.title("サブウィンドウ")
#     subwindow.geometry("300x150")

#     tk.Label(subwindow, text="値を入力してください:").pack(pady=10)
#     entry = tk.Entry(subwindow)
#     entry.pack(pady=5)

#     tk.Button(subwindow, text="OK", command=submit_value).pack(pady=10)

#     # サブウィンドウが閉じられるまで待機
#     subwindow.grab_set()
#     root.wait_window(subwindow)

#     return return_value

# def main():
#     result = open_subwindow()
#     if result:
#         label.config(text=f"入力された値: {result}")
#     else:
#         label.config(text="値が入力されませんでした")

# # メインウィンドウの設定
# root = tk.Tk()
# root.title("メインウィンドウ")
# root.geometry("400x200")

# label = tk.Label(root, text="サブウィンドウから値を取得します")
# label.pack(pady=20)

# button = tk.Button(root, text="サブウィンドウを開く", command=main)
# button.pack(pady=10)

# root.mainloop()


##########################################################################

import cv2

cap = cv2.VideoCapture(1, cv2.CAP_DSHOW)

cap.set(cv2.CAP_PROP_SETTINGS, 1)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1600.0)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1600.0)

while True:
   ret, img = cap.read()
   cv2.imshow('video image', img)
   key = cv2.waitKey(10)
   if key == 27:
       break

cap.release()
cv2.destroyAllWindows()

# import cv2
# import sys

# camera_id = 1
# delay = 1
# window_name = 'frame'

# cap = cv2.VideoCapture(camera_id)

# if not cap.isOpened():
#     sys.exit()

# while True:
#     ret, frame = cap.read()
#     cv2.imshow(window_name, frame)
#     if cv2.waitKey(delay) & 0xFF == ord('q'):
#         break

# cv2.destroyWindow(window_name)