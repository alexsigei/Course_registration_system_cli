class Course:
    def __init__(self, course_id, name, description=""):
        self.course_id = course_id
        self.name = name
        self.description = description
        self.module_ids = []

    def add_module(self, module_id):
        if module_id not in self.module_ids:
            self.module_ids.append(module_id)

    def to_dict(self):
        return {
            "course_id": self.course_id,
            "name": self.name,
            "description": self.description,
            "module_ids": self.module_ids
        }

    @classmethod
    def from_dict(cls, data):
        course = cls(
            course_id=data["course_id"],
            name=data["name"],
            description=data.get("description", "")
        )

        course.module_ids = data.get("module_ids", [])

        return course

    def __str__(self):
        return f"{self.course_id}: {self.name}"