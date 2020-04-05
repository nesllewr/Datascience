import sys
import itertools 
from decimal import Decimal, ROUND_HALF_UP

def generate_candidate(frequent_k, k):
    candidate = []
    frequent_k.sort()
    for i in range(len(frequent_k)):
        for j in range(i+1, len(frequent_k)):
            first = list(frequent_k[i])[:k-2]
            first.sort()
            second = list(frequent_k[j])[:k-2]
            second.sort()
            if first == second:
                candidate.append(set(frequent_k[i]) | set(frequent_k[j]))
    return candidate                

def pruning_candidate(candiate, frequent_k, k):
    new_frequent_set =[]
    for itemset in candidate :
        cnt =0
        for item in list(itertools.combinations(itemset, k -1)):
            if k ==2:
                item = list(item)
            else :
                item = set(item)
            
            if item not in frequent_k :
                break
            cnt +=1
        if cnt == k:
            new_frequent_set.append(itemset)
    return new_frequent_set
    
def get_association_rules(frequent_k, transaction):
    final = sum(frequent_k,[])
    line = ""
    for itemsets in final:
        if len(itemsets) > 1 :
            all = set()
            for i in range(1, len(itemsets)):
                all = all | set(itertools.combinations(itemsets, i))

            for subset in all:
                diff = set(itemsets) - set(subset)

                cnt = 0
                under_cnt =0
    
                for el in transaction:
                    if set(itemsets).issubset(set(el)):
                        cnt += 1
                    if set(subset).issubset(set(el)):
                        under_cnt +=1

                support_itemsets = round((cnt / len(transaction) * 100),2)
                #line += str(cnt) + " cnt " + str(under_cnt) +"  "+ str(round((cnt/under_cnt)*100,3))+"\t"
                round_confidence = Decimal(str((cnt/under_cnt)*100)).quantize(Decimal('0.01'),rounding=ROUND_HALF_UP)
                line += make_format(list(subset),list(diff),support_itemsets, round_confidence)
                
    return line

def make_format(left, right, support, confidence):
    return ("{%s}\t{%s}\t%.2f\t%.2f\n" % (", ".join(map(str, left)), ", ".join(map(str, right)), support, confidence))


if __name__ == '__main__' :
    '''
    if len(sys.argv) != 4 :
        sys.exit('Execute the program with three arguments : minimum support, input file name, output file name')
    
    min_support = float(sys.argv[1])
    '''
    min_support =5
    transaction = []
    with open('input.txt', 'r') as fp:
        inputfile = fp.read().split('\n')
        for line in inputfile :
            #transaction.append(line.split('\t'))
            result = line.split('\t')
            transaction.append(list(map(int,result)))        
    
    candidate_1 = {}
    total = 0
    for el in transaction :
        total +=1
        for item_id in el :
            if item_id in candidate_1.keys() :
                candidate_1[item_id] += 1
            else :
                candidate_1.setdefault(item_id, 1)

    frequent_1 =[]
    for key, value in candidate_1.items():
        if round((value/total)*100,3) >= min_support :
            keys = [int(key)]
            frequent_1.append(keys)

    frequent_sets = []
    frequent_sets.append(frequent_1)
    k = 2
    while True :
        candidate = generate_candidate(frequent_sets[k-2], k)
        prune_frequent = pruning_candidate(candidate, frequent_sets[k-2], k)
        new_frequent =[]
        for itemset in prune_frequent :
            cnt = 0
            for el in transaction :
                itemlist = set(el)
                if itemset.issubset(itemlist):
                    cnt +=1
            support = round((cnt/total)*100,3)
            if support >= min_support :
                new_frequent.append(itemset)
        if len(new_frequent) == 0 :
            break
        frequent_sets.append(new_frequent)
        k +=1
    
    with open('output4.txt','w') as fp :
        fp.write(get_association_rules(frequent_sets, transaction))

            