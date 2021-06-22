import tkinter as tk
from tkinter import Tk, ttk, messagebox
import random
import math
import winsound
import ctypes
from PIL import ImageTk, Image
import sqlite3
import SettingsPlay
import webbrowser


class DataBase:
    def run_query(self, query, parameters=()):
        with sqlite3.connect('DB.db') as db:
            c = db.cursor()
            action = c.execute(query, parameters)
            db.commit()
            return action


class CenterScreen:
    def GetGeometry(self, width, height):
        frm = Tk()
        screen_height = frm.winfo_screenheight()
        screen_width = frm.winfo_screenwidth()
        frm.destroy()
        window_height = height
        window_width = width
        fw = (screen_width - window_width) // 2
        fh = (screen_height - window_height) // 2
        L = [width, height, fw, fh]
        return L


class App:
    Names = ['Liam', 'Noah', 'William', 'James', 'Oliver', 'Benjamin', 'Elijah', 'Lucas', 'Mason', 'Logan',
             'Alexander', 'Ethan', 'Jacob', 'Michael', 'Daniel', 'Henry', 'Jackson', 'Sebastian', 'Aiden', 'Matthew',
             'Samuel', 'David', 'Joseph', 'Carter', 'Owen', 'Wyatt', 'John', 'Jack', 'Luke', 'Jayden', 'Dylan', 'Grays',
             'Levi']

    PICS = ['DATA/VSCOMP/Avatar/avatars/av-1.png', 'DATA/VSCOMP/Avatar/avatars/av-2.png',
            'DATA/VSCOMP/Avatar/avatars/av-3.png', 'DATA/VSCOMP/Avatar/avatars/av-4.png',
            'DATA/VSCOMP/Avatar/avatars/av-5.png', 'DATA/VSCOMP/Avatar/avatars/av-6.png',
            'DATA/VSCOMP/Avatar/avatars/av-7.png', 'DATA/VSCOMP/Avatar/avatars/av-8.png']

    def __init__(self):
        # get Data From SQL Lite Table
        self.Ldata = []
        datas = DataBase.run_query(self, query="SELECT * FROM ProgLang")
        for data in datas:
            self.Ldata.append(data)
        # MST IS Music State (on/off)
        self.MST = True
        self.screen = Tk()
        # Play Music Of Game
        winsound.PlaySound('DATA/Sounds/bg.wav', winsound.SND_ASYNC)
        # Title For App
        if self.Ldata[0][1] == 'True':
            # French
            self.screen.title('Dé Jeux')
        else:
            self.screen.title('Dice Game')
        # ICO FOR THE APP
        self.screen.iconbitmap(default='DATA/icon.ico')
        myappid = 'mycompany.myproduct.subproduct.version'
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
        # Disable The Full Screen Option
        self.screen.resizable(0, 0)
        # Fix The Screen Resolution and to get the window at the center of screen
        LR = []
        for i in CenterScreen.GetGeometry(self, 1280, 720): LR.append(i)
        self.screen.geometry("%dx%d+%d+%d" % (LR[0], LR[1], LR[2], LR[3]))
        self.screen.protocol("WM_DELETE_WINDOW", self.DestroyApp)
        if self.Ldata[0][1] == 'True':
            # French
            bgpath = 'DATA/main_frame/bg.png'
            phP = tk.PhotoImage(file='Data/main_frame/btn-play.png')
            phM = tk.PhotoImage(file='Data/main_frame/btn-more-games.png')
        else:
            # English
            bgpath = 'DATA/main_frame/bg-eng.png'
            phP = tk.PhotoImage(file='Data/main_frame/btn-play-eng.png')
            phM = tk.PhotoImage(file='Data/main_frame/btn-more-games-eng.png')
        # Setup The Image Of Background
        bg = ImageTk.PhotoImage(Image.open(bgpath))
        self.bg = ttk.Label(self.screen, image=bg)
        self.bg.image = bg
        self.bg.place(x=-6, y=0)
        # BUTTONS OF Play
        bu1 = tk.Button(self.screen, height=145, width=321, image=phP, borderwidth=0,command=self.Modejeu)
        bu1.image = phP
        bu1.place(x=730, y=340)
        # BUTTONS OF more games
        bu2 = tk.Button(self.screen, height=180, width=575, image=phM, borderwidth=0)
        bu2.image = phM
        bu2.place(x=600, y=520)
        # BUTTONS OF option
        ph = tk.PhotoImage(file='Data/main_frame/btn-options.png')
        bu2 = tk.Button(self.screen, height=70, width=100, image=ph, borderwidth=0, command=self.Setings)
        bu2.image = ph
        bu2.place(x=20, y=630)
        # BUTTONS OF Sound
        ph = tk.PhotoImage(file='Data/main_frame/btn-sound-on.png')
        self.buS = tk.Button(self.screen, height=64, width=100, image=ph, borderwidth=0, command=self.Sound)
        self.buS.image = ph
        self.buS.place(x=144, y=639)

        # To loop Our Screen
        self.screen.mainloop()

    def Setings(self):
        self.SettingsFrame = tk.Toplevel()
        # Fix The Background Image
        if self.Ldata[0][1] == 'True':
            bgpath = 'DATA/main_frame/Settings/bg-settings.png'
        else:
            bgpath = 'DATA/main_frame/Settings/bg-settings-eng.png'
        bg = ImageTk.PhotoImage(Image.open(bgpath))
        self.bg = ttk.Label(self.SettingsFrame, image=bg)
        self.bg.image = bg
        self.bg.place(x=-4, y=0)
        # Fix The Screen Resolution and to get the window at the center of screen
        LR = []
        for i in CenterScreen.GetGeometry(self, 1280, 720): LR.append(i)
        self.SettingsFrame.geometry("%dx%d+%d+%d" % (LR[0], LR[1], LR[2], LR[3]))
        self.SettingsFrame.grab_set()
        self.SettingsFrame.resizable(0, 0)
        # BUTTON OF Close
        ph = tk.PhotoImage(file='Data/main_frame/btn-close.png')
        self.buset = tk.Button(self.SettingsFrame, height=100, width=130, image=ph, borderwidth=0, command=self.Close)
        self.buset.image = ph
        self.buset.place(x=850, y=125)
        # Image of Flags
        if self.Ldata[0][1] == 'True':
            FlagF = tk.PhotoImage(file='Data/main_frame/Settings/BT/BT_Selected/FLG-French.png')
            FlagB = tk.PhotoImage(file='Data/main_frame/Settings/BT/BT_UnSelected/FLG-Britsh.png')
        else:
            FlagF = tk.PhotoImage(file='Data/main_frame/Settings/BT/BT_UnSelected/FLG-French.png')
            FlagB = tk.PhotoImage(file='Data/main_frame/Settings/BT/BT_Selected/FLG-Britsh.png')
        # BUTTONS OF Flag French
        self.buF1 = tk.Button(self.SettingsFrame, height=95, width=195, image=FlagF, borderwidth=0, command=self.selectFlagF)
        self.buF1.image = FlagF
        self.buF1.place(x=420, y=345)
        # BUTTONS OF Flag Britsh
        self.buF2 = tk.Button(self.SettingsFrame, height=95, width=195, image=FlagB, borderwidth=0, command=self.selectFlagB)
        self.buF2.image = FlagB
        self.buF2.place(x=662, y=350)

        # BUTTONS OF Info
        ph = tk.PhotoImage(file='Data/main_frame/Settings/btn-star.png')
        self.buSinf = tk.Button(self.SettingsFrame, height=85, width=120, image=ph, borderwidth=0, command=self.web)
        self.buSinf.image = ph
        self.buSinf.place(x=590, y=475)

    def selectFlagF(self):
        if self.Ldata[0][1] == 'True':
            pass
        elif self.Ldata[0][1] == 'False':
            if messagebox.askokcancel('Dé Games', 'Are You Sure To Change Language ?'):
                DataBase.run_query(self, query="UPDATE ProgLang SET  State = 'False' WHERE Lang = 'English'")
                DataBase.run_query(self, query="UPDATE ProgLang SET  State = 'True' WHERE Lang = 'French'")
                self.screen.destroy()
                import Begin
                Begin.Start()
            else:
                pass

    def selectFlagB(self):
        if self.Ldata[1][1] == 'True':
            pass
        elif self.Ldata[1][1] == 'False':
            if messagebox.askokcancel('Dé Jeux', 'Êtes-vous sûr de changer de langue?'):
                DataBase.run_query(self, query="UPDATE ProgLang SET  State = 'False' WHERE Lang = 'French'")
                DataBase.run_query(self, query="UPDATE ProgLang SET  State = 'True' WHERE Lang = 'English'")
                self.screen.destroy()
                import Begin
                Begin.Start()
            else:
                pass

    def Close(self):
        self.SettingsFrame.destroy()

    def Sound(self):
        if not self.MST:
            self.MST = True
            ph = tk.PhotoImage(file='Data/main_frame/btn-sound-on.png')
            self.buS.config(image=ph)
            self.buS.image = ph
            winsound.PlaySound('DATA/Sounds/bg.wav', winsound.SND_ASYNC)

        else:
            self.MST = False
            ph = tk.PhotoImage(file='Data/main_frame/btn-sound-off.png')
            self.buS.config(image=ph)
            self.buS.image = ph
            winsound.PlaySound('DATA/Sounds/stop.wav', winsound.SND_ASYNC)

    def DestroyApp(self):
        if self.Ldata[0][1] == 'True':
            if messagebox.askokcancel('Dé Jeux', 'Êtes-vous sûr de sortir ?'):
                self.screen.destroy()
                exit()
            else:
                pass
        else:
            if messagebox.askokcancel('Dé Game', 'Are You Sure To Exit ?'):
                self.screen.destroy()
                exit()
            else:
                pass

    def Modejeu(self):
        self.MinF = tk.Toplevel()
        # Fix The Screen Resolution and to get the window at the center of screen
        LR = []
        for i in CenterScreen.GetGeometry(self, 1280, 720): LR.append(i)
        self.MinF.geometry("%dx%d+%d+%d" % (LR[0], LR[1], LR[2], LR[3]))

        # Setup The Image Of Background
        if self.Ldata[0][1] == 'True':
            bgpath = 'DATA/modplay/bg.png'
            comp = 'Data/modplay/btn-vs-pc.png'
            player = 'Data/modplay/btn-vs-players.png'
        else:
            bgpath = 'DATA/modplay/bg-eng.png'
            comp = 'Data/modplay/btn-vs-pc-eng.png'
            player = 'Data/modplay/btn-vs-players-eng.png'
        bg = ImageTk.PhotoImage(Image.open(bgpath))
        self.bg = ttk.Label(self.MinF, image=bg)
        self.bg.image = bg
        self.bg.place(x=-6, y=0)
        self.MinF.grab_set()
        self.MinF.resizable(0, 0)
        # BUTTON OF VScomp
        ph = tk.PhotoImage(file=comp)
        self.buset = tk.Button(self.MinF, height=202, width=306, image=ph, borderwidth=0, command=self.SelctVsComp)
        self.buset.image = ph
        self.buset.place(x=300, y=261)
        # BUTTON OF VSPlayer
        ph = tk.PhotoImage(file=player)
        self.buset = tk.Button(self.MinF, height=202, width=312, image=ph, borderwidth=0, command=self.SelctVsPlayer)
        self.buset.image = ph
        self.buset.place(x=680, y=261)
        # BUTTON OF Close
        ph = tk.PhotoImage(file='Data/VSPLAYER/editplayer/btn-close.png')
        self.buset = tk.Button(self.MinF, height=88, width=90, image=ph, borderwidth=0, command=self.MinF.destroy)
        self.buset.image = ph
        self.buset.place(x=998, y=81)

    def SelctVsComp(self):
        self.MinF.destroy()
        self.soloplay()

    def SelctVsPlayer(self):
        self.MinF.destroy()
        self.teamplay()

    def soloplay(self):
        self.screen.destroy()
        SettingsPlay.VSComp()

    def teamplay(self):
        self.screen.destroy()
        SettingsPlay.VSPlayer()

    def web(self):
        webbrowser.open('https://github.com/yessinetrigui1')
