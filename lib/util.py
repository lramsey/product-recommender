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

def dist(v1, v2):
    comb = (v1 - v2)**2.
    distance = np.sum(comb)**(1./2)
    return distance

def findCenter(points):
    point = points[0]
    for i in range(1,len(points)):
        point += points[i]
    return point/len(points + 0.)

def scaleFeatures(matrix):
    matrix = np.array(matrix)
    amax = np.amax(matrix)
    amin = rightHandMin(matrix)
    scaledMatrix = (matrix - amin)*(1/(amax-amin))
    scaledMatrix = setDiagonals(scaledMatrix, -1)
    return scaledMatrix.tolist()

def setDiagonals(matrix, value):
    for i in range(0,len(matrix)):
        matrix[i][i] = -1
    return matrix

def rightHandMin(matrix):
    amin = 1.0
    for i in range(0,len(matrix)):
        for j in range(i+1,len(matrix[i])):
            if matrix[i][j] < amin:
                amin = matrix[i][j]
    return amin
