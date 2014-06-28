import products as p
import util     as u
import numpy    as np
import math

customers = []
customersMap = {}
matrix = []

class Customer(object):
    def __init__(self, name):
        self.purchases = {}
        self.purchasesArr = []
        for i in range(0,len(p.products)):
            self.purchases[p.products[i]] = 0
            self.purchasesArr.append(0)
        self.name = name
        customers.append(self)
    
    def purchaseItem(self, item):
        prodCount = self.purchases.get(item, 0)
        prodCount += 1
        self.purchases[item] = prodCount
        self.purchasesArr[p.productsMap[item]] = prodCount

def customerSim(person1, person2):
    one = person1.purchases
    two = person2.purchases
    intersection = 0.0
    union = 0.0
    for i in one:
        if one[i] > 0 and two[i] > 0:
            union += 1
            intersection += 1;
        elif one[i] > 0 or two[i] > 0:
            union += 1
            
    return math.tanh(math.sqrt(union - intersection))

def customerMatrixiser():
    customerMatrix = []
    for i in range(0, len(customers)):
        sims = []
        for j in range(0,len(customers)):
            sims.append(customerSim(customers[i], customers[j]))
        customerMatrix.append(sims)
    return u.scaleFeatures(customerMatrix)


def matrixBuilder():
    global matrix
    matr = []
    for i in range(0, len(customers)):
        row = np.zeros(len(customers[0].purchasesArr))
        for j in range(0, len(customers[i].purchasesArr)):
            if customers[i].purchasesArr[j] > 0:
                row[j] = 1
        matr.append(row)
    matrix = np.array(matr)
    global maxRow
    maxRow = row
