class CourseEnrollment:
    VALID_STATUSES = {
        "active",
        "completed",
        "withdrawn"
    }

    def __init__(
        self,
        enrollment_id,
        student_id,
        course_id,
        status="active"
    ):
        self.enrollment_id = enrollment_id
        self.student_id = student_id
        self.course_id = course_id
        self.status = status

        if status not in self.VALID_STATUSES:
            raise ValueError(
                "Invalid course enrollment status."
            )

    def complete(self):
        self.status = "completed"

    def withdraw(self):
        self.status = "withdrawn"

    def to_dict(self):
        return {
            "enrollment_id": self.enrollment_id,
            "student_id": self.student_id,
            "course_id": self.course_id,
            "status": self.status
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            enrollment_id=data["enrollment_id"],
            student_id=data["student_id"],
            course_id=data["course_id"],
            status=data.get("status", "active")
        )

    def __str__(self):
        return (
            f"{self.student_id} → "
            f"{self.course_id} "
            f"({self.status})"
        )