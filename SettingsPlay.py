import tkinter as tk
from tkinter import Tk, ttk, messagebox, filedialog
import random
import math
import winsound
import ctypes
from PIL import ImageTk, Image
import sqlite3
import MainScreen
import THEGAME


class VSComp:
    # Score Max
    SM = 2
    # Players Number
    NP = 2
    # Lang Liste
    Ldata = []
    # PlayerDICT = {Player 1 :{Name:'Yessine', PicPath:'DeafultPIC'}}
    PlayerDICT = {}
    Cur = 0
    path = ''

    def __init__(self):
        self.Gframe = Tk()
        datas = MainScreen.DataBase.run_query(self, query="SELECT * FROM ProgLang")
        for data in datas:
            VSComp.Ldata.append(data)
        self.Gframe.protocol("WM_DELETE_WINDOW", self.Backtoapp)
        # Title For App
        if VSComp.Ldata[0][1] == 'True':
            # French
            self.Gframe.title('Dé Jeux')
        else:
            self.Gframe.title('Dice Game')
        # Disable The Full Screen Option
        self.Gframe.resizable(0, 0)
        # Fix The Screen Resolution and to get the window at the center of screen
        LR = []
        for i in MainScreen.CenterScreen.GetGeometry(self, 1280, 720): LR.append(i)
        self.Gframe.geometry("%dx%d+%d+%d" % (LR[0], LR[1], LR[2], LR[3]))
        self.NOP = tk.StringVar()
        if VSComp.Ldata[0][1] == 'True':
            # French
            bgpath = 'DATA/VSCOMP/bg.png'
            phP = tk.PhotoImage(file='Data/VSCOMP/btn-play-2.png')
            phM = tk.PhotoImage(file='Data/VSCOMP/btn-annuler.png')
        else:
            # English
            bgpath = 'DATA/VSCOMP/bg-eng.png'
            phP = tk.PhotoImage(file='Data/VSCOMP/btn-play-eng-2.png')
            phM = tk.PhotoImage(file='Data/VSCOMP/btn-annuler-eng.png')

        # Setup The Image Of Background
        bg = ImageTk.PhotoImage(Image.open(bgpath))
        self.bg = ttk.Label(self.Gframe, image=bg)
        self.bg.image = bg
        self.bg.place(x=-6, y=0)
        # BUTTONS OF Play
        bu1 = tk.Button(self.Gframe, height=92, width=220, image=phP, borderwidth=0, command=self.Startplay)
        bu1.image = phP
        bu1.place(x=694, y=528)
        # BUTTONS OF Cancel
        bu2 = tk.Button(self.Gframe, height=94, width=216, image=phM, borderwidth=0, command=self.Backtoapp)
        bu2.image = phM
        bu2.place(x=380, y=528)
        # BUTTONS OF Up of Player Number
        ph = tk.PhotoImage(file='Data/VSCOMP/Up1.png')
        bu2 = tk.Button(self.Gframe, height=23, width=25, image=ph, borderwidth=0, command=self.addPNum)
        bu2.image = ph
        bu2.place(x=900, y=251)
        # BUTTONS OF Dwn of Player Number
        ph = tk.PhotoImage(file='Data/VSCOMP/Dwn1.png')
        bu2 = tk.Button(self.Gframe, height=22, width=25, image=ph, borderwidth=0, command=self.remPNum)
        bu2.image = ph
        bu2.place(x=900, y=280)
        # BUTTONS OF Up Of Scroe MAx
        ph = tk.PhotoImage(file='Data/VSCOMP/Up1.png')
        bu2 = tk.Button(self.Gframe, height=23, width=25, image=ph, borderwidth=0, command=self.addSNum)
        bu2.image = ph
        bu2.place(x=900, y=351)
        # BUTTONS OF Dwn Of Scroe MAx
        ph = tk.PhotoImage(file='Data/VSCOMP/Dwn1.png')
        bu2 = tk.Button(self.Gframe, height=22, width=25, image=ph, borderwidth=0, command=self.remSNum)
        bu2.image = ph
        bu2.place(x=900, y=380)
        # Label Of Number Players
        fnt = ('Gill Sans MT', 35)
        self.NBP = ttk.Label(self.Gframe, font=fnt)
        self.NBP.config(text=VSComp.NP, background='orange', foreground='brown')
        self.NBP.place(x=833, y=246)
        # Label Of Score MAx
        self.NBS = ttk.Label(self.Gframe, font=fnt)
        self.NBS.config(text=VSComp.SM, background='orange', foreground='brown')
        self.NBS.place(x=833, y=342)
        # Label Of Names Players
        print('len(Game.PlayerDICT): ', len(VSComp.PlayerDICT))
        print('Game.Cur: ', VSComp.Cur)
        if len(VSComp.PlayerDICT) == 1:
            name = VSComp.PlayerDICT['Player ' + str(VSComp.Cur)]['Name']
        else:
            name = ''
        self.NOBP = ttk.Label(self.Gframe, text=name, font=('Gill Sans MT', 30, "bold"))
        self.NOBP.config(background='orange', foreground='brown')
        self.NOBP.place(x=410, y=435)
        # BUTTONS OF Plus
        ph = tk.PhotoImage(file='Data/VSCOMP/plus.png')
        self.buPls = tk.Button(self.Gframe, height=58, width=60, image=ph, borderwidth=0, command=self.addPName)
        self.buPls.image = ph
        self.buPls.place(x=871, y=438)
        # BUTTONS OF SettingsUsers
        ph = tk.PhotoImage(file='Data/VSCOMP/btn-setting.png')
        bu2 = tk.Button(self.Gframe, height=59, width=60, image=ph, borderwidth=0, command=self.EditPlayers)
        bu2.image = ph
        bu2.place(x=789, y=440)
        self.Gframe.mainloop()

    # Add players Number
    def addPNum(self):
        if VSComp.NP < 6:
            VSComp.NP += 1
            self.NBP.config(text=VSComp.NP)
        else:
            if VSComp.Ldata[0][1] == 'True':
                # French
                messagebox.showerror('Dé Jeux', "Vous ne pouvez pas ajouter plus de 6 joueurs!")
            else:
                messagebox.showerror('Dice Game', "You can't add more than 6 Players !")

    # Remove players Number
    def remPNum(self):
        if VSComp.NP > 2 and VSComp.NP > len(VSComp.PlayerDICT):
            VSComp.NP -= 1
            self.NBP.config(text=VSComp.NP)
        else:
            if VSComp.NP == 2:
                if VSComp.Ldata[0][1] == 'True':
                    # French
                    messagebox.showerror('Dé Jeux', "Le minimum de joueurs est de 2!")
                else:
                    messagebox.showerror('Dice Game', "Minimum of players is 2 !")
            else:
                if VSComp.Ldata[0][1] == 'True':
                    # French
                    messagebox.showerror('Dé Jeux', 'Veuillez supprimer certains joueurs !')
                else:
                    messagebox.showerror('Dice Game', "Please Remove Some players !")

    # Add Score Number
    def addSNum(self):
        if VSComp.SM < 10:
            VSComp.SM += 1
            self.NBS.config(text=VSComp.SM)
        else:
            if VSComp.Ldata[0][1] == 'True':
                # French
                messagebox.showerror('Dé Jeux', "Vous ne pouvez pas ajouter plus de 10 dans le score!")
            else:
                messagebox.showerror('Dice Game', "You can't add more than 10 In Score !")

    # Remove Score Number
    def remSNum(self):
        if VSComp.SM > 2:
            VSComp.SM -= 1
            self.NBS.config(text=VSComp.SM)
        else:
            if VSComp.Ldata[0][1] == 'True':
                # French
                messagebox.showerror('Dé Jeux', "Le score minimum est de 2!")
            else:
                messagebox.showerror('Dice Game', "Minimum of Score is 2 !")

    # Add players Name
    def PnameDE(self):
        if VSComp.Cur > 1:
            VSComp.Cur -= 1
            self.NOBP.config(text=VSComp.PlayerDICT['Player ' + str(VSComp.Cur)]['Name'], background='orange',
                             foreground='brown')

    def PnameIN(self):
        if VSComp.Cur < len(VSComp.PlayerDICT):
            VSComp.Cur += 1
            self.NOBP.config(text=VSComp.PlayerDICT['Player ' + str(VSComp.Cur)]['Name'], background='orange',
                             foreground='brown')

    def Backtoapp(self):
        VSComp.Cur = 0
        VSComp.PlayerDICT = {}
        VSComp.NP = 2
        VSComp.path = ''
        VSComp.SM = 2
        self.Gframe.destroy()
        MainScreen.App()

    def addPName(self):
        if len(VSComp.PlayerDICT) < VSComp.NP:
            self.MinF = tk.Toplevel()
            # Fix The Screen Resolution and to get the window at the center of screen
            LR = []
            for i in MainScreen.CenterScreen.GetGeometry(self, 1280, 720): LR.append(i)
            self.MinF.geometry("%dx%d+%d+%d" % (LR[0], LR[1], LR[2], LR[3]))
            # Setup The Image Of Background
            bgpath = 'DATA/VSPLAYER/AddPlayer/bg-BP-BB.png'
            bg = ImageTk.PhotoImage(Image.open(bgpath))
            self.bg = ttk.Label(self.MinF, image=bg)
            self.bg.image = bg
            self.bg.place(x=-6, y=0)
            self.MinF.grab_set()
            self.MinF.resizable(0, 0)
            # BUTTON OF Close
            ph = tk.PhotoImage(file='Data/VSPLAYER/AddPlayer/btn-close2.png')
            self.buset = tk.Button(self.MinF, height=88, width=90, image=ph, borderwidth=0,
                                   command=self.MinF.destroy)
            self.buset.image = ph
            self.buset.place(x=879, y=42)
            # BUTTONS OF OK
            ph = tk.PhotoImage(file='Data/VSPLAYER/AddPlayer/btn-ok.png')
            bu = tk.Button(self.MinF, height=100, width=345, image=ph, borderwidth=0, command=self.AddPlayerDone)
            bu.image = ph
            bu.place(x=470, y=510)
            # BUTTONS OF Pic
            ph = tk.PhotoImage(file='Data/VSPLAYER/AddPlayer/btn-add-pic.png')
            self.buPIC = tk.Button(self.MinF, height=193, width=198, image=ph, background='orange',
                                   activebackground='orange', borderwidth=0, command=self.AddPIC)
            self.buPIC.image = ph
            self.buPIC.place(x=540, y=115)
            # Label NAme
            # Label NAme
            if VSComp.Ldata[0][1] == 'True':
                self.svn2 = 'Nom de joueur:'
            else:
                self.svn2 = 'Player Name:'
            ttk.Label(self.MinF, text=self.svn2, font=('Gill Sans MT', 30), background='orange',
                      foreground='white').place(x=520, y=344)
            self.NamePLayer = ttk.Entry(self.MinF, font=('Berlin Sans fb', 28), foreground='brown')
            self.NamePLayer.place(x=420, y=440)
        else:
            if Game.Ldata[0][1] == 'True':
                messagebox.showerror('Dé Jeux', 'Vous Avez Ajouté Trop de Joueur')
            else:
                messagebox.showerror('Dice Game', 'You Added Too Many Players')

    def AddPlayerDone(self):
        if len(self.NamePLayer.get()) > 0:
            VSComp.PlayerDICT['Player ' + str(len(VSComp.PlayerDICT) + 1)] = {'Name': '', 'PathPIC': '', 'Score': '0'}
            if len(VSComp.path) > 0:
                # Adding Path to the dict
                VSComp.PlayerDICT['Player ' + str(len(VSComp.PlayerDICT))]['PathPIC'] = VSComp.path
                VSComp.path = ''
            else:
                VSComp.PlayerDICT['Player ' + str(len(VSComp.PlayerDICT))]['PathPIC'] = MainScreen.App.PICS[
                    random.randint(0, len(MainScreen.App.PICS) - 1)]
                VSComp.path = ''
            VSComp.PlayerDICT['Player ' + str(len(VSComp.PlayerDICT))]['Name'] = self.NamePLayer.get()
            self.MinF.destroy()
            VSComp.Cur += 1
            self.NOBP.config(text=VSComp.PlayerDICT['Player ' + str(VSComp.Cur)]['Name'], background='orange',
                             foreground='brown')
            self.buPls.config(state='disabled')
        else:
            if VSComp.Ldata[0][1] == 'True':
                messagebox.showerror('Dé Jeux', 'Le nom du joueur est requis !')
            else:
                messagebox.showerror('Dice Game', 'Player name is required !')

    def AddPIC(self):
        VSComp.path = filedialog.askopenfilename(filetypes=[('Files PNG', '*.png'), ('Files JPEG', '*.jpeg')])
        if len(VSComp.path) > 0:
            image = Image.open(VSComp.path)
            image = image.resize((190, 190), Image.ANTIALIAS)
            ph = ImageTk.PhotoImage(image)
            self.buPIC = tk.Button(self.MinF, height=193, width=198, image=ph, borderwidth=0, command=self.AddPIC)
            self.buPIC.image = ph
            self.buPIC.place(x=540, y=115)

    def EditPlayers(self):
        if len(VSComp.PlayerDICT) > 0:
            self.MinF = tk.Toplevel()
            # Fix The Screen Resolution and to get the window at the center of screen
            LR = []
            for i in MainScreen.CenterScreen.GetGeometry(self, 1280, 720): LR.append(i)
            self.MinF.geometry("%dx%d+%d+%d" % (LR[0], LR[1], LR[2], LR[3]))
            # Setup The Image Of Background
            if VSComp.Ldata[0][1] == 'True':
                bgpath = 'DATA/VSPLAYER/editplayer/bg.png'
            else:
                bgpath = 'DATA/VSPLAYER/editplayer/bg-eng.png'
            bg = ImageTk.PhotoImage(Image.open(bgpath))
            self.bg = ttk.Label(self.MinF, image=bg)
            self.bg.image = bg
            self.bg.place(x=-6, y=0)
            self.MinF.grab_set()
            self.MinF.resizable(0, 0)
            # BUTTON OF Close
            ph = tk.PhotoImage(file='Data/VSPLAYER/editplayer/btn-close.png')
            self.buset = tk.Button(self.MinF, height=88, width=90, image=ph, borderwidth=0, command=self.MinF.destroy)
            self.buset.image = ph
            self.buset.place(x=998, y=81)
            # BUTTON OF Supper
            ph = tk.PhotoImage(file='Data/VSPLAYER/editplayer/btn-supper.png')
            self.buset = tk.Button(self.MinF, height=67, width=49, image=ph, borderwidth=0, command=self.DeleteUsr)
            self.buset.image = ph
            self.buset.place(x=921, y=227)
            # BUTTONS OF OK
            ph = tk.PhotoImage(file='Data/VSPLAYER/editplayer/btn-ok.png')
            bu = tk.Button(self.MinF, height=78, width=187, image=ph, borderwidth=0, command=self.DoneEdit)
            bu.image = ph
            bu.place(x=545, y=430)
            # BUTTONS OF Pic
            try:
                pic = VSComp.PlayerDICT['Player ' + str(VSComp.Cur)]['PathPIC']
                VSComp.path = pic
                image = Image.open(VSComp.path)
            except:
                pic = 'Data/VSPLAYER/editplayer/btn-add-pic.png'
                VSComp.path = pic
                image = Image.open(VSComp.path)
            image = image.resize((200, 200), Image.ANTIALIAS)
            ph = ImageTk.PhotoImage(image)
            self.buPICEdit = tk.Button(self.MinF, height=193, width=198, image=ph, borderwidth=0, command=self.ChngePic)
            self.buPICEdit.image = ph
            self.buPICEdit.place(x=274, y=196)
            # BUTTONS OF  Cancel
            ph = tk.PhotoImage(file='Data/VSPLAYER/editplayer/btn-cancel.png')
            bu = tk.Button(self.MinF, height=78, width=323, image=ph, borderwidth=0, command=self.MinF.destroy)
            bu.image = ph
            bu.place(x=473, y=520)
            # Label NAme
            if VSComp.Ldata[0][1] == 'True':
                self.svn2 = 'Nom de joueur:'
            else:
                self.svn2 = 'Player Name:'
            ttk.Label(self.MinF, text=self.svn2, font=('Gill Sans MT', 28), background='orange',
                      foreground='white').place(x=530, y=230)
            self.NamePLayer = tk.Entry(self.MinF, textvariable=tk.StringVar(self.MinF, value=
            VSComp.PlayerDICT['Player ' + str(VSComp.Cur)]['Name']), font=('Berlin Sans fb', 28), foreground='brown')
            self.NamePLayer.place(x=522, y=319)
        else:
            if VSComp.Ldata[0][1] == 'True':
                messagebox.showerror('Dé Jeux', "Vous n'avez pas encore ajouté de joueurs !")
            else:
                messagebox.showerror('Dice Game', 'You Have Not Added Players yet !')

    def DoneEdit(self):
        # Saving The New Name
        # Saving The New PIC
        if len(self.NamePLayer.get()) > 0:
            VSComp.PlayerDICT['Player ' + str(VSComp.Cur)]['Name'] = self.NamePLayer.get()
            VSComp.PlayerDICT['Player ' + str(VSComp.Cur)]['PathPIC'] = VSComp.path
            VSComp.path = ''
            self.MinF.destroy()
            self.NOBP.config(text=VSComp.PlayerDICT['Player ' + str(VSComp.Cur)]['Name'], background='orange',
                             foreground='brown')

    def DeleteUsr(self):
        self.MinF.destroy()
        long = len(VSComp.PlayerDICT)
        DP = VSComp.Cur
        VSComp.path = ''
        self.buPls.config(state='normal')
        if VSComp.Cur == long:
            print('P1')
            del VSComp.PlayerDICT['Player ' + str(long)]
        else:
            print('P2')
            del VSComp.PlayerDICT['Player ' + str(VSComp.Cur)]
            for i in range(DP, long):
                VSComp.PlayerDICT['Player ' + str(i)] = VSComp.PlayerDICT['Player ' + str(i + 1)]
            del VSComp.PlayerDICT['Player ' + str(long)]
        if len(VSComp.PlayerDICT) == 0:
            if VSComp.Ldata[0][1] == 'True':
                # French
                txt = 'Aucun joueur'
            else:
                txt = 'No Players'
            self.NOBP.config(text=txt, background='orange',
                             foreground='brown')
            VSComp.Cur = 0

        else:
            if VSComp.Cur > 1:
                VSComp.Cur -= 1
            self.NOBP.config(text=VSComp.PlayerDICT['Player ' + str(VSComp.Cur)]['Name'], background='orange',
                             foreground='brown')

    def ChngePic(self):
        VSComp.path = filedialog.askopenfilename(filetypes=[('Files PNG', '*.png'), ('Files JPEG', '*.jpeg')])
        if len(VSComp.path) > 0:
            image = Image.open(VSComp.path)
            image = image.resize((190, 190), Image.ANTIALIAS)
            ph = ImageTk.PhotoImage(image)
            self.buPICEdit.config(image=ph)
            self.buPICEdit.image = ph

    def Startplay(self):
        if len(VSComp.PlayerDICT) == 1:
            print('Score Max est: ', VSComp.SM)
            print('nombre de joueur est: ', VSComp.NP)
            print('dict of players data', VSComp.PlayerDICT)
            if len(VSComp.PlayerDICT['Player ' + str(VSComp.Cur)]['PathPIC']) == 0:
                VSComp.PlayerDICT['Player ' + str(VSComp.Cur)]['PathPIC'] = MainScreen.App.PICS[
                    random.randint(0, len(MainScreen.App.PICS) - 1)]
            for i in range(2, VSComp.NP + 1):
                VSComp.PlayerDICT['Player ' + str(i)] = {
                    'Name': MainScreen.App.Names[random.randint(0, len(MainScreen.App.Names) - 1)],
                    'PathPIC': MainScreen.App.PICS[random.randint(0, len(MainScreen.App.PICS) - 1)],
                    'Score': '0'}
            self.Gframe.destroy()
            print('Game Started')
            THEGAME.VersComp()
        else:
            print('Game is Not Ready to start')


