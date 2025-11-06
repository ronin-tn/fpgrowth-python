"""
Implémentation d'un noeud générique pour les arbres.
"""

from HashMap import HashMap

class TreeNode:
    """
    Représente un noeud générique dans un arbre.

    Chaque noeud stocke des données, une référence au parent,
    et utilise une HashMap pour stocker ses enfants (accès O(1) en moyenne).
    """
    def __init__(self,data=None,parent=None):
        """
        Initialise un noeud avec des données et un parent.
        
        Args:
            data: Les données stockées dans ce noeud (None pour le noeud racine)
            parent: Référence au noeud parent (None pour la racine)
        """
        self.data=data
        self.parent=parent
        self.children=HashMap(10)

    def find_child(self,data_key):
        """
        Recherche un enfant contenant des données avec une clé spécifique.
        
        Complexité: O(1) en moyenne grâce à l'utilisation de HashMap.
        
        Args:
            data_key: La clé des données à rechercher
        
        Returns:
            Le noeud enfant contenant les données, ou None si non trouvé
        """
        return self.children.get(data_key)

    def add_child(self,node):
        """
        Ajoute un noeud enfant à ce noeud.
        
        Complexité: O(1) en moyenne grâce à l'utilisation de HashMap.
        
        Args:
            node: Le noeud TreeNode à ajouter comme enfant
        """
        if node.data is not None:
            self.children.put(node.data,node)

