#made by Bosticado Andrea and Rebuffo Davide
#Istruzioni:https://it.wikipedia.org/wiki/Tris_(gioco)
import socket,os,time,pygame,sys,serial,webbrowser,random
import serial.tools.list_ports
from threading import Thread
import tkinter as tk 
from TicTacToe import GameController
from easyAI import TwoPlayersGame, AI_Player, Negamax
from easyAI.Player import Human_Player
from copy import deepcopy
class Coda():
    def __init__(self):self.coda=[]
    def enqueue(self,elemento):self.coda.append(elemento)
    def dequeue(self):
        if len(self.coda) != 0:return self.coda.pop(0)
        else:return None
coda = Coda()
class MyThread(Thread):
    def __init__(self,griglia,g1,g2,giocatori,connect,vincite,TicTacToe):
        Thread.__init__(self)
        self.running = True
        self.griglia = griglia
        self.g1 = g1
        self.g2 = g2
        self.tipo = None
        self.giocatori = giocatori
        self.posizione = 0
        self.inzio = 0
        self.end = 0
        self.connect = connect
        self.ok = True
        self.x = 0
        self.vincite = vincite
        self.TicTacToe = TicTacToe
        self.mossa = None
        self.dizioCoordinate = {0:[61.5,61.5],1:[196.5,61.5],2:[331.5,61.5],3:[61.5,196.5],4:[196.5,200],5:[331.5,196.5],6:[61.5,330.5],7:[196.5,330.5],8:[331.5,330.5]}
    def run(self):
        pygame.init()
        size = (400,475)
        fnt2 = pygame.font.SysFont("Times New Roman", 25)
        fnt = pygame.font.SysFont("Times New Roman", 110)
        fnt3 = pygame.font.SysFont("Times New Roman", 50)
        screen = pygame.display.set_mode(size)
        BLUNOTTE = (0,0,102)
        VERDE = (0,51,0)
        ARANCIONE = (255,153,51)
        while self.running:
            screen.fill((255,255,255))
            pygame.draw.rect(screen,(0,0,0),(130,10,5,380))
            pygame.draw.rect(screen,(0,0,0),(265,10,5,380))
            pygame.draw.rect(screen,(0,0,0),(10,130,380,5))
            pygame.draw.rect(screen,(0,0,0),(10,265,380,5))
            for chiave in self.dizioCoordinate:
                if self.griglia[chiave] == " ": surf_text = fnt.render(str(chiave), True, BLUNOTTE)
                else:
                    if self.griglia[chiave] == "X":surf_text = fnt.render(self.griglia[chiave], True, VERDE)
                    else:surf_text = fnt.render(self.griglia[chiave], True, ARANCIONE)
                screen.blit(surf_text, (self.dizioCoordinate[chiave][0]-20.5,self.dizioCoordinate[chiave][1]-50.5))
            for event in pygame.event.get():
                if event.type == pygame.QUIT: sys.exit()
                if event.type == pygame.KEYDOWN: 
                    if event.__dict__["unicode"] == "s":coda.enqueue("a")
                    if event.__dict__["unicode"] == "d":coda.enqueue("b")
                    if event.__dict__["unicode"] == "w":coda.enqueue("w")
                    if event.__dict__["unicode"] == "a":coda.enqueue("z")
                    if event.__dict__["unicode"] == " ":coda.enqueue("m")
            if self.ok: 
                TestoG1 = fnt2.render("".join(["* ",self.g1," = ",self.giocatori[self.g1], " - vittorie: ",str(self.vincite[self.g1])]), True, VERDE)
                screen.blit(TestoG1, (10,400)) 
                TestoG2 = fnt2.render("".join([self.g2," = ",self.giocatori[self.g2]," - vittorie: ",str(self.vincite[self.g2])]), True, ARANCIONE)
                screen.blit(TestoG2, (10,425))
            else:
                TestoG1 = fnt2.render("".join([self.g1," = ",self.giocatori[self.g1], " - vittorie: ",str(self.vincite[self.g1])]), True, VERDE)
                screen.blit(TestoG1, (10,400)) 
                TestoG2 = fnt2.render("".join(["* ",self.g2," = ",self.giocatori[self.g2]," - vittorie: ",str(self.vincite[self.g2])]), True, ARANCIONE)
                screen.blit(TestoG2, (10,425))
            mossa = str(coda.dequeue())
            if mossa != None:
                if mossa[0] == "a":
                    if self.posizione == 6: self.posizione = 0
                    elif self.posizione == 7: self.posizione = 1
                    elif self.posizione == 8: self.posizione = 2
                    else:self.posizione = self.posizione + 3
                if mossa[0] == "b":
                    if self.posizione == 2 :self.posizione = 0
                    elif self.posizione == 5: self.posizione = 3
                    elif self.posizione == 8: self.posizione = 6
                    else: self.posizione = self.posizione +  1
                if mossa[0] == "w":
                    if self.posizione == 0: self.posizione = 6
                    elif self.posizione == 1: self.posizione = 7
                    elif self.posizione == 2: self.posizione = 8
                    else:self.posizione = self.posizione - 3
                if mossa[0] == "z":
                    if self.posizione == 0 :self.posizione = 2
                    elif self.posizione == 3: self.posizione = 5
                    elif self.posizione == 6: self.posizione = 8
                    else: self.posizione = self.posizione -  1  
                #check that it is the player's turn and that a move has been made in the queue   
                if (mossa[0] == "m") and (self.ok):
                    m = self.posizione
                    #check if the move is valid
                    m = controllo(m,self.g1,self.griglia,self.giocatori)
                    if m != None:
                        posizionaMossa = pygame.mixer.Sound("suoni/pugno.mp3")
                        posizionaMossa.play()
                        if self.connect != None:
                            self.connect.sendall(str(m).encode())
                        else:
                            self.setMossa(m)
                        self.ok = False
                    else:
                        erroreMossa = pygame.mixer.Sound("suoni/errore.mp3")
                        erroreMossa.play()
                elif (mossa[0] == "m") and not(self.ok):
                    erroreMossa = pygame.mixer.Sound("suoni/errore.mp3")
                    erroreMossa.play()
                    print("Non ?? il tuo turno abbi pazienza")
            if self.tipo != None:
                if self.tipo == 3:
                    pygame.draw.rect(screen,(255,255,255),(0,400,400,75),0)
                    risultato = fnt3.render("Pareggio", True, (0,0,0))
                if self.tipo == 2:
                    loser = pygame.mixer.Sound("suoni/loser.mp3")
                    loser.play()
                    pygame.draw.rect(screen,(255,255,255),(0,400,400,75),0)
                    pygame.draw.line(screen, (0,0,0), self.inizio, self.end, 10)
                    risultato = fnt3.render(f"Hai perso", True, (255,0,0))
                if self.tipo == 1:
                    w = pygame.mixer.Sound("suoni/winner.mp3")
                    w.play()
                    pygame.draw.rect(screen,(255,255,255),(0,400,400,75),0)
                    pygame.draw.line(screen, (0,0,0), self.inizio, self.end, 10)
                    risultato = fnt3.render(f"Hai vinto", True, (0,255,0))
                screen.blit(risultato, (10,400)) 
            pygame.draw.rect(screen,(255,0,0),(self.dizioCoordinate[self.posizione][0]-35,self.dizioCoordinate[self.posizione][1]-35,100,100),2)
            pygame.display.flip() 
            if self.x == None:pygame.quit()
    def linea(self,s,e):
        self.inizio,self.end = self.dizioCoordinate[s],self.dizioCoordinate[e]
    def setMossa(self, m):
        self.mossa = m
