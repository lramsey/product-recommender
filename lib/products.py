import customers as c
import util      as u
import math

productMatrix = {}
productFreq = {}

products = []
productsMap = {}

def addProducts(prods):
    global products
    products = prods
    for i in range(0, len(prods)):
        productsMap[prods[i]] = i

def productSim(item1, item2):
    matrix = c.matrix
    one = productsMap[item1]
    two = productsMap[item2]

    intersection = 0.0
    union = 0.0
    for i in range(0,len(matrix)):
        if matrix[i][one] > 0 and matrix[i][two] > 0:
            union += 1
            intersection += 1
        elif matrix[i][one] > 0 or matrix[i][two] > 0:
            union += 1
    return math.tanh(math.sqrt(union - intersection))

def productMatrixiser():
    productMatrix = []
    for i in range(0, len(products)):
        sims = []
        for j in range(0, len(products)):
            sims.append(productSim(products[i], products[j]))
        productMatrix.append(sims)
    return u.scaleFeatures(productMatrix)
