class LinkedList:
    class Node:
        __slots__='element','next'
        def __init__(self,element,next_node=None):
            self.element=element
            self.next=next_node
    
    def __init__(self, max_size=None):
        self.head=None
        self.tail=None
        self.size=0
        self.max_size=max_size
        self.before_tail=None
    
    def is_empty(self):
        return self.size==0
    
    def add_first(self,element):
        new_node=self.Node(element)
        if self.is_empty():
            self.head=new_node
            self.tail=new_node
            self.before_tail=new_node
            new_node.next=new_node
        else:
            new_node.next=self.head
            self.head=new_node
            self.tail.next=self.head
        self.size +=1
    
    def add_last(self,element):
        new_node=self.Node(element)
        if self.is_empty():
            self.head=new_node
            self.tail=new_node
            self.before_tail=new_node
            new_node.next=None
        else:
            self.tail.next=new_node
            new_node.next=None
            self.before_tail=self.tail
            self.tail=new_node
        self.size +=1
    
    def remove_first(self):
        if self.is_empty():
            raise IndexError("LinkedList is empty")
        removed_element=self.head.element
        if self.size==1:
            self.head=None
            self.tail=None
        else:
            self.head=self.head.next
        self.size -=1
        return removed_element
    
    def remove_last(self):
        if self.is_empty():
            raise IndexError("LinkedList is empty")
        if self.size==1:
            return self.remove_first()

        removed_element=self.tail.element
        current=self.head
        while current.next !=self.tail:
            current=current.next
        current.next=None
        self.tail=current
        self.size -=1
        return removed_element
    
    def get_first(self):
        if self.is_empty():
            raise IndexError("LinkedList is empty")
        return self.head.element
    
    def get_last(self):
        if self.is_empty():
            raise IndexError("LinkedList is empty")
        return self.tail.element
    
    def __len__(self):
        return self.size
    def __str__(self):
        if self.is_empty():
            return "[]"
        result="["
        current=self.head
        visited=set()
        while current and current not in visited:
            visited.add(current)
            result +=str(current.element)
            if current.next and current.next not in visited:
                result +=", "
            current=current.next
        result +="]"
        return result
        
    def tri_insertion_desc(linkedlist):
        if linkedlist.head is None or linkedlist.head.next is None:
            return
        head=linkedlist.head
        current=linkedlist.head.next
        head.next=None
        while current:
            next_node=current.next
            if current.element.value>head.element.value:
                current.next=head
                head=current
            else:
                search=head
                while search.next and search.next.element.value>=current.element.value:
                    search=search.next
                current.next=search.next
                search.next=current
            current=next_node
        linkedlist.head=head
        temp=head
        while temp.next:
            temp=temp.next
        linkedlist.tail=temp

    def __iter__(self):
        current=self.head
        while current is not None:
            yield current.element
            current=current.next