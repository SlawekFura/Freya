import math

x = 0
y = 1
z = 2

def intersection(lst1, lst2):
    return list(set(lst1) & set(lst2))

def difference(lst1, lst2): 
    return list(set(lst1) - set(lst2))

def removeDuplicates(duplicate):
    final_list = []
    for num in duplicate:
        if num not in final_list:
            final_list.append(num)
    return final_list

def matchFloats(*floats):
    return all(math.isclose(floatToCompare, floats[0], abs_tol = 0.001) for floatToCompare in floats)

def match2FloatLists(floatList1, floatList2):
    for i in range(len(floatList1)):
        if not math.isclose(floatList1[i], floatList2[i], abs_tol = 0.001):
            return False
    return True

def roundFloatNestedList(floatNestedList, accuracy):
    return [[float(("%." + str(accuracy) + "f") % coord) for coord in elem] for elem in floatNestedList]

def roundFloatList(floatList, accuracy = 4):
    return [float(("%." + str(accuracy) + "f") % elem) for elem in floatList]


