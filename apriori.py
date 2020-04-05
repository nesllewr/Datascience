import sys
import itertools 
from decimal import Decimal, ROUND_HALF_UP

# generate candidate itemsets of length (k+1) from 
# frequent itemsets of length k
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

# remove candidates that don't satisfy
# the apriori pruning principle
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

# get support and confidence    
def get_association_rules(frequent_k, transaction):
    final = sum(frequent_k,[])
    line = ""
    for itemsets in final:
        if len(itemsets) > 1 :
            all = set()
            # find subsets of itemset which comes from i-size set
            for i in range(1, len(itemsets)):
                all = all | set(itertools.combinations(itemsets, i))
            for subset in all:
                diff = set(itemsets) - set(subset)
                cnt = 0
                under_cnt =0
                #count n(X U Y) and n (X) 
                for el in transaction:
                    if set(itemsets).issubset(set(el)):
                        cnt += 1
                    if set(subset).issubset(set(el)):
                        under_cnt +=1
                #calculate support and confidence with the countdown numbers
                support_itemsets = round_format((cnt/len(transaction))*100)
                round_confidence = round_format((cnt/under_cnt)*100)
                line += make_format(list(subset),list(diff),support_itemsets, round_confidence)
                
    return line

def round_format(value):
    return Decimal(str(value)).quantize(Decimal('0.01'),rounding=ROUND_HALF_UP)

def make_format(left, right, support, confidence):
    return ("{%s}\t{%s}\t%.2f\t%.2f\n" % (",".join(map(str, left)), ",".join(map(str, right)), support, confidence))


if __name__ == '__main__' :
    
    if len(sys.argv) != 4 :
        sys.exit('Execute the program with three arguments : minimum support, input file name, output file name')
    
    min_support = float(sys.argv[1])
    
    transaction = []
    with open(sys.argv[2], 'r') as fp:
        inputfile = fp.read().split('\n')
        for line in inputfile :
            #transaction.append(line.split('\t'))
            result = line.split('\t')
            transaction.append(list(map(int,result)))        
    
    candidate_1 = {}
    total = 0 # count the number of lines in input file
    for el in transaction :
        total +=1
        for item_id in el :
            # make table for 1-itemset in dictionary format
            if item_id in candidate_1.keys() :
                candidate_1[item_id] += 1
            else :
                candidate_1.setdefault(item_id, 1)
    # make frequent itemset of length 1
    frequent_1 =[]
    for key, value in candidate_1.items():
        if round_format((value/total)*100) >= min_support :
            keys = [int(key)]
            frequent_1.append(keys)

    frequent_sets = []
    frequent_sets.append(frequent_1)
    k = 2
    while True :
        # use function to get candidate that satisfy self-joining and pruning
        candidate = generate_candidate(frequent_sets[k-2], k)
        prune_frequent = pruning_candidate(candidate, frequent_sets[k-2], k)
        # check minimum support condition
        new_frequent =[]
        for itemset in prune_frequent :
            cnt = 0
            for el in transaction :
                itemlist = set(el)
                if itemset.issubset(itemlist):
                    cnt +=1
            support = round_format((cnt/total)*100)
            if support >= min_support :
                new_frequent.append(itemset)
        # break when no more candidates are generated
        if len(new_frequent) == 0 :
            break
        # when (k+1) frequent item exist, add it in list
        frequent_sets.append(new_frequent)
        k +=1
    
    with open(sys.argv[3],'w') as fp :
        fp.write(get_association_rules(frequent_sets, transaction))

            