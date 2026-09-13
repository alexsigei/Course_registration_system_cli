class Enrollment:
    VALID_STATUSES = {
        "active",
        "completed",
        "failed",
        "withdrawn"
    }

    def __init__(
        self,
        enrollment_id,
        student_id,
        module_id,
        cohort_id,
        status="active"
    ):
        self.enrollment_id = enrollment_id
        self.student_id = student_id
        self.module_id = module_id
        self.cohort_id = cohort_id
        self.status = status

        if status not in self.VALID_STATUSES:
            raise ValueError("Invalid enrollment status.")

    def complete(self):
        self.status = "completed"

    def fail(self):
        self.status = "failed"

    def withdraw(self):
        self.status = "withdrawn"

    def to_dict(self):
        return {
            "enrollment_id": self.enrollment_id,
            "student_id": self.student_id,
            "module_id": self.module_id,
            "cohort_id": self.cohort_id,
            "status": self.status
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            enrollment_id=data["enrollment_id"],
            student_id=data["student_id"],
            module_id=data["module_id"],
            cohort_id=data["cohort_id"],
            status=data.get("status", "active")
        )

    def __str__(self):
        return (
            f"{self.student_id} → "
            f"{self.module_id} → "
            f"{self.cohort_id} "
            f"({self.status})"
        )