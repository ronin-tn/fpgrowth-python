"""
Implémentation d'un arbre générique.
"""

from TreeNode import TreeNode

class Tree:
    """
    Arbre générique utilisé comme structure de base pour des arbres spécialisés.
    
    L'arbre permet de stocker des données hiérarchiques avec des relations parent-enfant.
    """
    def __init__(self,root_data=None,root_node=None):
        """
        Initialise un arbre avec une racine.
        
        Args:
            root_data: Les données pour le noeud racine (None par défaut)
            root_node: Un noeud racine personnalisé (si fourni, root_data est ignoré)
        """
        if root_node is not None:
            self.root=root_node
        else:
            self.root=TreeNode(root_data,None)

