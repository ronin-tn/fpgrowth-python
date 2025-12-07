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


def build_conditional_fptree(cpb_for_item, min_sup, size=50):
    """
    Construit un arbre FP conditionnel à partir d'une base de patterns conditionnels.
    
    Args:
        cpb_for_item: LinkedList de CheminCount (prefix, count) pour un item
        min_sup: Seuil de support minimal
        size: Taille de la table de hachage
    
    Returns:
        FPTree: Un nouvel arbre FP conditionnel, ou None si vide
    """
    from FPTree import FPTree
    
    freq=HashMap(size)
    current=cpb_for_item.head
    while current:
        chemin_count=current.element
        prefix=chemin_count.chemin
        count=chemin_count.count
        
        item_node=prefix.head
        while item_node:
            item=item_node.element
            if freq.contains_key(item):
                freq.put(item, freq.get(item) + count)
            else:
                freq.put(item, count)
            item_node=item_node.next
        current=current.next
    
    freq_items=HashMap(size)
    for bucket in freq.table:
        if not bucket.is_empty():
            node=bucket.head
            while node:
                if node.element.value >= min_sup:
                    freq_items.put(node.element.key, node.element.value)
                node=node.next
    
    if freq_items.size == 0:
        return None
    
    freq_list=LinkedList()
    for bucket in freq_items.table:
        if not bucket.is_empty():
            node=bucket.head
            while node:
                freq_list.add_last(node.element)
                node=node.next
    LinkedList.tri_insertion_desc(freq_list)
    
    conditional_tree=FPTree(size)
    
    current=cpb_for_item.head
    while current:
        chemin_count=current.element
        prefix=chemin_count.chemin
        count=chemin_count.count
        
        ordered_path=LinkedList()
        freq_node=freq_list.head
        while freq_node:
            item=freq_node.element.key
            path_node=prefix.head
            while path_node:
                if path_node.element == item:
                    ordered_path.add_last(item)
                    break
                path_node=path_node.next
            freq_node=freq_node.next
        
        if not ordered_path.is_empty():
            for _ in range(count):
                conditional_tree.insert(ordered_path)
        
        current=current.next
    
    if conditional_tree.header_table.size == 0:
        return None
    
    return conditional_tree


def get_header_items_ascending(fptree):
    """
    Récupère les items de la table header triés par ordre croissant de fréquence.
    
    Args:
        fptree: L'arbre FP
    
    Returns:
        LinkedList: Items triés par ordre croissant de fréquence
    """
    items_list=LinkedList()
    keys=fptree.header_table.keys()
    current_key=keys.head
    while current_key:
        item=current_key.element
        header_node=fptree.header_table.get(item)
        
        class ItemCount:
            def __init__(self, key, value):
                self.key=key
                self.value=value
        
        items_list.add_last(ItemCount(item, header_node.count))
        current_key=current_key.next
    
    LinkedList.tri_insertion_desc(items_list)
    
    reversed_list=LinkedList()
    current=items_list.head
    while current:
        reversed_list.add_first(current.element.key)
        current=current.next
    
    return reversed_list


def fp_growth(fptree, prefix, min_sup, frequent_patterns, size=50, depth=0, verbose=False):
    """
    Algorithme FP-Growth récursif pour découvrir tous les patterns fréquents.
    
    Args:
        fptree: L'arbre FP (ou arbre FP conditionnel)
        prefix: Préfixe courant (LinkedList d'items)
        min_sup: Seuil de support minimal
        frequent_patterns: Liste pour stocker les patterns découverts (LinkedList)
        size: Taille des tables de hachage
        depth: Profondeur de récursion (pour affichage)
        verbose: Si True, affiche les étapes de l'algorithme
    """
    class FrequentPattern:
        """Classe pour stocker un pattern fréquent avec son support."""
        def __init__(self, pattern, support):
            self.pattern=pattern
            self.support=support
        
        def __str__(self):
            return f"({self.pattern}, support={self.support})"
    
    indent="  " * depth
    
    items=get_header_items_ascending(fptree)
    
    current_item=items.head
    while current_item:
        item=current_item.element
        header_node=fptree.header_table.get(item)
        support=header_node.count
        
        new_pattern=LinkedList()
        prefix_node=prefix.head
        while prefix_node:
            new_pattern.add_last(prefix_node.element)
            prefix_node=prefix_node.next
        new_pattern.add_last(item)
        
        if verbose:
            print(f"{indent}Mining item '{item}' with support {support}")
            print(f"{indent}  Pattern found: {new_pattern}")
        
        frequent_patterns.add_last(FrequentPattern(new_pattern, support))
        
        cpb=conditional_pattern_base_for_item(fptree, item, size)
        
        if cpb is not None and not cpb.is_empty():
            if verbose:
                print(f"{indent}  Building conditional FP-Tree for '{item}'")
            
            conditional_tree=build_conditional_fptree(cpb, min_sup, size)
            
            if conditional_tree is not None:
                if verbose:
                    print(f"{indent}  Conditional tree has {conditional_tree.header_table.size} items")
                
                fp_growth(conditional_tree, new_pattern, min_sup, frequent_patterns, size, depth + 1, verbose)
        
        current_item=current_item.next


