import tkinter as tk
import cv2
from tkinter import messagebox
from tkinter import filedialog
from PIL import Image, ImageTk
import numpy as np
import os

import cv2



version = 1.0
Canvas_size = [600, 450]

class Application():
    def __init__(self, root):
        self.cap = cv2.VideoCapture(1)

        self.cap.set(cv2.CAP_PROP_AUTO_EXPOSURE, 0)
        self.cap.set(cv2.CAP_PROP_AUTO_WB, 0)
        self.base_image = np.array([])
        self.camera_image = np.array([])
        self.analusis_image = np.array([])



        # ウィンドウの作成
        self.root = root # Create the main application window
        self.root.title("異差検出ツール v" + str(version))
        self.root.geometry("1280x600")  # Set window size (width x height)

        self.root.resizable(False, False)        # サイズを固定
      
        # メニューバーの作成
        self.menu_bar = tk.Menu(root)

        #キャンバスエリア
        self.canvas1 = tk.Canvas(root, width = Canvas_size[0], height = Canvas_size[1], bg="gray")
        self.canvas2 = tk.Canvas(root, width = Canvas_size[0], height = Canvas_size[1], bg="gray")

        #キャンバスバインド
        self.canvas1.place(x=20, y=40)
        self.canvas2.place(x=660, y=40)

        # ファイルメニュー
        self.file_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.file_menu.add_command(label="標準画像選択", command=self.open_image)
        self.file_menu.add_command(label="標準画像確認", command=self.confirmation_image)
        self.file_menu.add_separator()
        self.file_menu.add_command(label="カメラ画像保存", command=self.photo_shoot )
        self.file_menu.add_command(label="標準画像保存", command=self.seave_image_base)
        self.file_menu.add_command(label="検査画像保存", command=self.seave_image_analusis)
        self.file_menu.add_separator()
        self.file_menu.add_command(label="終了", command=self.exit_app)
        self.menu_bar.add_cascade(label="ファイル", menu=self.file_menu)

        # 設定メニュー
        self.setting = tk.Menu(self.menu_bar, tearoff=0)
        self.setting.add_command(label="カメラ設定", command=lambda: messagebox.showinfo("カメラ設定画面", "未実装 デフォルト値固定"))
        self.setting.add_command(label="標準画像設定", command=lambda: messagebox.showinfo("検査設定画面", "未実装 デフォルト値固定" ))
        self.setting.add_command(label="検査設定", command=lambda: messagebox.showinfo("設定画面", "未実装 閾値値固定" ))
        self.menu_bar.add_cascade(label="設定", menu=self.setting)

        # ヘルプメニュー
        self.help_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.help_menu.add_command(label="バージョン情報", command=lambda: messagebox.showinfo("バージョン", "バージョン 1.0"))
        self.menu_bar.add_cascade(label="ヘルプ", menu=self.help_menu)

        root.config(menu=self.menu_bar)

        
        # ラベル
        self.lbl1 = tk.Label(root, text='検査画面', font=("メイリオ", "15", "normal"), bg="lightgrey")
        self.lbl1.place(x=22, y=5, width=600, height=35)
        self.lbl2 = tk.Label(root, text='検査結果', font=("メイリオ", "15", "normal"), bg="lightgrey")
        self.lbl2.place(x=662, y=5, width=600, height=35)
        self.lbl3 = tk.Label(root, text='ログ  ※未実装')
        self.lbl3.place(x=30, y=500)
        self.txt = tk.Entry(root, bg="lightgrey" )
        self.txt.place(x=20, y=520, width=800, height=50)

        # ボタン
        self.button1 = tk.Button(root, text="検査", bg="slategrey", command=self.on_button1)
        self.button1.place(x=870, y=510, width=100, height=60) 
        self.button2 = tk.Button(root, text="標準画像更新", bg="slategrey", command=self.base_image_update)
        self.button2.place(x=1000, y=510, width=100, height=60)
        self.button2 = tk.Button(root, text="検査画像保存", bg="slategrey", command=self.seave_image_analusis)
        self.button2.place(x=1130, y=510, width=100, height=60)

        self.root.bind("<Return>", self.on_enter)

        self.update_frame()

    def confirmation_image(self):
        if  self.base_image.size == 0:
            messagebox.showinfo("メッセージ", "標準画像が設定されていません")
            return
        else :
            self.custom_messagebox()

    def photo_shoot(self):

        file_path = filedialog.asksaveasfilename(
        defaultextension=".png",  # デフォルトの拡張子
        filetypes=[("画像ファイル", "*.png;*.jpg")],
        title="カメラ画像を保存"
        )
        try:
            ext = os.path.splitext(file_path)[1]
            result, n = cv2.imencode(ext, self.camera_image , None)
            
            if result:
                with open(file_path, mode='w+b') as f:
                    n.tofile(f)

        except Exception as e:
            print(e)

          

    def seave_image_analusis(self):
        if  self.analusis_image.size == 0:
            messagebox.showinfo("メッセージ", "検査画像がありません")
            return
        
        file_path = filedialog.asksaveasfilename(
        defaultextension=".png",  # デフォルトの拡張子
        filetypes=[("画像ファイル", "*.png;*.jpg")],
        title="検査画像を保存"
        )
        try:
            ext = os.path.splitext(file_path)[1]
            result, n = cv2.imencode(ext, self.analusis_image  , None)
            
            if result:
                with open(file_path, mode='w+b') as f:
                    n.tofile(f)

        except Exception as e:
            print(e)
            
    def seave_image_base(self):
        if  self.base_image.size == 0:
            messagebox.showinfo("メッセージ", "検査画像がありません")
            return
        
        file_path = filedialog.asksaveasfilename(
        defaultextension=".png",  # デフォルトの拡張子
        filetypes=[("画像ファイル", "*.png;*.jpg")],
        title="検査画像を保存"
        )
        try:
            ext = os.path.splitext(file_path)[1]
            result, n = cv2.imencode(ext, self.base_image  , None)
            
            if result:
                with open(file_path, mode='w+b') as f:
                    n.tofile(f)

        except Exception as e:
            print(e)




    def open_image(self):
        # ファイル選択ダイアログを開く
        file_path = filedialog.askopenfilename(
            filetypes=[("画像ファイル", "*.png;*.jpg")]
        )
        try:
            n = np.fromfile(file_path, np.uint8)
            cv_image = cv2.imdecode(n, cv2.IMREAD_COLOR)
            self.base_image  = cv_image
            messagebox.showinfo("メッセージ", "標準画像を登録しました")
            
             
        except Exception as e:
            print(e)
            return None
        
    def base_image_update(self):
        self.base_image = self.camera_image


    # 終了関数
    def exit_app(self):
        self.root.quit()
        self.root.destroy()
        self.cap.release()

    def camera_setting(self):
        messagebox.showinfo("未実装")

    def on_enter(self, event):
        
        if  self.base_image.size == 0:
            messagebox.showinfo("メッセージ", "標準画像を設定してください")
            return
        
        if  self.lbl2.cget("text") == "検査結果":
            result = self.Analusis() 
            if result:
                self.lbl2["text"] = " 検査結果 ≪≪ 異常 ≫≫ "
                self.lbl2["bg"] = "red"
            else:
                self.lbl2["text"] = " 検査結果 ≪≪ 正常 ≫≫ "
                self.lbl2["bg"] = "green2"
        else :
            self.lbl2["text"] = "検査結果"
            self.lbl2["bg"] = "slategrey"

        if  self.button1.cget("text") == "検査":
            self.button1["text"] = "リセット"
        else :
            self.button1["text"] = "検査"
            self.canvas2.delete("all")
            

    def on_button1(self):
        
        if  self.base_image.size == 0:
            messagebox.showinfo("メッセージ", "標準画像を設定してください")
            return
        
        if  self.lbl2.cget("text") == "検査結果":
            result = self.Analusis() 
            if result:
                self.lbl2["text"] = " 検査結果 ≪≪ 異常 ≫≫ "
                self.lbl2["bg"] = "red"
            else:
                self.lbl2["text"] = " 検査結果 ≪≪ 正常 ≫≫ "
                self.lbl2["bg"] = "green2"
        else :
            self.lbl2["text"] = "検査結果"
            self.lbl2["bg"] = "slategrey"

        if  self.button1.cget("text") == "検査":
            self.button1["text"] = "リセット"
        else :
            self.button1["text"] = "検査"
            self.canvas2.delete("all")

    def update_frame(self):
        ret, frame = self.cap.read()
        if ret:
            # OpenCVのBGRをRGBに変換
            self.camera_image=frame
            cv_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            pil_image = Image.fromarray(cv_image)
            image_siz = pil_image.size
            resize_height = Canvas_size[1]
            resized_image = pil_image.resize((int(image_siz[0]/(image_siz[1]/resize_height)), resize_height))
            tk_image = ImageTk.PhotoImage(resized_image)
            self.canvas1.create_image(Canvas_size[0]/2, Canvas_size[1]/2, image=tk_image) 
            self.canvas1.image = tk_image 
        
        # 10msごとに更新
        self.root.after(10, self.update_frame)

    def custom_messagebox(self):
        # 新しいウィンドウを作成
        print("test")
        messagebox = tk.Toplevel(root)
        messagebox.title("標準画像 確認画面")
        messagebox.geometry("400x400")
        messagebox.resizable(False, False)

        cv_image = cv2.cvtColor(self.base_image, cv2.COLOR_BGR2RGB)
        pil_image = Image.fromarray(cv_image)
        image_siz = pil_image.size
        resize_height = 350
        resized_image = pil_image.resize((int(image_siz[0]/(image_siz[1]/resize_height)), resize_height))
        photo = ImageTk.PhotoImage(resized_image)

        # 画像をラベルに表示
        image_label = tk.Label(messagebox, image=photo)
        image_label.image = photo  # 参照を保持する必要があります
        image_label.pack()

        # OKボタンを追加
        ok_button = tk.Button(messagebox, text="OK", command=messagebox.destroy)
        ok_button.pack(pady=10)

    def Analusis(self):
        self.analusis_image = self.camera_image
        #################################### 特徴点を抽出 ####################################
        # 画像サイズを取得
        hA, wA, cA = self.camera_image.shape[:3]
        hB, wB, cB = self.base_image.shape [:3]

        # 特徴量検出器を作成
        akaze = cv2.AKAZE_create()
        # 二つの画像の特徴点を抽出
        kpA, desA = akaze.detectAndCompute(self.camera_image,None)
        kpB, desB = akaze.detectAndCompute(self.base_image,None)

        
        #################################### 特徴点のマッチングと物体検出 ####################################
        # imageBを透視変換する
        # 透視変換: 斜めから撮影した画像を真上から見た画像に変換する感じ
        # BFMatcher型のオブジェクトを作成する
        bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
        # 記述子をマッチさせる。※スキャン画像(B2)の特徴抽出はforループ前に実施済み。
        matches = bf.match(desA,desB)
        # マッチしたものを距離順に並べ替える。
        matches = sorted(matches, key = lambda x:x.distance)
        # マッチしたもの（ソート済み）の中から上位★%（参考：15%)をgoodとする。
        good = matches[:int(len(matches) * 0.15)]
        # 対応が取れた特徴点の座標を取り出す？
        src_pts = np.float32([kpA[m.queryIdx].pt for m in good]).reshape(-1,1,2)
        dst_pts = np.float32([kpB[m.trainIdx].pt for m in good]).reshape(-1,1,2)
        # findHomography:二つの画像から得られた点の集合を与えると、その物体の投射変換を計算する
        M, mask = cv2.findHomography(dst_pts, src_pts, cv2.RANSAC,5.0) # dst_img作成の際だけ使う。warpperspectiveの使い方がわかってない。
        # imgBを透視変換。
        imgB_transform = cv2.warpPerspective(self.base_image, M, (wA, hA))

        #################################### 差分をとる ####################################
        # imgAとdst_imgの差分を求めてresultとする。グレースケールに変換。
        result = cv2.absdiff(self.camera_image, imgB_transform)
        result_gray = cv2.cvtColor(result, cv2.COLOR_BGR2GRAY)
        # 二値化
        _, result_bin = cv2.threshold(result_gray, 70, 255, cv2.THRESH_BINARY) # 閾値は50


        #################################### ノイズ除去  ####################################
        # カーネルを準備（オープニング用）
        kernel = np.ones((2,2),np.uint8)
        # オープニング（収縮→膨張）実行 ノイズ除去
        result_bin = cv2.morphologyEx(result_bin, cv2.MORPH_OPEN, kernel) # オープニング（収縮→膨張）。ノイズ除去。


        #################################### 後処理  ####################################
        # 二値画像をRGB形式に変換し、2枚の画像を重ねる。
        result_bin_rgb = cv2.cvtColor(result_bin, cv2.COLOR_GRAY2RGB)
        result_add = cv2.addWeighted(self.camera_image, 0.3, result_bin_rgb, 0.7, 2.2) # ２.２はガンマ値。大きくすると白っぽくなる

        cv_image = cv2.cvtColor(result_add, cv2.COLOR_BGR2RGB)
        pil_image = Image.fromarray(cv_image)
        image_siz = pil_image.size
        resize_height = Canvas_size[1]
        resized_image = pil_image.resize((int(image_siz[0]/(image_siz[1]/resize_height)), resize_height))
        tk_image = ImageTk.PhotoImage(resized_image)
        self.canvas2.create_image(Canvas_size[0]/2, Canvas_size[1]/2, image=tk_image) 
        self.canvas2.image = tk_image 


        return 1000 < cv2.countNonZero(result_bin)
        



# アプリケーションの起動
if __name__ == "__main__":
    root = tk.Tk()
    app = Application(root)
    root.mainloop()