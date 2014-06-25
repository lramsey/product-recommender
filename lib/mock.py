import customers    as c
import util         as u
import random

def mockProducts(productNum):
    products = u.generateItems(productNum, u.symbols)
    return products

def mockCustomers(nameNum):
    names = u.generateItems(nameNum, u.alphabet)
    return names

def mockDataBuilder(names, products):
    num = random.randint(8,20)
    for i in range(0, len(names)):
        for j in range(0, num):
            randProduct = products[random.randint(0, len(products)-1)]
            c.customers[i].purchaseItem(randProduct)
