#encoding:utf-8

import serial
import time
import datetime
import winsound
from tkinter import *
import json
from math import *
from PIL import Image, ImageTk

# Variables :
vitesse = float(0) # average speed
distance = float(0) # distance traveled in km
distMax = float(0) # max distance
kPoint = int(0) # points counter
kPente = int(0) # slope counter
kPhoto = int(0) # picture counter
reg = float(0) # home trainer setting number
peri = float(2.1) # wheel perimeter


# Fonctions :
def charger_image_from_PIL(filename, resize=None):  # this function is used to load an image and to pass it to tkinter
    image = Image.open(filename)
    if resize is not None:
        image = image.resize(resize, Image.ANTIALIAS)
    return ImageTk.PhotoImage(image) # return Tk image object


# Update de la fenetre :
def update():
    global vitesse,distance,reg,kPoint,kPhoto,kPente,idphoto,photo,x,y
    
    #if ser.inWaiting()>0 :                  # I just comment this part to test the program without the arduino
    #    data = str(ser.readline())
    #    data = data.replace("b'","")
    #    data = data.replace("\\r\\n'","")
    #    index = data.find(';')
    #    revs = int(data[:index])
    #    vitesse = float(data[index+1:])
    
    revs = 3    # number of wheel revolution since the last serial read
    vitesse = 20    # actual speed readed on the serial
    distance += ((revs*peri)/1000)*40   # incrementation of the distance
    reg = 0.942313*pentes[kPente]-0.09136   # calculation of the home-trainer setting taking into account the current slope
    if reg < 0 : reg = 0 # min setting
    elif reg > 5 : reg = 5 # max setting

    L_distance.config(text='Distance =\n'+str(round(distance,2))) # updating of the differents labels (distance, speed, slope, setting)
    L_vitesse.config(text='Vitesse =\n'+str(vitesse))
    L_pente.config(text='Pente =\n'+str(pentes[kPente]))
    L_reglage.config(text='Reglage =\n'+str(round(reg,0)))    

    if (distance < distMax) :
    
        if (distance > distPentes[kPente]) :
            #winsound.Beep(1500, 1000)
            kPente += 1

        if (distance > distPix[kPoint+1]) :
            kPoint += 1

        if (distance > distPhotos[kPhoto]) :
            kPhoto += 1
            photo = charger_image_from_PIL(str('courses/'+parcours+'/images/'+str(kPhoto)+'.png'), resize=(1120,700))
            fond.itemconfig(idphoto, image = photo)  

        x = pix[kPoint][0]*(1-((distance-distPix[kPoint])/(distPix[kPoint+1]-distPix[kPoint]))) + pix[kPoint+1][0]*((distance-distPix[kPoint])/(distPix[kPoint+1]-distPix[kPoint]))
        y = pix[kPoint][1]*(1-((distance-distPix[kPoint])/(distPix[kPoint+1]-distPix[kPoint]))) + pix[kPoint+1][1]*((distance-distPix[kPoint])/(distPix[kPoint+1]-distPix[kPoint]))
        trace.coords(rect, x-4, y-4, x+4, y+4)
        relieff.coords(ligne,18+570*(distance/distMax),0,18+570*(distance/distMax),80)

        fenetre.after(150,update)
        
    else :
        fond.destroy()
        trace.destroy()
        relieff.destroy()
        afficheur.destroy()
        fini = Label(fenetre, text="BRAVO")
        fini.pack()


# Initialisation :
#com = input("Quel COM ?\n")
#ser = serial.Serial(com, timeout=0.1)       # opening of the serial port (not use for testing the programm without the arduino connected)
parcours = input("Nom du parcours ?\n")
input("Appuyez sur Entrée pour commencer le parcours.\n")

# Reading course data :
with open(str('courses/'+parcours+'/donnees.json')) as json_data:
    data_dict = json.load(json_data)
    pix = data_dict["pix"]
    distPix = data_dict["distPix"]
    pentes = data_dict["pentes"]
    distPentes = data_dict["distPentes"]
    distPhotos = data_dict["distPhotos"]
distMax = distPentes[len(distPentes)-1]


# Creation fenetre :
fenetre = Tk()
fenetre.title('interface_graphique')

fond = Canvas(fenetre, width=1120, height=700, background='white')
photo = charger_image_from_PIL(str('courses/'+parcours+'/images/'+str(kPhoto)+'.png'), resize=(1120,700))
idphoto = fond.create_image(560, 350, image=photo)
fond.pack()

trace = Canvas(fond, width=340, height=340, background='white')
carte = PhotoImage(file='courses/'+parcours+'/carte.png')
trace.create_image(170, 170, image=carte)
rect = trace.create_rectangle(pix[kPoint][0]-4, pix[kPoint][1]-4, pix[kPoint][0]+4, pix[kPoint][1]+4, fill='red')
trace.place(x=0,y=0)

relieff = Canvas(fond, width=600, height=80, background='white')
relief = PhotoImage(file='courses/'+parcours+'/relief.png')
relieff.create_image(300, 40, image=relief)
ligne = relieff.create_line(18,0,18,80)
relieff.place(x=260,y=620)

afficheur = Frame(fond, borderwidth=2, relief=GROOVE)
afficheur.place(x=920,y=80, width = 200, heigh = 400)

L_distance = Label(afficheur, text='Distance =\n'+str(round(distance,2)), font=("Arial", 16))
L_distance.grid(column=0, row=0, pady = 20, padx = 20)
L_vitesse = Label(afficheur, text='Vitesse =\n'+str(vitesse), font=("Arial", 16))
L_vitesse.grid(column=0, row=1, pady = 20, padx = 20)
L_pente = Label(afficheur, text='Pente =\n'+str(pentes[kPente]), font=("Arial", 16))
L_pente.grid(column=0, row=2, pady = 20, padx = 20)
L_reglage = Label(afficheur, text='Reglage =\n'+str(round(reg,0)), font=("Arial", 16))
L_reglage.grid(column=0, row=3, pady = 20, padx = 20)

fenetre.after(50, update)

fenetre.mainloop()





    



