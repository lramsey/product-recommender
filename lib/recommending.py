import customers  as c
import products   as p
import math

recommendationMatrix = []
goodClusters = []

def buildRecommendations(names, clusters):
    global recommendationMatrix
    recommendationMatrix = []
    global goodClusters
    goodClusters = clusters
    for i in range(0, len(names)):
        recObj = {}
        recommendations = []
        history  = c.matrix[i]
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
    silhouette    = cluster[5]
    results       = findDiffs(hist, centroid, silhouette, index, recObj)
    return results

def findDiffs(hist, avg, sil, index, recObj):
    normals = []
    for i in range(0,len(avg)):
        normalized = sil * math.fabs(hist[i]-avg[i])
        val = recObj.get(p.products[i],0)
        if normalized > val:
            normals.append({normalized: p.products[i]})
            recObj[p.products[i]] = normalized
    normals.sort()
    return normals
