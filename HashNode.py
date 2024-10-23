import math

# Node for the doubly linked list
class HashNode:
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.next = None
        self.prev = None

# Doubly linked list for chaining in each bucket
class DoublyLinkedList:
    def __init__(self):
        self.head = None
        self.tail = None

    # Append a key-value pair into the list
    def append(self, key, value):
        new_node = HashNode(key, value)
        if not self.head:  # If list is empty
            self.head = self.tail = new_node
        else:
            self.tail.next = new_node
            new_node.prev = self.tail
            self.tail = new_node

    # Retrieve a node by key
    def retrieve(self, key):
        current = self.head
        while current:
            if current.key == key:
                return current
            current = current.next
        return None

    # Delete a node by key
    def delete(self, key):
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
class HashMap:
    def __init__(self, initial_capacity=8):
        self.capacity = initial_capacity
        self.size = 0
        self.load_factor = 0.75
        self.shrink_factor = 0.25
        self.buckets = [DoublyLinkedList() for _ in range(self.capacity)]

    # Compute hash using the multiplication method
    def compute_hash(self, key):
        A = (math.sqrt(5) - 1) / 2  # Golden ratio constant for multiplication method
        return int(self.capacity * (key * A % 1))

    # Rehash all elements when resizing the table
    def perform_rehash(self, new_capacity):
        old_buckets = self.buckets
        self.buckets = [DoublyLinkedList() for _ in range(new_capacity)]
        self.capacity = new_capacity
        self.size = 0  # Reset size and reinsert all elements

        # Rehash and reinsert all elements from the old buckets
        for bucket in old_buckets:
            current = bucket.head
            while current:
                self.add(current.key, current.value)
                current = current.next

    # Adjust table size (expand or shrink) if needed
    def adjust_size(self):
        # If the load factor is exceeded, double the capacity
        if self.size >= self.capacity * self.load_factor:
            self.perform_rehash(self.capacity * 2)
        # If the table is too empty, shrink it (but keep a minimum size)
        elif self.size <= self.capacity * self.shrink_factor and self.capacity > 8:
            self.perform_rehash(self.capacity // 2)

    # Add a key-value pair to the hash table
    def add(self, key, value):
        index = self.compute_hash(key)
        node = self.buckets[index].retrieve(key)

        # Update if the key already exists
        if node:
            node.value = value
        else:
            # Otherwise append it to the bucket list
            self.buckets[index].append(key, value)
            self.size += 1
            self.adjust_size()  # Resize if necessary

    # Remove a key-value pair from the hash table
    def remove_key(self, key):
        index = self.compute_hash(key)
        node = self.buckets[index].retrieve(key)

        if node:
            self.buckets[index].delete(key)
            self.size -= 1
            self.adjust_size()  # Resize if necessary

    # Get the value associated with a key
    def get_value(self, key):
        index = self.compute_hash(key)
        node = self.buckets[index].retrieve(key)
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

# Testing the HashMap
if __name__ == "__main__":
    hash_map = HashMap()

    # Add key-value pairs
    hash_map.add(1, 10)
    hash_map.add(2, 15)
    hash_map.add(3, 20)
    hash_map.add(4, 30)
    hash_map.add(12, 120)

    # Display the table
    hash_map.display()

    # Search for a key
    print(f"Search key 2: {hash_map.get_value(2)}")

    # Remove a key
    hash_map.remove_key(2)
    hash_map.display()

    # Try to search for a removed key
    try:
        print(hash_map.get_value(2))
    except KeyError as e:
        print(e)
