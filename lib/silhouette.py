import customers  as c

matrix = [[]]
silhouettesList = []
centroids = []

def __init__(mat, cents):
    global matrix
    matrix = mat
    global silhouettesList
    silhouettesList = []
    global centroids
    centroids = cents

def distFromCentroid(cluster, centroid):
    a = 0.0
    for i in range(0, len(cluster)):
        vector = matrix[c.customersMap[cluster[i].name]]
        dist = (matrix[c.customersMap[cluster[0].name]] - centroid)**2.0
        a += dist.sum()/len(vector)
    avg = a/len(cluster)
    return avg

def averageSilhouettes(clusters, matrix, centroids):
    __init__(matrix, centroids)
    silhouettes = 0.0
    for i in range(0, len(clusters)):
        s = silhouette(clusters[i], i)
        silhouettes += s
    return silhouettes/len(clusters)

def silhouette(cluster, index):
    a = distFromCentroid(cluster, centroids[index])
    b = a.size
    for i in range(0, len(centroids)):
        if i == index:
            continue
        dist = distFromCentroid(cluster, centroids[i])
        if dist < b:
            b = dist
    sil = (b-a)/max(a,b)
    silhouettesList.append(sil)
    return sil
