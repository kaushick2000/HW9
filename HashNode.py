import math

# Node for the doubly linked list
class EntryNode:
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.next = None
        self.prev = None

# Doubly linked list for chaining in each bucket
class LinkedList:
    def __init__(self):
        self.head = None
        self.tail = None

    # Append a key-value pair into the list
    def append(self, key, value):
        new_node = EntryNode(key, value)
        if not self.head:  # If list is empty
            self.head = self.tail = new_node
        else:
            self.tail.next = new_node
            new_node.prev = self.tail
            self.tail = new_node

    # Retrieve a node by key
    def find(self, key):
        current = self.head
        while current:
            if current.key == key:
                return current
            current = current.next
        return None

    # Remove a node by key
    def remove(self, key):
        current = self.head
        while current:
            if current.key == key:
                # Remove current node
                if current.prev:
                    current.prev.next = current.next
                if current.next:
                    current.next.prev = current.prev
                if current == self.head:
                    self.head = current.next
                if current == self.tail:
                    self.tail = current.prev
                return
            current = current.next

    def __len__(self):
        count = 0
        current = self.head
        while current:
            count += 1
            current = current.next
        return count

# Hash table class
class MyHashMap:
    def __init__(self, initial_capacity=8):
        self.capacity = initial_capacity
        self.size = 0
        self.load_factor = 0.75
        self.shrink_factor = 0.25
        self.buckets = [LinkedList() for _ in range(self.capacity)]

    # Compute hash using the multiplication method
    def _hash_function(self, key):
        A = (math.sqrt(5) - 1) / 2  # Golden ratio constant for multiplication method
        return int(self.capacity * (key * A % 1))

    # Rehash all elements when resizing the table
    def _rehash(self, new_capacity):
        old_buckets = self.buckets
        self.buckets = [LinkedList() for _ in range(new_capacity)]
        self.capacity = new_capacity
        self.size = 0  # Reset size and reinsert all elements

        # Rehash and reinsert all elements from the old buckets
        for bucket in old_buckets:
            current = bucket.head
            while current:
                self.put(current.key, current.value)
                current = current.next

    # Adjust table size (expand or shrink) if needed
    def _resize(self):
        # If the load factor is exceeded, double the capacity
        if self.size >= self.capacity * self.load_factor:
            self._rehash(self.capacity * 2)
        # If the table is too empty, shrink it (but keep a minimum size)
        elif self.size <= self.capacity * self.shrink_factor and self.capacity > 8:
            self._rehash(self.capacity // 2)

    # Insert a key-value pair into the hash table
    def put(self, key, value):
        index = self._hash_function(key)
        node = self.buckets[index].find(key)

        # Update if the key already exists
        if node:
            node.value = value
        else:
            # Otherwise append it to the bucket list
            self.buckets[index].append(key, value)
            self.size += 1
            self._resize()  # Resize if necessary

    # Delete a key-value pair from the hash table
    def remove(self, key):
        index = self._hash_function(key)
        node = self.buckets[index].find(key)

        if node:
            self.buckets[index].remove(key)
            self.size -= 1
            self._resize()  # Resize if necessary

    # Get the value associated with a key
    def get(self, key):
        index = self._hash_function(key)
        node = self.buckets[index].find(key)
        if node:
            return node.value
        else:
            raise KeyError(f"Key {key} not found")

    # Display the contents of the hash table
    def display(self):
        for i, bucket in enumerate(self.buckets):
            current = bucket.head
            print(f"Bucket {i}: ", end="")
            while current:
                print(f"({current.key}: {current.value})", end=" -> ")
                current = current.next
            print("None")

# Testing the MyHashMap
if __name__ == "__main__":
    my_hash_map = MyHashMap()

    # Add key-value pairs
    my_hash_map.put(10, 100)
    my_hash_map.put(20, 200)
    my_hash_map.put(30, 300)
    my_hash_map.put(40, 400)
    my_hash_map.put(15, 150)

    # Display the table
    my_hash_map.display()

    # Search for a key
    print(f"Search key 20: {my_hash_map.get(20)}")

    # Remove a key
    my_hash_map.remove(20)
    my_hash_map.display()

    # Try to search for a removed key
    try:
        print(my_hash_map.get(20))
    except KeyError as e:
        print(e)
