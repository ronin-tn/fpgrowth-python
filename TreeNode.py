"""
Implémentation d'un noeud générique pour les arbres.
"""

from HashMap import HashMap

class TreeNode:
    __slots__=('data','parent','children')
    
    def __init__(self,data=None,parent=None):
        self.data=data
        self.parent=parent
        self.children=HashMap(10)

    def find_child(self,data_key):
        return self.children.get(data_key)

    def add_child(self,node):
        if node.data is not None:
            self.children.put(node.data,node)

