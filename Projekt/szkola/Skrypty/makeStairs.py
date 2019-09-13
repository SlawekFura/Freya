import sys
import os
import math

def printPointG0(XPos, YPos, ZPos, FPrec):
    print('G0 X' + str(round(XPos, FPrec))  + ' Y' + str(round(YPos, FPrec)) + ' Z' +  str(round(ZPos, FPrec)))
def printPointG1(XPos, YPos, ZPos, FPrec, ZFeedRate):
    print('G1 X' + str(round(XPos, FPrec))  + ' Y' + str(round(YPos, FPrec)) + ' Z' +  str(round(ZPos, FPrec)) + ' F' + str(ZFeedRate))
def addXPos(XPos, XDir):
    if(XDir == "X+"):
        XPos += stairsWidth + 3.0 * toolDiameter
        return XPos, "X-"
    else:
        XPos -= stairsWidth + 3.0 * toolDiameter
        return XPos, "X+"


#stairsWidth = float(input("Enter stairs width: ")) 
#stairsHeight = float(input("Enter stairs height: ")) 
#stairsNum = int(input("Enter num of stairs: "))
#landingLength = input("Enter landingLength: ") 
#toolDiameter = input("Enter tool diameter: ") 
#upOrDownstairs = input("Up/Down/Both: ") 

stairsWidth = 4.27
stairsHeight = 3.68
stairsNum = 13

landingLength = 3.71;
stairsLength = 15.91;
toolDiameter = 3.0;

singleStepHeight = stairsHeight / stairsNum
singleStepLength = (stairsLength - landingLength) / (stairsNum - 1) / 2;

ZFeedRate = 200.0
XYFeedRate = 1000.0

baseXPosition = 0.0
baseYPosition = 0.0
baseZPosition = 0.0
SafeZPosition = 7.0
XPos = baseXPosition - toolDiameter * 1.5
YPos = baseYPosition - toolDiameter / 2
ZPos = baseZPosition

XDir = "X+"
FPrec = 2

printPointG0(XPos, YPos, SafeZPosition, FPrec)

for step in range (stairsNum + 1):
    YPos = baseYPosition + step * singleStepLength - toolDiameter / 2
    ZPos = baseZPosition + step * singleStepHeight
    printPointG1(XPos, YPos, ZPos, FPrec, ZFeedRate)
    XPos, XDir = addXPos(XPos, XDir)
    printPointG1(XPos, YPos, ZPos, FPrec, XYFeedRate)

for step in range (math.ceil(landingLength / (toolDiameter * 0.8))):
    YPos += toolDiameter * 0.8
    printPointG1(XPos, YPos, ZPos, FPrec, XYFeedRate)
    XPos, XDir = addXPos(XPos, XDir)
    printPointG1(XPos, YPos, ZPos, FPrec, XYFeedRate)

for step in range (stairsNum):
    YPos = baseYPosition + stairsNum * singleStepLength + landingLength + (step - 1) * singleStepLength + toolDiameter / 2  
    ZPos = baseZPosition + stairsHeight - (1 + step) * singleStepHeight
    printPointG1(XPos, YPos, ZPos, FPrec, ZFeedRate)
    XPos, XDir = addXPos(XPos, XDir)
    printPointG1(XPos, YPos, ZPos, FPrec, XYFeedRate)

XPos = baseXPosition + stairsWidth + toolDiameter / 2
printPointG1(XPos, YPos, ZPos, FPrec, XYFeedRate)
YPos -= (stairsLength + toolDiameter)
printPointG1(XPos, YPos, ZPos, FPrec, XYFeedRate)
XPos, XDir = addXPos(XPos, XDir)
XPos = baseXPosition - toolDiameter / 2
printPointG1(XPos, YPos, ZPos, FPrec, XYFeedRate)
YPos += stairsLength + toolDiameter
printPointG1(XPos, YPos, ZPos, FPrec, XYFeedRate)
printPointG1(XPos, YPos, SafeZPosition, FPrec, ZFeedRate)
printPointG0(baseXPosition, baseYPosition, SafeZPosition, FPrec)
