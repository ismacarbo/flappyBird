import pygame
import random

pygame.init()
#setto gli sfondi
decision=random.randint(0,1)
if decision==1:
    sfondo=pygame.image.load('immagini/sfondo.png')
else:
    sfondo=pygame.image.load('immagini/notte.jpg')
player=pygame.image.load('immagini/uccello.png')
base=pygame.image.load('immagini/base.png')
gameOver=pygame.image.load('immagini/gameover.png')
tuboGiu=pygame.image.load('immagini/tubo.png')
tuboSu=pygame.transform.flip(tuboGiu,False,True)#immagine da trasformare, fli orizz, flip verticale
FONT = pygame.font.SysFont('arial.ttf', 50)

schermo=pygame.display.set_mode((288,512))
FPS=50
AVANZA=3

class tubiClass:
    def __init__(self):
        self.x=300
        self.y=random.randint(-75,150)
    def avanzaDisegna(self):
        self.x-=AVANZA
        schermo.blit(tuboGiu,(self.x,self.y+210))
        schermo.blit(tuboSu,(self.x,self.y-210))
    
    def collisione(self,player,playerX,playerY):
        tolleranza=5
        destra=playerX+player.get_width()-tolleranza
        sinistra=playerX+tolleranza
        tubiDestra=self.x+tuboGiu.get_width()
        tubiSinistra=self.x
        playerLatoSu=playerY+tolleranza
        playerLatoGiu=playerY+player.get_height()-tolleranza
        tubiSopra=self.y+110
        tubiSotto=self.y+210
        if destra>tubiSinistra and sinistra<tubiDestra:
            if playerLatoSu<tubiSopra or playerLatoGiu> tubiSotto:
                perdita()
                
    def neiTubi(self,player,playerX):
        tolleranza=5
        destra=playerX+player.get_width()-tolleranza
        sinistra=playerX+tolleranza
        tubiDestra=self.x+tuboGiu.get_width()
        tubiSinistra=self.x
        if destra>tubiSinistra and sinistra<tubiDestra:
            return True
        
def disegna():
    schermo.blit(sfondo,(0,0))
    for t in tubi:
        t.avanzaDisegna()
    schermo.blit(player,(playerX,playerY))
    schermo.blit(base,(baseX,400))
    mostraPunti=FONT.render(str(punti),1,(255,255,255))
    schermo.blit(mostraPunti,(139,0))
    
    
def aggiorna():
    pygame.display.update()
    pygame.time.Clock().tick(FPS)
    

def inizializza():
    pygame.display.set_caption('Flappy Bird')
    global playerX,playerY, velocitaY
    global baseX
    global tubi
    global punti
    global inTubes
    global jumped
    playerX,playerY=60, 150 #faccio partire il giocatore in x=60, y=150
    velocitaY=0
    baseX=0
    punti=0
    tubi=[]
    tubi.append(tubiClass())
    inTubes=False
    jumped=False

def perdita():
    schermo.blit(gameOver,(50,180))
    aggiorna()
    ricomincia=False
    while not ricomincia:
        for event in pygame.event.get():
            if event.type==pygame.KEYDOWN and event.key==pygame.K_r:
                inizializza()
                ricomincia=True
            if event.type==pygame.QUIT:
                pygame.quit() 

inizializza()

while True:
    if baseX < -45: baseX=0
    baseX-=AVANZA
    velocitaY+=1
    playerY+=velocitaY
    #input da tastiera
    for event in pygame.event.get():
        if (event.type==pygame.KEYDOWN and event.key==pygame.K_SPACE):
          jumped = True
          if jumped:
              jumped=False
          velocitaY=-10
        if event.type==pygame.QUIT:
            pygame.quit()
    if playerY > 381: #la y al punto massimo dello schermo è 0, se vai in giu aumenta
        perdita()
    if tubi[-1].x<150: tubi.append(tubiClass())
    if not inTubes:
        for tubo in tubi:
            if tubo.neiTubi(player, playerX):
                inTubes=True
                break   
    if inTubes:
        inTubes=False
        for tubo in tubi:
            if tubo.neiTubi(player, playerX):
                inTubes=True
                break
        if not inTubes:
            punti+=1
        
        
    for tubo in tubi:
        tubo.collisione(player,playerX,playerY)
    disegna()
    aggiorna()