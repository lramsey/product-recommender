import customers as c
import numpy     as np
# from   scipy import sparse
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

# def checkProducts(shoppers):
#     sparseMatrix = sparse.csr_matrix(c.matrix)

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
    return 1.0 - math.tanh(math.sqrt(union - intersection))
    # intersection = 0.0
    # chances = 0.0
    # if one is not 'null' and two is not 'null':
    #     for i in range(0,len(one)):
    #         for j in range(0, len(two)):
    #             if one[i] == two[j]:
    #                 intersection += 1
    #     if(len(one) < len(two)):
    #         chances += len(one)
    #     else:
    #         chances += len(two)
    #     return 1.0 - math.tanh(math.sqrt(chances - intersection))
    # else:
    #     return 'null'

def productMatrixiser():
    productMatrix = []
    # checkProducts(c.customers)
    for i in range(0, len(products)):
        sims = []
        for j in range(0, len(products)):
            sims.append(productSim(products[i], products[j]))
        productMatrix.append(sims)
    return np.array(productMatrix)

def averageDistance(prodMatrix):
    rowDist = 0.0
    for i in range(0, len(prodMatrix)):
        rowDist += np.sum(prodMatrix[i])/len(prodMatrix[i])
    dist = rowDist/len(prodMatrix) 
    return dist

def combineProducts(cluster, transpose):
    reducedTranspose = []
    for i in range(0, len(cluster)):
        reducedRow = np.zeros((500))
        for j in range(0, len(cluster[i])):
            reducedRow = np.add(reducedRow, transpose[productsMap[cluster[i][j]]])
        reducedTranspose.append(reducedRow)
    numpyTranspose = np.array(reducedTranspose)
    global matrix
    matrix = numpyTranspose.transpose()
