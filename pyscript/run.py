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
    prodClusters = outputs[0]
    centroids = outputs[1]

    inputs = st.subMatrices(prodClusters)
    prodClusters = n.normalizeProdClusters(prodClusters, centroids, inputs[0], inputs[1], 0.2, 0.4)
    results.append(prodClusters)

    inputs = st.subMatrices(prodClusters)
    subMats = inputs[0]
    maps = inputs[1]
    indexMap = inputs[2]

    subClusters = []
    for i in range(0, len(subMats)):
        subCluster = st.createSubcluster(indexMap[i], subMats[i], maps[i])
        subCluster.append(r.buildRecommendations(names, [subCluster]))
        subClusters.append(subCluster)


    totCluster = st.createSubcluster(p.products, c.matrix, p.productsMap)
    totCluster.append(r.buildRecommendations(names,[totCluster]))
    powerClusters = []
    powerSil = []
    results.append('unfiltered results: ' + str(totCluster[4]))
    powerI = []
    for i in range(0, len(subClusters)):
        if subClusters[i][4] >= totCluster[4]:
            powerClusters.append(subClusters[i])
            powerSil.append(subClusters[i][4])
            powerI.append(i)
    if(len(powerSil) == 0):
        return 'again'
    else:
        results.append('filtered average: ' + str(sum(powerSil)/len(powerSil)))
    for i in range(0,len(powerI)):
        subClusters.pop(powerI[i])

    recommendationMatrix = r.buildRecommendations(names, powerClusters)
    results.append(recommendationMatrix)
    results.append(powerClusters)
    results.append(subClusters)
    results.append([totCluster])
    return results
