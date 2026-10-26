class DoctorNode:
    def __init__(self, name):
        self.name = name
        self.left = None
        self.right = None


class DoctorTree:
    def __init__(self):
        self.root = None

    def insert(self, parent_name, employee_name, side):
        """Insert a report, or create the root using parent_name=None.

        Return False for an invalid side, missing parent, or occupied position.
        The side must be 'left' or 'right', including when creating the root.
        """
        if side not in ("left", "right"):
            return False
        if self.root is None:
            if parent_name is not None:
                return False
            self.root = DoctorNode(employee_name)
            return True

        parent = self._find(self.root, parent_name)
        if parent is None or getattr(parent, side) is not None:
            return False
        setattr(parent, side, DoctorNode(employee_name))
        return True

    def _find(self, node, name):
        if node is None or node.name == name:
            return node
        return self._find(node.left, name) or self._find(node.right, name)

    def preorder(self, node):
        """Return doctor names in root, left, right order."""
        if node is None:
            return []
        return [node.name] + self.preorder(node.left) + self.preorder(node.right)

    def inorder(self, node):
        """Return doctor names in left, root, right order."""
        if node is None:
            return []
        return self.inorder(node.left) + [node.name] + self.inorder(node.right)

    def postorder(self, node):
        """Return doctor names in left, right, root order."""
        if node is None:
            return []
        return self.postorder(node.left) + self.postorder(node.right) + [node.name]
