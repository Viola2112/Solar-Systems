# Solar system class module
# Edition 1.3 (1.0 is origonal)
# 2/5/2020
# Binary stars are now stable 

from graphics import *
from math import *
from time import sleep

class Planet:

    def __init__(self,mass,radius,color,xPos,yPos,xVel=0,yVel=0):
        self.m = mass
        self.r = radius
        self.c = color
        self.xPos = xPos
        self.oldXPos = xPos
        self.yPos = yPos
        self.oldYPos = yPos
        self.xVel = xVel
        self.oldXVel = xVel
        self.yVel = yVel
        self.oldYVel = yVel
        self.circ = Circle(Point(self.xPos,self.yPos),self.r)
        self.circ.setFill(self.c)

    def _update_Circ(self):
        self.circ = Circle(Point(self.xPos,self.yPos),self.r)
        self.circ.setFill(self.c)

    def draw(self,win):
        self.circ.draw(win)

    def undraw(self):
        self.circ.undraw()

    def update(self,time,xXl=0,yXl=0):
        self.xVel += time*xXl
        self.yVel += time*yXl
        self.xPos += time*self.xVel
        self.yPos += time*self.yVel
        self._update_Circ()

    def oldUpdate(self,win,time,xXl=0,yXl=0):
        self.undraw()
        self.oldXVel += time*xXl
        self.oldYVel += time*yXl
        self.oldXPos += time*self.xVel
        self.oldYPos += time*self.yVel
        self._update_Circ()
        self.draw(win)

    def transcribe(self):
        self.oldXVel = self.xVel
        self.oldYVel = self.yVel
        self.oldXPos = self.xPos
        self.oldYPos = self.yPos

    def betUp(self,win,time,xXl=0,yXl=0):
        self.undraw()
        self.update(time,xXl,yXl)
        self.draw(win)

class SolarSystem:

    def __init__(self,planetList,name="Solar System",winSize=500,G=100):
        self.win = GraphWin(name,winSize,winSize)
        self.win.setCoords(-100,-100,100,100)
        self.win.setBackground("black")
        self.pList = planetList
        for p in self.pList:
            p.draw(self.win)
        self.G = G

    def updatePlanet(self,planetNum,time):
        tempPList = self.pList[:]
        tempPList.pop(planetNum)
        p = self.pList[planetNum]
        totxXl = 0
        totyXl = 0
        for plan in tempPList:
            dist = sqrt((plan.xPos-p.xPos)**2 + (plan.yPos-p.yPos)**2)
            sinTh = (plan.yPos-p.yPos)/(dist)
            cosTh = (plan.xPos-p.xPos)/(dist)
            fullXl = (self.G*plan.m)/(dist**2)
            xXl = cosTh*fullXl
            yXl = sinTh*fullXl
            totxXl += xXl
            totyXl += yXl
        p.betUp(self.win,time,totxXl,totyXl)

    def updateOldPlanet(self,planetNum,time):
        tempPList = self.pList[:]
        tempPList.pop(planetNum)
        p = self.pList[planetNum]
        totxXl = 0
        totyXl = 0
        for plan in tempPList:
            dist = sqrt((plan.oldXPos-p.oldXPos)**2
                        + (plan.oldYPos-p.oldYPos)**2)
            sinTh = (plan.oldYPos-p.oldYPos)/(dist)
            cosTh = (plan.oldXPos-p.oldXPos)/(dist)
            fullXl = (self.G*plan.m)/(dist**2)
            xXl = cosTh*fullXl
            yXl = sinTh*fullXl
            totxXl += xXl
            totyXl += yXl
        p.betUp(self.win,time,totxXl,totyXl)

    def updateAll(self,time):
        for i in range(len(self.pList)):
            self.updatePlanet(i,time)

    def updateOlds(self,time):
        for planet in self.pList:
            planet.transcribe()
        for i in range(len(self.pList)):
            self.updateOldPlanet(i,time)

    def updateAllButFirst(self,time):
        for i in range(len(self.pList)-1):
            self.updatePlanet(i+1,time)




class BigSolarSystem(SolarSystem):

    def __init__(self,planetList,name="Solar System",winSize=750,G=100):
        self.win = GraphWin(name,winSize,winSize)
        self.win.setCoords(-150,-150,150,150)
        self.win.setBackground("black")
        self.pList = planetList
        for p in self.pList:
            p.draw(self.win)
        self.G = G

class MegaSolarSystem(SolarSystem):

    def __init__(self,planetList,name="Solar System",winSize=750,G=100):
        self.win = GraphWin(name,winSize,winSize)
        self.win.setCoords(-300,-300,300,300)
        self.win.setBackground("black")
        self.pList = planetList
        for p in self.pList:
            p.draw(self.win)
        self.G = G

    

def test(starMass=100,pause=0.05):
    sun = Planet(starMass,10,"yellow",0,0)
    plan = Planet(1,3,"blue",25,0,0,20)
    sol = SolarSystem([sun,plan])
    while sol.win.checkKey() == "":
        sol.updatePlanet(1,0.1)
        sleep(pause)
    sol.win.close()

def test2(starMass=100,p1Mass=1,p2Mass=1,pause=0.025):
    sun = Planet(starMass,10,"yellow",0,0)
    plan = Planet(p1Mass,3,"blue",25,0,0,20)
    plan2 = Planet(p2Mass,3,"red",49,0,0,100/7)
    sol = SolarSystem([sun,plan,plan2])
    while sol.win.checkKey() == "":
        sol.updateAllButFirst(0.1)
        sleep(pause)
    sol.win.close()

