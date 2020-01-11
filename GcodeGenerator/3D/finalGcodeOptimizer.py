from shapely.geometry import Point
from shapely.geometry.polygon import Polygon

import sys
sys.path.append('../Common/')
import ReadWritePolysFromFile as RWPolys
from collections import OrderedDict 
from anytree import Node, RenderTree, AnyNode, PostOrderIter, search, LevelOrderIter, AsciiStyle
import GcodeCommandGenerator as gGen



class PolysContMap():
    def __init__(self):
        self.numOfContains = 0
        self.polylinesMap = {}
        self.polyDesc = 0
        self.contNumDesc = 1
    
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

def genOptimizationTree(offsetPolygonsMap = RWPolys.readPolysFromFile("dataFromCgal.txt")):
    optMap = {}
    for zCoord, polylines in offsetPolygonsMap.items():
        print("z:", zCoord, "num", len(polylines))
        
        polysContMap = PolysContMap()
    
        for polyIt in range(0, len(polylines)):
    
            polysContMap.initPoly(polyIt, polylines[polyIt])
     
            firstPoly = Polygon(polylines[polyIt])
            #print("for poly:", polyIt)
            for compIt in range(0, len(polylines)):
                polyToCompare = Polygon(polylines[compIt])
                if polyIt != compIt:
                    polysContMap.updatePolysMap(polyIt, firstPoly.contains(polyToCompare))
       
        polysContMap.sort()
        for key, val in polysContMap.polylinesMap.items():
            print (key, val[1])
    
        key = polysContMap.polylinesMap.items()[0][0]
        val = polysContMap.polylinesMap.items()[0][1]
        mainNode = AnyNode(id=-1, poly=None)
        for key, val in polysContMap.polylinesMap.items():
            polyline = val[0]
    
            nodesIds = [node.id for node in LevelOrderIter(mainNode)]
            nodesIds.reverse()
            #print(RenderTree(tree, style=AsciiStyle()).by_attr())
            
            isNewNodeAdd = False
            for nodeId in nodesIds:
                nodeToComp = search.findall(mainNode, lambda node: node.id == nodeId)[0]
                if not nodeToComp:
                    print "error!!"
                
                if Polygon(nodeToComp.poly).contains(Polygon(polyline)):
                    AnyNode(id=key, poly=polyline, parent=nodeToComp)
                    isNewNodeAdd = True
                    break
            if not isNewNodeAdd:
                AnyNode(id=key, poly=polyline, parent=mainNode)
            
        for pre, fill, node in RenderTree(mainNode):
            print("%s%s" % (pre, node.id))
        optMap[zCoord] = mainNode
    return optMap

tree = genOptimizationTree()
gGen.genGcode3DOpt("./optGcode.gcode", tree, 100, 300)
