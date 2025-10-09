from LinkedList import LinkedList
from HashMap import HashMap

def add_transaction(transactions,*items):
    trans=LinkedList()
    for item in items:
        trans.add_last(item)
    transactions.add_last(trans)

def calculate_freq(transactions,size):
    freq=HashMap(size)
    current_trans=transactions.head
    while current_trans:
        seen_items=HashMap(size)## bch ken item yetchef fi nafs transaction man3wdoch ne7sboh
        current_item=current_trans.element.head
        while current_item:
            item=current_item.element
            if not seen_items.contains_key(item):
                seen_items.put(item,True)
                if freq.contains_key(item):
                    freq.put(item,freq.get(item) + 1)
                else:
                    freq.put(item,1)
            current_item=current_item.next
        current_trans=current_trans.next
    return freq


def freq_pattern_set(transactions,freq,min_sup,size):
    ##ay wehd ikon value min support nzidoh fi table
    L=HashMap(size)
    current_bucket=freq.table.head
    while current_bucket:
        bucket=current_bucket.element
        node=bucket.head
        while node:
            k=node.element.key
            v=node.element.value
            if v >= min_sup:
                L.put(k,v)
            node=node.next
        current_bucket=current_bucket.next
    
    # najoutiwhom fi liste
    freq_list=LinkedList()
    current_bucket=L.table.head
    while current_bucket:
        bucket=current_bucket.element
        node=bucket.head
        while node:
            freq_list.add_last(node.element)
            node=node.next
        current_bucket=current_bucket.next
    
    # lista lezmha n3mlolha tri bch n5rjo frequent pattern base
    freq_list.tri_insertion_desc()
    return freq_list



def ordered_itemsets(transactions,freq_list):
    ordered_itemsets=LinkedList()
    current_trans=transactions.head
    while current_trans:
        transaction_items=current_trans.element
        ordered_items=LinkedList()
        # kel3ada dima nzido seen items bch mayt3wdoch fi nafs transaction
        seen_items=HashMap(50)
        freq_node=freq_list.head
        while freq_node:
            item=freq_node.element.key
            current_item=transaction_items.head
            found=False
            while current_item:
                if current_item.element==item and not seen_items.contains_key(item):
                    found=True
                    seen_items.put(item,True)
                    break
                current_item=current_item.next
            if found:
                ordered_items.add_last(item)
            freq_node=freq_node.next

        ordered_itemsets.add_last(ordered_items)
        current_trans=current_trans.next
    return ordered_itemsets


def get_prefix(node):
    reverse_prefix=LinkedList()
    current=node.parent
    while current and current.item != "NULL":
        reverse_prefix.add_last(current.item)
        current=current.parent
    prefix=LinkedList()
    curr=reverse_prefix.head
    while curr:
        prefix.add_first(curr.element)
        curr=curr.next
    return prefix


def conditional_pattern_base(fptree,size):
    class CheminCount:
        def __init__(self,chemin,count):
            self.chemin=chemin
            self.count=count
        def __str__(self):
            return f"({self.chemin},{self.count})"
    
    cpb=HashMap(size)
    # jib items kol mn header table
    keys=fptree.header_table.keys()
    current_key=keys.head
    while current_key:
        item=current_key.element
        header_node=fptree.header_table.get(item)
        #nsajlo prefixes t3 item kol fi lista 
        prefixes=LinkedList()
        current_node=header_node.first_node
        while current_node:
            # lahne rana njibo fi prefix wehd mt3 node, rodbelk dima tdhakrha
            prefix=get_prefix(current_node)
            
            #najoutiw chemin ken ki yebda prefix mahoch null
            if not prefix.is_empty():
                chemin_count=CheminCount(prefix,current_node.count)
                prefixes.add_last(chemin_count)
            
            # lahne t3ada lnafs item ama fi chemin ekhr
            current_node=current_node.node_link
        
        #ajouti prefies l conditional pattern base (hashmap)
        if not prefixes.is_empty():
            cpb.put(item,prefixes)
        
        current_key=current_key.next
    
    return cpb

## hedhy method bch tprinti cpb
def print_cpb(cpb):
    keys=cpb.keys()
    current_key=keys.head
    while current_key:
        key=current_key.element
        value=cpb.get(key)
        print(f"{key} : {value}")
        current_key=current_key.next

