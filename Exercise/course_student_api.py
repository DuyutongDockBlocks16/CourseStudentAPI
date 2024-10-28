from fastapi import APIRouter
from typing import List, Optional
from mongoengine import connect, disconnect
import json
from utils.data_class import Student, Course, CourseData, StudentData
from utils.json_converter import course_convert_to_json, student_convert_to_json


class CourseStudentAPI:
    def __init__(self):
        self.router = APIRouter()
        self.setup_routes()

    def setup_routes(self):
        # 添加路由到 APIRouter 实例
        self.router.post("/courses", status_code=201, response_model=dict)(self.create_course)
        self.router.get("/courses", status_code=200, response_model=List[dict])(self.get_courses)
        self.router.get("/courses/{course_id}", status_code=200, response_model=dict)(self.get_course)
        self.router.put("/courses/{course_id}", status_code=200, response_model=dict)(self.update_course)
        self.router.delete("/courses/{course_id}", status_code=200)(self.delete_course)

        self.router.post("/students", status_code=201, response_model=dict)(self.create_student)
        self.router.get("/students/{student_id}", status_code=200, response_model=dict)(self.get_student)
        self.router.put("/students/{student_id}", status_code=200)(self.update_student)
        self.router.delete("/students/{student_id}", status_code=200)(self.delete_student)

    def start_db(self):
        connect("fast-api-database", host="mongodb://mongo", port=27017)

    def shutdown_db(self):
        disconnect("fast-api-database")

    def create_course(self, course: CourseData):
        new_course = Course(**course.dict()).save()
        return {"message": "Course successfully created", "id": str(new_course.id)}

    def get_courses(self, tag: Optional[str] = None, studentName: Optional[str] = None):
        param = {}
        if studentName:
            student_course = Student.objects(student__in=studentName)
            if student_course:
                param["id__in"] = [str(student.id) for student in student_course]
        if tag:
            param["tags__in"] = tag

        student_courses = Course.objects(**param).to_json()
        student_courses = json.loads(student_courses)
        return student_courses

    def get_course(self, course_id: str):
        retrieved_course = Course.objects.get(id=course_id)
        return course_convert_to_json(retrieved_course)

    def update_course(self, course_id: str, course: CourseData):
        Course.objects.get(id=course_id).update(**course.dict())
        return {"message": "Course successfully updated"}

    def delete_course(self, course_id: str):
        Course.objects(id=course_id).delete()
        return {"message": "Course successfully deleted"}

    def create_student(self, student_data: StudentData):
        add_student = Student(**student_data.dict()).save()
        return {"message": "Student successfully created", "id": str(add_student.id)}

    def get_student(self, student_id: str):
        read_students = Student.objects.get(id=student_id)
        return student_convert_to_json(read_students)

    def update_student(self, student_id: str, student: StudentData):
        Student.objects.get(id=student_id).update(**student.dict())
        return {"message": "Student successfully updated"}

    def delete_student(self, student_id: str):
        Student.objects(id=student_id).delete()
        return {"message": "Student successfully deleted"}