class VSPlayer:
    # Score Max
    SM = 2
    # Players Number
    NP = 2
    # Lang Liste
    Ldata = []
    # PlayerDICT = {Player 1 :{Name:'Yessine', PicPath:'DeafultPIC'}}
    PlayerDICT = {}
    Cur = 0
    path = ''
    PATHS = []

    def __init__(self):
        self.Gframe = Tk()
        datas = MainScreen.DataBase.run_query(self, query="SELECT * FROM ProgLang")
        for data in datas:
            VSPlayer.Ldata.append(data)
        self.Gframe.protocol("WM_DELETE_WINDOW", self.Backtoapp)
        # Title For App
        if VSPlayer.Ldata[0][1] == 'True':
            # French
            self.Gframe.title('Dé Jeux')
        else:
            self.Gframe.title('Dice Game')
        # Disable The Full Screen Option
        self.Gframe.resizable(0, 0)
        # Fix The Screen Resolution and to get the window at the center of screen
        LR = []
        for i in MainScreen.CenterScreen.GetGeometry(self, 1280, 720): LR.append(i)
        self.Gframe.geometry("%dx%d+%d+%d" % (LR[0], LR[1], LR[2], LR[3]))
        self.NOP = tk.StringVar()
        if VSPlayer.Ldata[0][1] == 'True':
            # French
            bgpath = 'DATA/VSPLAYER/bg-BP.png'
            phP = tk.PhotoImage(file='Data/VSPLAYER/btn-play-2.png')
            phM = tk.PhotoImage(file='Data/VSPLAYER/btn-annuler.png')
        else:
            # English
            bgpath = 'DATA/VSPLAYER/bg-BP-eng.png'
            phP = tk.PhotoImage(file='Data/VSPLAYER/btn-play-eng-2.png')
            phM = tk.PhotoImage(file='Data/VSPLAYER/btn-annuler-eng.png')
        # Setup The Image Of Background
        bg = ImageTk.PhotoImage(Image.open(bgpath))
        self.bg = ttk.Label(self.Gframe, image=bg)
        self.bg.image = bg
        self.bg.place(x=-6, y=0)
        # BUTTONS OF Play
        bu1 = tk.Button(self.Gframe, height=92, width=220, image=phP, borderwidth=0, command=self.Startplay)
        bu1.image = phP
        bu1.place(x=694, y=528)
        # BUTTONS OF Cancel
        bu2 = tk.Button(self.Gframe, height=94, width=216, image=phM, borderwidth=0, command=self.Backtoapp)
        bu2.image = phM
        bu2.place(x=380, y=528)
        # BUTTONS OF Up of Player Number
        ph = tk.PhotoImage(file='Data/VSPLAYER/Up1.png')
        bu2 = tk.Button(self.Gframe, height=23, width=25, image=ph, borderwidth=0, command=self.addPNum)
        bu2.image = ph
        bu2.place(x=900, y=251)
        # BUTTONS OF Dwn of Player Number
        ph = tk.PhotoImage(file='Data/VSPLAYER/Dwn1.png')
        bu2 = tk.Button(self.Gframe, height=22, width=25, image=ph, borderwidth=0, command=self.remPNum)
        bu2.image = ph
        bu2.place(x=900, y=280)
        # BUTTONS OF Up Of Scroe MAx
        ph = tk.PhotoImage(file='Data/VSPLAYER/Up1.png')
        bu2 = tk.Button(self.Gframe, height=23, width=25, image=ph, borderwidth=0, command=self.addSNum)
        bu2.image = ph
        bu2.place(x=900, y=351)
        # BUTTONS OF Dwn Of Scroe MAx
        ph = tk.PhotoImage(file='Data/VSPLAYER/Dwn1.png')
        bu2 = tk.Button(self.Gframe, height=22, width=25, image=ph, borderwidth=0, command=self.remSNum)
        bu2.image = ph
        bu2.place(x=900, y=380)
        # Label Of Number Players
        fnt = ('Gill Sans MT', 35)
        self.NBP = ttk.Label(self.Gframe, font=fnt)
        self.NBP.config(text=VSPlayer.NP, background='orange', foreground='brown')
        self.NBP.place(x=833, y=246)
        # Label Of Score MAx
        self.NBS = ttk.Label(self.Gframe, font=fnt)
        self.NBS.config(text=VSPlayer.SM, background='orange', foreground='brown')
        self.NBS.place(x=833, y=342)
        # Label Of Names Players
        self.NOBP = ttk.Label(self.Gframe, font=('Gill Sans MT', 30, "bold"))
        self.NOBP.config(background='orange', foreground='brown')
        self.NOBP.place(x=410, y=435)
        # BUTTONS OF Right
        ph = tk.PhotoImage(file='Data/VSPLAYER/Right.png')
        bu2 = tk.Button(self.Gframe, height=32, width=29, image=ph, borderwidth=0, command=self.PnameIN)
        bu2.image = ph
        bu2.place(x=827, y=452)
        # BUTTONS OF Left
        ph = tk.PhotoImage(file='Data/VSPLAYER/Left.png')
        bu2 = tk.Button(self.Gframe, height=32, width=29, image=ph, borderwidth=0, command=self.PnameDE)
        bu2.image = ph
        bu2.place(x=791, y=452)
        # BUTTONS OF Plus
        ph = tk.PhotoImage(file='Data/VSPLAYER/plus.png')
        bu2 = tk.Button(self.Gframe, height=58, width=60, image=ph, borderwidth=0, command=self.addPName)
        bu2.image = ph
        bu2.place(x=871, y=438)
        # BUTTONS OF SettingsUsers
        ph = tk.PhotoImage(file='Data/VSPLAYER/btn-setting.png')
        bu2 = tk.Button(self.Gframe, height=59, width=60, image=ph, borderwidth=0, command=self.EditPlayers)
        bu2.image = ph
        bu2.place(x=710, y=440)
        self.Gframe.mainloop()

    # Add players Number
    def addPNum(self):
        if VSPlayer.NP < 6:
            VSPlayer.NP += 1
            self.NBP.config(text=VSPlayer.NP)
        else:
            if VSPlayer.Ldata[0][1] == 'True':
                # French
                messagebox.showerror('Dé Jeux', "Vous ne pouvez pas ajouter plus de 6 joueurs!")
            else:
                messagebox.showerror('Dice Game', "You can't add more than 6 Players !")

    # Remove players Number
    def remPNum(self):
        if VSPlayer.NP > 2 and VSPlayer.NP > len(VSPlayer.PlayerDICT):
            VSPlayer.NP -= 1
            self.NBP.config(text=VSPlayer.NP)
        else:
            if VSPlayer.NP == 2:
                if VSPlayer.Ldata[0][1] == 'True':
                    # French
                    messagebox.showerror('Dé Jeux', "Le minimum de joueurs est de 2!")
                else:
                    messagebox.showerror('Dice Game', "Minimum of players is 2 !")
            else:
                if VSPlayer.Ldata[0][1] == 'True':
                    # French
                    messagebox.showerror('Dé Jeux', 'Veuillez supprimer certains joueurs !')
                else:
                    messagebox.showerror('Dice Game', "Please Remove Some players !")

    # Add Score Number
    def addSNum(self):
        if VSPlayer.SM < 10:
            VSPlayer.SM += 1
            self.NBS.config(text=VSPlayer.SM)
        else:
            if VSPlayer.Ldata[0][1] == 'True':
                # French
                messagebox.showerror('Dé Jeux', "Vous ne pouvez pas ajouter plus de 10 dans le score!")
            else:
                messagebox.showerror('Dice Game', "You can't add more than 10 In Score !")

    # Remove Score Number
    def remSNum(self):
        if VSPlayer.SM > 2:
            VSPlayer.SM -= 1
            self.NBS.config(text=VSPlayer.SM)
        else:
            if VSPlayer.Ldata[0][1] == 'True':
                # French
                messagebox.showerror('Dé Jeux', "Le score minimum est de 2!")
            else:
                messagebox.showerror('Dice Game', "Minimum of Score is 2 !")

    # Add players Name
    def PnameDE(self):
        if VSPlayer.Cur > 1:
            VSPlayer.Cur -= 1
            print(VSPlayer.PlayerDICT['Player ' + str(VSPlayer.Cur + 1)]['Name'])
            self.NOBP.config(text=VSPlayer.PlayerDICT['Player ' + str(VSPlayer.Cur)]['Name'], background='orange',
                             foreground='brown')

    def PnameIN(self):
        if VSPlayer.Cur < len(VSPlayer.PlayerDICT):
            VSPlayer.Cur += 1
            self.NOBP.config(text=VSPlayer.PlayerDICT['Player ' + str(VSPlayer.Cur)]['Name'], background='orange',
                             foreground='brown')

    def Backtoapp(self):
        VSPlayer.Cur = 0
        VSPlayer.PlayerDICT = {}
        VSPlayer.NP = 2
        VSPlayer.path = ''
        VSPlayer.SM = 2
        PATHS = []
        self.Gframe.destroy()
        MainScreen.App()

    def addPName(self):
        if len(VSPlayer.PlayerDICT) < VSPlayer.NP:
            if len(VSPlayer.PlayerDICT) > 0:
                VSPlayer.Cur = len(VSPlayer.PlayerDICT)
                self.NOBP.config(text=VSPlayer.PlayerDICT['Player ' + str(VSPlayer.Cur)]['Name'], background='orange',
                                 foreground='brown')
            self.MinF = tk.Toplevel()
            # Fix The Screen Resolution and to get the window at the center of screen
            LR = []
            for i in MainScreen.CenterScreen.GetGeometry(self, 1280, 720): LR.append(i)
            self.MinF.geometry("%dx%d+%d+%d" % (LR[0], LR[1], LR[2], LR[3]))
            # Setup The Image Of Background
            bgpath = 'DATA/VSPLAYER/AddPlayer/bg-BP-BB.png'
            bg = ImageTk.PhotoImage(Image.open(bgpath))
            self.bg = ttk.Label(self.MinF, image=bg)
            self.bg.image = bg
            self.bg.place(x=-6, y=0)
            self.MinF.grab_set()
            self.MinF.resizable(0, 0)
            # BUTTON OF Close
            ph = tk.PhotoImage(file='Data/VSPLAYER/AddPlayer/btn-close2.png')
            self.buset = tk.Button(self.MinF, height=88, width=90, image=ph, borderwidth=0,
                                   command=self.cancelresetedit)
            self.buset.image = ph
            self.buset.place(x=879, y=42)
            # BUTTONS OF OK
            ph = tk.PhotoImage(file='Data/VSPLAYER/AddPlayer/btn-ok.png')
            bu = tk.Button(self.MinF, height=100, width=345, image=ph, borderwidth=0, command=self.AddPlayerDone)
            bu.image = ph
            bu.place(x=470, y=510)
            # BUTTONS OF Pic
            ph = tk.PhotoImage(file='Data/VSPLAYER/AddPlayer/btn-add-pic.png')
            self.buPIC = tk.Button(self.MinF, height=120, width=133, image=ph, background='orange',
                                   activebackground='orange', borderwidth=0, command=self.AddPIC)
            self.buPIC.image = ph
            self.buPIC.place(x=574, y=157)
            # Label NAme
            if VSPlayer.Ldata[0][1] == 'True':
                self.svn2 = 'Joueur N°' + str(len(VSPlayer.PlayerDICT) + 1)
            else:
                self.svn2 = 'Player number' + str(len(VSPlayer.PlayerDICT) + 1)
            ttk.Label(self.MinF, text=self.svn2, font=('Gill Sans MT', 28), background='orange',
                      foreground='white').place(x=550, y=344)
            self.NamePLayer = ttk.Entry(self.MinF, font=('Berlin Sans fb', 28), foreground='brown')
            self.NamePLayer.place(x=420, y=440)
        else:
            if VSPlayer.Ldata[0][1] == 'True':
                messagebox.showerror('Dé Jeux', 'Vous Avez Ajouté Trop de Joueur')
            else:
                messagebox.showerror('Dice Game', 'You Added Too Many Players')

    def cancelresetedit(self):
        VSPlayer.path = ''
        self.MinF.destroy()

    def AddPlayerDone(self):
        if len(self.NamePLayer.get()) > 0:
            VSPlayer.PlayerDICT['Player ' + str(len(VSPlayer.PlayerDICT) + 1)] = {'Name': '', 'PathPIC': '',
                                                                                  'Score': '0'}
            if len(VSPlayer.path) > 0:
                print('the userr add a pic and it is: ', VSPlayer.path)
                # Adding Path to the dict
                VSPlayer.PlayerDICT['Player ' + str(len(VSPlayer.PlayerDICT))]['PathPIC'] = VSPlayer.path
                VSPlayer.path = ''
            else:
                while True:
                    randpic = MainScreen.App.PICS[random.randint(0, len(MainScreen.App.PICS) - 1)]
                    if randpic not in VSPlayer.PATHS:
                        break
                VSPlayer.PlayerDICT['Player ' + str(VSPlayer.Cur+1)]['PathPIC'] = randpic
                print('pic is:', randpic)
                VSPlayer.PATHS.append(randpic)
                VSPlayer.path = ''
            VSPlayer.PlayerDICT['Player ' + str(len(VSPlayer.PlayerDICT))]['Name'] = self.NamePLayer.get()
            self.MinF.destroy()
            VSPlayer.Cur = len(VSPlayer.PlayerDICT)
            self.NOBP.config(text=VSPlayer.PlayerDICT['Player ' + str(len(VSPlayer.PlayerDICT))]['Name'], background='orange',
                             foreground='brown')

        else:
            if VSPlayer.Ldata[0][1] == 'True':
                messagebox.showerror('Dé Jeux', 'Le nom du joueur est requis !')
            else:
                messagebox.showerror('Dice Game', 'Player name is required !')

    def AddPIC(self):
        VSPlayer.path = filedialog.askopenfilename(filetypes=[('Files PNG', '*.png'), ('Files JPEG', '*.jpeg')])
        if len(VSPlayer.path) > 0:
            image = Image.open(VSPlayer.path)
            image = image.resize((200, 200), Image.ANTIALIAS)
            ph = ImageTk.PhotoImage(image)
            # self.buPIC = tk.Button(self.MinF, height=193, width=198, image=ph, borderwidth=0, command=self.AddPIC)
            self.buPIC.config(image=ph, height=193, width=198)
            self.buPIC.image = ph
            self.buPIC.place(x=540, y=120)

    def EditPlayers(self):
        if len(VSPlayer.PlayerDICT) > 0:
            self.MinF = tk.Toplevel()
            # Fix The Screen Resolution and to get the window at the center of screen
            LR = []
            for i in MainScreen.CenterScreen.GetGeometry(self, 1280, 720): LR.append(i)
            self.MinF.geometry("%dx%d+%d+%d" % (LR[0], LR[1], LR[2], LR[3]))
            # Setup The Image Of Background
            if VSPlayer.Ldata[0][1] == 'True':
                bgpath = 'DATA/VSPLAYER/editplayer/bg.png'
            else:
                bgpath = 'DATA/VSPLAYER/editplayer/bg-eng.png'
            bg = ImageTk.PhotoImage(Image.open(bgpath))
            self.bg = ttk.Label(self.MinF, image=bg)
            self.bg.image = bg
            self.bg.place(x=-6, y=0)
            self.MinF.grab_set()
            self.MinF.resizable(0, 0)
            # get the old pic to store it
            self.oldpic = VSPlayer.PlayerDICT['Player ' + str(VSPlayer.Cur)]['PathPIC']
            # BUTTON OF Close
            ph = tk.PhotoImage(file='Data/VSPLAYER/editplayer/btn-close.png')
            self.buset = tk.Button(self.MinF, height=88, width=90, image=ph, borderwidth=0, command=self.cancelresetedit)
            self.buset.image = ph
            self.buset.place(x=998, y=81)
            # BUTTON OF Supper
            ph = tk.PhotoImage(file='Data/VSPLAYER/editplayer/btn-supper.png')
            self.buset = tk.Button(self.MinF, height=67, width=49, image=ph, borderwidth=0, command=self.DeleteUsr)
            self.buset.image = ph
            self.buset.place(x=921, y=227)
            # BUTTONS OF OK
            ph = tk.PhotoImage(file='Data/VSPLAYER/editplayer/btn-ok.png')
            bu = tk.Button(self.MinF, height=78, width=187, image=ph, borderwidth=0, command=self.DoneEdit)
            bu.image = ph
            bu.place(x=545, y=430)
            # BUTTONS OF Pic
            try:
                pic = VSPlayer.PlayerDICT['Player ' + str(VSPlayer.Cur)]['PathPIC']
                VSPlayer.path = pic
                image = Image.open(VSPlayer.path)
            except:
                pic = 'Data/VSPLAYER/editplayer/btn-add-pic.png'
                VSPlayer.path = pic
                image = Image.open(VSPlayer.path)
            image = image.resize((200, 195), Image.ANTIALIAS)
            ph = ImageTk.PhotoImage(image)
            self.buPICEdit = tk.Button(self.MinF, height=194, width=192, image=ph, borderwidth=0, command=self.ChngePic)
            self.buPICEdit.image = ph
            self.buPICEdit.place(x=275, y=198)
            # BUTTONS OF Arrow Left
            ph = tk.PhotoImage(file='Data/VSPLAYER/editplayer/btn-Left.png')
            bu = tk.Button(self.MinF, height=95, width=160, image=ph, borderwidth=0, command=self.LeftUsr)
            bu.image = ph
            bu.place(x=288, y=424)
            # BUTTONS OF Arrow Right
            ph = tk.PhotoImage(file='Data/VSPLAYER/editplayer/btn-Right.png')
            bu = tk.Button(self.MinF, height=100, width=170, image=ph, borderwidth=0, command=self.RightUsr)
            bu.image = ph
            bu.place(x=823, y=415)
            # BUTTONS OF  Cancel
            ph = tk.PhotoImage(file='Data/VSPLAYER/editplayer/btn-cancel.png')
            bu = tk.Button(self.MinF, height=78, width=323, image=ph, borderwidth=0, command=self.cancelresetedit)
            bu.image = ph
            bu.place(x=473, y=520)
            # Label NAme
            if VSPlayer.Ldata[0][1] == 'True':
                self.svn2 = 'Joueur N°' + str(VSPlayer.Cur)
            else:
                self.svn2 = 'Player number' + str(VSPlayer.Cur)
            ttk.Label(self.MinF, text=self.svn2, font=('Gill Sans MT', 28), background='orange',
                      foreground='white').place(x=530, y=230)
            self.NamePLayer = tk.Entry(self.MinF, textvariable=tk.StringVar(self.MinF, value=
            VSPlayer.PlayerDICT['Player ' + str(VSPlayer.Cur)]['Name']), font=('Berlin Sans fb', 28),
                                       foreground='brown')
            self.NamePLayer.place(x=522, y=319)
        else:
            if VSPlayer.Ldata[0][1] == 'True':
                messagebox.showerror('Dé Jeux', "Vous n'avez pas encore ajouté de joueurs !")
            else:
                messagebox.showerror('Dice Game', 'You Have Not Added Players yet !')

    def DoneEdit(self):
        # Saving The New Name
        # Saving The New PIC
        if len(self.NamePLayer.get()) > 0:
            VSPlayer.PlayerDICT['Player ' + str(VSPlayer.Cur)]['Name'] = self.NamePLayer.get()
            VSPlayer.PlayerDICT['Player ' + str(VSPlayer.Cur)]['PathPIC'] = VSPlayer.path
            # find the old pic and replace it w ith new pic
            indexoldpic = VSPlayer.PATHS.index(self.oldpic)
            VSPlayer.PATHS[indexoldpic] = VSPlayer.path
            self.oldpic = ''
            VSPlayer.path = ''
            self.MinF.destroy()
            self.NOBP.config(text=VSPlayer.PlayerDICT['Player ' + str(VSPlayer.Cur)]['Name'], background='orange',
                             foreground='brown')

    def DeleteUsr(self):
        self.MinF.destroy()
        long = len(VSPlayer.PlayerDICT)
        DP = VSPlayer.Cur
        VSPlayer.path = ''
        if VSPlayer.Cur == long:
            print('P1')
            del VSPlayer.PlayerDICT['Player ' + str(long)]
        else:
            print('P2')
            del VSPlayer.PlayerDICT['Player ' + str(VSPlayer.Cur)]
            for i in range(DP, long):
                VSPlayer.PlayerDICT['Player ' + str(i)] = VSPlayer.PlayerDICT['Player ' + str(i + 1)]
            del VSPlayer.PlayerDICT['Player ' + str(long)]
        if len(VSPlayer.PlayerDICT) == 0:
            if VSPlayer.Ldata[0][1] == 'True':
                # French
                txt = 'Aucun joueur'
            else:
                txt = 'No Players'
            self.NOBP.config(text=txt, background='orange',
                             foreground='brown')
            VSPlayer.Cur = 0

        else:
            if VSPlayer.Cur > 1:
                VSPlayer.Cur -= 1
            self.NOBP.config(text=VSPlayer.PlayerDICT['Player ' + str(VSPlayer.Cur)]['Name'], background='orange',
                             foreground='brown')

    def LeftUsr(self):
        if VSPlayer.Cur > 1:
            VSPlayer.Cur -= 1
            try:
                pic = VSPlayer.PlayerDICT['Player ' + str(VSPlayer.Cur)]['PathPIC']
                VSPlayer.path = pic
                image = Image.open(VSPlayer.path)
            except:
                pic = 'Data/VSPLAYER/editplayer/btn-add-pic.png'
                VSPlayer.path = pic
                image = Image.open(VSPlayer.path)
            image = image.resize((190, 190), Image.ANTIALIAS)
            ph = ImageTk.PhotoImage(image)
            #self.buPICEdit = tk.Button(self.MinF, height=193, width=198, image=ph, borderwidth=0, command=self.ChngePic)
            self.buPICEdit.config(image=ph)
            self.buPICEdit.image = ph
            #self.buPICEdit.place(x=275, y=193)
            # Label NAme
            if VSPlayer.Ldata[0][1] == 'True':
                self.svn2 = 'Joueur N°' + str(VSPlayer.Cur)
            else:
                self.svn2 = 'Player number' + str(VSPlayer.Cur)
            ttk.Label(self.MinF, text=self.svn2, font=('Gill Sans MT', 28), background='orange',
                      foreground='white').place(x=530, y=230)
            self.NamePLayer = tk.Entry(self.MinF, textvariable=tk.StringVar(self.MinF, value=
            VSPlayer.PlayerDICT['Player ' + str(VSPlayer.Cur)]['Name']), font=('Berlin Sans fb', 28),
                                       foreground='brown')
            self.NamePLayer.place(x=522, y=319)

    def RightUsr(self):
        if VSPlayer.Cur < len(VSPlayer.PlayerDICT):
            VSPlayer.Cur += 1

            try:
                pic = VSPlayer.PlayerDICT['Player ' + str(VSPlayer.Cur)]['PathPIC']
                VSPlayer.path = pic
                image = Image.open(VSPlayer.path)
            except:
                pic = 'Data/VSPLAYER/editplayer/btn-add-pic.png'
                VSPlayer.path = pic
                image = Image.open(VSPlayer.path)
            image = image.resize((190, 190), Image.ANTIALIAS)
            ph = ImageTk.PhotoImage(image)
            #self.buPICEdit = tk.Button(self.MinF, height=193, width=198, image=ph, borderwidth=0, command=self.ChngePic)
            self.buPICEdit.config(image=ph)
            self.buPICEdit.image = ph
            #self.buPICEdit.place(x=275, y=193)
            # Label NAme
            if VSPlayer.Ldata[0][1] == 'True':
                self.svn2 = 'Joueur N°' + str(VSPlayer.Cur)
            else:
                self.svn2 = 'Player number' + str(VSPlayer.Cur)
            ttk.Label(self.MinF, text=self.svn2, font=('Gill Sans MT', 28), background='orange',
                      foreground='white').place(x=530, y=230)
            self.NamePLayer = tk.Entry(self.MinF, textvariable=tk.StringVar(self.MinF, value=
            VSPlayer.PlayerDICT['Player ' + str(VSPlayer.Cur)]['Name']), font=('Berlin Sans fb', 28),
                                       foreground='brown')
            self.NamePLayer.place(x=522, y=319)

    def ChngePic(self):
        VSPlayer.path = filedialog.askopenfilename(filetypes=[('Files PNG', '*.png'), ('Files JPEG', '*.jpeg')])
        if len(VSPlayer.path) > 0:
            image = Image.open(VSPlayer.path)
            image = image.resize((190, 190), Image.ANTIALIAS)
            ph = ImageTk.PhotoImage(image)
            self.buPICEdit.config(image=ph)
            self.buPICEdit.image = ph

    def Startplay(self):
        if VSPlayer.NP == len(VSPlayer.PlayerDICT):
            print('Score Max est: ', VSPlayer.SM)
            print('nombre de joueur est: ', VSPlayer.NP)
            print('dict of players data', VSPlayer.PlayerDICT)
            print('Game Started')
            self.Gframe.destroy()
            THEGAME.VersPlayer()
        else:
            print('Game is Not Ready to start')
