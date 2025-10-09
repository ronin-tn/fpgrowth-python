from FPNode import FPNode
from HashMap import *

class FPTree:
    def __init__(self, capacity=50):
        self.root=FPNode("NULL", 0)
        self.header_table=HashMap(capacity)
    class HeaderNode:
        def __init__(self,item_name):
            self.item=item_name
            self.count=0
            self.first_node=None
            self.last_node=None

    def insert(self, transaction):
        current_node=self.root
        current_item=transaction.head

        while current_item:
            child=current_node.find_child(current_item.element)
            if child:
                child.count += 1
            else:
                new_node=FPNode(current_item.element, 1, current_node)
                current_node.children.add_last(new_node)
                self.link_to_header_table(new_node)
                child=new_node
            current_node=child
            current_item=current_item.next
    
    def link_to_header_table(self, node):
        headernode=self.header_table.get(node.item)

        if headernode is None:
            headernode=self.HeaderNode(node.item)
            headernode.count=node.count
            headernode.first_node=node
            headernode.last_node=node
            self.header_table.put(node.item, headernode)
        else:
            headernode.count += node.count
            headernode.last_node.node_link=node
            headernode.last_node=node
