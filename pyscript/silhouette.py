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
        s = silhouette(clusters[i])
        silhouettes += s
    return silhouettes/len(clusters)

def silhouette(cluster):
    a = 1.0
    b = 1.0
    for i in range(0, len(cl.centroidList)):
        c = distFromCentroid(cluster, cl.centroidList[i])
        if c < a:
            b = a
            a = c
        elif c < b:
            b = c
        if b == 0:
            return 0
    sil = (b-a)/max(a,b)
    silhouettesList.append(sil)
    return sil
