"""
Implémentation d'une liste chaînée générique avec accès bidirectionnel.
"""

class LinkedList:
    """
    Liste chaînée doublement liée permettant l'ajout et la suppression en O(1) aux extrémités.
    Utilise une classe Node imbriquée pour l'encapsulation et __slots__ pour optimiser la mémoire.
    """
    class Node:
        """
        Classe interne représentant un nœud de la liste chaînée.
        
        Utilise __slots__ pour réduire la consommation mémoire en limitant les attributs
        aux seuls nécessaires (element et next), évitant ainsi le dictionnaire d'instance.
        """
        __slots__ = 'element', 'next'
        
        def __init__(self,element,next_node=None):
            """
            Initialise un nœud avec un élément et un pointeur vers le nœud suivant.
            
            Args:
                element: L'élément à stocker dans le nœud
                next_node: Référence au nœud suivant (None par défaut)
            """
            self.element=element
            self.next=next_node
    
    def __init__(self,max_size=None):
        """
        Initialise une liste chaînée vide.
        
        Args:
            max_size: Taille maximale autorisée (None pour taille illimitée)
        """
        if max_size is not None and max_size<=0:
            raise ValueError("max_size must be greater than 0")
        self.head=None
        self.tail=None
        self.size=0
        self.max_size=max_size
    
    def is_empty(self):
        """
        Vérifie si la liste est vide.
        
        Returns:
            True si la liste est vide, False sinon
        """
        return self.size==0
    
    def add_first(self,element):
        """
        Ajoute un élément au début de la liste en O(1).
        
        Args:
            element: L'élément à ajouter
        """
        new_node=self.Node(element)
        if self.is_empty():
            self.head=new_node
            self.tail=new_node
            new_node.next=None
        else:
            new_node.next=self.head
            self.head=new_node
        self.size+=1
    
    def add_last(self,element):
        """
        Ajoute un élément à la fin de la liste en O(1).
        
        Args:
            element: L'élément à ajouter
        """
        new_node=self.Node(element)
        if self.is_empty():
            self.head=new_node
            self.tail=new_node
            new_node.next=None
        else:
            self.tail.next=new_node
            new_node.next=None
            self.tail=new_node
        self.size+=1
    
    def remove_first(self):
        """
        Supprime et retourne le premier élément de la liste en O(1).
        
        Returns:
            L'élément supprimé
        
        Raises:
            IndexError: Si la liste est vide
        """
        if self.is_empty():
            raise IndexError("LinkedList is empty")
        removed_element=self.head.element
        if self.size==1:
            self.head=None
            self.tail=None
        else:
            self.head=self.head.next
        self.size-=1
        return removed_element

    def remove_last(self):
        """
        Supprime et retourne le dernier élément de la liste en O(n).
        
        Returns:
            L'élément supprimé
        
        Raises:
            IndexError: Si la liste est vide
        """
        if self.is_empty():
            raise IndexError("LinkedList is empty")
        if self.size==1:
            return self.remove_first()

        removed_element=self.tail.element
        current=self.head
        while current.next!=self.tail:
            current=current.next
        current.next=None
        self.tail=current
        self.size-=1
        return removed_element
    
    def get_first(self):
        """
        Retourne le premier élément sans le supprimer.
        
        Returns:
            Le premier élément
        
        Raises:
            IndexError: Si la liste est vide
        """
        if self.is_empty():
            raise IndexError("LinkedList is empty")
        return self.head.element
    
    def get_last(self):
        """
        Retourne le dernier élément sans le supprimer.
        
        Returns:
            Le dernier élément
        
        Raises:
            IndexError: Si la liste est vide
        """
        if self.is_empty():
            raise IndexError("LinkedList is empty")
        return self.tail.element
    
    def __len__(self):
        """
        Retourne le nombre d'éléments dans la liste.
        
        Returns:
            La taille de la liste
        """
        return self.size
    
    def __str__(self):
        """
        Représentation string de la liste sous forme [elem1, elem2, ...].
        
        Returns:
            Chaîne de caractères représentant la liste
        """
        if self.is_empty():
            return "[]"
        result="["
        current=self.head
        visited=set()
        while current and current not in visited:
            visited.add(current)
            result+=str(current.element)
            if current.next and current.next not in visited:
                result+=", "
            current=current.next
        result+="]"
        return result
    
    @staticmethod
    def tri_insertion_desc(linkedlist):
        """
        Trie la liste chaînée par ordre décroissant selon la valeur de l'attribut 'value' des éléments.
        
        Utilise l'algorithme de tri par insertion adapté aux listes chaînées.
        Les éléments doivent avoir un attribut 'value' pour la comparaison.
        
        Args:
            linkedlist: La liste chaînée à trier (modifiée en place)
        """
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
        """
        Itérateur permettant de parcourir la liste avec une boucle for.
        
        Yields:
            Chaque élément de la liste dans l'ordre
        """
        current=self.head
        while current is not None:
            yield current.element
            current=current.next