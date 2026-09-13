class Result:
     # Represents the academic result recorded for one student enrollment.
     # The result stores the score, pass mark, calculated grade, and PASS/FAIL status.
    def __init__(self,result_id,student_id, module_id, enrollment_id,score,pass_mark=50):

        self.result_id = result_id
        self.student_id = student_id
        self.module_id = module_id
        self.enrollment_id = enrollment_id
        self.score = score
        self.pass_mark = pass_mark

        # Grade is calculated from the student's score when the Result object is created.
        self.grade = self.calculate_grade()

        # A student passes when their score reaches or exceeds the module pass mark.
        self.passed = self.score >= self.pass_mark

    def calculate_grade(self):
        # Grade boundaries used by the course registration system.
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
         # Convert the Result object into a dictionary so it can be stored in JSON.
         # The calculated grade and PASS/FAIL status are persisted with the result.
        return {
            "result_id": self.result_id,
            "student_id": self.student_id,
            "module_id": self.module_id,
            "enrollment_id": self.enrollment_id,
            "score": self.score,
            "pass_mark": self.pass_mark,
            "grade": self.grade,
            "passed": self.passed
        }

    @classmethod
    def from_dict(cls, data):
        # Rebuild a Result object from data loaded from the JSON storage file.
        # Grade and passed are recalculated by __init__ to keep the object consistent.
        return cls(
            result_id=data["result_id"],
            student_id=data["student_id"],
            module_id=data["module_id"],
            enrollment_id=data["enrollment_id"],
            score=data["score"],
            pass_mark=data.get("pass_mark", 50)
        )

    def __str__(self):
        # Provide a simple human-readable representation for displaying a result.
        status = "PASS" if self.passed else "FAIL"


        return (
            f"{self.student_id} - "
            f"{self.module_id}: "
            f"{self.score}% ({self.grade}) - {status}"
        )