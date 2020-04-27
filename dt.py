import sys, math
from collections import defaultdict

# calculate the total count of label
# get sum of the probability of element in class label
def calculate_entropy(labeled_data):
    table = {}
    for label in labeled_data:    
        if label[class_name] in table :
            table[label[class_name]] +=1
        else :
            table[label[class_name]] =1
    total = sum(table.values())

    entropy = 0.0
    for label in table.values():
        if label != 0:
            prob = float(label)/ float(total)
            entropy += (-prob) * math.log(prob,2)
        else :
            prob = 1 / float(total)
    return entropy

# to get sum of weighted entropy
# multiply the ratio of part and return value of calculate_entropy function
def get_attribute_entropy(partition):
    total = 0 
    for part in partition :
        total += len(part)

    info_attribute = 0.0
    for part in partition:
        info_attribute += (len(part)/total) * calculate_entropy(part)
    return info_attribute

# make branch splited by attribute 'attri'
def split_partition(training_data, attri):
    branch = defaultdict(list)
    for data in training_data:
        key = data[attri]
        branch[key].append(data)
    return branch

# majority voting for classifying the leaf node
def calculate_majority(training_data):
    result_dic = {}
    for input_set in training_data:
        result = input_set[class_name]
        if result in result_dic.keys():
            result_dic[result] += 1
        else:
            result_dic[result] = 1

    majority = ''
    max_vote=0
    for key in result_dic.keys():
        if result_dic[key] > max_vote :
            max_vote = result_dic[key]
            majority = key
    return majority

# top-down recursive deivde-and-conqure tree
# check the conditions for stopping the partitioning process
def generate_tree(training_data, attri_list):
    #check if all samples belong to the same class
    check = training_data[0][class_name]
    count = len(training_data)
    i = 0 
    for line in training_data :
        if line[class_name] == check :
            i+=1
    if count == i:
        return calculate_majority(training_data)
    
    # to select the test attribute having the highest information gain
    # it is also possible with having the lowest expected information.  
    best_attri = ""
    min_value = 1000
    for attri in attri_list : 
        tmp_partition = split_partition(training_data,attri)
        value = get_attribute_entropy(tmp_partition.values())
        if value < min_value :
            min_value = value
            best_attri = attri
            partitions = tmp_partition
    
    # delete the attribute which used for spliting partitions
    attri_list = [attri for idx, attri in enumerate(attri_list) if attri != best_attri]

    # check if all attributes are used to split partitions
    if len(attri_list) > 0 :
        subtrees = {}
        for attri_value, subset in partitions.items():
            subtrees[attri_value] = generate_tree(subset, attri_list)
        subtrees['major'] = calculate_majority(training_data)
        return (best_attri, subtrees)
    else : 
        return calculate_majority(training_data)

# classify the test case with decision tree model
def classify(node, test_data, class_labels):
    if node in class_labels:
        return node
    best_attri, subtree = node
    key_attri = test_data.get(best_attri)
    if key_attri not in subtree:
        key_attri = 'major'
    return classify(subtree[key_attri], test_data, class_labels)

if __name__=='__main__':

    if len(sys.argv) != 4 :
        sys.exit('Execute the program with three arguments : training file name, test file name, output file name')
    
    attribute_names=[]   
    training_list = []
    class_labels = set()

    with open(sys.argv[1], 'r') as fp:
        attribute_names = fp.readline().split()
        class_name = attribute_names[-1]
        training_data = fp.read().split('\n')
        for line in training_data :
            if line =="":
                break
            data_line = line.split('\t')
            data_format ={}
            for idx, data in enumerate(data_line) :
                data_format[attribute_names[idx]] = data
            class_labels.add(data_format[class_name])
            training_list.append(data_format)

    # construct model for classification
    decision_tree = generate_tree(training_list, attribute_names[:-1])
    
    test_list=[]
    with open(sys.argv[2],'r') as fp:
        fp.readline().split()
        test_data = fp.read().split('\n')
        for line in test_data :
            if line =="":
                break
            data_line = line.split('\t')
            data_format ={}
            for idx, data in enumerate(data_line) :
                data_format[attribute_names[idx]] = data
            data_format[class_name] = classify(decision_tree,data_format,list(class_labels))
            test_list.append(data_format)    
     
    with open(sys.argv[3],'w') as fp:
        for attri in attribute_names[:-1]:
            fp.write("{}\t".format(attri))
        fp.write("{}\n".format(class_name))
        
        for idx, line in enumerate(test_list) :  
            for attri in line:
                if attri != class_name:
                    fp.write("{}\t".format(line[attri]))
                else :
                    fp.write("{}\n".format(line[attri]))