def test2i(starMass=100,p1mass=1,p2mass=1,pause=0.025): # Orbit not stable
    sun = Planet(starMass,10,"yellow",0,0)
    plan = Planet(p1mass,3,"blue",25,0,0,20)
    plan2 = Planet(p2mass,3,"red",49,0,0,100/7)
    sol = SolarSystem([sun,plan,plan2])
    while sol.win.checkKey() == "":
        sol.updateOlds(0.1)
        sleep(pause)
    sol.win.close()

def binStars(speed): #Can't get stable orbit
    star1 = Planet(50,10,"yellow",25,0,0,speed)
    star2 = Planet(50,10,"yellow",-25,0,0,-speed)
    sol = SolarSystem([star1,star2])
    while sol.win.checkKey() == "":
        sol.updateAll(0.1)
        sleep(0.025)
    sol.win.close()

def binStars2(speed=7.5): #Stable orbit!!!
    star1 = Planet(50,10,"yellow",25,0,0,speed)
    star2 = Planet(50,10,"yellow",-25,0,0,-speed)
    sol = SolarSystem([star1,star2])
    while sol.win.checkKey() == "":
        sol.updateOlds(0.1)
        sleep(0.025)
    sol.win.close()

def test3(starMass=100,p1Mass=1,p2Mass=1,p3Mass=1,pause=0.025):
    sun = Planet(starMass,10,"yellow",0,0)
    plan = Planet(p1Mass,3,"blue",25,0,0,20)
    plan2 = Planet(p2Mass,3,"red",49,0,0,100/7)
    plan3 = Planet(p3Mass,3,"orange",81,0,0,100/9)
    sol = SolarSystem([sun,plan,plan2,plan3])
    while sol.win.checkKey() == "":
        sol.updateAllButFirst(0.1)
        sleep(pause)
    sol.win.close()
    
def test4(starMass=100,p1Mass=1,p2Mass=1,p3Mass=1,p4Mass=1,pause=0.025):
    sun = Planet(starMass,10,"yellow",0,0)
    plan = Planet(p1Mass,3,"blue",25,0,0,20)
    plan2 = Planet(p2Mass,3,"red",49,0,0,100/7)
    plan3 = Planet(p3Mass,3,"orange",81,0,0,100/9)
    plan4 = Planet(p4Mass,3,"white",121,0,0,100/11)
    sol = SolarSystem([sun,plan,plan2,plan3,plan4])
    while sol.win.checkKey() == "":
        sol.updateAllButFirst(0.1)
        sleep(pause)
    sol.win.close()

def bigtest4(starMass=100,p1Mass=1,p2Mass=1,p3Mass=1,p4Mass=1,pause=0.025):
    sun = Planet(starMass,10,"yellow",0,0)
    plan = Planet(p1Mass,3,"blue",25,0,0,20)
    plan2 = Planet(p2Mass,3,"red",49,0,0,100/7)
    plan3 = Planet(p3Mass,3,"orange",81,0,0,100/9)
    plan4 = Planet(p4Mass,3,"white",121,0,0,100/11)
    sol = BigSolarSystem([sun,plan,plan2,plan3,plan4])
    while sol.win.checkKey() == "":
        sol.updateAllButFirst(0.1)
        sleep(pause)
    sol.win.close()

def bigtest5(starMass=100,p1Mass=1,p2Mass=1,p3Mass=1,p4Mass=1,p5Mass=1,pause=0.025):
    # Purple planet doesn't quite fit on screen :(
    # Not stable
    sun = Planet(starMass,10,"yellow",0,0)
    plan = Planet(p1Mass,3,"blue",25,0,0,20)
    plan2 = Planet(p2Mass,3,"red",49,0,0,100/7)
    plan3 = Planet(p3Mass,3,"orange",81,0,0,100/9)
    plan4 = Planet(p4Mass,3,"white",121,0,0,100/11)
    plan5 = Planet(p5Mass,3,"purple",169,0,0,100/13)
    sol = BigSolarSystem([sun,plan,plan2,plan3,plan4,plan5])
    while sol.win.checkKey() == "":
        sol.updateAllButFirst(0.1)
        sleep(pause)
    sol.win.close()

def megatest5(starMass=100,p1Mass=1,p2Mass=1,p3Mass=1,p4Mass=1,p5Mass=1,pause=0.025):
    # Not stable orbits - can make stable if planet masses are decreased
    sun = Planet(starMass,5,"yellow",0,0)
    plan = Planet(p1Mass,1.5,"blue",25,0,0,20)
    plan2 = Planet(p2Mass,1.5,"red",49,0,0,100/7)
    plan3 = Planet(p3Mass,1.5,"orange",81,0,0,100/9)
    plan4 = Planet(p4Mass,1.5,"white",121,0,0,100/11)
    plan5 = Planet(p5Mass,1.5,"light green",225,0,0,100/15)
    sol = MegaSolarSystem([sun,plan,plan2,plan3,plan4,plan5])
    while sol.win.checkKey() == "":
        sol.updateAllButFirst(0.1)
        sleep(pause)
    sol.win.close()







    
        
        
