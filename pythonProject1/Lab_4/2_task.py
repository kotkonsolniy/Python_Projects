import pickle

class TreeNode:
    def __init__(self, key):
        self.left = None
        self.right = None
        self.val = key

class BinarySearchTree:
    def __init__(self):
        self.root = None

    def insert(self, key):
        if self.root is None:
            self.root = TreeNode(key)
        else:
            self._insert_recursive(self.root, key)

    def _insert_recursive(self, node, key):
        if key < node.val:
            if node.left is None:
                node.left = TreeNode(key)
            else:
                self._insert_recursive(node.left, key)
        else:
            if node.right is None:
                node.right = TreeNode(key)
            else:
                self._insert_recursive(node.right, key)

    def search(self, key):
        return self._search_recursive(self.root, key)

    def _search_recursive(self, node, key):
        if node is None or node.val == key:
            return node
        if key < node.val:
            return self._search_recursive(node.left, key)
        return self._search_recursive(node.right, key)

    def delete(self, key):
        self.root = self._delete_recursive(self.root, key)

    def _delete_recursive(self, node, key):
        if node is None:
            return node

        if key < node.val:
            node.left = self._delete_recursive(node.left, key)
        elif key > node.val:
            node.right = self._delete_recursive(node.right, key)
        else:
            if node.left is None:
                return node.right
            elif node.right is None:
                return node.left

            temp = self._min_value_node(node.right)
            node.val = temp.val
            node.right = self._delete_recursive(node.right, temp.val)

        return node

    def _min_value_node(self, node):
        current = node
        while current.left is not None:
            current = current.left
        return current

    def inorder_traversal(self):
        result = []
        self._inorder_traversal_recursive(self.root, result)
        return result

    def _inorder_traversal_recursive(self, node, result):
        if node:
            self._inorder_traversal_recursive(node.left, result)
            result.append(node.val)
            self._inorder_traversal_recursive(node.right, result)

    def clear(self):
        self.root = None

    def dump(self, filename):
        with open(filename, 'wb') as file:
            pickle.dump(self.root, file)

    def load(self, filename):
        with open(filename, 'rb') as file:
            self.root = pickle.load(file)

def main():
    bst = BinarySearchTree()

    while True:
        command = input("Введите команду (add X, find X, delete X, print, clear, dump, load, exit): ").strip().split()

        if command[0] == "add":
            if len(command) != 2:
                print("Неверный формат команды. Используйте: add X")
                continue
            try:
                key = int(command[1])
                bst.insert(key)
                print(f"Элемент {key} добавлен в дерево.")
            except ValueError:
                print("Неверный формат числа.")

        elif command[0] == "find":
            if len(command) != 2:
                print("Неверный формат команды. Используйте: find X")
                continue
            try:
                key = int(command[1])
                if bst.search(key):
                    print(f"Элемент {key} найден в дереве.")
                else:
                    print(f"Элемент {key} не найден в дереве.")
            except ValueError:
                print("Неверный формат числа.")

        elif command[0] == "delete":
            if len(command) != 2:
                print("Неверный формат команды. Используйте: delete X")
                continue
            try:
                key = int(command[1])
                bst.delete(key)
                print(f"Элемент {key} удален из дерева.")
            except ValueError:
                print("Неверный формат числа.")

        elif command[0] == "print":
            if bst.root is None:
                print("Дерево пустое.")
            else:
                print("Элементы дерева в отсортированном порядке:", bst.inorder_traversal())

        elif command[0] == "clear":
            bst.clear()
            print("Дерево очищено.")

        elif command[0] == "dump":
            filename = input("Введите имя файла для сохранения: ").strip()
            bst.dump(filename)
            print(f"Дерево сохранено в файл {filename}.")

        elif command[0] == "load":
            filename = input("Введите имя файла для загрузки: ").strip()
            try:
                bst.load(filename)
                print(f"Дерево загружено из файла {filename}.")
            except FileNotFoundError:
                print(f"Файл {filename} не найден.")

        elif command[0] == "exit":
            print("Завершение работы программы.")
            break

        else:
            print("Неизвестная команда. Доступные команды: add, find, delete, print, clear, dump, load, exit.")

if __name__ == "__main__":
    main()