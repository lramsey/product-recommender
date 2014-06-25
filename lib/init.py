import customers    as c
import products     as p
import mock         as m
import run

names = []
products = []

def addCustomers(nameList):
    global names
    names = nameList
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

def init(nameList, productList, matrix):
    if isinstance(productList, int):
        products = m.mockProducts(productList)
    p.addProducts(products)

    if isinstance(nameList, int):
        nameList = m.mockCustomers(nameList)
    addCustomers(nameList)

    if isinstance(matrix, list):
        '''expected data: list of customers, list of products, list customer arrays containing 
        product purchases in same order as product list.'''
        dataBuilder(matrix);
    else:
        m.mockDataBuilder(names, products)
    c.matrixBuilder()

    recommend = run.run(names)
    while recommend == 'again':
        recommend = run.run(names)
    return recommend
