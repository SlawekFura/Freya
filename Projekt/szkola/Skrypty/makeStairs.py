import sys
import os
import math

def printPoint(XPos, YPoz, ZPos, FPrec):
    print('X' + str(round(XPos, FPrec))  + ' Y' + str(round(YPos, FPrec)) + ' Z' +  str(round(ZPos, FPrec)))

#stairsWidth = float(input("Enter stairs width: ")) 
#stairsHeight = float(input("Enter stairs height: ")) 
#stairsNum = int(input("Enter num of stairs: "))
#landingLength = input("Enter landingLength: ") 
#toolDiameter = input("Enter tool diameter: ") 
#upOrDownstairs = input("Up/Down/Both: ") 

stairsWidth = 7.69
stairsHeight = 3.92
stairsNum = 13

landingLength = 3.2;
starsLength = 15.20;
toolDiameter = 1.0;

singleStepHeight = stairsHeight/stairsNum
singleStepLength = (starsLength - landingLength) / (stairsNum - 1) / 2;
print ("singleStepLength: " + str(singleStepLength))

baseXPosition = 0.0
baseYPosition = 0.0
baseZPosition = 0.0
XPos = baseXPosition
YPos = baseYPosition - toolDiameter / 2
ZPos = baseZPosition

XDir = "X+"
FPrec = 2

format(XPos, '.3f')
format(ZPos, '.3f')
for step in range (stairsNum + 1):
    YPos = baseYPosition + step * singleStepLength - toolDiameter / 2
    ZPos = baseZPosition + step * singleStepHeight
    printPoint(XPos, YPos, ZPos, FPrec)
    if(XDir == "X+"):
        XPos += stairsWidth
        XDir = "X-"
    else:
        XPos -= stairsWidth
        XDir = "X+"
    printPoint(XPos, YPos, ZPos, FPrec)

for step in range (math.ceil(landingLength / (toolDiameter * 0.8))):
    printPoint(XPos, YPos, ZPos, FPrec)


