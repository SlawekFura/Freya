
x = 0
y = 1
z = 2

def intersection(lst1, lst2): 
    return list(set(lst1) & set(lst2))

def difference(lst1, lst2): 
    return list(set(lst1) - set(lst2))


