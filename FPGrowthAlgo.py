"""
Module contenant l'implémentation de l'algorithme FP-Growth pour la découverte de patterns fréquents.
"""

from LinkedList import LinkedList
from HashMap import HashMap

def add_transaction(transactions,*items):
    """
    Ajoute une nouvelle transaction à la liste de transactions.
    
    Args:
        transactions: Liste chaînée contenant toutes les transactions
        *items: Items à ajouter à la nouvelle transaction
    """
    trans=LinkedList()
    for item in items:
        trans.add_last(item)
    transactions.add_last(trans)

def calculate_freq(transactions,size):
    """
    Calcule la fréquence de chaque item dans l'ensemble de transactions.
    
    Args:
        transactions: Liste chaînée contenant toutes les transactions
        size: Taille de la table de hachage pour stocker les fréquences
    
    Returns:
        HashMap contenant chaque item comme clé et sa fréquence comme valeur
    """
    freq=HashMap(size)
    current_trans=transactions.head
    while current_trans:
        seen_items=HashMap(size)
        current_item=current_trans.element.head
        while current_item:
            item=current_item.element
            if not seen_items.contains_key(item):
                seen_items.put(item,True)
                if freq.contains_key(item):
                    freq.put(item,freq.get(item)+1)
                else:
                    freq.put(item,1)
            current_item=current_item.next
        current_trans=current_trans.next
    return freq


def freq_pattern_set(transactions,freq,min_sup,size):
    """
    Filtre les items fréquents selon le seuil de support minimal et les trie par ordre décroissant.
    
    Args:
        transactions: Liste chaînée contenant toutes les transactions
        freq: HashMap contenant les fréquences de chaque item
        min_sup: Seuil de support minimal
        size: Taille de la table de hachage
    
    Returns:
        Liste chaînée triée par ordre décroissant de fréquence contenant les items fréquents
    """
    L=HashMap(size)
    for bucket in freq.table:
        if not bucket.is_empty():
            node=bucket.head
            while node:
                k=node.element.key
                v=node.element.value
                if v>=min_sup:
                    L.put(k,v)
                node=node.next
    
    freq_list=LinkedList()
    for bucket in L.table:
        if not bucket.is_empty():
            node=bucket.head
            while node:
                freq_list.add_last(node.element)
                node=node.next
    
    LinkedList.tri_insertion_desc(freq_list)
    return freq_list



def ordered_itemsets(transactions,freq_list):
    """
    Réordonne les items de chaque transaction selon l'ordre de fréquence décroissante.
    
    Args:
        transactions: Liste chaînée contenant toutes les transactions
        freq_list: Liste chaînée des items fréquents triés par ordre décroissant
    
    Returns:
        Liste chaînée contenant les transactions avec items réordonnés
    """
    ordered_itemsets=LinkedList()
    current_trans=transactions.head
    while current_trans:
        transaction_items=current_trans.element
        ordered_items=LinkedList()
        seen_items=HashMap(50)
        freq_node=freq_list.head
        while freq_node:
            item=freq_node.element.key
            current_item=transaction_items.head
            found=False
            while current_item:
                if current_item.element==item and not seen_items.contains_key(item):
                    found=True
                    seen_items.put(item,True)
                    break
                current_item=current_item.next
            if found:
                ordered_items.add_last(item)
            freq_node=freq_node.next

        ordered_itemsets.add_last(ordered_items)
        current_trans=current_trans.next
    return ordered_itemsets


def get_prefix(node):
    """
    Récupère le préfixe (chemin depuis la racine) d'un nœud dans l'arbre FP.
    
    Args:
        node: Le nœud FPNode dont on veut obtenir le préfixe
    
    Returns:
        Liste chaînée contenant les items du préfixe dans l'ordre de la racine au nœud
    """
    reverse_prefix=LinkedList()
    current=node.parent
    while current and current.item!="NULL":
        reverse_prefix.add_last(current.item)
        current=current.parent
    prefix=LinkedList()
    curr=reverse_prefix.head
    while curr:
        prefix.add_first(curr.element)
        curr=curr.next
    return prefix


def conditional_pattern_base(fptree,size):
    """
    Construit la base de patterns conditionnels pour chaque item dans la table d'en-tête.
    
    Pour chaque item, collecte tous les préfixes (chemins depuis la racine) des nœuds
    contenant cet item, avec leur compte associé.
    
    Args:
        fptree: L'arbre FP pour lequel construire la base de patterns conditionnels
        size: Taille de la table de hachage
    
    Returns:
        HashMap où chaque clé est un item et la valeur est une liste de chemins avec leur compte
    """
    class CheminCount:
        """
        Classe interne pour stocker un chemin avec son compte.
        """
        def __init__(self,chemin,count):
            self.chemin=chemin
            self.count=count
        def __str__(self):
            return f"({self.chemin},{self.count})"
    
    cpb=HashMap(size)
    keys=fptree.header_table.keys()
    current_key=keys.head
    while current_key:
        item=current_key.element
        header_node=fptree.header_table.get(item)
        prefixes=LinkedList()
        current_node=header_node.first_node
        while current_node:
            prefix=get_prefix(current_node)
            
            if not prefix.is_empty():
                chemin_count=CheminCount(prefix,current_node.count)
                prefixes.add_last(chemin_count)
            
            current_node=current_node.node_link
        
        if not prefixes.is_empty():
            cpb.put(item,prefixes)
        
        current_key=current_key.next
    
    return cpb

def print_cpb(cpb):
    """
    Affiche la base de patterns conditionnels de manière lisible.
    
    Args:
        cpb: HashMap contenant la base de patterns conditionnels
    """
    keys=cpb.keys()
    current_key=keys.head
    while current_key:
        key=current_key.element
        value=cpb.get(key)
        print(f"{key} : {value}")
        current_key=current_key.next

