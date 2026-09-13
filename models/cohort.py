class Cohort:
    def __init__(
        self,
        cohort_id,
        module_id,
        name,
        capacity
    ):
        self.cohort_id = cohort_id
        self.module_id = module_id
        self.name = name
        self.capacity = capacity
        self.student_ids = []

    @property
    def seats_available(self):
        return self.capacity - len(self.student_ids)

    @property
    def is_full(self):
        return self.seats_available <= 0

    def add_student(self, student_id):
        if self.is_full:
            raise ValueError("This cohort is full.")

        if student_id in self.student_ids:
            raise ValueError("Student is already enrolled in this cohort.")

        self.student_ids.append(student_id)

    def remove_student(self, student_id):
        if student_id in self.student_ids:
            self.student_ids.remove(student_id)

    def to_dict(self):
        return {
            "cohort_id": self.cohort_id,
            "module_id": self.module_id,
            "name": self.name,
            "capacity": self.capacity,
            "student_ids": self.student_ids
        }

    @classmethod
    def from_dict(cls, data):
        cohort = cls(
            cohort_id=data["cohort_id"],
            module_id=data["module_id"],
            name=data["name"],
            capacity=data["capacity"]
        )

        cohort.student_ids = data.get("student_ids", [])

        return cohort

    def __str__(self):
        return (
            f"{self.name} - "
            f"{self.seats_available} seats available"
        )