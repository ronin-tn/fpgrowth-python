"""
Script principal pour tester l'algorithme FP-Growth.
Découvre tous les patterns fréquents dans un ensemble de transactions.
"""

from LinkedList import *
from HashMap import *
from FPGrowthAlgo import *
from FPTree import *

print("=== Algorithme FP-Growth ===\n")

transactions = LinkedList()

add_transaction(transactions, "E", "K", "M", "N", "O", "Y")
add_transaction(transactions, "D", "E", "K", "N", "O", "Y")
add_transaction(transactions, "A", "E", "K", "M")
add_transaction(transactions, "K", "M", "Y")
add_transaction(transactions, "C", "E", "I", "K", "O", "O")

size = 50
min_sup = 3

print(f"Seuil de support minimal: {min_sup}")
print(f"Nombre de transactions: {len(transactions)}\n")

freq = calculate_freq(transactions, size)

freq_list = freq_pattern_set(transactions, freq, min_sup, size)

print("Items fréquents (triés par ordre décroissant):")
current = freq_list.head
while current:
    print(f"  {current.element.key} : {current.element.value}")
    current = current.next
print()

ordered_itemsets = ordered_itemsets(transactions, freq_list)

print("Transactions réordonnées selon la fréquence:")
t = 1
current = ordered_itemsets.head
while current:
    print(f"  T{t}: {current.element}")
    current = current.next
    t += 1
print()

tree = FPTree()
for itemset in ordered_itemsets:
    tree.insert(itemset)

print("Base de patterns conditionnels:")
cpb = conditional_pattern_base(tree, size)
print_cpb(cpb)