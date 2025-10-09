from LinkedList import LinkedList

class HashMap:
    class Node:
        def __init__(self,key=-1,value=-1):
            self.key=key
            self.value=value
    def __init__(self,n):
        self.capacity=n
        self.size=0
        self.table=LinkedList()
        for i in range(n):
            self.table.add_last(LinkedList())

    def _hash(self, key):
        if isinstance(key, int):
            return key % self.capacity
        h=0
        for ch in str(key):
            h=(h * 31 + ord(ch)) % self.capacity
        return h
    def _get_bucket(self,index):
        if(index<0 or index>=self.capacity):
            raise IndexError("index out of range")
        current=self.table.head
        for i in range(index):
            current=current.next
        return current.element
    def put(self,key,value):
        i=self._hash(key)
        bucket=self._get_bucket(i)
        current=bucket.head
        while current:
            if current.element.key==key:
                current.element.value=value
                return
            current=current.next
        new_node=self.Node(key,value)
        bucket.add_last(new_node)
        self.size+=1
    
    def get(self,key):
        index=self._hash(key)
        bucket=self._get_bucket(index)
        if(bucket.is_empty()):
            return None
        current=bucket.head
        while(current):
            if(current.element.key==key):
                return current.element.value
            current=current.next
        return None

    def contains_key(self,key):
        return self.get(key) is not None
    def remove(self, key):
        index=self._hash(key)
        bucket=self._get_bucket(index)
        if(bucket.is_empty()):
            return "N'existe pas"

        current=bucket.head
        prev=None
        while current:
            if current.element.key==key:
                if prev is None:
                    removed=bucket.remove_first()
                elif current.next is None:
                    removed=bucket.remove_last()
                else:
                    prev.next=current.next
                    bucket.size-=1
                    removed=current.element
                self.size-=1
                return removed
            prev=current
            current=current.next

        return "N'existe pas"
    
    def keys(self):
        keys_list=LinkedList()
        current_bucket=self.table.head

        while current_bucket:
            bucket=current_bucket.element
            if not bucket.is_empty():
                current=bucket.head
                while current:
                    keys_list.add_last(current.element.key)
                    current=current.next
            current_bucket=current_bucket.next

        return keys_list