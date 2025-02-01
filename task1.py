import time
import random
from collections import OrderedDict


class LRUCache:
    def __init__(self, capacity):
        self.cache = OrderedDict()
        self.capacity = capacity

    def get(self, key):
        if key not in self.cache:
            return None
        self.cache.move_to_end(key)
        return self.cache[key]

    def put(self, key, value):
        if key in self.cache:
            self.cache.move_to_end(key)
        self.cache[key] = value
        if len(self.cache) > self.capacity:
            self.cache.popitem(last=False)

    def invalidate_range(self, index):
        keys_to_remove = [
            key for key in self.cache.keys() if key[0] <= index <= key[1]
        ]
        for key in keys_to_remove:
            del self.cache[key]


def range_sum_no_cache(array, L, R):
    return sum(array[L:R + 1])


def update_no_cache(array, index, value):
    array[index] = value


class CachedArrayQueries:
    def __init__(self, array, cache_size = 1000):
        self.array = array.copy()
        self.cache = LRUCache(cache_size)

    def range_sum_with_cache(self, L, R):
        cached_result = self.cache.get((L, R))
        if cached_result is not None:
            return cached_result

        result = sum(self.array[L:R + 1])
        self.cache.put((L, R), result)
        return result

    def update_with_cache(self, index, value):
        self.array[index] = value
        self.cache.invalidate_range(index)


def generate_test_data(array_size, num_queries):
    array = [random.randint(1, 1000) for _ in range(array_size)]
    queries = []

    for _ in range(num_queries):
        if random.random() < 0.8:
            L = random.randint(0, array_size - 2)
            R = random.randint(L + 1, array_size - 1)
            queries.append(('Range', L, R))
        else:
            index = random.randint(0, array_size - 1)
            value = random.randint(1, 1000)
            queries.append(('Update', index, value))

    return array, queries


def run_performance_test():
    ARRAY_SIZE = 100_000
    NUM_QUERIES = 50_000
    CACHE_SIZE = 1000

    array, queries = generate_test_data(ARRAY_SIZE, NUM_QUERIES)

    start_time = time.time()
    test_array = array.copy()

    for query_type, *args in queries:
        if query_type == 'Range':
            L, R = args
            range_sum_no_cache(test_array, L, R)
        else:
            index, value = args
            update_no_cache(test_array, index, value)

    no_cache_time = time.time() - start_time

    # Тестування з кешем
    start_time = time.time()
    cached_queries = CachedArrayQueries(array, CACHE_SIZE)

    for query_type, *args in queries:
        if query_type == 'Range':
            L, R = args
            cached_queries.range_sum_with_cache(L, R)
        else:
            index, value = args
            cached_queries.update_with_cache(index, value)

    cache_time = time.time() - start_time

    # Виведення результатів
    print(f"Час виконання без кешування: {no_cache_time:.2f} секунд")
    print(f"Час виконання з LRU-кешем: {cache_time:.2f} секунд")
    print(f"Прискорення: {no_cache_time / cache_time:.2f}x")


if __name__ == "__main__":
    run_performance_test()