def conditional_pattern_base_for_item(fptree, item, size):
    """
    Construit la base de patterns conditionnels pour un item spécifique.
    
    Args:
        fptree: L'arbre FP
        item: L'item pour lequel construire la CPB
        size: Taille de la table de hachage
    
    Returns:
        LinkedList de CheminCount, ou None si l'item n'existe pas
    """
    class CheminCount:
        def __init__(self, chemin, count):
            self.chemin=chemin
            self.count=count
        def __str__(self):
            return f"({self.chemin},{self.count})"
    
    header_node=fptree.header_table.get(item)
    if header_node is None:
        return None
    
    prefixes=LinkedList()
    current_node=header_node.first_node
    while current_node:
        prefix=get_prefix(current_node)
        if not prefix.is_empty():
            prefixes.add_last(CheminCount(prefix, current_node.count))
        current_node=current_node.node_link
    
    return prefixes


def mine_frequent_patterns(transactions, min_sup, size=50, verbose=False):
    """
    Point d'entrée principal pour découvrir tous les itemsets fréquents.
    
    Args:
        transactions: LinkedList contenant toutes les transactions
        min_sup: Seuil de support minimal
        size: Taille des tables de hachage
        verbose: Si True, affiche les étapes de l'algorithme
    
    Returns:
        LinkedList de FrequentPattern (pattern, support)
    """
    from FPTree import FPTree
    
    if verbose:
        print("=" * 60)
        print("ETAPE 1: Calcul des frequences")
        print("=" * 60)
    
    freq=calculate_freq(transactions, size)
    
    if verbose:
        print("Frequences calculees:")
        keys=freq.keys()
        current=keys.head
        while current:
            print(f"  {current.element}: {freq.get(current.element)}")
            current=current.next
        print()
    
    if verbose:
        print("=" * 60)
        print("ETAPE 2: Filtrage et tri des items frequents")
        print("=" * 60)
    
    freq_list=freq_pattern_set(transactions, freq, min_sup, size)
    
    if verbose:
        print("Items frequents (tries par ordre decroissant):")
        current=freq_list.head
        while current:
            print(f"  {current.element.key}: {current.element.value}")
            current=current.next
        print()
    
    if verbose:
        print("=" * 60)
        print("ETAPE 3: Reordonnement des transactions")
        print("=" * 60)
    
    ordered=ordered_itemsets(transactions, freq_list)
    
    if verbose:
        t=1
        current=ordered.head
        while current:
            print(f"  T{t}: {current.element}")
            current=current.next
            t += 1
        print()
    
    if verbose:
        print("=" * 60)
        print("ETAPE 4: Construction de l'arbre FP")
        print("=" * 60)
    
    tree=FPTree(size)
    for itemset in ordered:
        tree.insert(itemset)
    
    if verbose:
        print("Arbre FP construit avec succes")
        print_fptree(tree)
        print()
    
    if verbose:
        print("=" * 60)
        print("ETAPE 5: Extraction des patterns frequents (FP-Growth)")
        print("=" * 60)
    
    frequent_patterns=LinkedList()
    prefix=LinkedList()
    
    fp_growth(tree, prefix, min_sup, frequent_patterns, size, 0, verbose)
    
    if verbose:
        print()
        print("=" * 60)
        print("RESULTAT FINAL")
        print("=" * 60)
    
    return frequent_patterns


def print_frequent_patterns(patterns):
    """
    Affiche tous les patterns fréquents de manière formatée.
    
    Args:
        patterns: LinkedList de FrequentPattern
    """
    print("\n" + "=" * 50)
    print("PATTERNS FREQUENTS DECOUVERTS")
    print("=" * 50)
    
    count=0
    current=patterns.head
    while current:
        pattern=current.element
        items_str=str(pattern.pattern)
        print(f"  {items_str} : support={pattern.support}")
        count += 1
        current=current.next
    
    print("=" * 50)
    print(f"Total: {count} patterns frequents")
    print("=" * 50)


def print_fptree(fptree, node=None, indent=0):
    """
    Affiche une représentation visuelle de l'arbre FP.
    
    Args:
        fptree: L'arbre FP à afficher
        node: Noeud courant (None pour commencer à la racine)
        indent: Niveau d'indentation
    """
    if node is None:
        print("\n" + "=" * 40)
        print("VISUALISATION FP-TREE")
        print("=" * 40)
        node=fptree.root
        print(f"ROOT (NULL)")
    
    children_keys=node.children.keys()
    current_child_key=children_keys.head
    while current_child_key:
        child=node.children.get(current_child_key.element)
        prefix="  " * (indent + 1) + "+-- " if current_child_key.next else "  " * (indent + 1) + "`-- "
        print(f"{prefix}{child.item}:{child.count}")
        print_fptree(fptree, child, indent + 1)
        current_child_key=current_child_key.next
