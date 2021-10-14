import matplotlib.pyplot as plt
import gpxpy
import json
from math import *
from statistics import mean
 
gpx_file = open('C:/Users/User/Desktop/daniela.gpx', 'r')
gpx = gpxpy.parse(gpx_file)
 
points=gpx.tracks[0].segments[0].points
print(len(points))

data = {}
data['pix'] = []
data['distPix'] = []
data['pentes'] = []
data['distPentes'] = []

pentesActu = []
distance = 0
g=0
h=0
j=0
k = int(len(points)/300)
if k<1 :
    k=1

# pos sous forme [latitude, longitude]

posPix_hautGauche = [43.581220,1.978112]
posPix_basDroite = [43.361173,2.290648]
distMax = 110

def posToPix(pos) :
    res = [0,0]  #x,y
    res[0] = ((pos[1] - posPix_hautGauche[1])/(posPix_basDroite[1] - posPix_hautGauche[1]))*340
    res[1] = ((posPix_hautGauche[0] - pos[0])/(posPix_hautGauche[0] - posPix_basDroite[0]))*340
    return(res)

def pointToPos(point) :
    return([point.latitude,point.longitude,point.elevation])

def calcDist(point1,point2) :
    return((1852 * (60* acos(sin(pointToPos(point1)[0])*sin(pointToPos(point2)[0]) + cos(pointToPos(point1)[0])*cos(pointToPos(point2)[0])*cos(pointToPos(point2)[1]-pointToPos(point1)[1])))) /1000)  #en km

def calcPente(point1,point2) :
    return((pointToPos(point2)[2]-pointToPos(point1)[2])*(0.1/calcDist(point1,point2)))  #en degres

deltaPente = 0.5
deltaPix = distMax/100

data['distPix'].append(0)
data['pix'].append(posToPix([points[0].latitude,points[0].longitude]))


dernierPointPente = points[0]
dernierPointDist = points[0]
dernierPente = 0
pentesActu = [calcPente(points[0],points[1])]
for i in range(k,len(points),k):
    distance += calcDist(points[i-k],points[i])

    #print(calcPente(dernierPointPente,points[i]),dernierPente,mean(pentesActu))
    
    if calcDist(dernierPointPente,points[i]) > deltaPente :
        if abs(calcPente(dernierPointPente,points[i])-dernierPente)>0.8 :
            data['distPentes'].append(distance-0.05)
            dernierPente = mean(pentesActu)
            data['pentes'].append(dernierPente)
            pentesActu = [calcPente(dernierPointPente,points[i])]
            if i == len(points)-1 :
                g=1
        else :
            pentesActu.append(calcPente(dernierPointPente,points[i]))

        dernierPointPente=points[i]

    if calcDist(dernierPointDist,points[i]) > deltaPix :
        data['distPix'].append(distance)
        data['pix'].append(posToPix(pointToPos(points[i])))
        dernierPointDist=points[i]
        if i == len(points)-1 :
                h=1

    j=i

for i in range(j+1,len(points)) :
    distance += calcDist(points[i-1],points[i])   #calcul de la distance qu'il reste à la fin si le pas est plus grand que 1

if g==0 :
    data['distPentes'].append(distance)
    data['pentes'].append(calcPente(dernierPointPente,points[len(points)-1]))

if h==0 :    
    data['distPix'].append(distance)
    data['pix'].append(posToPix(pointToPos(points[len(points)-1])))
    
print(len(data['distPix']),len(data['pix']),len(data['distPentes']),len(data['pentes']))
print(distance)
plt.plot(data['distPentes'],data['pentes'])
plt.show()

with open('donnees.json', 'w') as outfile:
    json.dump(data, outfile)
