#Interface principale
import math
import os
from tkinter.filedialog import *
from tkinter import *
from PIL import Image
from webcolors import *
import io
from tkinter.colorchooser import *
import time
from tkinter import messagebox

"""
Définition des variables : 
    chemin : chemin absolu vers le fichier
    img : image originale
    ouv : image ouverte
    l,L : dimensions de l'image
    ImageEditee : liste contenant la totalité des pixels de l'image, tenant compte des modifications effectuées
    Calque0 : Canv
    as d'édition
    gommage : tuple contenant l'image originale
    historique : Liste contenant les versions précédentes de l'image éditée pour permettre l'annulation.
    CouleurH : Couleur de la palette en Hexadécimal
    Couleur : Couleur de la palette en rgb
    Variable : Valeur du RadioButton de la gomme
    Rayon : rayon du pinceau
    Rayonnage : valeur de la scale
    

Définition des fenêtres :
    Open : Fenêtre d'ouverture de l'image
    Fenprinc : Mainloop
    Filtre : Fenêtre esclave de sélection de filtre


"""
def start():
    #ouvre la fenêtre d'accueil
    global Open
    Open=Tk()
    Open.geometry("250x75+300+300")
    Open.title("Explorateur")
    Text= Label(Open, text="Ouvrir une image")
    Text.pack(side=TOP)
    Ouvrir=Button(Open,text="Ouvrir",command=ok)
    Ouvrir.pack()
    Open.bind("<Return>",okE)
    Open.mainloop()

def ok():
    #permet de sélectionner l'image à ouvrir, l'ouvre, puis lance le main
    global chemin, ouv, l, L, ImageEditee, img, Open
    chemin=askopenfilename(title="Ouvrir le fichier:", initialdir='e:\\',) #ouvre l'explorateur de fichiers
    if chemin!="":
        ouv=Image.open(chemin)
        img=list(ouv.getdata())
        l,L=ouv.size
        ImageEditee=img
        Open.destroy()
        main()
    
def okE(key):
    #permet de sélectionner l'image à ouvrir, l'ouvre, puis lance le main
    global chemin, ouv, l, L, ImageEditee, img,Open
    touche=key.keysym
    Ouverture=askopenfilename(title="Ouvrir le fichier:", initialdir='e:\\') #ouvre l'explorateur de fichiers
    if touche=="Return":
        if chemin!="":
            ouv=Image.open(chemin)
            img=list(ouv.getdata())
            l,L=ouv.size
            ImageEditee=img
            Open.destroy()
            main()
            
def Alpha():
    global ImageEditee
    #transforme les image en niveau de gris vers rgb
    for j in range (L):
        for i in range (l):
            if type(ImageEditee[(j-1)*l+i])==type(1):
                ImageEditee[(j-1)*l+i]=[int(ImageEditee[(j-1)*l+i]),int(ImageEditee[(j-1)*l+i]),int(ImageEditee[(j-1)*l+i])]
    #Enlève le canal alpha
    if (len(ImageEditee[0]))==4:
        print("Removing Alpha...")
        for i in range(len(ImageEditee)):
            liste=list(ImageEditee[i])
            del liste[3]
            ImageEditee[i]=liste
        print("Done.")
    
def title(chemin):
    #donne le nom pour enregistrer le fichier + renommer la fenetre principale
    global fenprinc, nom
    a=list(chemin)
    a.reverse()
    c=a.index("/")
    del a[c:]
    d=a.index(".")
    del a[:(d+1)]
    a.reverse()
    nom="".join(a) 
    fenprinc.title(nom)

def init():
    global rayon, couleurH, gommeFiltrée, gommage, historique, ImageEditee
    #initialise les variables
    rayon=1
    couleurH="#ffffff"
    gommage=tuple(tuple(i) for i in ImageEditee)
    historique=[]
    historique.append(gommage)
    gommeFiltrée=gommage
    
                
    
    
