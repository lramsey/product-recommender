import customers    as c
import products     as p
import recommending as r
import normalize    as n
import structure    as st
import clustering   as cl

transpose = []

def run(names):
    global products
    products = p.products
    results = [names, c.customersMap]

    global transpose
    transpose = c.matrix.transpose()
    cl.__init__(transpose, p.products)
    catNum = len(p.products)/8 + 1
    outputs = cl.kMeans(catNum,8)
    productClusters = outputs[0]
    centroids = outputs[1]

    inputs = st.subMatrices(productClusters)
    productClusters = n.normalizeProdClusters(productClusters, centroids, inputs[0], inputs[1], 0.2, 0.4)
    results.append(productClusters)
    results.append(p.productsMap)
    results.append(products)

    inputs = st.subMatrices(productClusters)
    subMats = inputs[0]
    maps = inputs[1]
    indexMap = inputs[2]

    subClustersHelpers = []
    for i in range(0, len(subMats)):
        subCluster = st.createSubclustersHelpers(indexMap[i], subMats[i], maps[i])
        subCluster.append(r.buildRecommendations(names, [subCluster]))
        subClustersHelpers.append(subCluster)


    customerClustersHelpers = st.createSubclustersHelpers(p.products, c.matrix, p.productsMap)
    customerClustersHelpers.append(r.buildRecommendations(names,[customerClustersHelpers]))
    powerClustersHelpers = []
    powerSil = []
    powerI = []
    for i in range(0, len(subClustersHelpers)):
        if subClustersHelpers[i][4] >= customerClustersHelpers[4]:
            powerClustersHelpers.append(subClustersHelpers[i])
            powerSil.append(subClustersHelpers[i][4])
            powerI.append(i)
    if(len(powerSil) == 0):
        return 'again'
    displacement = 0
    for i in range(0,len(powerI)):
        subClustersHelpers.pop(powerI[i]-displacement)
        displacement += 1

    powerRecMatrix = r.buildRecommendations(names, powerClustersHelpers)
    results.append(powerRecMatrix)
    results.append([customerClustersHelpers])
    results.append(subClustersHelpers)
    results.append(powerClustersHelpers)
    customerClusters = [customerClustersHelpers[0][0]] 
    results.append([customerClusters])
    subClusters = []
    for i in range(0, len(subClustersHelpers)):
        subClusters.append(subClustersHelpers[i][0])
    results.append(subClusters)
    powerClusters = []
    for i in range(0,len(powerClustersHelpers)):
        powerClusters.append(powerClustersHelpers[i][0])
    results.append(powerClusters)
    results.append(c.matrix)
    return results
