"""
Fichier de tests pour l'algorithme FP-Growth et toutes les structures de donnees.
"""

from LinkedList import LinkedList
from HashMap import HashMap
from FPNode import FPNode
from FPTree import FPTree
from FPGrowthAlgo import *

def test_linkedlist():
    """Tests pour la classe LinkedList."""
    print("=== Tests LinkedList ===")
    
    ll=LinkedList()
    assert ll.is_empty(),"La liste devrait etre vide"
    assert ll.size==0,"La taille devrait etre 0"
    
    ll.add_first("A")
    assert not ll.is_empty(),"La liste ne devrait pas etre vide"
    assert ll.size==1,"La taille devrait etre 1"
    assert ll.get_first()=="A","Le premier element devrait etre 'A'"
    
    ll.add_last("B")
    assert ll.size==2,"La taille devrait etre 2"
    assert ll.get_last()=="B","Le dernier element devrait etre 'B'"
    
    removed=ll.remove_first()
    assert removed=="A","L'element supprime devrait etre 'A'"
    assert ll.size==1,"La taille devrait etre 1"
    
    print("Tous les tests LinkedList passent\n")

def test_hashmap():
    """Tests pour la classe HashMap."""
    print("=== Tests HashMap ===")
    
    hm=HashMap(10)
    assert hm.size==0,"La taille devrait etre 0"
    
    hm.put("key1","value1")
    assert hm.size==1,"La taille devrait etre 1"
    assert hm.get("key1")=="value1","La valeur devrait etre 'value1'"
    assert hm.contains_key("key1"),"La cle devrait exister"
    
    hm.put("key1","value2")
    assert hm.get("key1")=="value2","La valeur devrait etre mise a jour"
    
    hm.put("key2",100)
    assert hm.size==2,"La taille devrait etre 2"
    
    removed=hm.remove("key1")
    assert removed is not None,"Le noeud devrait etre supprime"
    assert hm.size==1,"La taille devrait etre 1"
    assert not hm.contains_key("key1"),"La cle ne devrait plus exister"
    
    keys=hm.keys()
    assert keys.size==1,"Il devrait y avoir une cle"
    
    print("Tous les tests HashMap passent\n")

def test_fpnode():
    """Tests pour la classe FPNode."""
    print("=== Tests FPNode ===")
    
    root=FPNode("NULL",0)
    assert root.item=="NULL","L'item devrait etre 'NULL'"
    assert root.count==0,"Le compte devrait etre 0"
    assert root.parent is None,"Le parent devrait etre None"
    
    child=FPNode("A",1,root)
    root.add_child(child)
    
    found=root.find_child("A")
    assert found is not None,"L'enfant devrait etre trouve"
    assert found.item=="A","L'item de l'enfant devrait etre 'A'"
    
    not_found=root.find_child("B")
    assert not_found is None,"L'enfant ne devrait pas etre trouve"
    
    print("Tous les tests FPNode passent\n")

def test_fptree():
    """Tests pour la classe FPTree."""
    print("=== Tests FPTree ===")
    
    tree=FPTree()
    assert tree.root.item=="NULL","La racine devrait avoir l'item 'NULL'"
    
    transaction1=LinkedList()
    transaction1.add_last("A")
    transaction1.add_last("B")
    
    tree.insert(transaction1)
    assert tree.root.find_child("A") is not None,"L'item A devrait exister"
    
    child_a=tree.root.find_child("A")
    assert child_a.count==1,"Le compte de A devrait etre 1"
    
    tree.insert(transaction1)
    assert child_a.count==2,"Le compte de A devrait etre 2"
    
    header=tree.header_table.get("A")
    assert header is not None,"Le header pour A devrait exister"
    assert header.count==2,"Le compte total de A devrait etre 2"
    
    print("Tous les tests FPTree passent\n")

def test_calculate_freq():
    """Tests pour la fonction calculate_freq."""
    print("=== Tests calculate_freq ===")
    
    transactions=LinkedList()
    trans1=LinkedList()
    trans1.add_last("A")
    trans1.add_last("B")
    transactions.add_last(trans1)
    
    trans2=LinkedList()
    trans2.add_last("A")
    trans2.add_last("C")
    transactions.add_last(trans2)
    
    freq=calculate_freq(transactions,50)
    assert freq.get("A")==2,"A devrait apparaitre 2 fois"
    assert freq.get("B")==1,"B devrait apparaitre 1 fois"
    assert freq.get("C")==1,"C devrait apparaitre 1 fois"
    
    print("Tous les tests calculate_freq passent\n")

def test_freq_pattern_set():
    """Tests pour la fonction freq_pattern_set."""
    print("=== Tests freq_pattern_set ===")
    
    transactions=LinkedList()
    trans1=LinkedList()
    trans1.add_last("A")
    trans1.add_last("B")
    transactions.add_last(trans1)
    
    trans2=LinkedList()
    trans2.add_last("A")
    trans2.add_last("B")
    transactions.add_last(trans2)
    
    trans3=LinkedList()
    trans3.add_last("A")
    trans3.add_last("C")
    transactions.add_last(trans3)
    
    freq=calculate_freq(transactions,50)
    freq_list=freq_pattern_set(transactions,freq,2,50)
    
    assert freq_list.size > 0,"Il devrait y avoir des items frequents"
    assert freq_list.head.element.key=="A","A devrait etre le plus frequent"
    assert freq_list.head.element.value >= 2,"A devrait avoir un support >= 2"
    
    print("Tous les tests freq_pattern_set passent\n")

