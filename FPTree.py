"""
Implémentation de l'arbre FP (Frequent Pattern Tree) pour l'algorithme FP-Growth.
"""

from Tree import Tree
from FPNode import FPNode
from HashMap import *

class FPTree(Tree):
    """
    Frequent Pattern Tree utilisé pour stocker les transactions de manière compacte.
    
    Hérite de Tree et ajoute des fonctionnalités spécifiques à FP-Growth:
    - Table d'en-tête pour accès rapide aux noeuds
    - Insertion de transactions avec comptage de fréquences
    - Liens entre noeuds contenant le même item
    
    L'arbre FP permet de partager les préfixes communs entre transactions,
    reduisant ainsi l'espace memoire nécessaire. La table (header_table)
    permet un accès rapide à tous les noeuds contenant un item spécifique.
    """
    def __init__(self,capacity=50):
        """
        Initialise un arbre FP vide avec une racine et une table d'en-tête.
        
        Args:
            capacity: Capacité de la table d'en-tête (HashMap)
        """
        root_node=FPNode("NULL",0)
        super().__init__(root_node=root_node)
        self.header_table=HashMap(capacity)
    
    class HeaderNode:
        """
        Classe interne représentant une entrée dans le header table
        
        Stocke l'item, son compte total, et les references au premier et dernier
        noeud contenant cet item dans l'arbre (permettant de parcourir tous les noeuds
        d'un meme item via les node_link).
        """
        def __init__(self,item_name):
            """
            Initialise un noeud header pour un item.
            
            Args:
                item_name: Le nom de l'item
            """
            self.item=item_name
            self.count=0
            self.first_node=None
            self.last_node=None
    
    def insert(self,transaction):
        """
        Insère une transaction dans le FPTree.
        
        Si un chemin partiel existe déjà, incrémente les comptes.
        Sinon, crée de nouveaux noeuds et les lie à la table header.
        Complexité: O(m) où m est la taille de la transaction.
        
        Args:
            transaction: LinkedList contenant les items de la transaction
        """
        current_node=self.root
        current_item=transaction.head
        while current_item:
            child=current_node.find_child(current_item.element)
            if child:
                child.count+=1
                header_node=self.header_table.get(child.item)
                if header_node:
                    header_node.count+=1
            else:
                new_node=FPNode(current_item.element,1,current_node)
                current_node.add_child(new_node)
                self.link_to_header_table(new_node)
                child=new_node
            current_node=child
            current_item=current_item.next

    def link_to_header_table(self,node):
        """
        Lie un noeud à la table header correspondant à son item.
        
        Si l'item n'existe pas encore dans la table header, crée une nouvelle entrée.
        Sinon, met à jour le compte total et ajoute le noeud à la chaine de noeuds
        via node_link.
        
        Args:
            node: Le noeud FPNode à lier à la table header
        """
        headernode=self.header_table.get(node.item)

        if headernode is None:
            headernode=self.HeaderNode(node.item)
            headernode.count=node.count
            headernode.first_node=node
            headernode.last_node=node
            self.header_table.put(node.item,headernode)
        else:
            headernode.count+=node.count
            headernode.last_node.node_link=node
            headernode.last_node=node
