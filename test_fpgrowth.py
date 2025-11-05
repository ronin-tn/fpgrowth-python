"""
Fichier de tests pour l'algorithme FP-Growth et toutes les structures de données.
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
    assert ll.is_empty(),"La liste devrait être vide"
    assert ll.size==0,"La taille devrait être 0"
    
    ll.add_first("A")
    assert not ll.is_empty(),"La liste ne devrait pas être vide"
    assert ll.size==1,"La taille devrait être 1"
    assert ll.get_first()=="A","Le premier élément devrait être 'A'"
    
    ll.add_last("B")
    assert ll.size==2,"La taille devrait être 2"
    assert ll.get_last()=="B","Le dernier élément devrait être 'B'"
    
    removed=ll.remove_first()
    assert removed=="A","L'élément supprimé devrait être 'A'"
    assert ll.size==1,"La taille devrait être 1"
    
    print("Tous les tests LinkedList passent\n")

def test_hashmap():
    """Tests pour la classe HashMap."""
    print("=== Tests HashMap ===")
    
    hm=HashMap(10)
    assert hm.size==0,"La taille devrait être 0"
    
    hm.put("key1","value1")
    assert hm.size==1,"La taille devrait être 1"
    assert hm.get("key1")=="value1","La valeur devrait être 'value1'"
    assert hm.contains_key("key1"),"La clé devrait exister"
    
    hm.put("key1","value2")
    assert hm.get("key1")=="value2","La valeur devrait être mise à jour"
    
    hm.put("key2",100)
    assert hm.size==2,"La taille devrait être 2"
    
    removed=hm.remove("key1")
    assert removed is not None,"Le nœud devrait être supprimé"
    assert hm.size==1,"La taille devrait être 1"
    assert not hm.contains_key("key1"),"La clé ne devrait plus exister"
    
    keys=hm.keys()
    assert keys.size==1,"Il devrait y avoir une clé"
    
    print("Tous les tests HashMap passent\n")

def test_fpnode():
    """Tests pour la classe FPNode."""
    print("=== Tests FPNode ===")
    
    root=FPNode("NULL",0)
    assert root.item=="NULL","L'item devrait être 'NULL'"
    assert root.count==0,"Le compte devrait être 0"
    assert root.parent is None,"Le parent devrait être None"
    
    child=FPNode("A",1,root)
    root.add_child(child)
    
    found=root.find_child("A")
    assert found is not None,"L'enfant devrait être trouvé"
    assert found.item=="A","L'item de l'enfant devrait être 'A'"
    
    not_found=root.find_child("B")
    assert not_found is None,"L'enfant ne devrait pas être trouvé"
    
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
    assert child_a.count==1,"Le compte de A devrait être 1"
    
    tree.insert(transaction1)
    assert child_a.count==2,"Le compte de A devrait être 2"
    
    header=tree.header_table.get("A")
    assert header is not None,"Le header pour A devrait exister"
    assert header.count==2,"Le compte total de A devrait être 2"
    
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
    assert freq.get("A")==2,"A devrait apparaître 2 fois"
    assert freq.get("B")==1,"B devrait apparaître 1 fois"
    assert freq.get("C")==1,"C devrait apparaître 1 fois"
    
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
    
    assert freq_list.size > 0,"Il devrait y avoir des items fréquents"
    assert freq_list.head.element.key=="A","A devrait être le plus fréquent"
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
        
        print("=" * 50)
        print("TOUS LES TESTS SONT PASSÉS AVEC SUCCES!")
        print("=" * 50)
        
    except AssertionError as e:
        print(f"\n ERREUR: {e}")
        raise
    except Exception as e:
        print(f"\n EXCEPTION: {e}")
        raise

if __name__=="__main__":
    run_all_tests()

