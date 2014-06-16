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
    # indexes 0 and 1
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
    # index 2
    results.append(productClusters)
    # index 3
    results.append(p.productsMap)
    # index 4
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
    powerI = []
    for i in range(0, len(subClustersHelpers)):
        if subClustersHelpers[i][5] >= customerClustersHelpers[5]:
            powerClustersHelpers.append(subClustersHelpers[i])
            powerI.append(i)
    if(len(powerClustersHelpers) == 0):
        return 'again'
    displacement = 0
    for i in range(0,len(powerI)):
        subClustersHelpers.pop(powerI[i]-displacement)
        displacement += 1

    powerRecMatrix = r.buildRecommendations(names, powerClustersHelpers)
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
    
    return results
