"""
Implémentation d'un noeud pour l'arbre FP (Frequent Pattern Tree).
"""

from TreeNode import TreeNode

class FPNode(TreeNode):
    """
    Represente un noeud dans l'arbre FP utilisé par l'algorithme FP-Growth.

    Hérite de TreeNode et ajoute des fonctionnalités spécifiques à FP-Growth:
    - Compte (fréquence) de l'item
    - node_link pour lier tous les noeuds contenant le meme item
    """
    __slots__=('item','count','node_link')
    
    def __init__(self,item=None,count=1,parent=None):
        """
        Initialise un noeud FP avec un item, un compte et un parent.
        
        Args:
            item: L'item stocké dans ce noeud (None pour le noeud racine)
            count: Le compte (fréquence) de l'item dans ce chemin
            parent: Référence au noeud parent (None pour la racine)
        """
        super().__init__(item,parent)
        self.item=item
        self.count=count
        self.node_link=None

    def find_child(self,item_name):
        """
        Recherche un enfant contenant un item spécifique.
        
        Complexité: O(1) en moyenne grace à l'utilisation de HashMap.
        
        Args:
            item_name: Le nom de l'item à rechercher
        
        Returns:
            Le noeud enfant contenant l'item, ou None si non trouve
        """
        return super().find_child(item_name)

    def add_child(self,node):
        """
        Ajoute un noeud enfant à ce noeud.
        
        Complexité: O(1) en moyenne grace à l'utilisation de HashMap.
        
        Args:
            node: Le noeud FPNode à ajouter comme enfant
        """
        super().add_child(node)
