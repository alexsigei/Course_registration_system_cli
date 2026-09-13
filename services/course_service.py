from models.course import Course
from models.module import Module
from storage.json_storage import JSONStorage


class CourseService:
    def __init__(self, storage=None):
        self.storage = storage or JSONStorage()

        self.courses_file = "courses.json"
        self.modules_file = "modules.json"

    def _load_courses(self):
        data = self.storage.load(self.courses_file)

        return [
            Course.from_dict(course)
            for course in data
        ]

    def _save_courses(self, courses):
        data = [
            course.to_dict()
            for course in courses
        ]

        self.storage.save(self.courses_file, data)

    def _load_modules(self):
        data = self.storage.load(self.modules_file)

        return [
            Module.from_dict(module)
            for module in data
        ]

    def _save_modules(self, modules):
        data = [
            module.to_dict()
            for module in modules
        ]

        self.storage.save(self.modules_file, data)

    def get_courses(self):
        return self._load_courses()

    def get_course(self, course_id):
        courses = self._load_courses()

        for course in courses:
            if course.course_id == course_id:
                return course

        raise ValueError("Course not found.")

    def get_modules(self):
        return self._load_modules()

    def get_module(self, module_id):
        modules = self._load_modules()

        for module in modules:
            if module.module_id == module_id:
                return module

        raise ValueError("Module not found.")

    def get_modules_for_course(self, course_id):
        course = self.get_course(course_id)
        modules = self._load_modules()

        return [
            module
            for module in modules
            if module.module_id in course.module_ids
        ]

    def add_course(self, course_id, name, description=""):
        courses = self._load_courses()

        for course in courses:
            if course.course_id == course_id:
                raise ValueError(
                    "A course with this ID already exists."
                )

        course = Course(
            course_id=course_id,
            name=name,
            description=description
        )

        courses.append(course)

        self._save_courses(courses)

        return course

    def add_module(
        self,
        module_id,
        course_id,
        name,
        pass_mark=50
    ):
        courses = self._load_courses()
        modules = self._load_modules()

        for module in modules:
            if module.module_id == module_id:
                raise ValueError(
                    "A module with this ID already exists."
                )

        course = None

        for item in courses:
            if item.course_id == course_id:
                course = item
                break

        if course is None:
            raise ValueError("Course not found.")

        module = Module(
            module_id=module_id,
            course_id=course_id,
            name=name,
            pass_mark=pass_mark
        )

        modules.append(module)

        course.add_module(module_id)

        self._save_modules(modules)
        self._save_courses(courses)

        return module