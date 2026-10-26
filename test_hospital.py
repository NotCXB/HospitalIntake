import io
import random
import unittest
from contextlib import redirect_stdout

from doctor_tree import DoctorNode, DoctorTree
from emergency_queue import MinHeap, Patient


class DoctorTreeTests(unittest.TestCase):
    def setUp(self):
        self.tree = DoctorTree()
        for parent, name, side in [
            (None, "Dr. Croft", "left"),
            ("Dr. Croft", "Dr. Phan", "left"),
            ("Dr. Croft", "Dr. Goldsmith", "right"),
            ("Dr. Phan", "Dr. Morgan", "left"),
            ("Dr. Phan", "Dr. Carson", "right"),
        ]:
            self.assertTrue(self.tree.insert(parent, name, side))

    def test_traversal_orders(self):
        self.assertEqual(self.tree.preorder(self.tree.root), [
            "Dr. Croft", "Dr. Phan", "Dr. Morgan", "Dr. Carson", "Dr. Goldsmith"])
        self.assertEqual(self.tree.inorder(self.tree.root), [
            "Dr. Morgan", "Dr. Phan", "Dr. Carson", "Dr. Croft", "Dr. Goldsmith"])
        self.assertEqual(self.tree.postorder(self.tree.root), [
            "Dr. Morgan", "Dr. Carson", "Dr. Phan", "Dr. Goldsmith", "Dr. Croft"])

    def test_empty_and_single_node_traversals(self):
        tree = DoctorTree()
        self.assertIsNone(tree.root)
        for traversal in (tree.preorder, tree.inorder, tree.postorder):
            self.assertEqual(traversal(tree.root), [])
            self.assertEqual(traversal(DoctorNode("Solo")), ["Solo"])

    def test_subtree_traversals(self):
        node = self.tree.root.left
        self.assertEqual(self.tree.preorder(node), ["Dr. Phan", "Dr. Morgan", "Dr. Carson"])
        self.assertEqual(self.tree.inorder(node), ["Dr. Morgan", "Dr. Phan", "Dr. Carson"])
        self.assertEqual(self.tree.postorder(node), ["Dr. Morgan", "Dr. Carson", "Dr. Phan"])

    def test_invalid_insertions_preserve_tree(self):
        before = self.tree.preorder(self.tree.root)
        for parent, side in [("Missing", "left"), ("Dr. Phan", "up"),
                             ("Dr. Phan", "left"), (None, "right")]:
            with self.subTest(parent=parent, side=side):
                self.assertFalse(self.tree.insert(parent, "New", side))
                self.assertEqual(self.tree.preorder(self.tree.root), before)

    def test_empty_tree_rejects_missing_parent_and_invalid_side(self):
        tree = DoctorTree()
        self.assertFalse(tree.insert("Missing", "New", "left"))
        self.assertFalse(tree.insert(None, "New", "up"))
        self.assertIsNone(tree.root)

    def test_insert_finds_parent_in_right_subtree(self):
        self.assertTrue(self.tree.insert("Dr. Goldsmith", "New", "right"))
        self.assertEqual(self.tree.root.right.right.name, "New")

    def test_one_sided_tree(self):
        tree = DoctorTree()
        tree.insert(None, "A", "left")
        tree.insert("A", "B", "left")
        tree.insert("B", "C", "left")
        self.assertEqual(tree.preorder(tree.root), ["A", "B", "C"])
        self.assertEqual(tree.inorder(tree.root), ["C", "B", "A"])
        self.assertEqual(tree.postorder(tree.root), ["C", "B", "A"])


class MinHeapTests(unittest.TestCase):
    def assert_heap_property(self, heap):
        for index in range(1, len(heap.data)):
            self.assertLessEqual(heap.data[(index - 1) // 2].urgency,
                                 heap.data[index].urgency)

    def test_patient_attributes_and_validation(self):
        patient = Patient("Riley", 2)
        self.assertEqual((patient.name, patient.urgency), ("Riley", 2))
        for urgency in (0, 11, -1):
            with self.assertRaises(ValueError):
                Patient("Riley", urgency)
        for urgency in (True, 1.5, "2", None):
            with self.assertRaises(TypeError):
                Patient("Riley", urgency)
        with self.assertRaises(TypeError):
            Patient(123, 2)

    def test_example_queue_and_peek(self):
        heap = MinHeap()
        jordan, taylor, avery = Patient("Jordan", 3), Patient("Taylor", 1), Patient("Avery", 5)
        for patient in (jordan, taylor, avery):
            heap.insert(patient)
        self.assertIs(heap.peek(), taylor)
        self.assertEqual(len(heap.data), 3)
        output = io.StringIO()
        with redirect_stdout(output):
            heap.print_heap()
        self.assertEqual(output.getvalue(), "Current Queue:\n- Taylor (1)\n- Jordan (3)\n- Avery (5)\n")
        self.assertIs(heap.remove_min(), taylor)
        output = io.StringIO()
        with redirect_stdout(output):
            heap.print_heap()
        self.assertEqual(output.getvalue(), "Current Queue:\n- Jordan (3)\n- Avery (5)\n")

    def test_empty_and_single_patient(self):
        heap = MinHeap()
        for operation in (heap.peek, heap.remove_min):
            with self.assertRaises(IndexError):
                operation()
        patient = Patient("Solo", 10)
        heap.insert(patient)
        self.assertIs(heap.remove_min(), patient)
        self.assertEqual(heap.data, [])
        heap.insert(patient)
        self.assertIs(heap.peek(), patient)

    def test_heap_property_and_removal_order(self):
        rng = random.Random(42)
        for scores in (list(range(1, 11)), list(range(10, 0, -1)),
                       [4] * 10, [rng.randint(1, 10) for _ in range(100)]):
            with self.subTest(scores=scores):
                heap = MinHeap()
                patients = [Patient(str(i), score) for i, score in enumerate(scores)]
                for patient in patients:
                    heap.insert(patient)
                    self.assert_heap_property(heap)
                removed = []
                while heap.data:
                    removed.append(heap.remove_min())
                    self.assert_heap_property(heap)
                self.assertEqual([p.urgency for p in removed], sorted(scores))
                self.assertCountEqual(removed, patients)

    def test_interleaved_insertions_and_removals(self):
        heap = MinHeap()
        for urgency in (5, 2, 8):
            heap.insert(Patient(str(urgency), urgency))
        self.assertEqual(heap.remove_min().urgency, 2)
        heap.insert(Patient("Critical", 1))
        self.assertEqual([heap.remove_min().urgency for _ in range(3)], [1, 5, 8])

    def test_invalid_insert_preserves_queue(self):
        heap = MinHeap()
        with self.assertRaises(TypeError):
            heap.insert("Not a patient")
        self.assertEqual(heap.data, [])

    def test_print_empty_queue(self):
        output = io.StringIO()
        with redirect_stdout(output):
            MinHeap().print_heap()
        self.assertEqual(output.getvalue(), "Current Queue:\n")


if __name__ == "__main__":
    unittest.main()
