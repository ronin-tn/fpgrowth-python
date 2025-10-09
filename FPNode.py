from LinkedList import LinkedList

class FPNode:
    def __init__(self, item=None, count=1, parent=None):
        self.item=item
        self.count=count
        self.parent=parent
        self.children=LinkedList()
        self.node_link=None

    def find_child(self, item_name):
        current=self.children.head
        while current:
            if current.element.item==item_name:
                return current.element
            current=current.next
        return None
