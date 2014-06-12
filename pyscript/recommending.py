import customers  as c
import products   as p
import math

recommendationMatrix = []
goodClusters = []

def recommender(name):
    if len(recommendationMatrix) == 0:
        print 'Build the matrix first.'
    else:
        recommendation = recommendationMatrix[c.customersMap[name]].pop()
        attraction = recommendation.keys()[0]
        indexes = recommendation[attraction]
        cluster = goodClusters[indexes[1]]
        indexMap = cluster[3]
        product = indexMap[indexes[0]]
        return product

def buildRecommendations(names, clusters):
    global recommendationMatrix
    recommendationMatrix = []
    global goodClusters
    goodClusters = clusters
    for i in range(0, len(names)):
        recObj = {}
        recommendations = []
        target   = c.customers[i]
        history  = target.purchasesArr
        for j in range(0, len(clusters)):
            recommendations = recommendations + clusterRecommender(names[i], history, clusters[j], j, recObj)
        recommendations.sort()
        recommendationMatrix.append(recommendations)
    return recommendationMatrix

def clusterRecommender(name, hist, cluster, index, recObj):
    # cluster map
    clusterIndex  = cluster[2][name]
    # centroid of user's cluster
    centroid      = cluster[1][clusterIndex]
    silhouette    = cluster[4]
    results       = findDiffs(hist, centroid, silhouette, index, recObj)
    return results

def findDiffs(hist, avg, sil, index, recObj):
    normals = []
    for i in range(0,len(avg)):
        normalized = sil * math.fabs(hist[i]-avg[i])
        val = recObj.get(p.products[i],0)
        if normalized > val:
            normals.append({normalized: [i, index]})
            recObj[p.products[i]] = normalized
    normals.sort()
    return normals

def find3Diffs(hist, avg, sil, index):
    results = [{'0': [-1, index]},{'0': [-1, index]},{'0': [-1, index]}]
    for i in range(0,len(avg)):
        normalized = sil * math.fabs(hist[i]-avg[i])
        key1 = float(results[2].keys()[0])
        key2 = float(results[1].keys()[0])
        key3 = float(results[0].keys()[0])
        if normalized > key1:
            results[0] = results[1]
            results[1] = results[2]
            results[2] = {str(normalized): [i, index]}
        elif normalized > key2:
            results[0] = results[1]
            results[1] = {str(normalized): [i, index]}
        elif normalized > key3:
            results[0] = {str(normalized): [i, index]}
    return results
