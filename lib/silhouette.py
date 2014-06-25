import customers  as c
# import util       as u

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

# =======================================

# def averageSilhouettes(clusters, matrix, centroids):
#     __init__(matrix, centroids)
#     silhouettes = 0.0
#     for i in range(0, len(clusters)):
#         # s = silhouette(clusters[i], i)
#         s = silhouetteCluster(clusters[i], i)
#         silhouettes += s
#     return silhouettes/len(clusters)


# def silhouetteCluster(cluster, index):
#     center = centroids[index]
#     sil= 0.0
#     for i in range(0,len(cluster)):
#         point = matrix[c.customersMap[cluster[i].name]]
#         psil = silhouettePoint(point, center, index)
#         sil += psil
#     sil /= len(cluster)
#     silhouettesList.append(sil)
#     return sil

# def silhouettePoint(point, center, index):
#     a = u.dist(point, center)
#     b = a.size
#     for i in range(0,len(centroids)):
#         if i == index:
#             continue
#         dist = u.dist(point,centroids[i])
#         if dist < b:
#             b = dist
#     sil = (b-a)/max(a,b)
#     return sil
