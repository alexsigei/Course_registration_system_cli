class Module:
    def __init__(self, module_id, course_id, name, pass_mark=50):
        self.module_id = module_id
        self.course_id = course_id
        self.name = name
        self.pass_mark = pass_mark

    def is_passed(self, score):
        return score >= self.pass_mark

    def to_dict(self):
        return {
            "module_id": self.module_id,
            "course_id": self.course_id,
            "name": self.name,
            "pass_mark": self.pass_mark
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            module_id=data["module_id"],
            course_id=data["course_id"],
            name=data["name"],
            pass_mark=data.get("pass_mark", 50)
        )

    def __str__(self):
        return f"{self.module_id}: {self.name}"