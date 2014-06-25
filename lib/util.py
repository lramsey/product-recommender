import numpy as np
import math

alphabet  = ['b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
symbols   = ['~','=','@','#','<', '>','$','%','^','&','*','(',')','_','+','{','}','/','|']

def reducer(num,arr, modulos=[]):
    modulos.append(num%len(arr))
    if num/len(arr) > 0:
        return reducer(num/len(arr), arr, modulos)
    return modulos

def generateItems(num, arr):
    size = int(math.ceil(math.log(num, len(arr))))
    results = []
    for i in range(0, num):
        characters = reducer(i, arr)
        text = ''
        while len(characters) > 0:
            text += arr[characters.pop()]
        if len(text) < size:
            for j in range(0, size - len(text)):
                text = 'a' + text
        results.append(text)
    return results

def binarySearch(item, arr, low=0, high=-1):
    if high == -1:
        high = len(arr)
    if (low == high):
        return high
    elif item < arr[(low+high)/2]:
        return binarySearch(item, arr, low, (low+high)/2)
    elif item > arr[(low+high)/2]:
        if(low == high-1):
            return binarySearch(item, arr,low+1, high)
        return binarySearch(item, arr,(low+high)/2, high)
    else:
        return (low+high)/2

# def dupCheck(clusters):
#     check = {}
#     for i in range(0,len(clusters)):
#         for j in range(0,len(clusters[i])):
#             res = check.get(clusters[i][j], [0,-1])
#             res[0] += 1
#             res[1] = i
#             check[clusters[i][j]] = res
#     prods = check.keys()
#     for i in range(0,len(prods)):
#         if(check[prods[i]][0] > 1):
#             print 'failure: ' + prods[i] + ' -- ' + str(check[prods[i]])

def dist(v1, v2):
    comb = (v1 - v2)**2.
    distance = np.sum(comb)**(1./2)
    return distance

def findCenter(points):
    point = points[0]
    for i in range(1,len(points)):
        point += points[i]
    return point/len(points + 0.)