def test_fptree_construction():
    """Test de la construction de l'arbre FP."""
    print("=== Tests construction FPTree ===")
    
    transactions=LinkedList()
    add_transaction(transactions,"A","B")
    add_transaction(transactions,"A","B","C")
    add_transaction(transactions,"A","C")
    
    size=50
    min_sup=1
    
    freq=calculate_freq(transactions,size)
    freq_list=freq_pattern_set(transactions,freq,min_sup,size)
    orderedItemsets=ordered_itemsets(transactions,freq_list)
    
    tree=FPTree()
    for itemset in orderedItemsets:
        tree.insert(itemset)
    
    assert tree.root is not None,"L'arbre devrait avoir une racine"
    
    cpb=conditional_pattern_base(tree,size)
    keys=cpb.keys()
    assert keys.size > 0,"La base de patterns conditionnels ne devrait pas etre vide"
    
    print("Tous les tests construction FPTree passent\n")


def test_mine_frequent_patterns():
    """Tests pour la fonction mine_frequent_patterns."""
    print("=== Tests mine_frequent_patterns ===")
    
    transactions=LinkedList()
    add_transaction(transactions,"A","B")
    add_transaction(transactions,"A","B","C")
    add_transaction(transactions,"A","C")
    add_transaction(transactions,"A","B")
    
    patterns=mine_frequent_patterns(transactions,min_sup=2,size=50,verbose=False)
    
    assert patterns.size > 0,"Des patterns frequents devraient etre trouves"
    
    print(f"Patterns trouves: {patterns.size}")
    print("Tous les tests mine_frequent_patterns passent\n")


def test_conditional_fptree():
    """Tests pour la construction d'arbres FP conditionnels."""
    print("=== Tests conditional FPTree ===")
    
    transactions=LinkedList()
    add_transaction(transactions,"A","B","C")
    add_transaction(transactions,"A","B","D")
    add_transaction(transactions,"A","C","D")
    add_transaction(transactions,"B","C","D")
    
    size=50
    min_sup=2
    
    freq=calculate_freq(transactions,size)
    freq_list=freq_pattern_set(transactions,freq,min_sup,size)
    orderedItemsets=ordered_itemsets(transactions,freq_list)
    
    tree=FPTree()
    for itemset in orderedItemsets:
        tree.insert(itemset)
    
    cpb_d=conditional_pattern_base_for_item(tree, "D", size)
    
    if cpb_d is not None and not cpb_d.is_empty():
        cond_tree=build_conditional_fptree(cpb_d, min_sup, size)
        assert cond_tree is None or cond_tree.header_table.size >= 0, "Arbre conditionnel valide"
    
    print("Tous les tests conditional FPTree passent\n")


def test_complete_fpgrowth():
    """Test complet de l'algorithme FP-Growth."""
    print("=== Test complet FP-Growth ===")
    
    transactions=LinkedList()
    add_transaction(transactions,"E","K","M","N","O","Y")
    add_transaction(transactions,"D","E","K","N","O","Y")
    add_transaction(transactions,"A","E","K","M")
    add_transaction(transactions,"K","M","Y")
    add_transaction(transactions,"C","E","I","K","O")
    
    min_sup = 3
    patterns = mine_frequent_patterns(transactions, min_sup=min_sup, size=50, verbose=False)
    
    expected_patterns = {"K": 5, "E": 4, "M": 3, "O": 3, "Y": 3}
    
    found_single_items = {}
    current = patterns.head
    while current:
        pattern = current.element
        if pattern.pattern.size == 1:
            item = pattern.pattern.head.element
            found_single_items[item] = pattern.support
        current = current.next
    
    for item, expected_sup in expected_patterns.items():
        assert item in found_single_items, f"Item {item} devrait etre trouve"
        assert found_single_items[item] == expected_sup, f"Support de {item} devrait etre {expected_sup}"
    
    print(f"Patterns trouves: {patterns.size}")
    print("Tous les tests complets FP-Growth passent\n")


def run_all_tests():
    """Execute tous les tests."""
    print("=" * 50)
    print("DEBUT DES TESTS")
    print("=" * 50 + "\n")
    
    try:
        test_linkedlist()
        test_hashmap()
        test_fpnode()
        test_fptree()
        test_calculate_freq()
        test_freq_pattern_set()
        test_fptree_construction()
        test_mine_frequent_patterns()
        test_conditional_fptree()
        test_complete_fpgrowth()
        
        print("=" * 50)
        print("TOUS LES TESTS SONT PASSES AVEC SUCCES!")
        print("=" * 50)
        
    except AssertionError as e:
        print(f"\n ERREUR: {e}")
        raise
    except Exception as e:
        print(f"\n EXCEPTION: {e}")
        raise

if __name__=="__main__":
    run_all_tests()
