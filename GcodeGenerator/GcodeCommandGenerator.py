

def genGcode(outFile, polysMap): 
    fileToWrite = open(outFile,'w')
    safeHight = 48.0
    speed = 400.0;
    commandsMap = { "FastForward" : lambda x, y, z : "G00 " +  "X" + str(x) + " Y" + str(y) + " Z" + str(z) + "F" + str(speed) + "\n",
                    "Forward" : lambda x, y, z : "G01 " +  "X" + str(x) + " Y" + str(y) + " Z" + str(z) + "F" + str(speed) + "\n",
                    "SetCoordMM" : "G21\n\n",
                    "EndProgram" : "\nM02\n" }

    keys = sorted(polysMap.keys(), reverse = True)
    print(keys)
    fileToWrite.write(commandsMap["SetCoordMM"])
    for key in keys:
        for polys in polysMap[key]:
            fileToWrite.write(commandsMap["FastForward"](1,2,3))

    fileToWrite.write(commandsMap["EndProgram"])
    fileToWrite.close()
            
