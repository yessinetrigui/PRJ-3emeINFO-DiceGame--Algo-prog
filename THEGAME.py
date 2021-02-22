import tkinter as tk
from tkinter import Tk, ttk, messagebox
import random
import math
import winsound
import ctypes
from PIL import ImageTk, Image
import sqlite3
import SettingsPlay
import MainScreen
from threading import Thread
import time


class VersComp:
    randPos = {
        'xy1': {'D1': {'x': '608', 'y': '177'}, 'D2': {'x': '880', 'y': '342'}},
        'xy2': {'D1': {'x': '862', 'y': '170'}, 'D2': {'x': '555', 'y': '280'}},
        'xy3': {'D1': {'x': '555', 'y': '197'}, 'D2': {'x': '831', 'y': '307'}},
        'xy4': {'D1': {'x': '771', 'y': '170'}, 'D2': {'x': '540', 'y': '347'}},
        'xy5': {'D1': {'x': '558', 'y': '337'}, 'D2': {'x': '858', 'y': '337'}},
        'xy6': {'D1': {'x': '640', 'y': '199'}, 'D2': {'x': '871', 'y': '337'}},
        'xy7': {'D1': {'x': '572', 'y': '197'}, 'D2': {'x': '880', 'y': '187'}},
        'xy8': {'D1': {'x': '871', 'y': '197'}, 'D2': {'x': '561', 'y': '352'}},
        'xy9': {'D1': {'x': '532', 'y': '186'}, 'D2': {'x': '811', 'y': '277'}},
        'xy10': {'D1': {'x': '551', 'y': '221'}, 'D2': {'x': '837', 'y': '228'}}
    }
    RoundNumber = 0
    ClinetREP = False
    GameState = {
        'Player 1': {'RoundScore': '0'},
        'Player 2': {'RoundScore': '0'},
        'Player 3': {'RoundScore': '0'},
        'Player 4': {'RoundScore': '0'},
        'Player 5': {'RoundScore': '0'},
        'Player 6': {'RoundScore': '0'}
                 }

    def __init__(self):
        self.t1 = Thread(target=self.TheGameRL)
        self.screen = Tk()
        self.t1.start()
        self.t2 = Thread(target=self.TheGameLOOP)
        self.t2.start()
        self.screen.mainloop()

    def TheGameRL(self):
        # get Data From SQL Lite Table
        self.Ldata = []
        datas = MainScreen.DataBase.run_query(self, query="SELECT * FROM ProgLang")
        for data in datas:
            self.Ldata.append(data)
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
        for i in MainScreen.CenterScreen.GetGeometry(self, 1280, 740): LR.append(i)
        self.screen.geometry("%dx%d+%d+%d" % (LR[0], LR[1], LR[2], LR[3]))
        self.screen.protocol("WM_DELETE_WINDOW", exit)
        if self.Ldata[0][1] == 'True':
            # French
            if SettingsPlay.VSComp.NP == 2:
                bgpath = 'DATA/Game/bgP2.png'
            elif SettingsPlay.VSComp.NP == 3:
                bgpath = 'DATA/Game/bgP3.png'
            elif SettingsPlay.VSComp.NP == 4:
                bgpath = 'DATA/Game/bgP4.png'
            elif SettingsPlay.VSComp.NP == 5:
                bgpath = 'DATA/Game/bgP5.png'
            elif SettingsPlay.VSComp.NP == 6:
                bgpath = 'DATA/Game/bgP6.png'
        else:
            # English
            if SettingsPlay.VSComp.NP == 2:
                bgpath = 'DATA/Game/bgP2.png'
            elif SettingsPlay.VSComp.NP == 3:
                bgpath = 'DATA/Game/bgP3.png'
            elif SettingsPlay.VSComp.NP == 4:
                bgpath = 'DATA/Game/bgP4.png'
            elif SettingsPlay.VSComp.NP == 5:
                bgpath = 'DATA/Game/bgP5.png'
            elif SettingsPlay.VSComp.NP == 6:
                bgpath = 'DATA/Game/bgP6.png'
        # Setup The Image Of Background
        bg = ImageTk.PhotoImage(Image.open(bgpath))
        self.bg = ttk.Label(self.screen, image=bg)
        self.bg.image = bg
        self.bg.place(x=-5, y=0)
        # The Dices Image
        #phR = tk.PhotoImage(file='DATA/Game/DICE/1.png')
        #self.ROLL1 = tk.Label(self.screen, height=205, width=205, image=phR)
        #self.ROLL1.image = phR
        #self.ROLL1.place(x=608, y=177)
        #phR = tk.PhotoImage(file='DATA/Game/DICE/2.png')
        #self.ROLL2 = tk.Label(self.screen, height=205, width=205, image=phR)
        #self.ROLL2.image = phR
        #self.ROLL2.place(x=880, y=342)
        # BUTTONS OF Roll
        phR = tk.PhotoImage(file='DATA/Game/btn-roll.png')
        self.bu1 = tk.Button(self.screen, height=113, width=283, image=phR, borderwidth=0, command=self.player1CLICKED)
        self.bu1.image = phR
        self.bu1.place(x=695, y=580)
        # Label of Round TEXT
        Rnd = ttk.Label(self.screen, text='Round', background='orange', foreground='white', font=('Gill Sans MT', 20, "bold"))
        Rnd.place(x=1135, y=80)
        # Label of Score Max
        self.Scr = ttk.Label(self.screen, text='Score Max:  '+str(SettingsPlay.VSComp.SM), background='orange', foreground='white',
                                font=('Gill Sans MT', 20, "bold")).place(x=1057, y=682)

        # BUTTONS OF Roll
        phR = tk.PhotoImage(file='DATA/Game/btn-roll.png')
        self.bu1 = tk.Button(self.screen, height=113, width=283, image=phR, borderwidth=0, command=self.player1CLICKED)
        self.bu1.image = phR
        self.bu1.place(x=695, y=580)
        self.sp = tk.StringVar()
        self.sp.set('Now is the role of ' + SettingsPlay.VSComp.PlayerDICT['Player 1']['Name'])
        self.speak = ttk.Label(self.screen,
                               textvariable=self.sp,
                               background='orange', foreground='white',
                               font=('Gill Sans MT', 20, "bold"))
        self.speak.place(x=650, y=43)

        NameFNT = ('Gill Sans MT', 27)
        ScoreFNT = ('Berlin Sans fb', 22)
        self.PicY = 0
        self.NameY = 0
        self.ScoreY = 0
        self.RoundSCORE = 0
        self.whois = 'num1'
        for i in range(len(SettingsPlay.VSComp.PlayerDICT)):
            self.DATALoad(SettingsPlay.VSComp.PlayerDICT['Player '+str(i+1)]['PathPIC'],
                     SettingsPlay.VSComp.PlayerDICT['Player '+str(i+1)]['Name'])
        '''
        if SettingsPlay.VSComp.NP == 2:
            # PROFILE 1
            image = Image.open(SettingsPlay.VSComp.PlayerDICT['Player 1']['PathPIC'])
            image = image.resize((100, 100), Image.ANTIALIAS)
            ph = ImageTk.PhotoImage(image)
            self.picpro1 = tk.Label(self.screen, height=100, background='black', width=100, image=ph, borderwidth=0)
            self.picpro1.image = ph
            self.picpro1.place(x=48, y=280)
            # Label Of Name
            lblName1 = ttk.Label(self.screen, text=SettingsPlay.VSComp.PlayerDICT['Player 1']['Name'], font=NameFNT, background='orange', foreground='white')
            lblName1.place(x=155, y=290)
            # Label Of Score
            lblscore1 = ttk.Label(self.screen, text=SettingsPlay.VSComp.PlayerDICT['Player 1']['Score'], font=ScoreFNT, background='orange', foreground='white')
            lblscore1.place(x=173, y=338)
            # PROFILE 2
            image = Image.open(SettingsPlay.VSComp.PlayerDICT['Player 2']['PathPIC'])
            image = image.resize((100, 100), Image.ANTIALIAS)
            ph = ImageTk.PhotoImage(image)
            self.picpro2 = tk.Label(self.screen, height=100, background='black', width=100, image=ph, borderwidth=0)
            self.picpro2.image = ph
            self.picpro2.place(x=48, y=414)
            # Label Of Name
            lblName1 = ttk.Label(self.screen, text=SettingsPlay.VSComp.PlayerDICT['Player 2']['Name'], font=NameFNT, background='orange', foreground='white')
            lblName1.place(x=155, y=424)
            # Label Of Score
            lblscore1 = ttk.Label(self.screen, text=SettingsPlay.VSComp.PlayerDICT['Player 2']['Score'], font=ScoreFNT, background='orange', foreground='white')
            lblscore1.place(x=173, y=472)

        elif SettingsPlay.VSComp.NP == 3:
            # PROFILE 1
            image = Image.open('Data/GAME/img-err.png')
            image = image.resize((100, 100), Image.ANTIALIAS)
            ph = ImageTk.PhotoImage(image)
            self.picpro1 = tk.Label(self.screen, height=100, background='black', width=100, image=ph, borderwidth=0)
            self.picpro1.image = ph
            self.picpro1.place(x=48, y=226)
            # Label Of Name
            lblName1 = ttk.Label(self.screen, text=SettingsPlay.VSComp.PlayerDICT['Player 1']['Name'], font=NameFNT, background='orange', foreground='white')
            lblName1.place(x=155, y=236)
            # Label Of Score
            lblscore1 = ttk.Label(self.screen, text='Player Score', font=ScoreFNT, background='orange',
                                  foreground='white')
            lblscore1.place(x=173, y=284)
            # PROFILE 2
            image = Image.open('Data/GAME/img-err.png')
            image = image.resize((100, 100), Image.ANTIALIAS)
            ph = ImageTk.PhotoImage(image)
            self.picpro2 = tk.Label(self.screen, height=100, background='black', width=100, image=ph, borderwidth=0)
            self.picpro2.image = ph
            self.picpro2.place(x=48, y=360)
            # Label Of Name
            lblName2 = ttk.Label(self.screen, text=SettingsPlay.VSComp.PlayerDICT['Player 2']['Name'], font=NameFNT, background='orange', foreground='white')
            lblName2.place(x=155, y=370)
            # Label Of Score
            lblscore2 = ttk.Label(self.screen, text='Player Score', font=ScoreFNT, background='orange',
                                  foreground='white')
            lblscore2.place(x=173, y=418)
            # PROFILE 3
            image = Image.open('Data/GAME/img-err.png')
            image = image.resize((100, 100), Image.ANTIALIAS)
            ph = ImageTk.PhotoImage(image)
            self.picpro3 = tk.Label(self.screen, height=100, background='black', width=100, image=ph, borderwidth=0)
            self.picpro3.image = ph
            self.picpro3.place(x=48, y=494)
            # Label Of Name
            lblName3 = ttk.Label(self.screen, text=SettingsPlay.VSComp.PlayerDICT['Player 3']['Name'], font=NameFNT, background='orange', foreground='white')
            lblName3.place(x=155, y=504)
            # Label Of Score
            lblscore3 = ttk.Label(self.screen, text='Player Score', font=ScoreFNT, background='orange',
                                  foreground='white')
            lblscore3.place(x=173, y=552)
        elif SettingsPlay.VSComp.NP == 4:
            # PROFILE 1
            image = Image.open('Data/GAME/img-err.png')
            image = image.resize((100, 100), Image.ANTIALIAS)
            ph = ImageTk.PhotoImage(image)
            self.picpro1 = tk.Label(self.screen, height=100, background='black', width=100, image=ph, borderwidth=0)
            self.picpro1.image = ph
            self.picpro1.place(x=48, y=159)
            # Label Of Name
            lblName1 = ttk.Label(self.screen, text=SettingsPlay.VSComp.PlayerDICT['Player 1']['Name'], font=NameFNT, background='orange', foreground='white')
            lblName1.place(x=155, y=169)
            # Label Of Score
            lblscore1 = ttk.Label(self.screen, text='Player Score', font=ScoreFNT, background='orange',
                                  foreground='white')
            lblscore1.place(x=173, y=217)
            # PROFILE 2
            image = Image.open('Data/GAME/img-err.png')
            image = image.resize((100, 100), Image.ANTIALIAS)
            ph = ImageTk.PhotoImage(image)
            self.picpro2 = tk.Label(self.screen, height=100, background='black', width=100, image=ph, borderwidth=0)
            self.picpro2.image = ph
            self.picpro2.place(x=48, y=293)
            # Label Of Name
            lblName2 = ttk.Label(self.screen, text=SettingsPlay.VSComp.PlayerDICT['Player 2']['Name'], font=NameFNT, background='orange', foreground='white')
            lblName2.place(x=155, y=303)
            # Label Of Score
            lblscore2 = ttk.Label(self.screen, text='Player Score', font=ScoreFNT, background='orange',
                                  foreground='white')
            lblscore2.place(x=173, y=351)
            # PROFILE 3
            image = Image.open('Data/GAME/img-err.png')
            image = image.resize((100, 100), Image.ANTIALIAS)
            ph = ImageTk.PhotoImage(image)
            self.picpro3 = tk.Label(self.screen, height=100, background='black', width=100, image=ph, borderwidth=0)
            self.picpro3.image = ph
            self.picpro3.place(x=48, y=427)
            # Label Of Name
            lblName3 = ttk.Label(self.screen, text=SettingsPlay.VSComp.PlayerDICT['Player 3']['Name'], font=NameFNT, background='orange', foreground='white')
            lblName3.place(x=155, y=437)
            # Label Of Score
            lblscore3 = ttk.Label(self.screen, text='Player Score', font=ScoreFNT, background='orange',
                                  foreground='white')
            lblscore3.place(x=173, y=485)
            # PROFILE 4
            image = Image.open('Data/GAME/img-err.png')
            image = image.resize((100, 100), Image.ANTIALIAS)
            ph = ImageTk.PhotoImage(image)
            self.picpro4 = tk.Label(self.screen, height=100, background='black', width=100, image=ph, borderwidth=0)
            self.picpro4.image = ph
            self.picpro4.place(x=48, y=561)
            # Label Of Name
            lblName4 = ttk.Label(self.screen, text=SettingsPlay.VSComp.PlayerDICT['Player 4']['Name'], font=NameFNT, background='orange', foreground='white')
            lblName4.place(x=155, y=571)
            # Label Of Score
            lblscore4 = ttk.Label(self.screen, text='Player Score', font=ScoreFNT, background='orange',
                                  foreground='white')
            lblscore4.place(x=173, y=619)
        elif SettingsPlay.VSComp.NP == 5:
            # PROFILE 1
            image = Image.open('Data/GAME/img-err.png')
            image = image.resize((100, 100), Image.ANTIALIAS)
            ph = ImageTk.PhotoImage(image)
            self.picpro1 = tk.Label(self.screen, height=100, background='black', width=100, image=ph, borderwidth=0)
            self.picpro1.image = ph
            self.picpro1.place(x=48, y=92)
            # Label Of Name
            lblName1 = ttk.Label(self.screen, text=SettingsPlay.VSComp.PlayerDICT['Player 1']['Name'], font=NameFNT, background='orange', foreground='white')
            lblName1.place(x=155, y=102)
            # Label Of Score
            lblscore1 = ttk.Label(self.screen, text='Player Score', font=ScoreFNT, background='orange',
                                  foreground='white')
            lblscore1.place(x=173, y=150)
            # PROFILE 2
            image = Image.open('Data/GAME/img-err.png')
            image = image.resize((100, 100), Image.ANTIALIAS)
            ph = ImageTk.PhotoImage(image)
            self.picpro2 = tk.Label(self.screen, height=100, background='black', width=100, image=ph, borderwidth=0)
            self.picpro2.image = ph
            self.picpro2.place(x=48, y=226)
            # Label Of Name
            lblName2 = ttk.Label(self.screen, text=SettingsPlay.VSComp.PlayerDICT['Player 2']['Name'], font=NameFNT, background='orange', foreground='white')
            lblName2.place(x=155, y=236)
            # Label Of Score
            lblscore2 = ttk.Label(self.screen, text='Player Score', font=ScoreFNT, background='orange',
                                  foreground='white')
            lblscore2.place(x=173, y=284)
            # PROFILE 3
            image = Image.open('Data/GAME/img-err.png')
            image = image.resize((100, 100), Image.ANTIALIAS)
            ph = ImageTk.PhotoImage(image)
            self.picpro3 = tk.Label(self.screen, height=100, background='black', width=100, image=ph, borderwidth=0)
            self.picpro3.image = ph
            self.picpro3.place(x=48, y=360)
            # Label Of Name
            lblName3 = ttk.Label(self.screen, text=SettingsPlay.VSComp.PlayerDICT['Player 3']['Name'], font=NameFNT, background='orange', foreground='white')
            lblName3.place(x=155, y=370)
            # Label Of Score
            lblscore3 = ttk.Label(self.screen, text='Player Score', font=ScoreFNT, background='orange',
                                  foreground='white')
            lblscore3.place(x=173, y=418)
            # PROFILE 4
            image = Image.open('Data/GAME/img-err.png')
            image = image.resize((100, 100), Image.ANTIALIAS)
            ph = ImageTk.PhotoImage(image)
            self.picpro4 = tk.Label(self.screen, height=100, background='black', width=100, image=ph, borderwidth=0)
            self.picpro4.image = ph
            self.picpro4.place(x=48, y=494)
            # Label Of Name
            lblName4 = ttk.Label(self.screen, text=SettingsPlay.VSComp.PlayerDICT['Player 4']['Name'], font=NameFNT, background='orange', foreground='white')
            lblName4.place(x=155, y=504)
            # Label Of Score
            lblscore4 = ttk.Label(self.screen, text='Player Score', font=ScoreFNT, background='orange',
                                  foreground='white')
            lblscore4.place(x=173, y=552)
            # PROFILE 5
            image = Image.open('Data/GAME/img-err.png')
            image = image.resize((100, 100), Image.ANTIALIAS)
            ph = ImageTk.PhotoImage(image)
            self.picpro5 = tk.Label(self.screen, height=100, background='black', width=100, image=ph, borderwidth=0)
            self.picpro5.image = ph
            self.picpro5.place(x=48, y=628)
            # Label Of Name
            lblName5 = ttk.Label(self.screen, text=SettingsPlay.VSComp.PlayerDICT['Player 5']['Name'], font=NameFNT, background='orange', foreground='white')
            lblName5.place(x=155, y=638)
            # Label Of Score
            lblscore5 = ttk.Label(self.screen, text='Player Score', font=ScoreFNT, background='orange',
                                  foreground='white')
            lblscore5.place(x=173, y=686)
        elif SettingsPlay.VSComp.NP == 6:
            # PROFILE 1
            image = Image.open(SettingsPlay.VSComp.PlayerDICT['Player 1']['PathPIC'])
            image = image.resize((100, 100), Image.ANTIALIAS)
            ph = ImageTk.PhotoImage(image)
            self.picpro1 = tk.Label(self.screen, height=100, background='black', width=100, image=ph, borderwidth=0)
            self.picpro1.image = ph
            self.picpro1.place(x=48, y=25)
            # Label Of Name
            lblName1 = ttk.Label(self.screen, text=SettingsPlay.VSComp.PlayerDICT['Player 1']['Name'], font=NameFNT, background='orange', foreground='white')
            lblName1.place(x=155, y=35)
            # Label Of Score
            lblscore1 = ttk.Label(self.screen, text=SettingsPlay.VSComp.PlayerDICT['Player 1']['Score'], font=ScoreFNT, background='orange',
                                  foreground='white')
            lblscore1.place(x=173, y=83)
            # PROFILE 2
            image = Image.open(SettingsPlay.VSComp.PlayerDICT['Player 2']['PathPIC'])
            image = image.resize((100, 100), Image.ANTIALIAS)
            ph = ImageTk.PhotoImage(image)
            self.picpro2 = tk.Label(self.screen, height=100, background='black', width=100, image=ph, borderwidth=0)
            self.picpro2.image = ph
            self.picpro2.place(x=48, y=159)
            # Label Of Name
            lblName2 = ttk.Label(self.screen, text=SettingsPlay.VSComp.PlayerDICT['Player 2']['Name'], font=NameFNT, background='orange', foreground='white')
            lblName2.place(x=155, y=169)
            # Label Of Score
            lblscore2 = ttk.Label(self.screen, text=SettingsPlay.VSComp.PlayerDICT['Player 2']['Score'], font=ScoreFNT, background='orange',
                                  foreground='white')
            lblscore2.place(x=173, y=217)
            # PROFILE 3
            image = Image.open(SettingsPlay.VSComp.PlayerDICT['Player 3']['PathPIC'])
            image = image.resize((100, 100), Image.ANTIALIAS)
            ph = ImageTk.PhotoImage(image)
            self.picpro3 = tk.Label(self.screen, height=100, background='black', width=100, image=ph, borderwidth=0)
            self.picpro3.image = ph
            self.picpro3.place(x=48, y=293)
            # Label Of Name
            lblName3 = ttk.Label(self.screen, text=SettingsPlay.VSComp.PlayerDICT['Player 3']['Name'], font=NameFNT, background='orange', foreground='white')
            lblName3.place(x=155, y=303)
            # Label Of Score
            lblscore3 = ttk.Label(self.screen, text=SettingsPlay.VSComp.PlayerDICT['Player 3']['Score'], font=ScoreFNT, background='orange',
                                  foreground='white')
            lblscore3.place(x=173, y=351)
            # PROFILE 4
            image = Image.open(SettingsPlay.VSComp.PlayerDICT['Player 4']['PathPIC'])
            image = image.resize((100, 100), Image.ANTIALIAS)
            ph = ImageTk.PhotoImage(image)
            self.picpro4 = tk.Label(self.screen, height=100, background='black', width=100, image=ph, borderwidth=0)
            self.picpro4.image = ph
            self.picpro4.place(x=48, y=427)
            # Label Of Name
            lblName4 = ttk.Label(self.screen, text=SettingsPlay.VSComp.PlayerDICT['Player 4']['Name'], font=NameFNT, background='orange', foreground='white')
            lblName4.place(x=155, y=437)
            # Label Of Score
            lblscore4 = ttk.Label(self.screen, text=SettingsPlay.VSComp.PlayerDICT['Player 4']['Score'], font=ScoreFNT, background='orange',
                                  foreground='white')
            lblscore4.place(x=173, y=485)
            # PROFILE 5
            image = Image.open(SettingsPlay.VSComp.PlayerDICT['Player 5']['PathPIC'])
            image = image.resize((100, 100), Image.ANTIALIAS)
            ph = ImageTk.PhotoImage(image)
            self.picpro5 = tk.Label(self.screen, height=100, background='black', width=100, image=ph, borderwidth=0)
            self.picpro5.image = ph
            self.picpro5.place(x=48, y=561)
            # Label Of Name
            lblName5 = ttk.Label(self.screen, text=SettingsPlay.VSComp.PlayerDICT['Player 5']['Name'], font=NameFNT, background='orange', foreground='white')
            lblName5.place(x=155, y=571)
            # Label Of Score
            lblscore5 = ttk.Label(self.screen, text=SettingsPlay.VSComp.PlayerDICT['Player 5']['Score'], font=ScoreFNT, background='orange',
                                  foreground='white')
            lblscore5.place(x=173, y=619)
            # PROFILE 6
            image = Image.open(SettingsPlay.VSComp.PlayerDICT['Player 6']['PathPIC'])
            image = image.resize((100, 100), Image.ANTIALIAS)
            ph = ImageTk.PhotoImage(image)
            self.picpro6 = tk.Label(self.screen, height=100, background='black', width=100, image=ph, borderwidth=0)
            self.picpro6.image = ph
            self.picpro6.place(x=48, y=695)
            # Label Of Name
            lblName6 = ttk.Label(self.screen, text=SettingsPlay.VSComp.PlayerDICT['Player 6']['Name'], font=NameFNT, background='orange', foreground='white')
            lblName6.place(x=155, y=705)
            # Label Of Score
            lblscore6 = ttk.Label(self.screen, text=SettingsPlay.VSComp.PlayerDICT['Player 6']['Score'], font=ScoreFNT, background='orange',
                                  foreground='white')
            lblscore6.place(x=173, y=753)
'''

    def TheGameLOOP(self):
        Scores = []
        if SettingsPlay.VSComp.SM not in Scores:
            # append to list th check if anyone of players get the max score
            for i in range(1, len(SettingsPlay.VSComp.PlayerDICT)):
                Scores.append(SettingsPlay.VSComp.PlayerDICT['Player '+str(i+1)])
            if SettingsPlay.VSComp.SM in Scores:
                self.GameFinished()
            self.t3 = Thread(target=self.Player1)
            self.t3.start()

    def DATALoad(self, pic, name, score='x'):
            NameFNT = ('Gill Sans MT', 27)
            ScoreFNT = ('Berlin Sans fb', 22)
            image = Image.open(pic)
            image = image.resize((100, 85), Image.ANTIALIAS)
            ph = ImageTk.PhotoImage(image)
            self.pic = tk.Label(self.screen, height=85, background='black', width=99, image=ph, borderwidth=0)
            self.pic.image = ph
            self.PicY += 115
            self.NameY += 115
            self.ScoreY += 115
            self.RoundSCORE += 134
            if self.whois == 'num1':
                self.PicY = 20
                self.NameY = 21
                self.ScoreY = 63
                self.RoundSCORE = 97
                self.whois = 'None'
            self.pic.place(x=54, y=self.PicY)
            # Label Of Name
            lblName1 = ttk.Label(self.screen, text=name, font=NameFNT, background='orange', foreground='white')
            lblName1.place(x=168, y=self.NameY)
            # Label Of Score
            lblscore1 = ttk.Label(self.screen, text='Score: '+score, font=ScoreFNT, background='orange', foreground='white')
            lblscore1.place(x=180, y=self.ScoreY)

    def RoundUpdate(self):
        # reset the scores of this round
        VersComp.GameState = {
            'Player 1': {'RoundScore': '0'},
            'Player 2': {'RoundScore': '0'},
            'Player 3': {'RoundScore': '0'},
            'Player 4': {'RoundScore': '0'},
            'Player 5': {'RoundScore': '0'},
            'Player 6': {'RoundScore': '0'}
        }
        return

    def Player1(self):
        # Label of Round NUmber
        VersComp.RoundNumber += 1
        self.Nround = ttk.Label(self.screen, text='N°' + str(VersComp.RoundNumber), background='orange',
                                foreground='white',
                                font=('Gill Sans MT', 20, "bold")).place(x=1155, y=110)


        # BUTTONS OF Roll
        phR = tk.PhotoImage(file='DATA/Game/btn-roll.png')
        self.bu1 = tk.Button(self.screen, height=113, width=283, image=phR, borderwidth=0, command=self.player1CLICKED)
        self.bu1.image = phR
        self.bu1.place(x=695, y=580)
        if VersComp.ClinetREP:
            breakpoint()
        time.sleep(5)

    def player1CLICKED(self):
        try:
            self.ROLL1.destroy()
            self.ROLL2.destroy()
        except:
            pass
        ScoreFNT = ('Berlin Sans fb', 22)
        VersComp.ClinetREP =True
        self.bu1.config(state='disabled')
        # Random the pic of roll
        # waiting some seconds
        # saving his data (data of how much he get in the face of any of this dice)
        # waiting some seconds
        NUm1 = random.randint(1, 6)
        NUm2 = random.randint(1, 6)
        # The Dices Image
        phR = tk.PhotoImage(file='DATA/Game/DICE/' + str(NUm1) + '.png')
        self.ROLL1 = tk.Label(self.screen, height=205, width=205, image=phR)
        self.ROLL1.image = phR

        phR = tk.PhotoImage(file='DATA/Game/DICE/' + str(NUm2) + '.png')
        self.ROLL2 = tk.Label(self.screen, height=205, width=205, image=phR)
        self.ROLL2.image = phR
        # placing the dices randomly
        numx = random.randint(1, 10)

        self.ROLL1.place(x=VersComp.randPos['xy'+str(numx)]['D1']['x'], y=VersComp.randPos['xy'+str(numx)]['D1']['y'])
        self.ROLL2.place(x=VersComp.randPos['xy'+str(numx)]['D2']['x'], y=VersComp.randPos['xy'+str(numx)]['D2']['y'])
        #self.ROLL1.place(x=608, y=177)
        #self.ROLL2.place(x=880, y=342)
        VersComp.GameState['Player 1']['RoundScore'] = NUm1+NUm2
        # Label Of Score ROUND score
        self.RoundSCORELBL = ttk.Label(self.screen, text='0', font=ScoreFNT, background='orange',
                                       foreground='white')
        self.RoundSCORELBL.config(text=NUm1+NUm2)
        self.RoundSCORELBL.place(x=315, y=62)
        VersComp.GameState['Player 1']['RoundScore'] = NUm1+NUm2
        self.t3 = Thread(target=self.ContinueBotsPlaying)
        self.t3.start()

    def ContinueBotsPlaying(self):
        ScoreFNT = ('Berlin Sans fb', 22)
        # generating random pic of dices
        # saving data returned
        # waiting some seconds
        # go to the next bot if there is
        # if not get back to the player number one
        playeris = 'P2'
        while playeris != 'NextRound':

            self.sp.set('Now is the role of ' + SettingsPlay.VSComp.PlayerDICT['Player ' + playeris[-1]]['Name'])
            NUm1 = random.randint(1, 6)
            NUm2 = random.randint(1, 6)
            # The Dices Image
            time.sleep(5)
            self.ROLL1.destroy()
            self.ROLL2.destroy()
            phR = tk.PhotoImage(file='DATA/Game/DICE/'+str(NUm1)+'.png')
            self.ROLL1 = tk.Label(self.screen, height=205, width=205, image=phR)
            self.ROLL1.image = phR

            phR = tk.PhotoImage(file='DATA/Game/DICE/'+str(NUm2)+'.png')
            self.ROLL2 = tk.Label(self.screen, height=205, width=205, image=phR)
            self.ROLL2.image = phR
            numx = random.randint(1, 10)

            self.ROLL1.place(x=VersComp.randPos['xy' + str(numx)]['D1']['x'],
                             y=VersComp.randPos['xy' + str(numx)]['D1']['y'])
            self.ROLL2.place(x=VersComp.randPos['xy' + str(numx)]['D2']['x'],
                             y=VersComp.randPos['xy' + str(numx)]['D2']['y'])

            #self.ROLL1.place(x=608, y=177)
            #self.ROLL2.place(x=880, y=342)
            self.RoundSCORELBL = ttk.Label(self.screen, text='0', font=ScoreFNT, background='orange',
                                           foreground='white')
            self.RoundSCORELBL.config(text=NUm1 + NUm2)
            VersComp.GameState['Player '+str(playeris[-1])]['RoundScore'] = NUm1 + NUm2
            self.RoundSCORELBL.place(x=315, y=177+(115*(int(playeris[-1])-2)))
            # adding +1 in the playeris to go to the next player
            playeris= playeris[0] + str(int(playeris[1])+1)
            if playeris == 'P'+str(SettingsPlay.VSComp.NP+1):
                playeris = 'NextRound'
                time.sleep(3)
                ListofScores = []
                for i in VersComp.GameState:
                    ListofScores.append(int(VersComp.GameState[i]['RoundScore']))
                mx = max(ListofScores)
                # go on loop and check the biggest number and if we got two biggest number w add them +1
                try:
                    while ListofScores.index(mx) != -1:
                        numP = int(ListofScores.index(mx)) + 1
                        SettingsPlay.VSComp.PlayerDICT['Player ' + str(numP)]['Score'] = str(int(SettingsPlay.VSComp.PlayerDICT['Player ' + str(numP)]['Score']) + 1)
                        ListofScores[ListofScores.index(mx)] = 0
                except:
                    pass
                # check the final score
                ListofScoresFINAL = []
                ListofNamesFINAL = []
                for i in SettingsPlay.VSComp.PlayerDICT:
                    if SettingsPlay.VSComp.SM == int(SettingsPlay.VSComp.PlayerDICT[i]['Score']):
                            self.t3 = Thread(target=self.THEWINNER(i))
                            self.t3.start()


                    #ListofScoresFINAL.append(int(SettingsPlay.VSComp.PlayerDICT[i]['Score']))
                    #ListofNamesFINAL.append(int(SettingsPlay.VSComp.PlayerDICT[i]['Name']))
               # if SettingsPlay.VSComp.SM in ListofScoresFINAL:

                    #exit()
                self.PicY = 0
                self.NameY = 0
                self.ScoreY = 0
                self.RoundSCORE = 0
                self.whois = 'num1'
                for i in range(len(SettingsPlay.VSComp.PlayerDICT)):
                    self.DATALoad(SettingsPlay.VSComp.PlayerDICT['Player ' + str(i + 1)]['PathPIC'],
                                  SettingsPlay.VSComp.PlayerDICT['Player ' + str(i + 1)]['Name'],
                                  SettingsPlay.VSComp.PlayerDICT['Player ' + str(i + 1)]['Score'])

        # get the scores of all players and get the biggest score



        self.Player1()
        return



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

    def THEWINNER(self, i):
        NameFNT = ('Gill Sans MT', 27)
        self.screenF = tk.Toplevel()
        self.screenF.overrideredirect(True)
        self.screenF.wm_attributes("-topmost", True)
        LR = []
        for f in MainScreen.CenterScreen.GetGeometry(self, 1270, 740): LR.append(f)
        self.screenF.geometry("%dx%d+%d+%d" % (LR[0], LR[1], LR[2], LR[3]))
        # Setup The Image Of Background
        if self.Ldata[0][1] == 'True':
            # French
            bgpath = 'DATA/Game/winner/bg.png'
        else:
            bgpath = 'DATA/Game/winner/bg-eng.png'
        bg = ImageTk.PhotoImage(Image.open(bgpath))
        self.bg = ttk.Label(self.screenF, image=bg)
        self.bg.image = bg
        self.bg.place(x=-5, y=0)
        image = Image.open(SettingsPlay.VSComp.PlayerDICT[i]['PathPIC'])
        image = image.resize((150, 150), Image.ANTIALIAS)
        ph = ImageTk.PhotoImage(image)
        self.pic = tk.Label(self.screenF, height=148, background='black', width=148, image=ph,
                            borderwidth=0)
        self.pic.image = ph
        self.pic.place(x=565, y=295)
        # Label Of Name
        lblName1 = ttk.Label(self.screenF, text=SettingsPlay.VSComp.PlayerDICT[i]['Name'], font=NameFNT,
                             background='orange',
                             foreground='white')
        lblName1.place(x=565, y=500)

        # BUTTON OF Close
        ph = tk.PhotoImage(file='Data/VSPLAYER/editplayer/btn-close.png')
        self.buset = tk.Button(self.screenF, height=88, width=90, image=ph, borderwidth=0, command=self.xit)
        self.buset.image = ph
        self.buset.place(x=996, y=83)

    def xit(self):
        self.t1.join()
        self.t2.join()
        self.t3.join()

        self.screen.destroy()
        import Begin
        Begin.Start()


