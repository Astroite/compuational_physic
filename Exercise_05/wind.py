# -*- coding: utf-8 -*-
"""
Created on Tue Oct 17 23:05:54 2017

@author: 王乎
"""

import sys
import math
import time
import numpy 
from matplotlib import pyplot
from numpy import arange

# fixed 
g        = 9.8
#B2m      = 4e-5
iniSpeed = 50
sita     = math.pi/2
sign     = -2
vwinds    = arange(-2,6,2)
##############################################
#    Set  Angle 
'''
inputStartAngle = arange(0,95,5)
##
inputStartAngle = input("Start Angle : ")
startAngle = float(inputStartAngle)
if startAngle >= 0 and startAngle <= 90:
    Angle = (startAngle/90)*sita 
else :
    print("error") 
    exit()
'''


class FlightState:
    def __init__(self, _x = 0, _y = 0, _vx = 0, _vy = 0, _t = 0):
        self.x  = _x
        self.y  = _y
        self.vx = _vx
        self.vy = _vy
        self.t  = _t


class CannonShell:
    def __init__(self, _fs = FlightState(0, 0, 0, 0, 0), _dt = 0.1):
        self.flightState = []
        self.flightState.append(_fs)
        self.dt = _dt
        print ("good!")
        
    def getNextState(self,currentState):
        #currentState = self.flightState[-1]
        nx  = currentState.x  + currentState.vx * self.dt
        ny  = currentState.y  + currentState.vy * self.dt
        nvx = currentState.vx + self.getCurrentAcc(currentState)[0] * self.dt
        nvy = currentState.vy + self.getCurrentAcc(currentState)[1] * self.dt
        return FlightState(nx, ny, nvx, nvy, currentState.t + self.dt)
        
    def shoot(self):
        while not(self.flightState[-1].y < 0):
            self.flightState.append(self.getNextState(self.flightState[-1]))
            
        r = - self.flightState[-2].y / self.flightState[-1].y
        self.flightState[-1].x = (self.flightState[-2].x + r * self.flightState[-1].x)/(r+1)
        self.flightState[-1].y = 0
    
    def getCurrentAcc(self,currentState):
        factor     = self.getFactor(currentState)
        B2m        = self.getB2m(currentState)
        v     = math.sqrt(currentState.vx ** 2 + currentState.vy ** 2)
        ax         = factor * (-B2m * abs(v - vwind) * (currentState.vx - vwind))
        ay         = factor * (-B2m * abs(v - vwind) * currentState.vy) - g
        #ax         = (-B2m * abs(v - vwind) * (currentState.vx - vwind))
        #ay         = (-B2m * abs(v - vwind) * currentState.vy) - g
        currentAcc = [ax,ay]
        return currentAcc
        
    def getFactor(self,currentState):
        alpha  = 2.5
        a      = 6.5e-3
        factor = (1-a*currentState.y / 287.15) ** alpha
        return factor
     
    def getB2m(self,currentState):
        v     = math.sqrt(currentState.vx ** 2 + currentState.vy ** 2)
        const = 0.0039
        vd    = 35
        det   = 5
        mid   = math.exp((v-vd) / det)
        B2m   = const + 0.0058 / (1 + mid)
        return B2m
    
    def showTrajectory(self):
        x = []
        y = []
        for fs in self.flightState:
            x.append(fs.x)
            y.append(fs.y)
        pyplot.plot(x, y, label='$V_{wind} = $%sm/s'%vwind)
        pyplot.legend(loc='$V_wind = $%s'%vwind)
    
        
        


###################################################################################
fig = pyplot.figure(figsize=(16,8))
xmin, xmax = 0., 150
ymin, ymax = 0., 50
dx = (xmax - xmin) * 0.1
dy = (ymax - ymin) * 0.2
ax = pyplot.axes(xlim = (xmin, xmax + dx), ylim = (ymin, ymax + dy))


inputStartAngle = [45]

for i in range(len(inputStartAngle)):
    for j in range(len(vwinds)):
        vwind = vwinds[j]
        startAngle = inputStartAngle[i]
        Angle      = (startAngle/90)*sita
        
        # name the axis
        pyplot.xlabel(r'$x(m)$', fontsize=16)
        pyplot.ylabel(r'$y(m)$', fontsize=16)
        pyplot.title("Baseball Trajectory at Angle $45^{\circ}$")
##################################################################################
        iniVy = iniSpeed*math.sin(Angle)
        iniVx = iniSpeed*math.cos(Angle)
        cannonShell = CannonShell(FlightState(0, 0, iniVx, iniVy, 0), _dt = 0.1)
        cannonShell.shoot()
        cannonShell.showTrajectory()

pyplot.savefig("Baseball Trajectory")

pyplot.show()


