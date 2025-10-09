
from LinkedList import *
from HashMap import *
from FPGrowthAlgo import *
from FPTree import *

transactions=LinkedList()

add_transaction(transactions,"E", "K", "M", "N", "O", "Y")  # T1
add_transaction(transactions,"D", "E", "K", "N", "O", "Y")  # T2
add_transaction(transactions,"A", "E", "K", "M")            # T3
add_transaction(transactions,"K", "M", "Y")                 # T4
add_transaction(transactions,"C", "E", "I", "K", "O", "O")  # T5

##size men 3andna
size=50
freq=calculate_freq(transactions,size)

min_sup=3

freq_list=freq_pattern_set(transactions,freq,min_sup,size)

print("Frequent Pattern Set:")
current=freq_list.head
while current:
    print(f"{current.element.key} : {current.element.value}")
    current=current.next

ordered_itemsets=ordered_itemsets(transactions,freq_list)

print("Ordered-Item-Sets:")
t=1
current=ordered_itemsets.head
while current:
    print(f"T{t}: {current.element}")
    current=current.next
    t += 1


#FPTree
tree=FPTree()
for itemset in ordered_itemsets:
    tree.insert(itemset)

print("Conditional Pattern Base:")
cpb=conditional_pattern_base(tree,size)
print_cpb(cpb)