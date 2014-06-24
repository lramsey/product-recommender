import customers  as c
import clustering as cl

matrix = [[]]
silhouettesList = []

def __init__(mat):
    global matrix
    matrix = mat
    global silhouettesList
    silhouettesList = []

def distFromCentroid(cluster, centroid):
    a = 0.0
    for i in range(0, len(cluster)):
        vector = matrix[c.customersMap[cluster[i].name]]
        dist = (matrix[c.customersMap[cluster[0].name]] - centroid)**2.0
        a += dist.sum()/len(vector)
    avg = a/len(cluster)
    return avg

def averageSilhouettes(clusters, matrix):
    __init__(matrix)
    silhouettes = 0.0
    for i in range(0, len(clusters)):
        s = silhouette(clusters[i], i)
        silhouettes += s
    return silhouettes/len(clusters)

def silhouette(cluster, index):
    a = distFromCentroid(cluster, cl.centroidList[index])
    b = a.size
    for i in range(0, len(cl.centroidList)):
        if i == index:
            continue
        dist = distFromCentroid(cluster, cl.centroidList[i])
        if dist < b:
            b = dist
        if b == 0:
            return 0
    sil = (b-a)/max(a,b)
    silhouettesList.append(sil)
    return sil
