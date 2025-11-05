"""
Implémentation d'une table de hachage générique avec résolution des collisions par chaînage.
"""

from LinkedList import LinkedList


class HashMap:
    """
    Table de hachage utilisant le chaînage pour gérer les collisions.
    
    Utilise une classe Node imbriquée pour stocker les paires clé-valeur.
    La fonction de hachage utilise un multiplicateur constant pour les chaines de caracteres.
    """
    HASH_MULTIPLIER=31
    
    class Node:
        """
        Classe interne représentant une paire clé-valeur dans la table de hachage.
        
        Utilise une classe imbriquée pour l'encapsulation et éviter l'exposition
        des détails d'implémentation à l'extérieur de la classe HashMap.
        """
        def __init__(self,key=None,value=None):
            """
            Initialise un nœud avec une clé et une valeur.
            
            Args:
                key: La clé de la paire
                value: La valeur associée à la clé
            """
            self.key=key
            self.value=value
    
    def __init__(self,n):
        """
        Initialise une table de hachage vide avec une capacite donnee.
        
        Args:
            n: La capacite initiale de la table (nombre de buckets)
        
        Raises:
            ValueError: Si la capacité est inferieure ou egale à 0
        """
        if n<=0:
            raise ValueError("Capacite doit etre superieur a 0")
        self.capacity=n
        self.size=0
        self.table=[LinkedList() for i in range(n)]

    def _hash(self,key):
        """
        Calcule l'index de hachage pour une clé donnee.
        
        Utilise le modulo pour les entiers et une fonction polynomiale
        avec multiplicateur constant pour les chaines de caracteres.
        
        Args:
            key: La clé à hacher
        
        Returns:
            L'index dans la table de hachage
        """
        if isinstance(key,int):
            return key%self.capacity
        hash_value=0
        for char in str(key):
            hash_value=(hash_value*HashMap.HASH_MULTIPLIER+ord(char))%self.capacity
        return hash_value
    
    def _get_bucket(self,index):
        """
        Récupere le bucket (liste chainee) à l'index specifie.
        
        Args:
            index: L'index du bucket à récupérer
        
        Returns:
            La LinkedList correspondant au bucket
        
        Raises:
            IndexError: Si l'index est hors limites
        """
        if index<0 or index>=self.capacity:
            raise IndexError("index out of range")
        return self.table[index]
    
    def put(self,key,value):
        """
        Insère ou met à jour une paire clé-valeur dans la table.
        
        Si la clé existe déjà, la valeur est mise à jour.
        Sinon, une nouvelle entrée est ajoutée.
        Complexité: O(1) en moyenne, O(n) dans le pire cas.
        
        Args:
            key: La clé à insérer ou mettre à jour
            value: La valeur associée à la clé
        
        Raises:
            ValueError: Si la clé est None
        """
        if key is None:
            raise ValueError("Key cannot be None")
        index=self._hash(key)
        bucket=self._get_bucket(index)
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
        """
        Récupère la valeur associée à une clé.
        
        Complexité: O(1) en moyenne, O(n) dans le pire cas.
        
        Args:
            key: La clé dont on veut récupérer la valeur
        
        Returns:
            La valeur associée à la clé, ou None si la clé n'existe pas
        """
        index=self._hash(key)
        bucket=self._get_bucket(index)
        if bucket.is_empty():
            return None
        current=bucket.head
        while current:
            if current.element.key==key:
                return current.element.value
            current=current.next
        return None

    def contains_key(self,key):
        """
        Vérifie si une clé existe dans la table.
        
        Args:
            key: La clé à rechercher
        
        Returns:
            True si la clé existe, False sinon
        """
        return self.get(key) is not None
    
    def remove(self,key):
        """
        Supprime une paire clé-valeur de la table.
        
        Complexité: O(1) en moyenne, O(n) dans le pire cas.
        
        Args:
            key: La clé de la paire à supprimer
        
        Returns:
            Le nœud supprimé (contenant la clé et la valeur), ou None si la clé n'existe pas
        """
        index=self._hash(key)
        bucket=self._get_bucket(index)
        if bucket.is_empty():
            return None

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

        return None
    
    def keys(self):
        """
        Retourne toutes les clés présentes dans la table.
        
        Returns:
            Une LinkedList contenant toutes les clés
        """
        keys_list=LinkedList()
        for bucket in self.table:
            if not bucket.is_empty():
                current=bucket.head
                while current:
                    keys_list.add_last(current.element.key)
                    current=current.next
        
        return keys_list