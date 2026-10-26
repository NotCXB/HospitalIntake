class Patient:
    def __init__(self, name, urgency):
        if not isinstance(name, str):
            raise TypeError("Patient name must be a string")
        if isinstance(urgency, bool) or not isinstance(urgency, int):
            raise TypeError("Urgency must be an integer")
        if not 1 <= urgency <= 10:
            raise ValueError("Urgency must be between 1 and 10")
        self.name = name
        self.urgency = urgency


class MinHeap:
    def __init__(self):
        self.data = []

    def heapify_up(self, index):
        while index > 0:
            parent = (index - 1) // 2
            if self.data[parent].urgency <= self.data[index].urgency:
                break
            self.data[parent], self.data[index] = self.data[index], self.data[parent]
            index = parent

    def heapify_down(self, index):
        while 2 * index + 1 < len(self.data):
            left = 2 * index + 1
            right = left + 1
            smaller = left
            if right < len(self.data) and self.data[right].urgency < self.data[left].urgency:
                smaller = right
            if self.data[index].urgency <= self.data[smaller].urgency:
                break
            self.data[index], self.data[smaller] = self.data[smaller], self.data[index]
            index = smaller

    def insert(self, patient):
        if not isinstance(patient, Patient):
            raise TypeError("The queue accepts Patient objects")
        self.data.append(patient)
        self.heapify_up(len(self.data) - 1)

    def print_heap(self):
        print("Current Queue:")
        for patient in self.data:
            print(f"- {patient.name} ({patient.urgency})")

    def peek(self):
        if not self.data:
            raise IndexError("Cannot peek at an empty queue")
        return self.data[0]

    def remove_min(self):
        if not self.data:
            raise IndexError("Cannot remove from an empty queue")
        patient = self.data[0]
        last = self.data.pop()
        if self.data:
            self.data[0] = last
            self.heapify_down(0)
        return patient