def main():
    #programme principal qui appelle les fonctions
    global fenprinc, Calque0
    fenprinc=Tk()
    fenprinc.configure(width=2*l,height=2*L)
    
    Alpha()
    
    title(chemin)
    
    init()
    
    MiseEnPage()
    
    afficher()
    
    Calque0.bind('<B1-Motion>', dessin)
    Calque0.bind('<Button-1>', dessin)
    Calque0.bind('<Button-2>', filtres)
    Calque0.bind('<Button-3>', gomme)
    Calque0.bind('<B3-Motion>', gomme)
    Calque0.bind('<ButtonRelease-3>', actualiser)
    
    fenprinc.mainloop()

def MiseEnPage():
    #génération de l'interface
    global Variable, fenprinc, rayonnage, Calque0, Palette, pinceau
    valeurs = ['A', 'B']
    etiqs = ['Gommage filtré', 'Gommage parfait']
    Variable = StringVar()
    Variable.set(valeurs[1])
    etiquette=LabelFrame(fenprinc, text="Gomme (clic droit)")
    for i in range(0,2,1):
        selecteur = Radiobutton(etiquette, variable=Variable, text=etiqs[i], value=valeurs[i])
        selecteur.grid(row =i, column =1, padx=5, pady=5)
    etiquette.grid(row=3, column =2, rowspan=3, padx=5, pady=5)
    
    rayonnage=Scale(fenprinc, orient='vertical', from_=0, to=50, resolution=1, tickinterval=5, length=100, label='Pinceau', command=majPinceau)
    pinceau=Canvas(fenprinc,width=101,height=101,bg="white")
    pinceau.create_oval(51-rayon,51+rayon,51-rayon,51+rayon,outline="black",fill="white")
    
    Palette=Canvas(fenprinc,width=50,height=30,bg="white")
    filtreoriginal=Button(fenprinc,text="Choisir un filtre",command=filtre) #On crée le bouton qui      ouvre la fenêtre des filtres
    filtreoriginal.grid(row =3, column =3, padx=5, pady=5)
    ChangCoul=Button(fenprinc,text="Couleur",command=getColor)
    ChangCoul.grid(row =1, column =2, padx=5, pady=5) #Bouton pour changer de couleur de dessin
    save=Button(fenprinc, text="Enregistrer sous", command=enregistrer)
    save.grid(row =5, column =3, padx=5, pady=5) #Bouton pour enregistrer l'image
    Calque0=Canvas(fenprinc,width=l,height=L,bg="white")
    Calque0.grid(row =1, column =1, rowspan =5, padx =10, pady =10)
    rayonnage.grid(row =1, column =3, rowspan =2, padx=5, pady=5)
    Palette.grid(row =2, column =2, padx=5, pady=5) 
    pinceau.grid(row =1, column =4, rowspan =2, padx=5, pady=5) 
    Quitte=Button(fenprinc, text="Quitter", command=sur)
    Quitte.grid(row =5, column =4, padx=5, pady=5) 

def afficher():
    #affiche l'image
    global ImageEditee, Calque0
   
    print("Refreshing Data...")
    for j in range (L):
        for i in range (l):
            
            triplet=ImageEditee[(j-1)*l+i]
            fill0=rgb_to_hex(triplet)
            Calque0.create_oval(i,j,i,j,outline=fill0,fill=fill0)
    print("Done.")

def actualiser(evt):
    afficher()


def dessin(evt) :
    #dessine au pinceau
    global ImageEditee, Calque0
    Calque0.create_oval((evt.x)-(rayon), evt.y-rayon, evt.x+rayon, evt.y+rayon, fill=couleurH, outline=couleurH)
    list=Rayon(rayon,evt.x,evt.y)
    none=0
    for i in list:
        try :
            ImageEditee[(i[1]-1)*l+i[0]]=hex_to_rgb(couleurH)
        except :
            none+=1
            
    time.sleep(0.005)
    
def majPinceau(evt):
    #modifie le rayon du pinceau/de la gomme et met à jour l'aperçu
    global rayon, pinceau
    rayon=rayonnage.get()
    pinceau.delete('all')
    pinceau.create_oval(51-rayon,51-rayon,51+rayon,51+rayon,outline="black",fill="white")

