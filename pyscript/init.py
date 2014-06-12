import customers    as c
import products     as p
import mock         as m
import run

names = []
products = []

def addCustomers(names):
    for i in range(0, len(names)):
        c.Customer(names[i]) 
        c.customersMap[names[i]] = i

def dataBuilder(matrix):
    for i in range(0, len(matrix)):
        for j in range(0,len(matrix[i])):
            num = matrix[i][j]
            while num > 0:
                c.customers[i].purchaseItem(products[j])
                num -= 1

def buildHistory(nameList, prodList, matrix):
    global names
    names = nameList
    global products
    products = prodList
    p.addProducts(products)
    addCustomers(names)
    dataBuilder(matrix)

def init(names, products, matrix):
    if isinstance(names, int):
        names = m.mockData(names, products)
    else:
        '''expected data: list of customers, list of products, list customer arrays containing 
        product purchases in same order as product list.'''
        buildHistory(names, products, matrix);
    c.matrixBuilder()

    recommend = run.run(names)
    while recommend == 'again':
        recommend = run.run(names)
    return recommend
