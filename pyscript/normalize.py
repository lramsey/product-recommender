import products     as p
import clustering   as cl
import structure    as st
import numpy        as np

# ceil is a float between 0 and 1, max percent of total population in group
# floor is similar
def normalizeProdClusters(clusts, centroids, mats, maps, floor, ceil):
    displacement = 0
    again = False
    for i in range(0,len(clusts)):
        ratio = len(clusts[i - displacement])/len(clusts)
        if ratio < floor:
            again = True
            merge(clusts, centroids, mats, maps, i - displacement)
            displacement += 1
    mats = st.subMatrices(clusts)[0]
        
    displacement = 0
    for i in range(0,len(clusts)):
        t1 = len(clusts[i])/(0.0 + len(p.products)) > ceil
        t2 = len(clusts[i]) > 8
        if (t1 and t2):
            again = True
            dissolve(clusts, centroids, mats, maps, i - displacement)
            displacement += 1
    subs = st.subMatrices(clusts)
    if(again):
        clusts = normalizeProdClusters(clusts, centroids, subs[0], subs[1], floor, ceil)
    else:
        displacement = 0
        for i in range(0,len(clusts)):
            if not isinstance(clusts[i-displacement],list):
                clusts.pop(i - displacement)
                displacement += 1
    return clusts

def merge(clusts, centroids, mats, maps, i):
    minDist = -1
    index = -1
    cent = centroids[i]
    for j in range(0, len(centroids)):
        distance = dist(cent,centroids[j])
        if (i == j):
            continue
        elif (minDist == -1) or distance < minDist:
            minDist = distance
            index = j
    for j in range(0, len(clusts[i])):
        if not isinstance(clusts[index],list):
            clusts[index].tolist()
        clusts[index].append(clusts[i][j])
    
    newMat = []
    newMap = {}
    st.redoMatrix(clusts, index, newMat, newMap)
    mats[index] = np.array(newMat)
    maps[index] = newMap
    newCent = findCenter(mats[index])
    centroids[index] = newCent

    maps.pop(i)
    mats.pop(i)
    centroids.pop(i)    
    clusts.pop(i)

def dissolve(clusts, centroids, mats, maps, i):
    trans = mats[i].transpose()
    cl.__init__(trans, clusts[i], maps[i])
    num = len(clusts[i])/8+1
    results = cl.kMeans(num, 20)

    pClusts = results[0]
    pCents = results[1]
    clusts.pop(i)
    centroids.pop(i)
    mats.pop(i)
    maps.pop(i)

    for j in range(0, len(pClusts)):
        clusts.append(pClusts[j])
        centroids.append(pCents[j])
        newMat = []
        newMap = {}
        st.redoMatrix(clusts,len(clusts)-1,newMat, newMap)
        mats.append(newMat)
        maps.append(newMap)


def dist(v1, v2):
    comb = (v1 + v2)**2.
    distance = np.sum(comb)**(1./2)
    return distance

def findCenter(points):
    point = points[0]
    for i in range(1,len(points)):
        point += points[i]
    return point/len(points + 0.)