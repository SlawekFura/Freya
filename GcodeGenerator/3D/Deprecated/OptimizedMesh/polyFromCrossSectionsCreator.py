


def genPolylinesFromCrossSections(self):
    polyMap = {}

    for key, values in self.linesMap.items():
        linesList = list(values)
        polylines = [list(linesList[0][1:])]
        linesList.remove(linesList[0])
        for polyline in polylines:
            token = True
            while(token):
                token = False
                for lineIt in reversed(linesList):
                    line = copy.deepcopy(lineIt)
                    if polyline[0] == line[0]:
                        polyline.insert(0, line[1])
                    elif polyline[-1] == line[0]:
                        polyline.append(line[1])
                    elif polyline[0] == line[1]:
                        polyline.insert(0, line[0])
                    elif polyline[-1] == line[1]:
                        polyline.append(line[0])
                    else:
                        continue
                    linesList.remove(line)
                    token = True
            if linesList:
                polylines.append(list(linesList[0][1:]))
                linesList.remove(linesList[0])
        polyMap.update({key : polylines})
    return polyMap, self.verticesMap