def Rayon(r,x,y):
    #Renvoie les coordonnées de tous les points à traiter en fonction du rayon du pinceau
    listcoord=[]
    g=0
    cercle=[]
    if r==0:
        r=1
    while g<2*math.pi:
        cercle.append(g)
        g+=(math.pi/(r*4))
    for i in cercle:
        for j in range(0,r+1,1):
            xad=x+int(round(math.cos(i)*j,0))
            yad=y+int(round(math.sin(i)*j,0))
            listcoord.append([xad,yad])
    return listcoord
    
def getColor():
    #pour la palette de couleurs
    global couleur, couleurH
    color=askcolor()
    couleur = color[0]
    couleurH=color[1]
    Palette.configure(bg=couleurH)
    
def gomme(evt) :
    #effectue l'action inverse de dessin
    global ImageEditee, Calque0
    Calque0.create_oval((evt.x)-(rayon), evt.y-rayon, evt.x+rayon, evt.y+rayon, fill="black", outline="white")
    list=Rayon(rayon,evt.x,evt.y)
    for i in list:
        none=0
        if Variable.get()=="B":
            try :
                ImageEditee[(i[1]-1)*l+i[0]]=historique[0][(i[1]-1)*l+i[0]]
            except :
                none+=1
        else :
            try :
                ImageEditee[(i[1]-1)*l+i[0]]=gommeFiltrée[(i[1]-1)*l+i[0]]
            except :
                none+=1
            
    time.sleep(0.005)
    
    
            

    


            


def filtres(evt):
    #fenetre qui va regrouper tout les filtres
    Filtre=Toplevel() 
    Filtre.title("Filtres")
    Filtre.geometry("350x140+300+300")
    Negatif=Button(Filtre,text="Négatif",command=filtrenegatif)
    Negatif.grid(row=0, column=0, padx=5, pady=5)
    rose=Button(Filtre, text= "Filtre rose", command=filtrerose)
    rose.grid(row=0, column=1, padx=5, pady=5)
    bleu=Button(Filtre, text= "Filtre bleu", command=filtrebleu)
    bleu.grid(row=0, column=2, padx=5, pady=5)
    jaune=Button(Filtre, text="Filtre jaune", command=filtrejaune)
    jaune.grid(row=0, column=3, padx=5, pady=5)
    annule=Button(Filtre,text="Annuler",command=annuler)
    annule.grid(row=1, column=1, padx=5, pady=5)
    okey=Button(Filtre, text="Ok", command= Filtre.destroy)
    okey.grid(row=1, column=2, padx=5, pady=5)
    anuletout=Button(Filtre, text="Annuler tout", command=annulertout)
    anuletout.grid(row=2, column=3, padx=5, pady=5)
    Filtre.mainloop()
    
def filtre():
    #fenetre qui va regrouper tout les filtres
    Filtre=Toplevel() 
    Filtre.title("Filtres")
    Filtre.geometry("350x140+300+300")
    Negatif=Button(Filtre,text="Négatif",command=filtrenegatif)
    Negatif.grid(row=0, column=0, padx=5, pady=5)
    rose=Button(Filtre, text= "Filtre rose", command=filtrerose)
    rose.grid(row=0, column=1, padx=5, pady=5)
    bleu=Button(Filtre, text= "Filtre bleu", command=filtrebleu)
    bleu.grid(row=0, column=2, padx=5, pady=5)
    jaune=Button(Filtre, text="Filtre jaune", command=filtrejaune)
    jaune.grid(row=0, column=3, padx=5, pady=5)
    annule=Button(Filtre,text="Annuler",command=annuler)
    annule.grid(row=1, column=1, padx=5, pady=5)
    okey=Button(Filtre, text="Ok", command= Filtre.destroy)
    okey.grid(row=1, column=2, padx=5, pady=5)
    anuletout=Button(Filtre, text="Annuler tout", command=annulertout)
    anuletout.grid(row=2, column=3, padx=5, pady=5)
    Filtre.mainloop()

