"""
Script principal pour tester l'algorithme FP-Growth complet.
Decouvre tous les patterns frequents dans un ensemble de transactions.
"""

from LinkedList import LinkedList
from FPGrowthAlgo import (
    add_transaction,
    mine_frequent_patterns,
    print_frequent_patterns,
    print_fptree,
    calculate_freq,
    freq_pattern_set,
    ordered_itemsets
)
from FPTree import FPTree

print("=" * 70)
print("        ALGORITHME FP-GROWTH - IMPLEMENTATION COMPLETE")
print("=" * 70)

# ============================================================================
# EXEMPLE 1: Jeu de donnees du cours
# ============================================================================
print("\n" + "=" * 70)
print("EXEMPLE 1: Jeu de donnees classique")
print("=" * 70)

transactions = LinkedList()
add_transaction(transactions, "E", "K", "M", "N", "O", "Y")
add_transaction(transactions, "D", "E", "K", "N", "O", "Y")
add_transaction(transactions, "A", "E", "K", "M")
add_transaction(transactions, "K", "M", "Y")
add_transaction(transactions, "C", "E", "I", "K", "O", "O")

size = 50
min_sup = 3

print(f"\nNombre de transactions: {len(transactions)}")
print(f"Seuil de support minimal: {min_sup}")

# Afficher les transactions originales
print("\nTransactions originales:")
t = 1
current = transactions.head
while current:
    print(f"  T{t}: {current.element}")
    current = current.next
    t += 1

# Executer l'algorithme FP-Growth avec trace detaillee
print("\n" + "-" * 70)
print("EXECUTION DE L'ALGORITHME FP-GROWTH (mode verbose)")
print("-" * 70)

patterns = mine_frequent_patterns(transactions, min_sup, size, verbose=True)

# Afficher les resultats
print_frequent_patterns(patterns)

# ============================================================================
# EXEMPLE 2: Market Basket Analysis
# ============================================================================
print("\n" + "=" * 70)
print("EXEMPLE 2: Analyse du panier d'achat (Market Basket)")
print("=" * 70)

market_transactions = LinkedList()
add_transaction(market_transactions, "Pain", "Lait", "Beurre")
add_transaction(market_transactions, "Pain", "Lait", "Oeufs")
add_transaction(market_transactions, "Pain", "Beurre", "Oeufs")
add_transaction(market_transactions, "Pain", "Lait", "Beurre", "Oeufs")
add_transaction(market_transactions, "Lait", "Beurre")
add_transaction(market_transactions, "Pain", "Lait")

print(f"\nNombre de transactions: {len(market_transactions)}")
print(f"Seuil de support minimal: 3")

market_patterns = mine_frequent_patterns(market_transactions, min_sup=3, size=50, verbose=False)
print_frequent_patterns(market_patterns)

# ============================================================================
# VISUALISATION DE L'ARBRE FP
# ============================================================================
print("\n" + "=" * 70)
print("VISUALISATION DE L'ARBRE FP (Exemple 1)")
print("=" * 70)

# Reconstruire l'arbre pour la visualisation
freq = calculate_freq(transactions, size)
freq_list = freq_pattern_set(transactions, freq, min_sup, size)
ordered = ordered_itemsets(transactions, freq_list)

tree = FPTree(size)
for itemset in ordered:
    tree.insert(itemset)

print_fptree(tree)

# ============================================================================
# RESUME
# ============================================================================
print("\n" + "=" * 70)
print("RESUME DE L'IMPLEMENTATION")
print("=" * 70)
print("""
Structures de donnees implementees from scratch:
  [OK] LinkedList - Liste chainee avec operations O(1)
  [OK] HashMap    - Table de hachage avec chainage
  [OK] Tree       - Arbre generique
  [OK] TreeNode   - Noeud d'arbre avec HashMap pour les enfants
  [OK] FPNode     - Noeud FP avec count et node_link
  [OK] FPTree     - Arbre FP avec header table

Fonctionnalites de l'algorithme FP-Growth:
  [OK] Calcul des frequences des items
  [OK] Filtrage et tri des items frequents
  [OK] Construction de l'arbre FP
  [OK] Extraction de la Conditional Pattern Base
  [OK] Construction des arbres FP conditionnels
  [OK] Algorithme recursif de mining

Visualisation et sortie:
  [OK] Affichage textuel de l'arbre FP
  [OK] Patterns frequents avec support
  [OK] Mode verbose pour tracage detaille
""")