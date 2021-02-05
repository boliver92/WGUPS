from wgups.ds.bst_node import BSTNode


class BinarySearchTree:

    def __init__(self, root=None):
        self.root = root

    def search_in_order(self, key):
        current_node = self.root
        while current_node is not None:
            if key == current_node.key:
                return current_node.value
            else:
                if key < current_node.key:
                    current_node = current_node.left_child
                else:
                    current_node = current_node.right_child
        return None

    def insert(self, node):
        if self.root is None:
            self.root = node
            return

        current_node = self.root
        while current_node is not None:
            if node.key < current_node.key:
                if current_node.left_child is None:
                    current_node.left_child = node
                    return
                else:
                    current_node = current_node.left_child
            if node.key > current_node.key:
                if current_node.right_child is None:
                    current_node.right_child = node
                    return
                else:
                    current_node = current_node.right_child

    def print_bst(self, current_node=None):

        if self.root is None:
            print("Root is none, BST Empty")
            return

        if current_node is None:
            current_node = self.root

        if current_node.left_child is not None:
            self.print_bst(current_node.left_child)

        print(f"{current_node.key} : {current_node.value}")

        if current_node.right_child is not None:
            self.print_bst(current_node.right_child)
