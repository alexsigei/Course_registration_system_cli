import json
from pathlib import Path

from models.course_enrollment import CourseEnrollment


DATA_DIR = Path(__file__).resolve().parent.parent / "data"

COURSES_FILE = DATA_DIR / "courses.json"
ENROLLMENTS_FILE = DATA_DIR / "course_enrollments.json"


class CourseEnrollmentService:
    def _load_courses(self):
        with open(COURSES_FILE, "r") as file:
            return json.load(file)

    def _load_enrollments(self):
        if not ENROLLMENTS_FILE.exists():
            return []

        with open(ENROLLMENTS_FILE, "r") as file:
            return json.load(file)

    def _save_enrollments(self, enrollments):
        with open(ENROLLMENTS_FILE, "w") as file:
            json.dump(enrollments, file, indent=4)

    def _course_exists(self, course_id):
        courses = self._load_courses()

        return any(
            course["course_id"] == course_id
            for course in courses
        )

    def is_enrolled(self, student_id, course_id):
        enrollments = self._load_enrollments()

        return any(
            enrollment["student_id"] == student_id
            and enrollment["course_id"] == course_id
            and enrollment.get("status", "active") == "active"
            for enrollment in enrollments
        )

    def enroll_student(self, student_id, course_id):
        if not self._course_exists(course_id):
            raise ValueError("Course does not exist.")

        if self.is_enrolled(student_id, course_id):
            raise ValueError(
                "Student is already enrolled in this course."
            )

        enrollments = self._load_enrollments()

        enrollment_number = len(enrollments) + 1
        enrollment_id = f"CENR{enrollment_number:03d}"

        enrollment = CourseEnrollment(
            enrollment_id=enrollment_id,
            student_id=student_id,
            course_id=course_id
        )

        enrollments.append(enrollment.to_dict())

        self._save_enrollments(enrollments)

        return enrollment

    def get_student_enrollments(self, student_id):
        enrollments = self._load_enrollments()

        return [
            CourseEnrollment.from_dict(enrollment)
            for enrollment in enrollments
            if enrollment["student_id"] == student_id
        ]

    def get_student_courses(self, student_id):
        courses = self._load_courses()
        enrollments = self.get_student_enrollments(student_id)

        course_ids = {
            enrollment.course_id
            for enrollment in enrollments
            if enrollment.status == "active"
        }

        return [
            course
            for course in courses
            if course["course_id"] in course_ids
        ]