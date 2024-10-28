from mongoengine import Document, StringField, ReferenceField, ListField, IntField
from pydantic import BaseModel


class Student(Document):
    name = StringField(required=True)
    student_number = IntField()


class Course(Document):
    name = StringField(required=True)
    description = StringField()
    tags = ListField(StringField())
    students = ListField(ReferenceField(Student))


class CourseData(BaseModel):
    name: str
    description: str | None
    tags: list[str] | None
    students: list[str] | None


class StudentData(BaseModel):
    name: str
    student_number: int | None
