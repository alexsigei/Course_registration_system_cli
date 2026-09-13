class Result:
    def __init__(
        self,
        result_id,
        student_id,
        module_id,
        enrollment_id,
        score
    ):
        self.result_id = result_id
        self.student_id = student_id
        self.module_id = module_id
        self.enrollment_id = enrollment_id
        self.score = score

        self.grade = self.calculate_grade()
        self.passed = self.score >= 50

    def calculate_grade(self):
        if self.score >= 70:
            return "A"
        elif self.score >= 60:
            return "B"
        elif self.score >= 50:
            return "C"
        elif self.score >= 40:
            return "D"
        else:
            return "F"

    def to_dict(self):
        return {
            "result_id": self.result_id,
            "student_id": self.student_id,
            "module_id": self.module_id,
            "enrollment_id": self.enrollment_id,
            "score": self.score,
            "grade": self.grade,
            "passed": self.passed
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            result_id=data["result_id"],
            student_id=data["student_id"],
            module_id=data["module_id"],
            enrollment_id=data["enrollment_id"],
            score=data["score"]
        )

    def __str__(self):
        status = "PASS" if self.passed else "FAIL"

        return (
            f"{self.student_id} - "
            f"{self.module_id}: "
            f"{self.score}% ({self.grade}) - {status}"
        )