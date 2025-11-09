"""
Implémentation d'un arbre générique.
"""

from TreeNode import TreeNode

class Tree:
    __slots__=('root',)
    
    def __init__(self,root_data=None,root_node=None):
        if root_node is not None:
            self.root=root_node
        else:
            self.root=TreeNode(root_data,None)

