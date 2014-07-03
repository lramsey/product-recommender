import customers  as c
import util       as u

matrix = [[]]
silhouettesList = []
centroids = []

def __init__(mat, cents):
    global matrix
    matrix = mat
    global centroids
    centroids = cents

def averageSilhouettes(clusters, matrix, centroids):
    __init__(matrix, centroids)
    silhouettes = 0.0
    for i in range(0, len(clusters)):
        center = centroids[i]
        neighbor = neighboringCentroid(clusters[i], i)
        s = 0.0
        for j in range(0, len(clusters[i])):
            point = customerPoint(clusters[i][j])
            s += silhouette(point, center, neighbor)
        clustSil = s/len(clusters[i])
        silhouettesList.append(clustSil)
        silhouettes += s
    return silhouettes/len(c.customers)

def silhouette(point, centroid, neighbor):
    a = u.dist(point, centroid)
    b = u.dist(point, neighbor)
    sil = (b-a)/max(a,b)
    return sil

def neighboringCentroid(cluster, index):
    amin = len(customerPoint(cluster[0]))
    neighborIndex = -.1
    for i in range(0,len(centroids)):
        if i == index:
            continue
        dist = u.dist(centroids[i], centroids[index])
        if dist < amin:
            amin = dist
            neighborIndex = i
    neighbor = centroids[neighborIndex]
    return neighbor

def customerPoint(customer):
    return matrix[c.customersMap[customer.name]]