class LetturaSeriale(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.running = True
    def run(self):
        #I read the ports
        port,microbit = self.letturaPorte()
        #if I have found something connected to the ports I listen to them otherwise I continue the search
        while(port == None): 
            port,microbit = self.letturaPorte()
            time.sleep(1)
        if port != None:
            while self.running:
                # I read the serial port
                data = microbit.readline().decode()
                if(data != ""): #check that it's not empty
                    # I put it in the queue
                    coda.enqueue(data[:-1])
    def letturaPorte(self):
        ports = serial.tools.list_ports.comports()
        #I check all the ports and connect to the first one
        for port, desc, hwid in sorted(ports):
            print("{}: {} [{}]".format(port, desc, hwid))
            break
        if ports == []:
            port = None
            microbit = None
        else:
            try: #I connect to the serial
                microbit = serial.Serial(port=port, baudrate=115200, timeout=1)
            except Exception as e:
                microbit,port = None,None
        return port,microbit
    def stop(self):
        self.running = False
OptionList = [
            "7-Impossibile",
            "6-Esperto",
            "5-Complicato",
            "4-Medio",
            "3-Facile",
            "2-elemnetare",
            "1-Noob",
            ]  
#Graph Tkinter to read the name
class GUI(tk.Tk):
    def __init__(self):
        super().__init__()
        #initialize the screen
        self.var1 = tk.IntVar()
        self.geometry('500x250')
        self.title("Nome")
        self.level = 7
        #I set up the grill
        self.grid_columnconfigure(0, weight=1)
        ##create the text widget
        self.variable = tk.StringVar(self)
        self.variable.set("Seleziona un livello di difficolt??")
        self.textwidget = tk.Label(self,
                                    text="Inserire il nome, poi premere Enter\n",
                                    font=("Helvetica", 15))
        self.text_input = tk.Entry()
        self.opt = tk.OptionMenu(self, self.variable, *OptionList)
        self.name = "giocatore 1"
        #function create = loop
        self.crea()
    def crea(self):
        #I create the different objects: buttons and text labels
        welcome_label = tk.Label(self,text="Inserisci il tuo nome",font=("Helvetica", 15))
        welcome_label.grid(row=0, column=0, sticky="WE", padx=10, pady=10)                       
        self.text_input.grid(row=1, column=0, sticky="WE", padx=10)
        self.textwidget.grid(row=2, column=0, sticky="N", padx=10, pady=10)
        download_button = tk.Button(text="Enter", command=self.nome)
        download_button.grid(row=1, column=1, sticky="WE", pady=10, padx=10)
        link_button = tk.Button(text="instructions", command=self.rules)
        link_button.grid(row=3, sticky="WE", pady=0, padx=10)
        gitHub_button = tk.Button(text="gitHub", command=self.gitHub)
        gitHub_button.grid(row=4, sticky="WE", pady=0, padx=10)
        solo_button = tk.Button(text="Solo Mode", command=self.check)
        solo_button.grid(row=5, sticky="WE", pady=0, padx=10)
        c1 = tk.Checkbutton(self, text='Solo Mode',variable=self.var1, onvalue=1, offvalue=0)#command=print_selection
        c1.grid(row=5,column=1, sticky="N", pady=0, padx=10)
        if self.var1.get() == 1:
            welcome_label.destroy()
            welcome_label = tk.Label(self,text='If this button is checked you are playing alone against an AI',font=("Times New Roman", 12))
            welcome_label.grid(row=6, column=0, sticky="WE", padx=10, pady=10)  
        else:
            welcome_label.destroy()
            welcome_label = tk.Label(self,text='If this button is checked you are playing alone against an AI',font=("Times New Roman", 12))
            welcome_label.grid(row=7, column=0, sticky="WE", padx=10, pady=10)
        self.variable.trace("w", self.callback) 
    #functions for links
    def callback(self,*arg):
        self.level = self.variable.get().split("-")[0]
    def check(self):
        if self.var1.get() == 1:
            self.var1.set(0)
            self.opt.destroy()
            self.opt = tk.OptionMenu(self, self.variable, *OptionList)
        else:
            self.opt.config(height=1,font=('Helvetica', 12))
            self.opt.grid(row=6,column=0, sticky="WE", pady=10, padx=10)
            self.var1.set(1)
    def rules(self):
        webbrowser.open_new(r"https://it.wikipedia.org/wiki/Tris_(gioco)")
    def gitHub(self):
        webbrowser.open_new(r"https://github.com/Bosticardo-Andrea/Microbit-Project")
    #functions to take the name and display it
    def nome(self,):
        if self.text_input.get():
            user_input = self.text_input.get()
            nome = user_input
            self.name = user_input
            print(self.name)
            self.destroy()
        else:
            nome = "Inserire il nome, poi premere Enter\n"
        self.textwidget.destroy()
        self.textwidget = tk.Label(self,
                                    text=nome,
                                    font=("Helvetica", 15))
        self.textwidget.grid(row=2, column=0, sticky="WE", padx=10, pady=10)
def connessione():
    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    #s.bind(("192.168.88.98",8000))
    s.bind(("127.0.0.1",8000))
    s.listen()
    print("In attesa di connessione...")
    connect,address = s.accept()
    return connect,address
def controllo(x,g,griglia,giocatori):
    if((griglia[x] != " ")):       
        print("Cella occupata")
        #x = int(input("Inserici mossa:"))
        x = None
    else: griglia[x] = giocatori[g]   
    return x
def disegnaGriglia(griglia,giocatori,g1,g2):
    """Disegno la griglia con i giocatori che si sfidano"""
    print(f"\n{g1} [{giocatori[g1]}] vs {g2} [{giocatori[g2]}]\n")
    print(f" {griglia[0]} | {griglia[1]} | {griglia[2]} ")
    print(f"---+---+---")
    print(f" {griglia[3]} | {griglia[4]} | {griglia[5]} ")
    print(f"---+---+---")
    print(f" {griglia[6]} | {griglia[7]} | {griglia[8]} ")
    print("\n")
def vittoria(griglia,disegno):
    """controllo tutte i  possibili casi in cui si pu?? vincere"""
    vittoria = False
    if ((griglia[0]==griglia[1]==griglia[2]) & (griglia[0]!=" ")):
        disegno.linea(0,2)
        vittoria = True
    elif ( (griglia[3]==griglia[4]==griglia[5]) & (griglia[3]!=" ")):
        disegno.linea(3,5)
        vittoria = True
    elif ( (griglia[6]==griglia[7]==griglia[8]) & (griglia[6]!=" ")):
        disegno.linea(6,8)
        vittoria = True
    elif ((griglia[0]==griglia[3]==griglia[6]) & (griglia[0]!=" ")):
        disegno.linea(0,6)
        vittoria = True
    elif( (griglia[1]==griglia[4]==griglia[7]) & (griglia[1]!=" ")):
        disegno.linea(1,7)
        vittoria = True
    elif( (griglia[2]==griglia[5]==griglia[8]) & (griglia[2]!=" ")):
        disegno.linea(2,8)
        vittoria = True
    elif ((griglia[0]==griglia[4]==griglia[8]) & (griglia[0]!=" ")):
        disegno.linea(0,8)
        vittoria = True 
    elif(( griglia[2]==griglia[4]==griglia[6]) & (griglia[2]!=" ")):
        disegno.linea(2,6)
        vittoria = True
    return vittoria  
def primo(G1,G2,disegno,vincite,griglia,giocatori,connect,conta):
    while(True):
            print(f"{G1}")
            print(f"Tocca a: {G1}")
            disegno.ok = True
            ric = True
            while disegno.ok == True:
                if(vittoria(griglia,disegno)):
                    print(f"Ha vinto {G1}")
                    vincite[G1]+=1
                    disegno.tipo = 1
                    ric = False
                    break
            os.system('cls') 
            disegnaGriglia(griglia,giocatori,G1,G2)
            if ric == False:
                break
            if(conta <= 8): 
                conta += 1
            else: 
                disegno.tipo = 3
                break
            print(f"{G2}")
            print(f"Tocca a: {G2}")
            print("Attendi....")
            if connect != None:
                m = int(connect.recv(4096).decode())
            else:
                pass
            griglia[m] = giocatori[G2]
            os.system('cls')
            disegnaGriglia(griglia,giocatori,G1,G2)
            if(vittoria(griglia,disegno)):
                print(f"Ha vinto {G2}")
                vincite[G2]+=1
                disegno.tipo = 2
                break
            if(conta <= 8): 
                conta += 1
            else: 
                disegno.tipo = 3
                break 
def secondo(G1,G2,disegno,vincite,griglia,giocatori,connect,conta):
     while(True):
            print(f"{G1}")
            print(f"Tocca a: {G1}")
            print("Attendi....")
            if connect != None:
                m = int(connect.recv(4096).decode())
            else:
                pass
            griglia[m] = giocatori[G1]
            os.system('cls')
            disegnaGriglia(griglia,giocatori,G1,G2)
            if(vittoria(griglia,disegno)):
                print(f"Ha vinto {G1}")
                vincite[G1]+=1
                disegno.tipo = 1
                break
            if(conta <= 8): 
                conta += 1
            else: 
                disegno.tipo = 3
                break
            print(f"{G2}")
            print(f"Tocca a: {G2}")
            disegno.ok = True
            #os.system('cls')
            #disegnaGriglia(griglia,giocatori,G1,G2)
            ric = True
            while disegno.ok == True:
                if(vittoria(griglia,disegno)):
                    print(f"Ha vinto {G2}")
                    vincite[G2]+=1
                    disegno.tipo = 2
                    ric = False
                    break
            os.system('cls') 
            disegnaGriglia(griglia,giocatori,G1,G2)
            if ric == False:
                break
            if(conta <= 8): 
                conta += 1
            else: 
                disegno.tipo = 3
                break
def doppio(G1):
    #inserisciNome.start()
    connect,address = connessione()
    #G1 = input("Inserisci Giocatore1[X]: ")e
    connect.sendall(G1.encode())
    G2 = connect.recv(4096).decode()
    giocatori = {G1:"X",G2:"O"}
    vincite = {G1 : 0, G2 : 0}
    # I draw a player by lot
    inizio = random.choice(list(giocatori.keys()))
    #Send the extracted player
    connect.sendall(inizio.encode())
    ##exchange players in case the server doesn't start
    if inizio == G2: G1,G2 = G2,G1
    #check if someone has won at least 3 times
    while ((vincite[G1] - vincite[G2] <= 2) or(vincite[G1] - vincite[G2] <= 2)):
        #I start everything and start with the game
        griglia = {0: " ", 1: " ",2: " ",3: " ",4: " ",5: " ",6: " ",7: " ",8: " "}
        conta = 1 
        os.system('cls') 
        disegnaGriglia(griglia,giocatori,G1,G2)
        movimento = LetturaSeriale()
        movimento.start()
        disegno = MyThread(griglia,G1,G2,giocatori,connect,vincite,None)
        disegno.start()
        #starts who has been extracted
        if inizio == G1:primo(G1,G2,disegno,vincite,griglia,giocatori,connect,conta)
        else:secondo(G1,G2,disegno,vincite,griglia,giocatori,connect,conta)
        #I wait 5 seconds and then I close everything to start the whole thing over
        time.sleep(5)
        movimento.stop()
        disegno.running = False
        disegno.x = None
        disegno.join()
    movimento.join()
    disegno.join()
    sys.exit()
def solo(griglia,g1,g2, level):
    giocatori = {g1:"X",g2:"O"}
    vincite = {g1 : 0, g2 : 0}
    m = None
    prima_volta = False
    sorteggio = random.choice(list(giocatori.keys()))
    if sorteggio == g1:
        prima_volta=False
        inizio = 1
    else:
        prima_volta = True
        inizio = 2
    print(sorteggio,prima_volta)
    time.sleep(1)
    while 1:
        if (vincite[g1] - vincite[g2] >= 2) or (vincite[g2] - vincite[g1] >= 2):
            break
        griglia = {0: " ", 1: " ",2: " ",3: " ",4: " ",5: " ",6: " ",7: " ",8: " "}
        algorithm = Negamax(level) # 7 (imbattibile)
        disegno = MyThread(griglia,g1,g2,giocatori,None,vincite,None)
        disegno.start()
        gioco_tris = GameController([Human_Player(), AI_Player(algorithm)],inizio)
        while True:
            if prima_volta:
                mossa_robot = gioco_tris.inizio_mossa_robot()
                if  mossa_robot != None:
                    mb = mossa_robot
                    griglia[int(mb)] = giocatori[g2]
                    os.system("cls")
                    disegnaGriglia(griglia,giocatori,g1,g2)
                    prima_volta = False
            else:
                """m = (int(input("inserisci un numero: ")))
                while (m not in gioco_tris.possible_moves()):
                    print(gioco_tris.possible_moves())
                    m = (int(input("inserisci un numero: ")))
                    #print(gioco_tris.possible_moves())"""
                while disegno.ok: pass
                if disegno.mossa != None:
                    m = disegno.mossa
                    griglia[int(disegno.mossa)] = giocatori[g1]
                    os.system("cls")
                    os.system("cls")
                    disegnaGriglia(griglia,giocatori,g1,g2)
                    disegno.setMossa(None)
                else:
                    mossa_robot = gioco_tris.play(m)
                    if "Partita finita" not in str(mossa_robot):
                        mb = mossa_robot
                        griglia[int(mb)] = giocatori[g2]
                        os.system("cls")
                        disegnaGriglia(griglia,giocatori,g1,g2)
                        disegno.ok = True
                isover, vincitore = gioco_tris.is_over_2()
                x = vittoria(griglia,disegno)
                if isover :
                    print(vincitore)
                    if "Ho vinto!" in vincitore:
                        vincite[g2] += 1
                        disegno.tipo = 2
                    elif "Complimenti hai vinto!" in vincitore:
                        vincite[g1] += 1
                        disegno.tipo = 1
                    if inizio == 1:
                        inizio = 2
                        prima_volta = True
                    else:
                        inizio = 1
                    time.sleep(3)
                    disegno.running = False
                    disegno.x = None
                    disegno.join()
                    break
def main():
    griglia = {0: " ", 1: " ",2: " ",3: " ",4: " ",5: " ",6: " ",7: " ",8: " "}
    app = GUI()
    app.mainloop()
    # I take the name from the GUI and wait for a connection
    soloMode = app.var1.get()
    G1 = app.name
    os.system("cls")
    if soloMode == 1:
        level = app.level
        solo(griglia,G1,"AI",level)
    else:
        doppio(G1)
if __name__=="__main__":
    main()                                                                                                                                                                                                                                                                                                                                                                                              #gitHub link: https://github.com/Bosticardo-Andrea/Microbit-Project