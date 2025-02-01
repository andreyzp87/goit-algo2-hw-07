from functools import lru_cache
import timeit
import matplotlib.pyplot as plt


class Node:
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.left = None
        self.right = None


class SplayTree:
    def __init__(self):
        self.root = None

    def rotate_right(self, x):
        y = x.left
        x.left = y.right
        y.right = x
        return y

    def rotate_left(self, x):
        y = x.right
        x.right = y.left
        y.left = x
        return y

    def splay(self, root, key):
        if root is None or root.key == key:
            return root

        if root.key > key:
            if root.left is None:
                return root
            if root.left.key > key:
                root.left.left = self.splay(root.left.left, key)
                root = self.rotate_right(root)
            elif root.left.key < key:
                root.left.right = self.splay(root.left.right, key)
                if root.left.right:
                    root.left = self.rotate_left(root.left)
            if root.left is None:
                return root
            return self.rotate_right(root)
        else:
            if root.right is None:
                return root
            if root.right.key > key:
                root.right.left = self.splay(root.right.left, key)
                if root.right.left:
                    root.right = self.rotate_right(root.right)
            elif root.right.key < key:
                root.right.right = self.splay(root.right.right, key)
                root = self.rotate_left(root)
            if root.right is None:
                return root
            return self.rotate_left(root)

    def insert(self, key, value):
        if self.root is None:
            self.root = Node(key, value)
            return

        self.root = self.splay(self.root, key)

        if self.root.key == key:
            self.root.value = value
            return

        new_node = Node(key, value)
        if self.root.key > key:
            new_node.right = self.root
            new_node.left = self.root.left
            self.root.left = None
        else:
            new_node.left = self.root
            new_node.right = self.root.right
            self.root.right = None
        self.root = new_node

    def search(self, key):
        if self.root is None:
            return None

        self.root = self.splay(self.root, key)
        if self.root.key == key:
            return self.root.value
        return None


@lru_cache(maxsize=None)
def fibonacci_lru(n):
    if n <= 1:
        return n
    return fibonacci_lru(n - 1) + fibonacci_lru(n - 2)


def fibonacci_splay(n, tree):
    result = tree.search(n)
    if result is not None:
        return result

    if n <= 1:
        tree.insert(n, n)
        return n

    result = fibonacci_splay(n - 1, tree) + fibonacci_splay(n - 2, tree)
    tree.insert(n, result)
    return result


def print_table(n_values, lru_times, splay_times):
    col_width = 20

    header = f"{'n':^{col_width}}{'LRU Cache Time (s)':^{col_width}}{'Splay Tree Time (s)':^{col_width}}"
    separator = "-" * (col_width * 3)

    print(header)
    print(separator)

    for n, lru, splay in zip(n_values, lru_times, splay_times):
        row = f"{n:^{col_width}}{lru:^{col_width}.8f}{splay:^{col_width}.8f}"
        print(row)

def main():
    n_values = range(0, 951, 50)
    lru_times = []
    splay_times = []

    tree = SplayTree()

    times_num = 1

    for n in n_values:
        lru_time = timeit.timeit(lambda: fibonacci_lru(n), number=times_num) / times_num
        splay_time = timeit.timeit(lambda: fibonacci_splay(n, tree), number=times_num) / times_num

        lru_times.append(lru_time)
        splay_times.append(splay_time)

        print(f"Completed measurements for n={n}")

    # Побудова графіка
    plt.figure(figsize=(12, 6))
    plt.plot(list(n_values), lru_times, 'b-', label='LRU Cache')
    plt.plot(list(n_values), splay_times, 'r-', label='Splay Tree')
    plt.xlabel('n (номер числа Фібоначчі)')
    plt.ylabel('Середній час виконання (секунди)')
    plt.title('Порівняння часу виконання обчислення чисел Фібоначчі')
    plt.legend()
    plt.grid(True)
    plt.savefig('fibonacci_comparison.png')
    plt.show()

    print("\nРезультати вимірювань:")
    print_table(n_values, lru_times, splay_times)


if __name__ == "__main__":
    main()