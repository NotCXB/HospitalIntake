# Doctor Reporting Tree & Emergency Queue

## Running and testing

From the `HospitalIntake` directory, run `python -B -m unittest discover -v`.

Create the doctor tree root with `tree.insert(None, "Dr. Croft", "left")`.
Subsequent insertions use the parent's name and either `"left"` or `"right"`.
Insertion returns `False` for an invalid side, missing parent, or occupied child
position, leaving the tree unchanged. Traversals return lists of names; passing
`None` returns an empty list.

Patients require a string name and an integer urgency from 1 to 10.
`peek()` and `remove_min()` raise `IndexError` when the queue is empty.
Equal urgency scores have equal priority; their service order is unspecified.
`print_heap()` displays the internal heap order, which is not a fully sorted list.

This assignment simulates a medical management system built using non-linear data structures. Students will implement a custom binary tree to model a doctor reporting structure and a min-heap to manage patient urgency in an emergency room queue. These components provide practice in recursive methods, priority-based operations, and tree traversal techniques.

## Classes

### `DoctorNode` Class
Represents a doctor in the reporting hierarchy.

**Constructor**
```python
DoctorNode(name)
```

**Attributes**
- `name` (str): The doctor’s name.
- `left` (DoctorNode or None): Reference to the left report.
- `right` (DoctorNode or None): Reference to the right report.

### `DoctorTree` Class
Manages the binary tree structure of doctor reports.

**Constructor**
```python
DoctorTree()
```

**Attributes**
- `root` (DoctorNode or None): Reference to the root doctor.

**Methods**
- `insert(parent_name: str, employee_name: str, side: str) -> bool`
  - Adds a new doctor under a specified parent node on the given side.
- `preorder(node: DoctorNode) -> list`
  - Returns a list of doctor names using preorder traversal.
- `inorder(node: DoctorNode) -> list`
  - Returns a list of doctor names using inorder traversal.
- `postorder(node: DoctorNode) -> list`
  - Returns a list of doctor names using postorder traversal.

---

### `Patient` Class
Represents a patient waiting for emergency care.

**Constructor**
```python
Patient(name, urgency)
```

**Attributes**
- `name` (str): The patient’s name.
- `urgency` (int): A score from 1 to 10, where 1 is most urgent.

### `MinHeap` Class
Manages patients using a priority queue based on urgency.

**Constructor**
```python
MinHeap()
```

**Attributes**
- `data` (list): List of Patient instances. Index 0 is the most urgent patient.

**Methods**
- `insert(patient: Patient) -> None`
  - Adds a new patient and reorders the heap.
- `remove_min() -> Patient`
  - Removes and returns the most urgent patient.
- `peek() -> Patient`
  - Returns the most urgent patient without removing.
- `print_heap() -> None`
  - Prints each patient and their urgency level.