def filtrenegatif():
    
    global ImageEditee, historique, gommeFiltrée
    def Inversion (octet):
        return 255-octet
    
    raj=ImageEditee
    historique.append(raj) # on ajoute la liste des pixels à l'historique pour pouvoir annuler le filtre
    liste=[list(i) for i in raj]
    long=len(liste)
    for i in range (long):
        for j in range (3):
            a=liste[i][j]
            liste[i][j]=Inversion(a) #chaque couleur de chaque pixel est inversée
    

    ImageEditee=liste #on replace les pixels inversés dans l'image
    
    raj=gommeFiltrée # On actualise la gomme
    liste=[list(i) for i in raj]
    long=len(liste)
    
    for i in range (long):
        for j in range (3):
            a=liste[i][j]
            liste[i][j]=Inversion(a) #chaque couleur de chaque pixel est inversée
    liste=tuple(liste)
    gommeFiltrée=liste
    
    afficher()
    
def filtrerose():
    global ImageEditee, historique, gommeFiltrée
    raj=[list(i) for i in ImageEditee] #on récupère les pixels de l'image sous forme de liste
    historique.append(ImageEditee)
    long=len(raj)
    for i in range (long) :
        raj[i][1]=0 #pour chaque octet, on enlève le vert
        
    ImageEditee=raj #on replace les nouveaux pixels dans l'image
    
    raj=[list(i) for i in gommeFiltrée] #Gomme
    long=len(raj)
    for i in range (long) :
        raj[i][1]=0 #pour chaque octet, on enlève le vert
        
    gommeFiltrée=tuple(raj) #on replace les nouveaux pixels dans l'image
    afficher()
    
def filtrebleu():
    global ImageEditee,historique, gommeFiltrée
    historique.append(ImageEditee)
    raj=[list(i) for i in ImageEditee] #on récupère les pixels de l'image sous forme de liste
    long=len(raj)
    for i in range (long) :
        raj[i][0]=0 #pour chaque octet on enlève le rouge
        
    ImageEditee=raj
    
    raj=[list(i) for i in gommeFiltrée] #Gomme
    long=len(raj)
    for i in range (long) :
        raj[i][0]=0 #pour chaque octet on enlève le rouge
        
    gommeFiltrée=tuple(raj)
    afficher()
    
def filtrejaune():
    global ImageEditee, historique, gommeFiltrée
    historique.append(ImageEditee)
    raj=[list(i) for i in ImageEditee] #on récupère les pixels de l'image sous forme de liste
    long=len(raj)
    for i in range (long) :
        raj[i][2]=0 #pour chaque octet, on enlève le vert
        
    ImageEditee=raj
    
    raj=[list(i) for i in gommeFiltrée] #Gomme
    long=len(raj)
    for i in range (long) :
        raj[i][2]=0 
    gommeFiltrée=tuple(raj)
    
    afficher()
    
def annuler(): 
    #Pour annuler un filtre
    global historique, ImageEditee
    long=len(historique)
    try: #On teste afin que s'il n'y ait rien à annuler il n'y ai pas de message d'erreur
        ImageEditee=historique[long-1]
        del historique[long-2:]
    except:
        ImageEditee=ImageEditee
    
    afficher()
    
def annulertout():
    #pour revenir à l'original
    global historique, ImageEditee, gommeFiltrée
    try:
        ImageEditee=historique[0]
        del historique[1:]
    except:
        ImageEditee=ImageEditee
    gommeFiltrée=historique[0]
    afficher()
    
def enregistrer():
    #pour enregistrer
    global fenprinc
    Nouvim= Image.new(ouv.mode, ouv.size)
    Nouvim.putdata([tuple (i) for i in ImageEditee])
    sauve = asksaveasfilename(title="Enregistrer sous",initialfile=nom+ "_modifié_par_modificator2000", defaultextension= ".png") #explorateur pour sauvegarder le fichier, save prend la valeur du chemin complet du fichier à enregistrer
    if sauve!="":
        Nouvim.save(sauve)
        fenprinc.destroy()
    
def sur():
    #fenetre "êtes vous sur de quitter?"
    global fenprinc
    if messagebox.askokcancel("Confirmation", "Etes-vous sûr de vouloir quitter ? ") :
        fenprinc.destroy() 
        
start()
