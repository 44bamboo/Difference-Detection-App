from PIL import Image, ImageTk
from tool.funcdispatch import funcdispatch
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import cv2
import json


"""
opencvのプロパティ設定ダイアログ参考
二度と実装したくない


ToDo
● 色の使用
● PowerLineの頻度設定 現状60Hz固定
● 低光量補正(L)

Error
Textboxが空状態で規定値を押しても更新されない
"""

class CameraSettingWindow :
    
    def __init__(self, root ,cap):
        # 設定ファイルの読み込み
        self.cam_settings_data =  self.ReadCamSettings()

        # # カメラ初期値設定
        self.cap = cap
        
        # ウィンドウの作成
        self.root = root # Create the main application window
        self.root.title("カメラ設定")
        self.root.geometry("450x420")  # Set window size (width x height)
        self.root.resizable(False, False)        # サイズを固定

        # カメラ画像表示用キャンパス
        # self.cam_canvas = tk.Canvas(self.root, width = 500, height = 400, bg="gray")
        # #キャンバス(カメラ画像)バインド
        # self.cam_canvas.grid(row=0, column=0, rowspan = 2)


        # ドロップダウンリストの作成
        name_list = [item["name"] for item in self.cam_settings_data["User_Setting_data"]]
        # 初期値設定
        self.v = tk.StringVar()
        self.v.set(name_list[0])
        self.combobox = ttk.Combobox(self.root, textvariable=self.v, values=name_list, style="office.TCombobox", height= 1)

        self.combobox.bind("<<ComboboxSelected>>", self.ChangeCombobox)

        self.adaptation_button = tk.Button(self.root, text="適用"      , command=self.WriteCamSettings)  
        self.cancel_button     = tk.Button(self.root, text="キャンセル" , command=self.CloseWindow)  
        self.adaptation_button.grid(row=2, column=1)
        self.cancel_button.grid(row=2, column=2)
        

        # Notebookウィジェットの作成
        self.notebook = ttk.Notebook(self.root, height = 350)
        # タブ1の作成
        self.img_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.img_tab           , text="画像の調整")
        self.label_Auto1 = ttk.Label(self.img_tab, text="自動"         , font=("メイリオ", 7))

        self.label_Br = ttk.Label(self.img_tab, text="明るさ(Br)"           , font=("メイリオ", 10))
        self.label_C  = ttk.Label(self.img_tab, text="コントラスト(C)"      , font=("メイリオ", 10))
        self.label_H  = ttk.Label(self.img_tab, text="色合い(H)"            , font=("メイリオ", 10))
        self.label_S  = ttk.Label(self.img_tab, text="鮮やかさ(S)"           , font=("メイリオ", 10))
        self.label_P  = ttk.Label(self.img_tab, text="鮮明度(P)"            , font=("メイリオ", 10))
        self.label_G  = ttk.Label(self.img_tab, text="ガンマ(G)"            , font=("メイリオ", 10))
        self.label_W  = ttk.Label(self.img_tab, text="ホワイトバランス(W)"   , font=("メイリオ", 10))
        self.label_Ba = ttk.Label(self.img_tab, text="逆光補正(Ba)"         , font=("メイリオ", 10))
        self.label_Ga = ttk.Label(self.img_tab, text="ゲイン(Ga)"           , font=("メイリオ", 10))

        self.volume_slider_Br = tk.Scale(self.img_tab, from_=0, to=255, orient='horizontal', showvalue=False, length=200, command=self.ChangeTextBrightness) # 明るさ(Br)
        self.volume_slider_C  = tk.Scale(self.img_tab, from_=0, to=255, orient='horizontal', showvalue=False, length=200, command=self.ChangeTextContrast  ) # コントラスト(C)
        self.volume_slider_H  = tk.Scale(self.img_tab, from_=0, to=255, orient='horizontal', showvalue=False, length=200, command=self.ChangeTextHue ) # 色合い(H)
        self.volume_slider_S  = tk.Scale(self.img_tab, from_=0, to=255, orient='horizontal', showvalue=False, length=200, command=self.ChangeTextSaturation ) # 鮮やかさ(S)
        self.volume_slider_P  = tk.Scale(self.img_tab, from_=0, to=255, orient='horizontal', showvalue=False, length=200, command=self.ChangeTextPinto) # 鮮明度(P)
        self.volume_slider_G  = tk.Scale(self.img_tab, from_=0, to=255, orient='horizontal', showvalue=False, length=200, command=self.ChangeTextGamma) # ガンマ(G)
        self.volume_slider_W  = tk.Scale(self.img_tab, from_=0, to=10000, orient='horizontal', showvalue=False, length=200, command=self.ChangeTextWhiteBalance ) # ホワイトバランス(W)
        self.volume_slider_Ba = tk.Scale(self.img_tab, from_=0, to=1, orient='horizontal', showvalue=False, length=200, command=self.ChangeTextBacklight ) # 逆光補正(Ba)
        self.volume_slider_Ga = tk.Scale(self.img_tab, from_=0, to=255, orient='horizontal', showvalue=False, length=200, command=self.ChangeTextGain) # ゲイン(Ga)

        self.txt_Br = tk.Entry(self.img_tab, width=5) # 明るさ(Br)
        self.txt_C  = tk.Entry(self.img_tab, width=5) # コントラスト(C)
        self.txt_H  = tk.Entry(self.img_tab, width=5) # 色合い(H)
        self.txt_S  = tk.Entry(self.img_tab, width=5) # 鮮やかさ(S)
        self.txt_P  = tk.Entry(self.img_tab, width=5) # 鮮明度(P)
        self.txt_G  = tk.Entry(self.img_tab, width=5) # ガンマ(G)
        self.txt_W  = tk.Entry(self.img_tab, width=5) # ホワイトバランス(W)
        self.txt_Ba = tk.Entry(self.img_tab, width=5) # 逆光補正(Ba)
        self.txt_Ga = tk.Entry(self.img_tab, width=5) # ゲイン(Ga)

        self.txt_Br.bind("<FocusOut>", self.ChangeSlideBrightness)
        self.txt_C .bind("<FocusOut>", self.ChangeSlideContrast)
        self.txt_H .bind("<FocusOut>", self.ChangeSlideHue)
        self.txt_S .bind("<FocusOut>", self.ChangeSlideSaturation)
        self.txt_P .bind("<FocusOut>", self.ChangeSlidePinto)
        self.txt_G .bind("<FocusOut>", self.ChangeSlideGamma)
        self.txt_W .bind("<FocusOut>", self.ChangeSlideWhiteBalance)
        self.txt_Ba.bind("<FocusOut>", self.ChangeSlideBacklight)
        self.txt_Ga.bind("<FocusOut>", self.ChangeSlideGain)

        self.chk_Br = tk.Checkbutton(self.img_tab) # 明るさ(Br)
        self.chk_C  = tk.Checkbutton(self.img_tab) # コントラスト(C)
        self.chk_H  = tk.Checkbutton(self.img_tab) # 色合い(H)
        self.chk_S  = tk.Checkbutton(self.img_tab) # 鮮やかさ(S)
        self.chk_P  = tk.Checkbutton(self.img_tab) # 鮮明度(P)
        self.chk_G  = tk.Checkbutton(self.img_tab) # ガンマ(G)
        self.chk_W  = tk.Checkbutton(self.img_tab) # ホワイトバランス(W)
        self.chk_Ba = tk.Checkbutton(self.img_tab) # 逆光補正(Ba)
        self.chk_Ga = tk.Checkbutton(self.img_tab) # ゲイン(Ga)
       
        self.img_defo_button = tk.Button(self.img_tab, text="規定値", command=self.UpdataImgParameter)  

        self.label_Auto1.grid(row=1,  column=4)

        self.label_Br .grid(row=2,  column=1, sticky=tk.E)
        self.label_C  .grid(row=3,  column=1, sticky=tk.E)
        self.label_H  .grid(row=4,  column=1, sticky=tk.E)
        self.label_S  .grid(row=5,  column=1, sticky=tk.E)
        self.label_P  .grid(row=6,  column=1, sticky=tk.E)
        self.label_G  .grid(row=7,  column=1, sticky=tk.E)
        self.label_W  .grid(row=8,  column=1, sticky=tk.E)
        self.label_Ba .grid(row=9,  column=1, sticky=tk.E)
        self.label_Ga .grid(row=10, column=1, sticky=tk.E)

        self.volume_slider_Br .grid(row=2,  column=2)
        self.volume_slider_C  .grid(row=3,  column=2)
        self.volume_slider_H  .grid(row=4,  column=2)
        self.volume_slider_S  .grid(row=5,  column=2)
        self.volume_slider_P  .grid(row=6,  column=2)
        self.volume_slider_G  .grid(row=7,  column=2)
        self.volume_slider_W  .grid(row=8,  column=2)
        self.volume_slider_Ba .grid(row=9,  column=2)
        self.volume_slider_Ga .grid(row=10,  column=2)

        self.txt_Br .grid(row=2,  column=3, sticky=tk.W)
        self.txt_C  .grid(row=3,  column=3, sticky=tk.W)
        self.txt_H  .grid(row=4,  column=3, sticky=tk.W)
        self.txt_S  .grid(row=5,  column=3, sticky=tk.W)
        self.txt_P  .grid(row=6,  column=3, sticky=tk.W)
        self.txt_G  .grid(row=7,  column=3, sticky=tk.W)
        self.txt_W  .grid(row=8,  column=3, sticky=tk.W)
        self.txt_Ba .grid(row=9,  column=3, sticky=tk.W)
        self.txt_Ga .grid(row=10, column=3, sticky=tk.W)
        
        self.chk_Br .grid(row=2,  column=4, sticky=tk.E)
        self.chk_C  .grid(row=3,  column=4, sticky=tk.E)
        self.chk_H  .grid(row=4,  column=4, sticky=tk.E)
        self.chk_S  .grid(row=5,  column=4, sticky=tk.E)
        self.chk_P  .grid(row=6,  column=4, sticky=tk.E)
        self.chk_G  .grid(row=7,  column=4, sticky=tk.E)
        self.chk_W  .grid(row=8,  column=4, sticky=tk.E)
        self.chk_Ba .grid(row=9,  column=4, sticky=tk.E)
        self.chk_Ga .grid(row=10, column=4, sticky=tk.E)

        self.img_defo_button.grid(row=11, column=2)




        # タブ2の作成
        self.cam_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.cam_tab, text="カメラ制御")

        self.label_Auto2 = ttk.Label(self.cam_tab, text="自動"         , font=("メイリオ", 7))

        self.label_Z  = ttk.Label(self.cam_tab, text="             ズーム(Z)"  , font=("メイリオ", 10))
        self.label_F  = ttk.Label(self.cam_tab, text="焦点(F)"    , font=("メイリオ", 10))
        self.label_E  = ttk.Label(self.cam_tab, text="露出(E)"    , font=("メイリオ", 10))
        self.label_Ap = ttk.Label(self.cam_tab, text="絞り(Ap)"   , font=("メイリオ", 10))
        self.label_A  = ttk.Label(self.cam_tab, text="虹彩(A)"    , font=("メイリオ", 10))
        self.label_Pa = ttk.Label(self.cam_tab, text="パン(P)"    , font=("メイリオ", 10))
        self.label_T  = ttk.Label(self.cam_tab, text="傾き(T)"    , font=("メイリオ", 10))
        self.label_R  = ttk.Label(self.cam_tab, text="回転(R)"    , font=("メイリオ", 10))

        self.volume_slider_Z  = tk.Scale(self.cam_tab, from_=0, to=255, orient='horizontal', showvalue=False, length=200, command=self.ChangeTextZoom) # ズーム(Z)
        self.volume_slider_F  = tk.Scale(self.cam_tab, from_=0, to=255, orient='horizontal', showvalue=False, length=200, command=self.ChangeTextFocus) # 焦点(F)
        self.volume_slider_E  = tk.Scale(self.cam_tab, from_=0, to=255, orient='horizontal', showvalue=False, length=200, command=self.ChangeTextExposure) # 露出(E)
        self.volume_slider_Ap = tk.Scale(self.cam_tab, from_=0, to=255, orient='horizontal', showvalue=False, length=200, command=self.ChangeTextSqueeze) # 絞り(Ap)
        self.volume_slider_A  = tk.Scale(self.cam_tab, from_=0, to=255, orient='horizontal', showvalue=False, length=200, command=self.ChangeTextIris) # 虹彩(A)
        self.volume_slider_Pa = tk.Scale(self.cam_tab, from_=0, to=255, orient='horizontal', showvalue=False, length=200, command=self.ChangeTextPan) # パン(P)
        self.volume_slider_T  = tk.Scale(self.cam_tab, from_=0, to=255, orient='horizontal', showvalue=False, length=200, command=self.ChangeTextTilt) # 傾き(T)
        self.volume_slider_R  = tk.Scale(self.cam_tab, from_=0, to=255, orient='horizontal', showvalue=False, length=200, command=self.ChangeTextRotation) # 回転(R)

        self.txt_Z  = tk.Entry(self.cam_tab, width=10) # ズーム(Z)
        self.txt_F  = tk.Entry(self.cam_tab, width=10) # 焦点(F)
        self.txt_E  = tk.Entry(self.cam_tab, width=10) # 露出(E)
        self.txt_Ap = tk.Entry(self.cam_tab, width=10) # 絞り(Ap)
        self.txt_A  = tk.Entry(self.cam_tab, width=10) # 虹彩(A)
        self.txt_Pa = tk.Entry(self.cam_tab, width=10) # パン(P)
        self.txt_T  = tk.Entry(self.cam_tab, width=10) # 傾き(T)
        self.txt_R  = tk.Entry(self.cam_tab, width=10) # 回転(R)

        self.txt_Z .bind("<FocusOut>", self.ChangeSlideZoom)
        self.txt_F .bind("<FocusOut>", self.ChangeSlideFocus)
        self.txt_E .bind("<FocusOut>", self.ChangeSlideExposure)
        self.txt_Ap.bind("<FocusOut>", self.ChangeSlideSqueeze)
        self.txt_A .bind("<FocusOut>", self.ChangeSlidetIris)
        self.txt_Pa.bind("<FocusOut>", self.ChangeSlideWhitePan)
        self.txt_T .bind("<FocusOut>", self.ChangeSlideTilt)
        self.txt_R .bind("<FocusOut>", self.ChangeSlideRotation)

        self.chk_Z  = tk.Checkbutton(self.cam_tab)  # ズーム(Z)
        self.chk_F  = tk.Checkbutton(self.cam_tab)  # 焦点(F)
        self.chk_E  = tk.Checkbutton(self.cam_tab)  # 露出(E)
        self.chk_Ap = tk.Checkbutton(self.cam_tab)  # 絞り(Ap)
        self.chk_A  = tk.Checkbutton(self.cam_tab)  # 虹彩(A)
        self.chk_Pa = tk.Checkbutton(self.cam_tab)  # パン(P)
        self.chk_T  = tk.Checkbutton(self.cam_tab)  # 傾き(T)
        self.chk_R  = tk.Checkbutton(self.cam_tab)  # 回転(R)

        self.cam_defo_button = tk.Button(self.cam_tab, text="規定値", command=self.UpdataCamParameter)  

        self.label_Auto2.grid(row=1,  column=4)

        self.label_Z .grid(row=2,  column=1, sticky=tk.E)
        self.label_F .grid(row=3,  column=1, sticky=tk.E)
        self.label_E .grid(row=4,  column=1, sticky=tk.E)
        self.label_Ap.grid(row=5,  column=1, sticky=tk.E)
        self.label_A .grid(row=6,  column=1, sticky=tk.E)
        self.label_Pa.grid(row=7,  column=1, sticky=tk.E)
        self.label_T .grid(row=8,  column=1, sticky=tk.E)
        self.label_R .grid(row=9,  column=1, sticky=tk.E)

        self.volume_slider_Z .grid(row=2,  column=2)
        self.volume_slider_F .grid(row=3,  column=2)
        self.volume_slider_E .grid(row=4,  column=2)
        self.volume_slider_Ap.grid(row=5,  column=2)
        self.volume_slider_A .grid(row=6,  column=2)
        self.volume_slider_Pa.grid(row=7,  column=2)
        self.volume_slider_T .grid(row=8,  column=2)
        self.volume_slider_R .grid(row=9,  column=2)

        self.txt_Z .grid(row=2,  column=3, sticky=tk.W)
        self.txt_F .grid(row=3,  column=3, sticky=tk.W)
        self.txt_E .grid(row=4,  column=3, sticky=tk.W)
        self.txt_Ap.grid(row=5,  column=3, sticky=tk.W)
        self.txt_A .grid(row=6,  column=3, sticky=tk.W)
        self.txt_Pa.grid(row=7,  column=3, sticky=tk.W)
        self.txt_T .grid(row=8,  column=3, sticky=tk.W)
        self.txt_R .grid(row=9,  column=3, sticky=tk.W)
        
        self.chk_Z  .grid(row=2,  column=4, sticky=tk.E)
        self.chk_F  .grid(row=3,  column=4, sticky=tk.E)
        self.chk_E  .grid(row=4,  column=4, sticky=tk.E)
        self.chk_Ap .grid(row=5,  column=4, sticky=tk.E)
        self.chk_A  .grid(row=6,  column=4, sticky=tk.E)
        self.chk_Pa .grid(row=7,  column=4, sticky=tk.E)
        self.chk_T  .grid(row=8,  column=4, sticky=tk.E)
        self.chk_R  .grid(row=9,  column=4, sticky=tk.E)

        self.cam_defo_button.grid(row=11, column=2)



        self.combobox.grid(row=0,  column=1, sticky=tk.NW)
        self.notebook.grid(row=1,  column=1, sticky=tk.NW, columnspan=2)


        self.UpdataAllParameter() 


        # ▽ 未実装部分のため無効化
        self.volume_slider_P.configure(state='disabled')
        self.txt_P.configure(state='readonly')
        self.chk_P.configure(state='disabled')
        self.volume_slider_Ba.configure(state='disabled')
        self.txt_Ba.configure(state='readonly')
        self.chk_Ba.configure(state='disabled')


        self.volume_slider_Z.configure(state='disabled')
        self.txt_Z.configure(state='readonly')
        self.chk_Z.configure(state='disabled')
        self.volume_slider_Ap.configure(state='disabled')
        self.txt_Ap.configure(state='readonly')
        self.chk_Ap.configure(state='disabled')
        self.volume_slider_A.configure(state='disabled')
        self.txt_A.configure(state='readonly')
        self.chk_A.configure(state='disabled')


        # self.UpdataFrame()
        self.UpdataFrame()
    ###################################################
    ##################### Updata ######################
    ###################################################



    def UpdataAllParameter(self):  
        self.UpdataImgParameter() 
        self.UpdataCamParameter() 

    def UpdataImgParameter(self):
        setting_data1 = self.cam_settings_data["User_Setting_data"][self.combobox.current()]
        setting_data1_img = setting_data1["画像の調整"]
        self.ChangeTextBrightness   (setting_data1_img["Brightness"  ])
        self.ChangeSlideBrightness  (setting_data1_img["Brightness"  ])
        self.ChangeTextContrast     (setting_data1_img["Contrast"    ])
        self.ChangeSlideContrast    (setting_data1_img["Contrast"    ])
        self.ChangeTextHue          (setting_data1_img["Hue"         ])
        self.ChangeSlideHue         (setting_data1_img["Hue"         ])
        self.ChangeTextSaturation   (setting_data1_img["Saturation"  ])
        self.ChangeSlideSaturation  (setting_data1_img["Saturation"  ])
        self.ChangeTextPinto        (setting_data1_img["Pinto"       ])
        self.ChangeSlidePinto       (setting_data1_img["Pinto"       ])
        self.ChangeTextGamma        (setting_data1_img["Gamma"       ])
        self.ChangeSlideGamma       (setting_data1_img["Gamma"       ])
        self.ChangeTextWhiteBalance (setting_data1_img["WhiteBalance"])
        self.ChangeSlideWhiteBalance(setting_data1_img["WhiteBalance"])
        self.ChangeTextBacklight    (setting_data1_img["Backlight"   ])
        self.ChangeSlideBacklight   (setting_data1_img["Backlight"   ])
        self.ChangeTextGain         (setting_data1_img["Gain"        ])
        self.ChangeSlideGain        (setting_data1_img["Gain"        ])

    def UpdataCamParameter(self):
        setting_data1 = self.cam_settings_data["User_Setting_data"][self.combobox.current()]
        setting_data1_cam = setting_data1["カメラ制御"]
        self.ChangeTextZoom         (setting_data1_cam["Zoom"        ])
        self.ChangeSlideZoom        (setting_data1_cam["Zoom"        ])
        self.ChangeTextFocus        (setting_data1_cam["Focus"       ])
        self.ChangeSlideFocus       (setting_data1_cam["Focus"       ])
        self.ChangeSlideExposure    (setting_data1_cam["Exposure"    ])
        self.ChangeTextExposure    (setting_data1_cam["Exposure"    ])
        self.ChangeSlideSqueeze     (setting_data1_cam["Squeeze"     ])
        self.ChangeTextSqueeze     (setting_data1_cam["Squeeze"     ])
        self.ChangeSlidetIris       (setting_data1_cam["tIris"       ])
        self.ChangeTextIris       (setting_data1_cam["tIris"       ])
        self.ChangeSlideWhitePan    (setting_data1_cam["WhitePan"    ])
        self.ChangeTextPan          (setting_data1_cam["WhitePan"    ])
        self.ChangeSlideTilt        (setting_data1_cam["Tilt"        ])
        self.ChangeTextTilt        (setting_data1_cam["Tilt"        ])
        self.ChangeSlideRotation    (setting_data1_cam["Rotation"    ])
        self.ChangeTextRotation    (setting_data1_cam["Rotation"    ])

    # def UpdataFrame(self):
        # ret, frame = self.cap.read()
        # if ret:
        #     self.camera_image=frame
        #     cv_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        #     pil_image = Image.fromarray(cv_image)
        #     image_siz = pil_image.size
        #     resize_height = 600
        #     resized_image = pil_image.resize((int(image_siz[0]/(image_siz[1]/resize_height)), resize_height))
        #     tk_image = ImageTk.PhotoImage(resized_image)
        #     self.cam_canvas.create_image(500/2, 600/2, image=tk_image) 
        #     self.cam_canvas.image = tk_image 
        # 10msごとに更新
        # self.root.after(10, self.UpdataFrame)

    def UpdataFrame(self):
        img_Parameters ,cam_Parameters = self.CollectionData()
        self.cap.set(cv2.CAP_PROP_BRIGHTNESS,     img_Parameters["Brightness"  ])
        self.cap.set(cv2.CAP_PROP_CONTRAST,       img_Parameters["Contrast"    ])
        self.cap.set(cv2.CAP_PROP_HUE,            img_Parameters["Hue"         ])
        self.cap.set(cv2.CAP_PROP_SATURATION,     img_Parameters["Saturation"  ])
        #  self.cap.set(cv2.Pinto,                img_Parameters["Pinto"       ])
        self.cap.set(cv2.CAP_PROP_GAMMA,          img_Parameters["Gamma"       ])
        self.cap.set(cv2.CAP_PROP_WB_TEMPERATURE, img_Parameters["WhiteBalance"])
        #  self.cap.set(cv2.Backlight,            img_Parameters["Backlight"   ])
        self.cap.set(cv2.CAP_PROP_GAIN,           img_Parameters["Gain"        ])
        
        
        # self.cap.set(cv2.CAP_PROP_Zoom    ,     cam_Parameters["Zoom"      ])
        self.cap.set(cv2.CAP_PROP_FOCUS     ,     cam_Parameters["Focus"     ])
        self.cap.set(cv2.CAP_PROP_EXPOSURE  ,     cam_Parameters["Exposure"  ])
        # self.cap.set(cv2.CAP_PROP_Squeeze ,     cam_Parameters["Squeeze"   ])
        # self.cap.set(cv2.CAP_PROP_tIris   ,     cam_Parameters["tIris"     ])
        self.cap.set(cv2.CAP_PROP_PAN       ,     cam_Parameters["WhitePan"  ])
        self.cap.set(cv2.CAP_PROP_TILT      ,     cam_Parameters["Tilt"      ])
        self.cap.set(cv2.CAP_PROP_ROLL      ,     cam_Parameters["Rotation"  ])

        # self.root.after(10, self.UpdataFrame)

    

    ###################################################
    ##################### Change ######################
    ###################################################
    def ChangeTextBrightness(self, num):
        self.txt_Br.delete(0, tk.END)
        self.txt_Br.insert(0, num) 
        self.cap.set(cv2.CAP_PROP_BRIGHTNESS,  int(num))


    def ChangeTextContrast(self, num):
        self.txt_C.delete(0, tk.END)
        self.txt_C.insert(0, num) 
        self.cap.set(cv2.CAP_PROP_CONTRAST,   int(num))


    def ChangeTextHue(self, num):
        self.txt_H.delete(0, tk.END)
        self.txt_H.insert(0, num) 
        self.cap.set(cv2.CAP_PROP_HUE,     int(num))


    def ChangeTextSaturation(self, num):
        self.txt_S.delete(0, tk.END)
        self.txt_S.insert(0, num) 
        self.cap.set(cv2.CAP_PROP_SATURATION,   int(num))


    def ChangeTextPinto(self, num):
        self.txt_P.delete(0, tk.END)
        self.txt_P.insert(0, num) 
        #  self.cap.set(cv2.Pinto,    int(num))


    def ChangeTextGamma(self, num):
        self.txt_G.delete(0, tk.END)
        self.txt_G.insert(0, num) 
        self.cap.set(cv2.CAP_PROP_GAMMA,    int(num))
        

    def ChangeTextWhiteBalance(self, num):
        self.txt_W.delete(0, tk.END)
        self.txt_W.insert(0, num) 
        self.cap.set(cv2.CAP_PROP_WB_TEMPERATURE,  int(num))


    def ChangeTextBacklight(self, num):
        self.txt_Ba.delete(0, tk.END)
        self.txt_Ba.insert(0, num) 
        #  self.cap.set(cv2.Backlight,       int(num))


    def ChangeTextGain(self, num):
        self.txt_Ga.delete(0, tk.END)
        self.txt_Ga.insert(0, num) 
        self.cap.set(cv2.CAP_PROP_GAIN,      int(num))


    def ChangeTextZoom(self, num):
        self.txt_Z.delete(0, tk.END)
        self.txt_Z.insert(0, num) 
        # self.cap.set(cv2.CAP_PROP_Zoom    ,   int(num))

    def ChangeTextFocus(self, num):
        self.txt_F.delete(0, tk.END)
        self.txt_F.insert(0, num) 
        self.cap.set(cv2.CAP_PROP_FOCUS     ,   int(num))


    def ChangeTextExposure(self, num):
        self.txt_E.delete(0, tk.END)
        self.txt_E.insert(0, num) 
        self.cap.set(cv2.CAP_PROP_EXPOSURE  ,   int(num))

    def ChangeTextSqueeze(self, num):
        self.txt_Ap.delete(0, tk.END)
        self.txt_Ap.insert(0, num) 
        # self.cap.set(cv2.CAP_PROP_Squeeze ,   int(num))

    def ChangeTextIris(self, num):
        self.txt_A.delete(0, tk.END)
        self.txt_A.insert(0, num) 
        # self.cap.set(cv2.CAP_PROP_tIris   ,   int(num))

    def ChangeTextPan(self, num):
        self.txt_Pa.delete(0, tk.END)
        self.txt_Pa.insert(0, num) 
        self.cap.set(cv2.CAP_PROP_PAN       ,   int(num))

    def ChangeTextTilt(self, num):
        self.txt_T.delete(0, tk.END)
        self.txt_T.insert(0, num) 
        self.cap.set(cv2.CAP_PROP_TILT      ,   int(num))

    def ChangeTextRotation(self, num):
        self.txt_R.delete(0, tk.END)
        self.txt_R.insert(0, num) 
        self.cap.set(cv2.CAP_PROP_ROLL      ,   int(num))

    ####### ChangeSlideBrightness #######
    @funcdispatch()
    def ChangeSlideBrightness(self, event):
        if not event.widget.get().isdigit() :
            self.txt_Br.delete(0, tk.END)
            messagebox.showerror("Error0","数字を入力してください!!")
        else:
            self.volume_slider_Br.set( event.widget.get())
    @ChangeSlideBrightness.register
    def __(self, event: int):
        self.volume_slider_Br.set(event)
    @ChangeSlideBrightness.register
    def __(self, event: str):
        self.txt_Br.delete(0, tk.END)

    ####### ChangeSlideContrast #######
    @funcdispatch()
    def ChangeSlideContrast(self, event):
        if not event.widget.get().isdigit() :
            self.txt_C.delete(0, tk.END)
            messagebox.showerror("Error1","数字を入力してください!!")
        else:
            self.volume_slider_C.set( event.widget.get())
    @ChangeSlideContrast.register
    def __(self, event: int):
        self.volume_slider_C.set(event)
    @ChangeSlideContrast.register
    def __(self, event: str):
        if not  event:
            pass
        else:
            self.volume_slider_C.set( int(event))

    ####### ChangeSlideHue #######
    @funcdispatch()
    def ChangeSlideHue(self, event):
        if not event.widget.get().isdigit() :
            self.txt_H.delete(0, tk.END)
            messagebox.showerror("Error2","数字を入力してください!!")
        else:
            self.volume_slider_H.set( event.widget.get())

    @ChangeSlideHue.register
    def __(self, event: int):
        self.volume_slider_H.set(event)

    @ChangeSlideHue.register
    def __(self, event: str):
        if not  event:
            pass
        else:
            self.volume_slider_H.set( int(event))

    ####### ChangeSlideSaturation  #######
    @funcdispatch()
    def ChangeSlideSaturation(self, event):
        if not event.widget.get().isdigit() :
            self.txt_S.delete(0, tk.END)
            messagebox.showerror("Error3","数字を入力してください!!")
        else:
            self.volume_slider_S.set( event.widget.get())

    @ChangeSlideSaturation.register
    def __(self, event: int):
        self.volume_slider_S.set(event)

    @ChangeSlideSaturation.register
    def __(self, event: str):
        if not  event:
            pass
        else:
            self.volume_slider_S.set( int(event))

     ####### ChangeSlidePinto  #######
    @funcdispatch()
    def ChangeSlidePinto(self, event):
        if not event.widget.get().isdigit() :
            self.txt_P.delete(0, tk.END)
            messagebox.showerror("Error4","数字を入力してください!!")
        else:
            self.volume_slider_P.set( event.widget.get())

    @ChangeSlidePinto.register
    def __(self, event: int):
        self.volume_slider_P.set(event)

    @ChangeSlidePinto.register
    def __(self, event: str):
        if not  event:
            pass
        else:
            self.volume_slider_P.set( int(event))

    ####### ChangeSlideGamma  #######
    @funcdispatch()
    def ChangeSlideGamma(self, event):
        if not event.widget.get().isdigit() :
            self.txt_G.delete(0, tk.END)
            messagebox.showerror("Error5","数字を入力してください!!")
        else:
            self.volume_slider_G.set( event.widget.get())

    @ChangeSlideGamma.register
    def __(self, event: int):
        self.volume_slider_G.set(event)

    @ChangeSlideGamma.register
    def __(self, event: str):
        if not  event:
            pass
        else:
            self.volume_slider_G.set( int(event))

    ####### ChangeSlideWhiteBalance  #######
    @funcdispatch()
    def ChangeSlideWhiteBalance(self, event):
        if not event.widget.get().isdigit() :
            self.txt_W.delete(0, tk.END)
            messagebox.showerror("Error6","数字を入力してください!!")
        else:
            self.volume_slider_W.set( event.widget.get())

    @ChangeSlideWhiteBalance.register
    def __(self, event: int):
        self.volume_slider_W.set(event)

    @ChangeSlideWhiteBalance.register
    def __(self, event: str):
        if not  event:
            pass
        else:
            self.volume_slider_W.set( int(event))

    ####### ChangeSlideBacklight  #######
    @funcdispatch()
    def ChangeSlideBacklight(self, event):
        if not event.widget.get().isdigit() :
            self.txt_Ba.delete(0, tk.END)
            messagebox.showerror("Error7","数字を入力してください!!")
        else:
            self.volume_slider_Ba.set( event.widget.get())

    @ChangeSlideBacklight.register
    def __(self, event: int):
        self.volume_slider_Ba.set(event)

    @ChangeSlideBacklight.register
    def __(self, event: str):
        if not  event:
            pass
        else:
            self.volume_slider_Ba.set( int(event))

    ####### ChangeSlideGain  #######
    @funcdispatch()
    def ChangeSlideGain(self, event):
        if not event.widget.get().isdigit() :
            self.txt_Ga.delete(0, tk.END)
            messagebox.showerror("Erro8r","数字を入力してください!!")
        else:
            self.volume_slider_Ga.set( event.widget.get())

    @ChangeSlideGain.register
    def __(self, event: int):
        self.volume_slider_Ga.set(event)

    @ChangeSlideGain.register
    def __(self, event: str):
        if not  event:
            pass
        else:
            self.volume_slider_Ga.set( int(event))

    ####### ChangeSlideZoom  #######
    @funcdispatch()
    def ChangeSlideZoom(self, event):
        if not event.widget.get().isdigit() :
            self.txt_Z.delete(0, tk.END)
            messagebox.showerror("Error9","数字を入力してください!!")
        else:
            self.volume_slider_Z.set( event.widget.get())

    @ChangeSlideZoom.register
    def __(self, event: int):
        self.volume_slider_Z.set(event)

    @ChangeSlideZoom.register
    def __(self, event: str):
        if not  event:
            pass
        else:
            self.volume_slider_Z.set( int(event))

    ####### ChangeSlideFocus  #######
    @funcdispatch()
    def ChangeSlideFocus(self, event):
        if not event.widget.get().isdigit() :
            self.txt_F.delete(0, tk.END)
            messagebox.showerror("Error10","数字を入力してください!!")
        else:
            self.volume_slider_F.set( event.widget.get())

    @ChangeSlideFocus.register
    def __(self, event: int):
        self.volume_slider_F.set(event)

    @ChangeSlideFocus.register
    def __(self, event: str):
        if not  event:
            pass
        else:
            self.volume_slider_F.set( int(event))

    ####### ChangeSlideExposure  #######
    @funcdispatch()
    def ChangeSlideExposure(self, event):
        if not event.widget.get().isdigit() :
            self.txt_E.delete(0, tk.END)
            messagebox.showerror("Error11","数字を入力してください!!")
        else:
            self.volume_slider_E.set( event.widget.get())

    @ChangeSlideExposure.register
    def __(self, event: int):
        self.volume_slider_E.set(event)

    @ChangeSlideExposure.register
    def __(self, event: str):
        if not  event:
            pass
        else:
            self.volume_slider_E.set( int(event))

    ####### ChangeSlideSqueeze  #######
    @funcdispatch()
    def ChangeSlideSqueeze(self, event):
        if not event.widget.get().isdigit() :
            self.txt_Ap.delete(0, tk.END)
            messagebox.showerror("Error12","数字を入力してください!!")
        else:
            self.volume_slider_Ap.set( event.widget.get())

    @ChangeSlideSqueeze.register
    def __(self, event: int):
        self.volume_slider_Ap.set(event)

    @ChangeSlideSqueeze.register
    def __(self, event: str):
        if not  event:
            pass
        else:
            self.volume_slider_Ap.set( int(event))

    ####### ChangeSlidetIris  #######
    @funcdispatch()
    def ChangeSlidetIris(self, event):
        if not event.widget.get().isdigit() :
            self.txt_A.delete(0, tk.END)
            messagebox.showerror("Error13","数字を入力してください!!")
        else:
            self.volume_slider_A.set( event.widget.get())

    @ChangeSlidetIris.register
    def __(self, event: int):
        self.volume_slider_A.set(event)

    @ChangeSlidetIris.register
    def __(self, event: str):
        if not  event:
            pass
        else:
            self.volume_slider_A.set( int(event))

    ####### ChangeSlideWhitePan  #######
    @funcdispatch()
    def ChangeSlideWhitePan(self, event):
        if not event.widget.get().isdigit() :
            self.txt_Pa.delete(0, tk.END)
            messagebox.showerror("Error14","数字を入力してください!!")
        else:
            self.volume_slider_Pa.set( event.widget.get())

    @ChangeSlideWhitePan.register
    def __(self, event: int):
        self.volume_slider_Pa.set(event)

    @ChangeSlideWhitePan.register
    def __(self, event: str):
        if not  event:
            pass
        else:
            self.volume_slider_Pa.set( int(event))

    ####### ChangeSlideTilt  #######
    @funcdispatch()
    def ChangeSlideTilt(self, event):
        if not event.widget.get().isdigit() :
            self.txt_T.delete(0, tk.END)
            messagebox.showerror("Error15","数字を入力してください!!")
        else:
            self.volume_slider_T.set( event.widget.get())

    @ChangeSlideTilt.register
    def __(self, event: int):
        self.volume_slider_T.set(event)

    @ChangeSlideTilt.register
    def __(self, event: str):
        if not  event:
            pass
        else:
            self.volume_slider_T.set( int(event))

    ####### ChangeSlideRotation  #######
    @funcdispatch()
    def ChangeSlideRotation(self, event):
        if not event.widget.get().isdigit() :
            self.txt_R.delete(0, tk.END)
            messagebox.showerror("Error16","数字を入力してください!!")
        else:
            self.volume_slider_R.set( event.widget.get())

    @ChangeSlideRotation.register
    def __(self, event: int):
        self.volume_slider_R.set(event)

    @ChangeSlideRotation.register
    def __(self, event: str):
        if not  event:
            pass
        else:
            self.volume_slider_R.set( int(event))

    def ChangeCombobox(self, event):
        self.UpdataAllParameter()

    ######################################################
    ##################### interface ######################
    ######################################################
    

    # カメラ設定値の反映 camera_user_sttingsファイルを更新する

    def WriteCamSettings(self):
        img_Parameters ,cam_Parameters = self.CollectionData()
        if img_Parameters== None or cam_Parameters  == None:
            pass
        else:
            with open('v_1.1\Configuration\camera_user_sttings.json', "w", encoding="utf-8") as file:
                self.cam_settings_data[ "User_Setting_data"][self.combobox.current()] = {"name":self.combobox.get(),"画像の調整":img_Parameters,"カメラ制御": cam_Parameters}
                json.dump(self.cam_settings_data, file, ensure_ascii=False, indent=4)

    def ReadCamSettings(self):
        with open('v_1.1\Configuration\camera_user_sttings.json', 'r', encoding='utf-8') as file:
            data = json.load(file)
        return data

    def CollectionData(self):
        img_Parameters = {}
        img_Parameters["Brightness"   ] = int( self.txt_Br.get())
        img_Parameters["Contrast"     ] = int( self.txt_C .get())
        img_Parameters["Hue"          ] = int( self.txt_H .get())
        img_Parameters["Saturation"   ] = int( self.txt_S .get())
        img_Parameters["Pinto"        ] = int( self.txt_P .get())
        img_Parameters["Gamma"        ] = int( self.txt_G .get())
        img_Parameters["WhiteBalance" ] = int( self.txt_W .get())
        img_Parameters["Backlight"    ] = int( self.txt_Ba.get())
        img_Parameters["Gain"         ] = int( self.txt_Ga.get())

        cam_Parameters = {}
        cam_Parameters["Zoom"         ] = int(self.txt_Z .get())
        cam_Parameters["Focus"        ] = int(self.txt_F .get())
        cam_Parameters["Exposure"     ] = int(self.txt_E .get())
        cam_Parameters["Squeeze"      ] = int(self.txt_Ap.get())
        cam_Parameters["tIris"        ] = int(self.txt_A .get())
        cam_Parameters["WhitePan"     ] = int(self.txt_Pa.get())
        cam_Parameters["Tilt"         ] = int(self.txt_T .get())
        cam_Parameters["Rotation"     ] = int(self.txt_R .get())
        

        img_is_None =  [key for key, value in img_Parameters.items() if value == ""]
        cam_is_None =  [key for key, value in cam_Parameters.items() if value == ""]


        # ▽ 空文字の場合上のint()でErrorが表示されるので現状未機能状態
        if img_is_None != [] or cam_is_None != []:
            messagebox.showerror("Error17","設定値に無効な値が入力されています(空文字)")
            img_Parameters = None
            cam_Parameters = None

        return img_Parameters, cam_Parameters

    def CloseWindow(self):
        img_Parameters ,cam_Parameters = self.CollectionData()
        if self.cam_settings_data[ "User_Setting_data"][self.combobox.current()] != {"name":self.combobox.get(),"画像の調整":img_Parameters,"カメラ制御": cam_Parameters}:
            result = messagebox.askyesno("確認", "未保存の設定値が存在します \n保存して閉じますか？")
            if result:
                self.WriteCamSettings()

        self.root.destroy()


