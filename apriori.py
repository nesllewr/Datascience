import sys
import itertools

def generate_candidate( frequent_k, k):
    candidate = []
    for i in range(len(frequent_k)):
        for j in range(i+1, len(frequent_k)):
            first = list(frequent_k[i])[:k-2]
            first.sort()
            second = list(frequent_k[i])[:k-2]
            second.sort()
            if first == second:
                candidate.append(frequent_k[i] | frequent_k[j] )

    return candidate                


if __name__ == '__main__' :
    if len(sys.argv) != 4 :
        sys.exit('Execute the program with three arguments : minimum support, input file name, output file name')

    transaction = []
    with open(sys.argv[2], 'r') as fp:
        inputfile = fp.read().split('\n')
        for line in inputfile :
            transaction.append(line.split('\t'))
    
    candidate1 = {}
    cnt = 0
    for el in transaction :
        for item_id in el :
            cnt +=1
            if item_id in candidate1.keys() :
                candidate1[item_id] += 1
            else :
                candidate1.setdefault(item_id, 1)

    while True :
        candidate = generate_candidate(,k)
    
    print(candidate1)
   # with open(sys.argv[3],'w') as fw :
            