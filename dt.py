import sys



if __name__=='__main__':
    # if len(sys.argv) != 4 :
    #     sys.exit('Execute the program with three arguments : training file name, test file name, output file name')
    

#    with open(sys.argv[1], 'r') as fp:

    attribute_names=[]   
    training_list =[]
    with open('dt_train.txt', 'r') as fp:
        attribute_names = fp.readline().split()
        #attribute_names[-1] = attribute_names[-1].strip('Class:')
        print(attribute_names)
        training_data = fp.read().split('\n')
        for line in training_data :
            if line =="":
                break
            training_list.append(line.split('\t'))     
    
    test_list=[]
    with open('dt_test.txt','r') as fp:
        fp.readline().split()
        #attribute_names[-1] = attribute_names[-1].strip('Class:')
        test_data = fp.read().split('\n')
        for line in test_data :
            if line =="":
                break
            test_list.append(line.split('\t'))     
        
    with open('dt_result.txt','w') as fp:
        for attri in attribute_names[:-1]:
            fp.write("{}\t".format(attri))
        fp.write("{}\n".format(attribute_names[-1]))

        for line in test_list :          
            for attri in line[:-1]:
                fp.write("{}\t".format(attri))
            fp.write("{}\n".format(line[-1]))

    
        