class VersPlayer:
    randPos = {
        'xy1': {'D1': {'x': '608', 'y': '177'}, 'D2': {'x': '880', 'y': '342'}},
        'xy2': {'D1': {'x': '862', 'y': '170'}, 'D2': {'x': '555', 'y': '280'}},
        'xy3': {'D1': {'x': '555', 'y': '197'}, 'D2': {'x': '831', 'y': '307'}},
        'xy4': {'D1': {'x': '771', 'y': '170'}, 'D2': {'x': '540', 'y': '347'}},
        'xy5': {'D1': {'x': '558', 'y': '337'}, 'D2': {'x': '858', 'y': '337'}},
        'xy6': {'D1': {'x': '640', 'y': '199'}, 'D2': {'x': '871', 'y': '337'}},
        'xy7': {'D1': {'x': '572', 'y': '197'}, 'D2': {'x': '880', 'y': '187'}},
        'xy8': {'D1': {'x': '871', 'y': '197'}, 'D2': {'x': '561', 'y': '352'}},
        'xy9': {'D1': {'x': '532', 'y': '186'}, 'D2': {'x': '811', 'y': '277'}},
        'xy10': {'D1': {'x': '551', 'y': '221'}, 'D2': {'x': '837', 'y': '228'}}
    }
    RoundNumber = 0
    ClinetREP = False
    GameState = {
        'Player 1': {'RoundScore': '0'},
        'Player 2': {'RoundScore': '0'},
        'Player 3': {'RoundScore': '0'},
        'Player 4': {'RoundScore': '0'},
        'Player 5': {'RoundScore': '0'},
        'Player 6': {'RoundScore': '0'}
    }
    wherei = 1

    def __init__(self):

        self.t1 = Thread(target=self.TheGameScreen)
        self.screen = Tk()
        self.t1.start()
        self.t2 = Thread(target=self.TheGameBackend)
        self.t2.start()
        self.screen.mainloop()

    def DATALoad(self, pic, name, score='.'):
        NameFNT = ('Gill Sans MT', 27)
        ScoreFNT = ('Berlin Sans fb', 22)
        image = Image.open(pic)
        image = image.resize((100, 85), Image.ANTIALIAS)
        ph = ImageTk.PhotoImage(image)
        self.pic = tk.Label(self.screen, height=85, background='black', width=99, image=ph, borderwidth=0)
        self.pic.image = ph
        self.PicY += 115
        self.NameY += 115
        self.ScoreY += 115
        self.RoundSCORE += 134
        if self.whois == 'num1':
            self.PicY = 20
            self.NameY = 21
            self.ScoreY = 63
            self.RoundSCORE = 97
            self.whois = 'None'
        self.pic.place(x=54, y=self.PicY)
        # Label Of Name
        lblName1 = ttk.Label(self.screen, text=name, font=NameFNT, background='orange', foreground='white')
        lblName1.place(x=168, y=self.NameY)
        # Label Of Score
        lblscore1 = ttk.Label(self.screen, text='Score: ' + score, font=ScoreFNT, background='orange',
                              foreground='white')
        lblscore1.place(x=180, y=self.ScoreY)

    def TheGameScreen(self):

        # get Data From SQL Lite Table
        self.Ldata = []
        datas = MainScreen.DataBase.run_query(self, query="SELECT * FROM ProgLang")
        for data in datas:
            self.Ldata.append(data)
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
        for i in MainScreen.CenterScreen.GetGeometry(self, 1280, 740): LR.append(i)
        self.screen.geometry("%dx%d+%d+%d" % (LR[0], LR[1], LR[2], LR[3]))
        self.screen.protocol("WM_DELETE_WINDOW", exit)
        if self.Ldata[0][1] == 'True':
            # French
            if SettingsPlay.VSPlayer.NP == 2:
                bgpath = 'DATA/Game/bgP2.png'
            elif SettingsPlay.VSPlayer.NP == 3:
                bgpath = 'DATA/Game/bgP3.png'
            elif SettingsPlay.VSPlayer.NP == 4:
                bgpath = 'DATA/Game/bgP4.png'
            elif SettingsPlay.VSPlayer.NP == 5:
                bgpath = 'DATA/Game/bgP5.png'
            elif SettingsPlay.VSPlayer.NP == 6:
                bgpath = 'DATA/Game/bgP6.png'
        else:
            # English
            if SettingsPlay.VSPlayer.NP == 2:
                bgpath = 'DATA/Game/bgP2.png'
            elif SettingsPlay.VSPlayer.NP == 3:
                bgpath = 'DATA/Game/bgP3.png'
            elif SettingsPlay.VSPlayer.NP == 4:
                bgpath = 'DATA/Game/bgP4.png'
            elif SettingsPlay.VSPlayer.NP == 5:
                bgpath = 'DATA/Game/bgP5.png'
            elif SettingsPlay.VSPlayer.NP == 6:
                bgpath = 'DATA/Game/bgP6.png'
        # Setup The Image Of Background
        bg = ImageTk.PhotoImage(Image.open(bgpath))
        self.bg = ttk.Label(self.screen, image=bg)
        self.bg.image = bg
        self.bg.place(x=-5, y=0)

        # Label of Round TEXT
        Rnd = ttk.Label(self.screen, text='Round', background='orange', foreground='white',
                        font=('Gill Sans MT', 20, "bold"))
        Rnd.place(x=1135, y=80)
        # Label of Score Max
        self.Scr = ttk.Label(self.screen, text='Score Max:  ' + str(SettingsPlay.VSPlayer.SM), background='orange',
                             foreground='white',
                             font=('Gill Sans MT', 20, "bold")).place(x=1057, y=682)

        # BUTTONS OF Roll
        phR = tk.PhotoImage(file='DATA/Game/btn-roll.png')
        self.bu1 = tk.Button(self.screen, height=113, width=283, image=phR, borderwidth=0, command=None)
        self.bu1.image = phR
        self.bu1.place(x=695, y=580)
        # Text of the game
        self.sp = tk.StringVar()
        self.sp.set('Change This !!')
        self.speak = ttk.Label(self.screen,
                               textvariable=self.sp,
                               background='orange', foreground='white',
                               font=('Gill Sans MT', 20, "bold"))
        self.speak.place(x=650, y=43)

        NameFNT = ('Gill Sans MT', 27)
        ScoreFNT = ('Berlin Sans fb', 22)
        self.PicY = 0
        self.NameY = 0
        self.ScoreY = 0
        self.RoundSCORE = 0
        self.whois = 'num1'
        for i in range(len(SettingsPlay.VSPlayer.PlayerDICT)):
            self.DATALoad(SettingsPlay.VSPlayer.PlayerDICT['Player ' + str(i + 1)]['PathPIC'],
                          SettingsPlay.VSPlayer.PlayerDICT['Player ' + str(i + 1)]['Name'])

    def TheGameBackend(self):
        self.setat()
        time.sleep(0.1)
        self.player1()

    def setat(self):
        setattr(VersPlayer, 'sp', tk.StringVar())

    def player1(self):
        VersPlayer.RoundNumber += 1
        self.Nround = ttk.Label(self.screen, text='N°' + str(VersPlayer.RoundNumber), background='orange',
                                foreground='white',
                                font=('Gill Sans MT', 20, "bold")).place(x=1155, y=110)

        self.sp.set('Now is The Role Of ' + SettingsPlay.VSPlayer.PlayerDICT['Player 1']['Name'])
        # BUTTONS OF Roll
        phR = tk.PhotoImage(file='DATA/Game/btn-roll.png')
        self.bu1 = tk.Button(self.screen, height=113, width=283, image=phR, borderwidth=0, command=self.player1CLICKED)
        self.bu1.image = phR
        self.bu1.place(x=695, y=580)

    def player1CLICKED(self):
        try:
            self.ROLL1.destroy()
            self.ROLL2.destroy()
        except:
            pass
        ScoreFNT = ('Berlin Sans fb', 22)
        # Random the pic of roll
        # waiting some seconds
        # saving his data (data of how much he get in the face of any of this dice)
        # waiting some seconds
        NUm1 = random.randint(1, 6)
        NUm2 = random.randint(1, 6)
        # The Dices Image
        phR = tk.PhotoImage(file='DATA/Game/DICE/' + str(NUm1) + '.png')
        self.ROLL1 = tk.Label(self.screen, height=205, width=205, image=phR)
        self.ROLL1.image = phR

        phR = tk.PhotoImage(file='DATA/Game/DICE/' + str(NUm2) + '.png')
        self.ROLL2 = tk.Label(self.screen, height=205, width=205, image=phR)
        self.ROLL2.image = phR
        # placing the dices randomly
        numx = random.randint(1, 10)

        self.ROLL1.place(x=VersComp.randPos['xy'+str(numx)]['D1']['x'], y=VersPlayer.randPos['xy'+str(numx)]['D1']['y'])
        self.ROLL2.place(x=VersComp.randPos['xy'+str(numx)]['D2']['x'], y=VersPlayer.randPos['xy'+str(numx)]['D2']['y'])
        VersPlayer.GameState['Player 1']['RoundScore'] = NUm1+NUm2
        # Label Of Score ROUND score
        x = NUm1+NUm2
        if x<10:
            x = '_'+str(x)
        if x==11:
            x = '_' + str(x)
        self.RoundSCORELBL = ttk.Label(self.screen, text=x, font=ScoreFNT, background='orange', foreground='white')
        self.RoundSCORELBL.place(x=315, y=62)
        # player of 2
        self.player2()
        # BUTTONS OF Roll
        phR = tk.PhotoImage(file='DATA/Game/btn-roll.png')
        self.bu1 = tk.Button(self.screen, height=113, width=283, image=phR, borderwidth=0, command=self.player2CLICKED)
        self.bu1.image = phR
        self.bu1.place(x=695, y=580)

    def player2(self):
        self.sp.set('Now is The Role Of ' + SettingsPlay.VSPlayer.PlayerDICT['Player 2']['Name'])

    def player2CLICKED(self):
        try:
            self.ROLL1.destroy()
            self.ROLL2.destroy()
        except:
            pass
        ScoreFNT = ('Berlin Sans fb', 22)
        # Random the pic of roll
        # waiting some seconds
        # saving his data (data of how much he get in the face of any of this dice)
        # waiting some seconds
        NUm1 = random.randint(1, 6)
        NUm2 = random.randint(1, 6)
        # The Dices Image
        phR = tk.PhotoImage(file='DATA/Game/DICE/' + str(NUm1) + '.png')
        self.ROLL1 = tk.Label(self.screen, height=205, width=205, image=phR)
        self.ROLL1.image = phR

        phR = tk.PhotoImage(file='DATA/Game/DICE/' + str(NUm2) + '.png')
        self.ROLL2 = tk.Label(self.screen, height=205, width=205, image=phR)
        self.ROLL2.image = phR
        # placing the dices randomly
        numx = random.randint(1, 10)

        self.ROLL1.place(x=VersComp.randPos['xy'+str(numx)]['D1']['x'], y=VersPlayer.randPos['xy'+str(numx)]['D1']['y'])
        self.ROLL2.place(x=VersComp.randPos['xy'+str(numx)]['D2']['x'], y=VersPlayer.randPos['xy'+str(numx)]['D2']['y'])
        VersPlayer.GameState['Player 2']['RoundScore'] = NUm1+NUm2
        # Label Of Score ROUND score
        x = NUm1+NUm2
        if x<10:
            x = '_'+str(x)
        if x==11:
            x = '_' + str(x)
        self.RoundSCORELBL = ttk.Label(self.screen, text=x, font=ScoreFNT, background='orange', foreground='white')
        self.RoundSCORELBL.place(x=315, y=177)
        # player of 2
        if SettingsPlay.VSPlayer.NP == 2:
            RScores = []
            # append all sroes round in one liste
            for i in range(SettingsPlay.VSPlayer.NP):
                RScores.append(VersPlayer.GameState['Player ' + str(i+1)]['RoundScore'])
            # get the maximum number in the list
            maxim = max(RScores)
            RScores = []
            for i in range(SettingsPlay.VSPlayer.NP):
                RScores.append(str(VersPlayer.GameState['Player ' + str(i+1)]['RoundScore']))
            # return the list to str to use find function
            ch = ''.join(RScores)
            while ch.find(str(maxim)) != -1:
                x = RScores.index(str(maxim)) + 1
                SettingsPlay.VSPlayer.PlayerDICT['Player ' + str(x)]['Score'] = int(
                    SettingsPlay.VSPlayer.PlayerDICT['Player ' + str(x)]['Score']) + 1
                # Label Of Score
                lblscore1 = ttk.Label(self.screen,
                                      text='Score: ' + str(
                                      SettingsPlay.VSPlayer.PlayerDICT['Player ' + str(x)]['Score']),
                                      font=ScoreFNT, background='orange',
                                      foreground='white')
                lblscore1.place(x=180, y=63 + (115 * (x - 1)))
                ch = 'x'+ch[ch.find(str(maxim))+1:]
                RScores[RScores.index(str(maxim))] = '_'


            if SettingsPlay.VSPlayer.PlayerDICT['Player 2']['Score'] == SettingsPlay.VSPlayer.SM and SettingsPlay.VSPlayer.PlayerDICT['Player 1']['Score'] == SettingsPlay.VSPlayer.SM:
                self.DBLTHEWINNER(2)
            elif SettingsPlay.VSPlayer.PlayerDICT['Player 2']['Score'] == SettingsPlay.VSPlayer.SM:
                self.screen.destroy()
                self.THEWINNER(2)
            elif SettingsPlay.VSPlayer.PlayerDICT['Player 1']['Score'] == SettingsPlay.VSPlayer.SM:
                self.screen.destroy()
                self.THEWINNER(1)
            else:
                self.player1()
        else:
            self.player3()

    def player3(self):
        self.sp.set('Now is The Role Of ' + SettingsPlay.VSPlayer.PlayerDICT['Player 3']['Name'])
        # BUTTONS OF Roll
        phR = tk.PhotoImage(file='DATA/Game/btn-roll.png')
        self.bu1 = tk.Button(self.screen, height=113, width=283, image=phR, borderwidth=0, command=self.player3CLICKED)
        self.bu1.image = phR
        self.bu1.place(x=695, y=580)

    def player3CLICKED(self):
        try:
            self.ROLL1.destroy()
            self.ROLL2.destroy()
        except:
            pass
        ScoreFNT = ('Berlin Sans fb', 22)
        # Random the pic of roll
        # waiting some seconds
        # saving his data (data of how much he get in the face of any of this dice)
        # waiting some seconds
        NUm1 = random.randint(1, 6)
        NUm2 = random.randint(1, 6)
        # The Dices Image
        phR = tk.PhotoImage(file='DATA/Game/DICE/' + str(NUm1) + '.png')
        self.ROLL1 = tk.Label(self.screen, height=205, width=205, image=phR)
        self.ROLL1.image = phR

        phR = tk.PhotoImage(file='DATA/Game/DICE/' + str(NUm2) + '.png')
        self.ROLL2 = tk.Label(self.screen, height=205, width=205, image=phR)
        self.ROLL2.image = phR
        # placing the dices randomly
        numx = random.randint(1, 10)
        self.ROLL1.place(x=VersComp.randPos['xy'+str(numx)]['D1']['x'], y=VersPlayer.randPos['xy'+str(numx)]['D1']['y'])
        self.ROLL2.place(x=VersComp.randPos['xy'+str(numx)]['D2']['x'], y=VersPlayer.randPos['xy'+str(numx)]['D2']['y'])
        VersPlayer.GameState['Player 3']['RoundScore'] = NUm1+NUm2
        # Label Of Score ROUND score
        x = NUm1+NUm2
        if x<10:
            x = '_'+str(x)
        if x==11:
            x = '_' + str(x)
        self.RoundSCORELBL = ttk.Label(self.screen, text=x, font=ScoreFNT, background='orange', foreground='white')
        self.RoundSCORELBL.place(x=315, y=177+115)
        # player of 3
        if SettingsPlay.VSPlayer.NP == 3:
            RScores = []
            # append all sroes round in one liste
            for i in range(SettingsPlay.VSPlayer.NP):
                RScores.append(VersPlayer.GameState['Player ' + str(i+1)]['RoundScore'])
            # get the maximum number in the list

            maxim = max(RScores)
            RScores = []
            for i in range(SettingsPlay.VSPlayer.NP):
                RScores.append(str(VersPlayer.GameState['Player ' + str(i+1)]['RoundScore']))
            # return the list to str to use find function
            ch = ''.join(RScores)
            while ch.find(str(maxim)) != -1:
                x = RScores.index(str(maxim)) + 1
                SettingsPlay.VSPlayer.PlayerDICT['Player ' + str(x)]['Score'] = int(
                    SettingsPlay.VSPlayer.PlayerDICT['Player ' + str(x)]['Score']) + 1
                # Label Of Score
                lblscore1 = ttk.Label(self.screen,
                                      text='Score: ' + str(
                                          SettingsPlay.VSPlayer.PlayerDICT['Player ' + str(x)]['Score']),
                                      font=ScoreFNT, background='orange',
                                      foreground='white')
                lblscore1.place(x=180, y=63 + (115 * (x - 1)))
                ch = 'x'+ch[ch.find(str(maxim))+1:]
                RScores[RScores.index(str(maxim))] = '_'

                print('ch after remove the max')
            if SettingsPlay.VSPlayer.PlayerDICT['Player 2']['Score'] == SettingsPlay.VSPlayer.SM and SettingsPlay.VSPlayer.PlayerDICT['Player 1']['Score'] == SettingsPlay.VSPlayer.SM:
                self.DBLTHEWINNER(2)
            elif SettingsPlay.VSPlayer.PlayerDICT['Player 3']['Score'] == SettingsPlay.VSPlayer.SM:
                self.screen.destroy()
                self.THEWINNER(3)
            elif SettingsPlay.VSPlayer.PlayerDICT['Player 2']['Score'] == SettingsPlay.VSPlayer.SM:
                self.screen.destroy()
                self.THEWINNER(2)
            elif SettingsPlay.VSPlayer.PlayerDICT['Player 1']['Score'] == SettingsPlay.VSPlayer.SM:
                self.screen.destroy()
                self.THEWINNER(1)
            else:
                self.player1()
        else:
            self.player4()

    def player4(self):
        self.sp.set('Now is The Role Of ' + SettingsPlay.VSPlayer.PlayerDICT['Player 4']['Name'])
        # BUTTONS OF Roll
        phR = tk.PhotoImage(file='DATA/Game/btn-roll.png')
        self.bu1 = tk.Button(self.screen, height=113, width=283, image=phR, borderwidth=0, command=self.player4CLICKED)
        self.bu1.image = phR
        self.bu1.place(x=695, y=580)

    def player4CLICKED(self):
        try:
            self.ROLL1.destroy()
            self.ROLL2.destroy()
        except:
            pass
        ScoreFNT = ('Berlin Sans fb', 22)
        # Random the pic of roll
        # waiting some seconds
        # saving his data (data of how much he get in the face of any of this dice)
        # waiting some seconds
        NUm1 = random.randint(1, 6)
        NUm2 = random.randint(1, 6)
        # The Dices Image
        phR = tk.PhotoImage(file='DATA/Game/DICE/' + str(NUm1) + '.png')
        self.ROLL1 = tk.Label(self.screen, height=205, width=205, image=phR)
        self.ROLL1.image = phR

        phR = tk.PhotoImage(file='DATA/Game/DICE/' + str(NUm2) + '.png')
        self.ROLL2 = tk.Label(self.screen, height=205, width=205, image=phR)
        self.ROLL2.image = phR
        # placing the dices randomly
        numx = random.randint(1, 10)
        self.ROLL1.place(x=VersComp.randPos['xy'+str(numx)]['D1']['x'], y=VersPlayer.randPos['xy'+str(numx)]['D1']['y'])
        self.ROLL2.place(x=VersComp.randPos['xy'+str(numx)]['D2']['x'], y=VersPlayer.randPos['xy'+str(numx)]['D2']['y'])
        VersPlayer.GameState['Player 4']['RoundScore'] = NUm1+NUm2
        # Label Of Score ROUND score
        x = NUm1+NUm2
        if x<10:
            x = '_'+str(x)
        if x==11:
            x = '_' + str(x)
        self.RoundSCORELBL = ttk.Label(self.screen, text=x, font=ScoreFNT, background='orange', foreground='white')
        self.RoundSCORELBL.place(x=315, y=177+115+115)
        # player of 3
        if SettingsPlay.VSPlayer.NP == 4:
            RScores = []
            # append all sroes round in one liste
            for i in range(SettingsPlay.VSPlayer.NP):
                RScores.append(VersPlayer.GameState['Player ' + str(i+1)]['RoundScore'])
            # get the maximum number in the list
            maxim = max(RScores)
            RScores = []
            for i in range(SettingsPlay.VSPlayer.NP):
                RScores.append(str(VersPlayer.GameState['Player ' + str(i+1)]['RoundScore']))
            # return the list to str to use find function
            ch = ''.join(RScores)
            while ch.find(str(maxim)) != -1:
                x = RScores.index(str(maxim)) + 1
                SettingsPlay.VSPlayer.PlayerDICT['Player ' + str(x)]['Score'] = int(
                    SettingsPlay.VSPlayer.PlayerDICT['Player ' + str(x)]['Score']) + 1
                # Label Of Score
                lblscore1 = ttk.Label(self.screen,
                                      text='Score: ' + str(
                                          SettingsPlay.VSPlayer.PlayerDICT['Player ' + str(x)]['Score']),
                                      font=ScoreFNT, background='orange',
                                      foreground='white')
                lblscore1.place(x=180, y=63 + (115 * (x - 1)))
                ch = 'x'+ch[ch.find(str(maxim))+1:]
                RScores[RScores.index(str(maxim))] = '_'

            if SettingsPlay.VSPlayer.PlayerDICT['Player 2']['Score'] == SettingsPlay.VSPlayer.SM and SettingsPlay.VSPlayer.PlayerDICT['Player 1']['Score'] == SettingsPlay.VSPlayer.SM:
                self.DBLTHEWINNER(2)
            elif SettingsPlay.VSPlayer.PlayerDICT['Player 4']['Score'] == SettingsPlay.VSPlayer.SM:
                self.screen.destroy()
                self.THEWINNER(4)
            elif SettingsPlay.VSPlayer.PlayerDICT['Player 3']['Score'] == SettingsPlay.VSPlayer.SM:
                self.screen.destroy()
                self.THEWINNER(3)
            elif SettingsPlay.VSPlayer.PlayerDICT['Player 2']['Score'] == SettingsPlay.VSPlayer.SM:
                self.screen.destroy()
                self.THEWINNER(2)
            elif SettingsPlay.VSPlayer.PlayerDICT['Player 1']['Score'] == SettingsPlay.VSPlayer.SM:
                self.screen.destroy()
                self.THEWINNER(1)
            else:
                self.player1()
        else:
            self.player5()

    def player5(self):
        self.sp.set('Now is The Role Of ' + SettingsPlay.VSPlayer.PlayerDICT['Player 5']['Name'])
        # BUTTONS OF Roll
        phR = tk.PhotoImage(file='DATA/Game/btn-roll.png')
        self.bu1 = tk.Button(self.screen, height=113, width=283, image=phR, borderwidth=0, command=self.player5CLICKED)
        self.bu1.image = phR
        self.bu1.place(x=695, y=580)

    def player5CLICKED(self):
        try:
            self.ROLL1.destroy()
            self.ROLL2.destroy()
        except:
            pass
        ScoreFNT = ('Berlin Sans fb', 22)
        # Random the pic of roll
        # waiting some seconds
        # saving his data (data of how much he get in the face of any of this dice)
        # waiting some seconds
        NUm1 = random.randint(1, 6)
        NUm2 = random.randint(1, 6)
        # The Dices Image
        phR = tk.PhotoImage(file='DATA/Game/DICE/' + str(NUm1) + '.png')
        self.ROLL1 = tk.Label(self.screen, height=205, width=205, image=phR)
        self.ROLL1.image = phR

        phR = tk.PhotoImage(file='DATA/Game/DICE/' + str(NUm2) + '.png')
        self.ROLL2 = tk.Label(self.screen, height=205, width=205, image=phR)
        self.ROLL2.image = phR
        # placing the dices randomly
        numx = random.randint(1, 10)
        self.ROLL1.place(x=VersComp.randPos['xy'+str(numx)]['D1']['x'], y=VersPlayer.randPos['xy'+str(numx)]['D1']['y'])
        self.ROLL2.place(x=VersComp.randPos['xy'+str(numx)]['D2']['x'], y=VersPlayer.randPos['xy'+str(numx)]['D2']['y'])
        VersPlayer.GameState['Player 5']['RoundScore'] = NUm1+NUm2
        # Label Of Score ROUND score
        x = NUm1+NUm2
        if x<10:
            x = '_'+str(x)
        if x==11:
            x = '_' + str(x)
        self.RoundSCORELBL = ttk.Label(self.screen, text=x, font=ScoreFNT, background='orange', foreground='white')
        self.RoundSCORELBL.place(x=315, y=177+(115*3))
        # player of 5
        if SettingsPlay.VSPlayer.NP == 5:
            RScores = []
            # append all sroes round in one liste
            for i in range(SettingsPlay.VSPlayer.NP):
                RScores.append(VersPlayer.GameState['Player ' + str(i+1)]['RoundScore'])
            # get the maximum number in the list
            maxim = max(RScores)
            RScores = []
            for i in range(SettingsPlay.VSPlayer.NP):
                RScores.append(str(VersPlayer.GameState['Player ' + str(i+1)]['RoundScore']))
            # return the list to str to use find function
            ch = ''.join(RScores)
            while ch.find(str(maxim)) != -1:
                x = RScores.index(str(maxim)) + 1
                print('x is: ', x)
                SettingsPlay.VSPlayer.PlayerDICT['Player ' + str(x)]['Score'] = int(
                    SettingsPlay.VSPlayer.PlayerDICT['Player ' + str(x)]['Score']) + 1
                # Label Of Score
                lblscore1 = ttk.Label(self.screen,
                                      text='Score: ' + str(
                                      SettingsPlay.VSPlayer.PlayerDICT['Player ' + str(x)]['Score']),
                                      font=ScoreFNT, background='orange',
                                      foreground='white')
                lblscore1.place(x=180, y=63 + (115 * (x - 1)))
                ch = 'x'+ch[ch.find(str(maxim))+1:]
                RScores[RScores.index(str(maxim))] = '_'

            if SettingsPlay.VSPlayer.PlayerDICT['Player 2']['Score'] == SettingsPlay.VSPlayer.SM and SettingsPlay.VSPlayer.PlayerDICT['Player 1']['Score'] == SettingsPlay.VSPlayer.SM:
                self.DBLTHEWINNER(2)
            elif SettingsPlay.VSPlayer.PlayerDICT['Player 5']['Score'] == SettingsPlay.VSPlayer.SM:
                self.screen.destroy()
                self.THEWINNER(5)
            elif SettingsPlay.VSPlayer.PlayerDICT['Player 4']['Score'] == SettingsPlay.VSPlayer.SM:
                self.screen.destroy()
                self.THEWINNER(4)
            elif SettingsPlay.VSPlayer.PlayerDICT['Player 3']['Score'] == SettingsPlay.VSPlayer.SM:
                self.screen.destroy()
                self.THEWINNER(3)
            elif SettingsPlay.VSPlayer.PlayerDICT['Player 2']['Score'] == SettingsPlay.VSPlayer.SM:
                self.screen.destroy()
                self.THEWINNER(2)
            elif SettingsPlay.VSPlayer.PlayerDICT['Player 1']['Score'] == SettingsPlay.VSPlayer.SM:
                self.screen.destroy()
                self.THEWINNER(1)
            else:
                self.player1()
        else:
            self.player6()

    def player6(self):
        self.sp.set('Now is The Role Of ' + SettingsPlay.VSPlayer.PlayerDICT['Player 6']['Name'])
        # BUTTONS OF Roll
        phR = tk.PhotoImage(file='DATA/Game/btn-roll.png')
        self.bu1 = tk.Button(self.screen, height=113, width=283, image=phR, borderwidth=0, command=self.player6CLICKED)
        self.bu1.image = phR
        self.bu1.place(x=695, y=580)

    def player6CLICKED(self):
        try:
            self.ROLL1.destroy()
            self.ROLL2.destroy()
        except:
            pass
        ScoreFNT = ('Berlin Sans fb', 22)
        # Random the pic of roll
        # waiting some seconds
        # saving his data (data of how much he get in the face of any of this dice)
        # waiting some seconds
        NUm1 = random.randint(1, 6)
        NUm2 = random.randint(1, 6)
        # The Dices Image
        phR = tk.PhotoImage(file='DATA/Game/DICE/' + str(NUm1) + '.png')
        self.ROLL1 = tk.Label(self.screen, height=205, width=205, image=phR)
        self.ROLL1.image = phR

        phR = tk.PhotoImage(file='DATA/Game/DICE/' + str(NUm2) + '.png')
        self.ROLL2 = tk.Label(self.screen, height=205, width=205, image=phR)
        self.ROLL2.image = phR
        # placing the dices randomly
        numx = random.randint(1, 10)
        self.ROLL1.place(x=VersComp.randPos['xy'+str(numx)]['D1']['x'], y=VersPlayer.randPos['xy'+str(numx)]['D1']['y'])
        self.ROLL2.place(x=VersComp.randPos['xy'+str(numx)]['D2']['x'], y=VersPlayer.randPos['xy'+str(numx)]['D2']['y'])
        VersPlayer.GameState['Player 6']['RoundScore'] = NUm1+NUm2
        # Label Of Score ROUND score
        x = NUm1+NUm2
        if x<10:
            x = '_'+str(x)
        if x==11:
            x = '_' + str(x)
        self.RoundSCORELBL = ttk.Label(self.screen, text=x, font=ScoreFNT, background='orange', foreground='white')
        self.RoundSCORELBL.place(x=315, y=177+(115*4))
        # player of 5
        if SettingsPlay.VSPlayer.NP == 6:
            RScores = []
            # append all sroes round in one liste
            for i in range(SettingsPlay.VSPlayer.NP):
                RScores.append(VersPlayer.GameState['Player ' + str(i+1)]['RoundScore'])
            # get the maximum number in the list
            maxim = max(RScores)
            RScores = []
            for i in range(SettingsPlay.VSPlayer.NP):
                RScores.append(str(VersPlayer.GameState['Player ' + str(i+1)]['RoundScore']))
            # return the list to str to use find function
            ch = ''.join(RScores)
            while ch.find(str(maxim)) != -1:
                x = RScores.index(str(maxim)) + 1
                SettingsPlay.VSPlayer.PlayerDICT['Player ' + str(x)]['Score'] = int(
                    SettingsPlay.VSPlayer.PlayerDICT['Player ' + str(x)]['Score']) + 1
                # Label Of Score
                lblscore1 = ttk.Label(self.screen,
                                      text='Score: ' + str(
                                      SettingsPlay.VSPlayer.PlayerDICT['Player ' + str(x)]['Score']),
                                      font=ScoreFNT, background='orange',
                                      foreground='white')
                lblscore1.place(x=180, y=63 + (115 * (x - 1)))
                ch = 'x'+ch[ch.find(str(maxim))+1:]
                RScores[RScores.index(str(maxim))] = '_'

            if SettingsPlay.VSPlayer.PlayerDICT['Player 2']['Score'] == SettingsPlay.VSPlayer.SM and SettingsPlay.VSPlayer.PlayerDICT['Player 1']['Score'] == SettingsPlay.VSPlayer.SM:
                self.DBLTHEWINNER(2)
            elif SettingsPlay.VSPlayer.PlayerDICT['Player 6']['Score'] == SettingsPlay.VSPlayer.SM:
                self.screen.destroy()
                self.THEWINNER(6)
            elif SettingsPlay.VSPlayer.PlayerDICT['Player 5']['Score'] == SettingsPlay.VSPlayer.SM:
                self.screen.destroy()
                self.THEWINNER(5)
            elif SettingsPlay.VSPlayer.PlayerDICT['Player 4']['Score'] == SettingsPlay.VSPlayer.SM:
                self.screen.destroy()
                self.THEWINNER(4)
            elif SettingsPlay.VSPlayer.PlayerDICT['Player 3']['Score'] == SettingsPlay.VSPlayer.SM:
                self.screen.destroy()
                self.THEWINNER(3)
            elif SettingsPlay.VSPlayer.PlayerDICT['Player 2']['Score'] == SettingsPlay.VSPlayer.SM:
                self.screen.destroy()
                self.THEWINNER(2)
            elif SettingsPlay.VSPlayer.PlayerDICT['Player 1']['Score'] == SettingsPlay.VSPlayer.SM:
                self.screen.destroy()
                self.THEWINNER(1)
            else:
                self.player1()

    def THEWINNER(self, i):
        NameFNT = ('Gill Sans MT', 27)

        self.screenF =  Tk()
        self.screenF.overrideredirect(True)
        self.screenF.wm_attributes("-topmost", True)
        LR = []
        for f in MainScreen.CenterScreen.GetGeometry(self, 1270, 740): LR.append(f)
        self.screenF.geometry("%dx%d+%d+%d" % (LR[0], LR[1], LR[2]+10, LR[3]+30))
        # Setup The Image Of Background
        if self.Ldata[0][1] == 'True':
            # French
            bgpath = 'DATA/Game/winner/bg.png'
        else:
            bgpath = 'DATA/Game/winner/bg-eng.png'
        bg = ImageTk.PhotoImage(Image.open(bgpath))
        self.bg = ttk.Label(self.screenF, image=bg)
        self.bg.image = bg
        self.bg.place(x=-5, y=0)
        image = Image.open(SettingsPlay.VSPlayer.PlayerDICT['Player '+str(i)]['PathPIC'])
        image = image.resize((150, 150), Image.ANTIALIAS)
        ph = ImageTk.PhotoImage(image)
        self.pic = tk.Label(self.screenF, height=148, background='black', width=148, image=ph,
                            borderwidth=0)
        self.pic.image = ph
        self.pic.place(x=565, y=295)
        # Label Of Name
        lblName1 = ttk.Label(self.screenF, text=SettingsPlay.VSPlayer.PlayerDICT['Player '+str(i)]['Name'], font=NameFNT,
                             background='orange',
                             foreground='white')
        lblName1.place(x=565, y=500)

        # BUTTON OF Close
        ph = tk.PhotoImage(file='Data/VSPLAYER/editplayer/btn-close.png')
        self.buset = tk.Button(self.screenF, height=88, width=90, image=ph, borderwidth=0, command=self.xit)
        self.buset.image = ph
        self.buset.place(x=996, y=83)

    def DBLTHEWINNER(self, i):
        self.screen.destroy()
        NameFNT = ('Gill Sans MT', 27)
        self.screenFDBL = Tk()
        self.screenFDBL.overrideredirect(True)
        self.screenFDBL.wm_attributes("-topmost", True)
        LR = []
        for f in MainScreen.CenterScreen.GetGeometry(self, 1270, 740): LR.append(f)
        self.screenFDBL.geometry("%dx%d+%d+%d" % (LR[0], LR[1], LR[2] + 10, LR[3] + 30))
        # Setup The Image Of Background
        if self.Ldata[0][1] == 'True':
            # French
            bgpath = 'DATA/Game/winner/bg.png'
        else:
            bgpath = 'DATA/Game/winner/bg-eng.png'
        bg = ImageTk.PhotoImage(Image.open(bgpath))
        self.bg = ttk.Label(self.screenFDBL, image=bg)
        self.bg.image = bg
        self.bg.place(x=-5, y=0)
        image = Image.open(SettingsPlay.VSPlayer.PlayerDICT['Player ' + str(i)]['PathPIC'])
        image = image.resize((150, 150), Image.ANTIALIAS)
        ph = ImageTk.PhotoImage(image)
        self.pic = tk.Label(self.screenFDBL, height=148, background='black', width=148, image=ph,
                            borderwidth=0)
        self.pic.image = ph
        self.pic.place(x=565, y=295)
        # Label Of Name
        lblName1 = ttk.Label(self.screenFDBL, text=SettingsPlay.VSPlayer.PlayerDICT['Player ' + str(i)]['Name'],
                             font=NameFNT,
                             background='orange',
                             foreground='white')
        lblName1.place(x=565, y=500)

        # BUTTON OF Close
        ph = tk.PhotoImage(file='Data/VSPLAYER/editplayer/btn-close.png')
        self.buset = tk.Button(self.screenFDBL, height=88, width=90, image=ph, borderwidth=0, command=self.xitDBL)
        self.buset.image = ph
        self.buset.place(x=996, y=83)

    def xit(self):
        self.screenF.destroy()
        import Begin
        Begin.Start()

    def xitDBL(self):
        self.screenFDBL.destroy()
        self.THEWINNER(1)
