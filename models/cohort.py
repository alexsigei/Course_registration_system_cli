from datetime import date


class Cohort:
    def __init__(
        self,
        cohort_id,
        course_id,
        name,
        capacity,
        start_date=None,
        end_date=None
    ):
        self.cohort_id = cohort_id
        self.course_id = course_id
        self.name = name
        self.capacity = capacity
        self.student_ids = []

        self.start_date = start_date
        self.end_date = end_date

    @property
    def seats_available(self):
        return self.capacity - len(self.student_ids)

    @property
    def is_full(self):
        return self.seats_available <= 0

    @property
    def status(self):
        """
        Determine the current lifecycle status of the cohort.
        """

        if not self.start_date or not self.end_date:
            return "UNSCHEDULED"

        today = date.today()

        start = date.fromisoformat(self.start_date)
        end = date.fromisoformat(self.end_date)

        if today < start:
            return "NOT_STARTED"

        if today > end:
            return "COMPLETED"

        return "IN_PROGRESS"

    @property
    def progress_percentage(self):
        """
        Calculate how far the cohort has progressed
        based on its start and end dates.
        """

        if not self.start_date or not self.end_date:
            return 0

        today = date.today()

        start = date.fromisoformat(self.start_date)
        end = date.fromisoformat(self.end_date)

        total_days = (end - start).days

        if total_days <= 0:
            return 100

        elapsed_days = (today - start).days

        if elapsed_days <= 0:
            return 0

        if elapsed_days >= total_days:
            return 100

        return round(
            (elapsed_days / total_days) * 100,
            1
        )

    def add_student(self, student_id):
        if self.is_full:
            raise ValueError("This cohort is full.")

        if self.status == "COMPLETED":
            raise ValueError(
                "This cohort has already completed."
            )

        if self.status == "IN_PROGRESS":
            raise ValueError(
                "Students cannot join a cohort that has already started."
            )

        if student_id in self.student_ids:
            raise ValueError(
                "Student is already enrolled in this cohort."
            )

        self.student_ids.append(student_id)

    def remove_student(self, student_id):
        if student_id in self.student_ids:
            self.student_ids.remove(student_id)

    def to_dict(self):
        return {
            "cohort_id": self.cohort_id,
            "course_id": self.course_id,
            "name": self.name,
            "capacity": self.capacity,
            "student_ids": self.student_ids,
            "start_date": self.start_date,
            "end_date": self.end_date
        }

    @classmethod
    def from_dict(cls, data):
        cohort = cls(
            cohort_id=data["cohort_id"],
            course_id=data["course_id"],
            name=data["name"],
            capacity=data["capacity"],
            start_date=data.get("start_date"),
            end_date=data.get("end_date")
        )

        cohort.student_ids = data.get("student_ids", [])

        return cohort

    def __str__(self):
        return (
            f"{self.name} - "
            f"{self.seats_available} seats available - "
            f"{self.status}"
        )