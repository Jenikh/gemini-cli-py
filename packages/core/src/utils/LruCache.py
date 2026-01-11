from collections import OrderedDict

class LruCache:
  """
  A simple Least Recently Used (LRU) cache implementation.
  """
  def __init__(self, maxSize: int):
    # Use collections.OrderedDict to maintain the order of items.
    self.cache = OrderedDict()
    self.maxSize = maxSize

  def get(self, key):
    """
    Gets an item from the cache and marks it as most recently used.
    """
    if key not in self.cache:
      return None
    
    # Move the accessed item to the end to mark it as most recently used.
    self.cache.move_to_end(key)
    return self.cache[key]

  def set(self, key, value):
    """
    Sets an item in the cache. If the cache is full, evicts the
    least recently used item.
    """
    if key in self.cache:
      # Move existing key to the end, then update value.
      self.cache.move_to_end(key)
    self.cache[key] = value

    # If cache exceeds max size, remove the oldest item.
    if len(self.cache) > self.maxSize:
      # popitem(last=False) removes the first item inserted (the LRU item).
      self.cache.popitem(last=False)
      
  def clear(self):
    """
    Clears the entire cache.
    """
    self.cache.clear()