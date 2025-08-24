from PIL import Image, ImageTk
from tool.funcdispatch import funcdispatch
import tkinter as tk
import cv2
import numpy as np


"""
検査画像の編集
"""

class IMGProcessingWindow :
    
    def __init__(self, root ,img):


        self.circle_count = 0
        self.points = [[0, 0],[0, 0],[0, 0],[0, 0]]

        self.Canvas_size = (600, 450)

        # ウィンドウの作成
        self.root = root # Create the main application window
        self.root.title("検査画像編集")
        self.root.geometry("850x470")  # Set window size (width x height)
        self.root.resizable(False, False)        # サイズを固定

        self.frame = tk.Frame(root, height = self.Canvas_size[0])


        self.choice1_button = tk.Button(self.frame, text="検査区域を指定 (四角)  " ,  width=20, command=self.SelectionIMGRange  )  
        self.choice2_button = tk.Button(self.frame, text="検査区域を指定 (多角形)" ,  width=20, command=lambda:tk.messagebox.showinfo("メッセージ", "未実装" )  )  
        self.choice3_button = tk.Button(self.frame, text="検査区域を指定 (曲線)  " ,  width=20, command=lambda:tk.messagebox.showinfo("メッセージ", "未実装" )  )  
        self.cancel_button  = tk.Button(self.frame, text="キャンセル" , command=self.CancelProcessing)  
        self.save_button    = tk.Button(self.frame, text="保存" )  
        self.clause_button  = tk.Button(self.frame, text="閉じる" , command=self.CloseWindow )  

        self.choice1_button.grid(row=0, column=0, padx=5,  columnspan=3)
        self.choice2_button.grid(row=1, column=0, padx=5,  columnspan=3)
        self.choice3_button.grid(row=2, column=0, padx=5,  columnspan=3)

        self.save_button.grid  (row=3, column=0, pady=20)  
        self.cancel_button.grid(row=3, column=1, pady=20)
        self.clause_button.grid(row=3, column=2, pady=20)
         

    
        
        self.canvas = tk.Canvas(root, width = self.Canvas_size[0], height = self.Canvas_size[1], bg="gray",highlightthickness=1, highlightbackground="black", highlightcolor="black" )
        self.canvas.grid(row=0, column=0, padx=10, pady=10)

        self.frame.grid(row=0, column=1, sticky=tk.NSEW, pady=10)


        self.copy_img = img.copy()
        self.copy_img = cv2.resize(self.copy_img,  self.Canvas_size)

        cv_image = cv2.cvtColor(self.copy_img, cv2.COLOR_BGR2RGB)
        pil_image = Image.fromarray(cv_image)
        image_siz = pil_image.size
        resize_height = self.Canvas_size[1]
        resized_image = pil_image.resize((int(image_siz[0]/(image_siz[1]/resize_height)), resize_height))
        self.tk_image = ImageTk.PhotoImage(resized_image)

        self.canvas.create_image(self.Canvas_size[0]/2, self.Canvas_size[1]/2, image=self.tk_image) 
        self.canvas.image = self.tk_image 

    def DrawCircle(self, event):

        mj
        # 円の半径
        radius = 2
        # クリックした位置に円を描画
        self.canvas.create_oval(
            event.x - radius, event.y - radius, 
            event.x + radius, event.y + radius, 
            fill="red", outline="black"
        )
        
        self.points[ self.circle_count] = [event.x ,  event.y ]
        self.circle_count += 1 

        if  self.circle_count == 4:
            self.canvas.delete("all")

            # height,  width  = self.copy_img.shape[:2]

            # # input_pts = np.float32([[71, 95], [420,45], [160, 311], [505,245]])
            # # アウトプットは元画像と同じサイズ
            # output_pts = np.float32([[0, 0], [width, 0], [0, height], [width, height]])
            # # getPerspectiveTransformの行列の取得
            # matrix = cv2.getPerspectiveTransform(np.float32(self.points), output_pts)
            # # matrix = cv2.getPerspectiveTransform(input_pts,  output_pts)
            # result = cv2.warpPerspective( self.copy_img, matrix, (width, height))

            # マスクを作成
            mask = np.zeros(self.copy_img.shape[:2], dtype=np.uint8)
            cv2.fillPoly(mask, [np.array(self.points)], 255)

            # マスクを適用してポリゴン領域を切り取る
            result = cv2.bitwise_and(self.copy_img, self.copy_img, mask=mask)

            # 背景を透明にする場合 (オプション)
            result_with_alpha = cv2.cvtColor(result, cv2.COLOR_BGR2BGRA)
            result_with_alpha[:, :, 3] = mask


            # 変換の適用
            cv_image = cv2.cvtColor(result, cv2.COLOR_BGR2RGB)
            pil_image = Image.fromarray(cv_image)
            self.tk_image = ImageTk.PhotoImage(pil_image)

            self.canvas.create_image(self.Canvas_size[0]/2, self.Canvas_size[1]/2, image=self.tk_image) 
            self.circle_count = 0
            self.canvas.unbind("<Button-1>")

    def CancelProcessing(self):
        cv_image = cv2.cvtColor(self.copy_img, cv2.COLOR_BGR2RGB)
        pil_image = Image.fromarray(cv_image)
        image_siz = pil_image.size
        resize_height = self.Canvas_size[1]
        resized_image = pil_image.resize((int(image_siz[0]/(image_siz[1]/resize_height)), resize_height))
        self.tk_image = ImageTk.PhotoImage(resized_image)

        self.canvas.create_image(self.Canvas_size[0]/2, self.Canvas_size[1]/2, image=self.tk_image) 
        self.canvas.image = self.tk_image 
            

    def SelectionIMGRange(self):
        tk.messagebox.showinfo("範囲選択", "検査を実施したい範囲の四隅を選択してください" )
        # クリックイベントをバインド
        self.canvas.bind("<Button-1>", self.DrawCircle)


    def CloseWindow(self):
        self.root.destroy()

    def SaveIMG(self):
        self.copy_img = self.tk_image 
        


