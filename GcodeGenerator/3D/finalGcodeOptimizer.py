from shapely.geometry import Point
from shapely.geometry.polygon import Polygon

import sys
sys.path.append('../Common/')
import ReadWritePolysFromFile as RWPolys
from collections import OrderedDict 
from anytree import Node, RenderTree, AnyNode, PostOrderIter, search, LevelOrderIter, AsciiStyle
import GcodeCommandGenerator as gGen
from utils import *



class PolysContMap():
    def __init__(self, polylines):
        self.numOfContains = 0
        self.polylinesMap = {}
        self.polyDesc = 0
        self.contNumDesc = 1

        for polyIt in range(0, len(polylines)):
    
            self.initPoly(polyIt, polylines[polyIt])
     
            firstPoly = Polygon(polylines[polyIt])
            #print("for poly:", polyIt)
            for compIt in range(0, len(polylines)):
                polyToCompare = Polygon(polylines[compIt])
                if polyIt != compIt:
                    self.updatePolysMap(polyIt, firstPoly.contains(polyToCompare))
    

    def update(self, polyIt, polyline, isContaintful):
        if self.polylinesMap[polyIt]: 
            if isContaintful:
                self.polylineMap[polyIt]

    def initPoly(self, polyIt, poly):
        initNumOfcontainments = 0
        self.polylinesMap[polyIt] = [poly, initNumOfcontainments]
    
    def updatePolysMap(self, polyIt, isContained):
        if isContained:
            self.polylinesMap[polyIt][self.contNumDesc] += 1
    
    def sort(self):
        
        sortedPolymap = sorted(self.polylinesMap.items(), key=lambda (k,v): v[1], reverse = True)
        self.polylinesMap = OrderedDict()
        keyDesc = 0
        valDesc = 1
        for elem in sortedPolymap:
            key = elem[keyDesc]
            val = elem[valDesc]
            self.polylinesMap[key] = [val[self.polyDesc], val[self.contNumDesc]] 




def isPolyCloseEnoughToAnother(poly1, poly2, sufficientDist):
    for i in range(0, len(poly1)):    
        x1 = poly1[i][x]
        y1 = poly1[i][y]
        for j in range(0, len(poly2)):    
            x2 = poly2[j][x]
            y2 = poly2[j][y]
            newDist = math.hypot(x2 - x1, y2 - y1)
            if newDist < sufficientDist:
                return True
    return False

def genOptimizationTree(offsetPolygonsMap = RWPolys.readPolysFromFile("dataFromCgal.txt"), diameter = 3):
    optMap = {}
    for zCoord, polylines in offsetPolygonsMap.items():
        #print("z:", zCoord, "num", len(polylines))
        
        polysContMap = PolysContMap(polylines)
        polysContMap.sort()

        key = polysContMap.polylinesMap.items()[0][0]
        val = polysContMap.polylinesMap.items()[0][1]
        mainNode = AnyNode(id=-1, poly=None)

        keyIdx = 0
        polyContIdx = 1
        polyIdx = 0

        values = polysContMap.polylinesMap.items()
        mainPolyCont = values[0]#[1][0]
        mainPolyContKey = mainPolyCont[keyIdx]
        mainPolyContPoly = mainPolyCont[polyContIdx][polyIdx]
        
        #print mainPolyContPoly
        AnyNode(id=mainPolyContKey, poly=mainPolyContPoly, parent=mainNode)
        del values[mainPolyContKey]
        #print values

        while values:
            isThereAnyNodeAddition = False
            contPoly = None
            
            for elem in values:
                key = elem[keyIdx]
                #print("key", key) 
                contPoly = elem[polyContIdx][polyIdx]
                nodesIds = [node.id for node in LevelOrderIter(mainNode, filter_=lambda n: n.id != -1)]
                
                for nId in nodesIds:
                    nodeToComp = search.findall(mainNode, lambda node: node.id == nId)[0]
                    #print("nid", nId) 
                    if isPolyCloseEnoughToAnother(nodeToComp.poly, contPoly, diameter):
                        AnyNode(id=key, poly=contPoly, parent=nodeToComp)
                        values.remove(elem)
                        isThereAnyNodeAddition = True
                        break
                    
                #print nodesIds
                #print "\n"
            if not isThereAnyNodeAddition:
                elem = values[0]
                key = elem[keyIdx]
                contPoly = elem[polyContIdx][polyIdx]
                AnyNode(id=key, poly=contPoly, parent=mainNode)
                values.remove(elem)
                

        #for pre, fill, node in RenderTree(mainNode):
        #    print("%s%s" % (pre, node.id))
        optMap[zCoord] = mainNode
    return optMap

#tree = genOptimizationTree()
#gGen.genGcode3DOpt("./optGcode.gcode", tree, 100, 300, 3.0)
