import sys,math

data_set = dict()

# calculate distance between id-data and whole data_set
# compare with epsilon to check wheter the value is near to id-data
def search_neighborhoods( id, epsilon):
    x = data_set[id][0]
    y = data_set[id][1]
    neighborhoods = list()
    for key, value in data_set.items():
        distance = math.sqrt(math.pow(value[0]-x,2) + math.pow(value[1]-y,2))
        if distance <= epsilon:
            neighborhoods.append(key)        
    return neighborhoods

def option(num, cluster_id):
    # If cluster id is larger than givien cluster number
    cluster = dict()
    for idx in range(cluster_id):
        cluster[idx]= 0

    for value in data_set.values():
        if value[2] > -1:
            cluster[value[2]] +=1

    cluster = sorted(cluster.items(), key=lambda item: item[1])
    cleaning = list()
    for cl in cluster[:cluster_id - num] :
        cleaning.append(cl[0])
    return cleaning

if __name__=='__main__':

    if len(sys.argv) != 5 :
        sys.exit('Execute the program with four arguments : input data file name, n, Eps and MinPts')
    
    num = int(sys.argv[2])
    epsilon = float(sys.argv[3])
    minPts = int(sys.argv[4])

    with open(sys.argv[1], 'r') as fp:
        lines = fp.read().split("\n")
        for line in lines:
            if line=="":
                break
            point = list(map(float, line.split("\t")))
            id = int(point[0])
            point.insert(3,-1)
            data_set[id] = point[1:]
    
    # start with cluster_id 0
    # find other neighborhood data to put same cluster
    cluster_id = 0
    for key, value in data_set.items():
        if value[2] != -1 :
            continue
        
        # retrieve all points with respect to epsilon
        neighborhoods = search_neighborhoods(key, epsilon)

        # compare with minPts to find outliers
        # and directly density-reachable data
        if len(neighborhoods) < minPts:
            value[2] = -2    
        else:
            for neighbor in neighborhoods:
                data_set[neighbor][2] = cluster_id
            
            # if neighbor is core point, put id in same cluster
            # but if no points are density-reachable
            # visit the next point of data_set
            while len(neighborhoods) > 0:
                cur_id = neighborhoods.pop()
                new_neighbor = search_neighborhoods(cur_id, epsilon)

                if len(new_neighbor) >= minPts:
                    for new in new_neighbor:
                        if data_set[new][2] == -1 :
                            neighborhoods.append(new)
                            data_set[new][2] = cluster_id

            cluster_id +=1

    output = sys.argv[1][:-4]
    
    for i in range(num):
        with open(output+"_cluster_"+str(i)+".txt",'w') as fp:
            for key, value in data_set.items() :
                if value[2] == i:
                    fp.write("{}\n".format(key))
 
    # if cluster_id > num:
    #     condition = option(num, cluster_id)
    #     for i in range(cluster_id):
    #         if i not in condition:
    #             with open(output+"_cluster_"+str(i)+".txt",'w') as fp:
    #                 for key, value in data_set.items() :
    #                     if value[2] == i:
    #                         fp.write("{}\n".format(key))
       
    # else: 
    #     for i in range(num):
    #         with open(output+"_cluster_"+str(i)+".txt",'w') as fp:
    #             for key, value in data_set.items() :
    #                 if value[2] == i:
    #                     fp.write("{}\n".format(key))
