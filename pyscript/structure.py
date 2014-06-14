import products     as p
import customers    as c
import silhouette   as s 
import clustering   as cl
import numpy        as np
import run

def redoMatrix(clusters, i, clusterMat=[], clusterMap={}, indexProds=[]):
    for j in range(0, len(clusters[i])):
        clusterMat.append(run.transpose[p.productsMap[clusters[i][j]]])
        clusterMap[clusters[i][j]] = j
        indexProds.append(clusters[i][j])

def subMatrices(clusters):
    results = []
    maps = []
    indexMap = []
    for i in range(0,len(clusters)):
        clusterMat = []
        clusterMap = {}
        indexProds = []
        redoMatrix(clusters, i, clusterMat, clusterMap, indexProds)
        mat = np.array(clusterMat).transpose()
        results.append(mat)
        maps.append(clusterMap)
        indexMap.append(indexProds)
    return [results, maps, indexMap]

def createSubclustersHelpers(indexMap, subMatrix, aMap):
    cl.__init__(subMatrix, c.customers, aMap)
    clust = []
    results = cl.kMeans(25,8)
    clusters = results[0]
    clust.append(clusters)
    centroids = results[1]
    clust.append(centroids)
    clust.append(cl.clusterMap)
    clust.append(indexMap)
    avgSils = s.averageSilhouettes(clust[0], subMatrix)
    clust.append(s.silhouettesList)
    clust.append(avgSils)
    return clust
