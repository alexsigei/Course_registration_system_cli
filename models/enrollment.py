class Enrollment:
    # Allowed enrollment statuses
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
        # Store enrollment details
        self.enrollment_id = enrollment_id
        self.student_id = student_id
        self.module_id = module_id
        self.cohort_id = cohort_id
        self.status = status

        # Validate enrollment status
        if status not in self.VALID_STATUSES:
            raise ValueError("Invalid enrollment status.")

    def complete(self):
        # Mark enrollment as completed
        self.status = "completed"

    def fail(self):
        # Mark enrollment as failed
        self.status = "failed"

    def withdraw(self):
        # Mark enrollment as withdrawn
        self.status = "withdrawn"

    def to_dict(self):
        # Convert enrollment to dictionary
        return {
            "enrollment_id": self.enrollment_id,
            "student_id": self.student_id,
            "module_id": self.module_id,
            "cohort_id": self.cohort_id,
            "status": self.status
        }

    @classmethod
    def from_dict(cls, data):
        # Create enrollment from dictionary
        return cls(
            enrollment_id=data["enrollment_id"],
            student_id=data["student_id"],
            module_id=data["module_id"],
            cohort_id=data["cohort_id"],
            status=data.get("status", "active")
        )

    def __str__(self):
        # Display enrollment information
        return (
            f"{self.student_id} → "
            f"{self.module_id} → "
            f"{self.cohort_id} "
            f"({self.status})"
        )
