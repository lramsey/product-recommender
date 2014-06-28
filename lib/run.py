import customers    as c
import products     as p
import recommending as r
import normalize    as n
import structure    as st
import clustering   as cl

transpose = []
names = []
products = []

def buildProductClusters():
    global transpose
    transpose = c.matrix.transpose()
    cl.__init__(transpose, p.products)
    catNum = len(p.products)/8 + 1
    outputs = cl.kMeans(catNum,8)
    return outputs

def buildCustomerHelpers():
    customerClustersHelpers = st.createClusterHelpers(p.products, c.matrix, p.productsMap)
    customerClustersHelpers.append(r.buildRecommendations(names,[customerClustersHelpers]))
    return customerClustersHelpers

def buildSubHelpers(indexMaps, subMatrices, aMaps):
    subClustersHelpers = []
    for i in range(0, len(subMatrices)):
        subCluster = st.createClusterHelpers(indexMaps[i], subMatrices[i], aMaps[i])
        subCluster.append(r.buildRecommendations(names, [subCluster]))
        subClustersHelpers.append(subCluster)
    return subClustersHelpers

def buildPowerHelpers(subClustersHelpers, customerClustersHelpers):
    powerClustersHelpers = []
    powerI = []
    powerCount = 0
    productClusterLocator = []
    for i in range(0, len(subClustersHelpers)):
        if subClustersHelpers[i][5] >= customerClustersHelpers[5]:
            powerClustersHelpers.append(subClustersHelpers[i])
            powerI.append(i)
            productClusterLocator.append(['power', powerCount])
            powerCount += 1
        else:
            productClusterLocator.append(['sub', i - powerCount])
    displacement = 0
    for i in range(0,len(powerI)):
        subClustersHelpers.pop(powerI[i]-displacement)
        displacement += 1

    return [powerClustersHelpers, productClusterLocator]

def run(nameList):
    global products
    products = p.products
    global names
    names = nameList
    
    outputs = buildProductClusters()
    productClusters = outputs[0]
    centroids = outputs[1]

    inputs = st.subMatrices(productClusters)
    productClusters = n.normalizeProdClusters(productClusters, centroids, inputs[0], inputs[1], 0.2, 0.4)

    inputs = st.subMatrices(productClusters)
    subMats = inputs[0]
    maps = inputs[1]
    indexMap = inputs[2]


    customerClustersHelpers = buildCustomerHelpers()
    subClustersHelpers = buildSubHelpers(indexMap, subMats, maps)

    powerups = buildPowerHelpers(subClustersHelpers,customerClustersHelpers)
    powerClustersHelpers = powerups[0]
    productClusterLocator = powerups[1]

    powerRecMatrix = r.buildRecommendations(names, powerClustersHelpers)
    productClustersMap = st.createClusterMap(productClusters)
    
    customerMatrix = c.customerMatrixiser()
    productMatrix  = p.productMatrixiser()

    if(len(powerClustersHelpers) == 0):
        return 'again'
    else:
        results = []
        # index 0
        results.append(names) 
        # index 1
        results.append(c.customersMap)
        # index 2
        results.append(productClusters)
        # index 3
        results.append(p.productsMap)
        # index 4
        results.append(products)
        # index 5
        results.append(powerRecMatrix)
        # index 6
        results.append([customerClustersHelpers])
        # index 7
        results.append(subClustersHelpers)
        # index 8
        results.append(powerClustersHelpers)
        # index 9
        results.append(c.matrix)
        # index 10
        results.append(productClustersMap)
        # index 11
        results.append(productClusterLocator)
        # index 12
        results.append(customerMatrix)
        # index 13
        results.append(productMatrix)
    
        return results
