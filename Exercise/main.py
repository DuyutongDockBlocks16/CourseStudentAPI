from fastapi import FastAPI, HTTPException
from mongoengine import (
    connect,
    disconnect,
    Document,
    StringField,
    ReferenceField,
    ListField,
    IntField
)
import json
from pydantic import BaseModel

app = FastAPI()


@app.on_event("startup")
def startup_db_client():
    connect("fast-api-database", host="mongodb://mongo", port=27017)
    #connect("fast-api-database", host="localhost", port=27017)


@app.on_event("shutdown")
def shutdown_db_client():
    disconnect("fast-api-database")


# Helper functions to convert MongeEngine documents to json

def course_to_json(course):
    course = json.loads(course.to_json())
    course["students"] = list(map(lambda dbref: str(dbref["$oid"]), course["students"]))
    course["id"] = str(course["_id"]["$oid"])
    course.pop("_id")
    return course


def student_to_json(student):
    student = json.loads(student.to_json())
    student["id"] = str(student["_id"]["$oid"])
    student.pop("_id")
    return student

# Schema

class Student(Document):
    name = StringField(required=True)
    student_number = IntField()

class Course(Document):
    name = StringField(required=True)
    description = StringField()
    tags = ListField(StringField())
    students = ListField(ReferenceField(Student))
    

# Input Validators

class CourseData(BaseModel):
    name: str
    description: str | None
    tags: list[str] | None
    students: list[str] | None


class StudentData(BaseModel):
    name: str
    student_number: int | None

@app.post("/courses", status_code=201, response_model=dict)
def create_course(course: CourseData):
    c = Course(**course.dict()).save()
    return {"message": "Course successfully created", "id" : str(c.id)}
    

@app.get("/courses", status_code=200,response_model=list[dict])
def read_courses(tag: str|None, studentName:str|None):
    param={}
    if tag:
        param["tags__in"]=tag
    if studentName:
        student_course = Student.objects(student__in=studentName) 
        if student_course:  
            #studentList = [str(student.id) for student in student_course] 
            param["id__in"] =[str(student.id)for student in student_course]
    student_courses= Course.objects(**param).to_json()
    student_courses = json.loads(student_courses)
    return student_courses

@app.get("/courses/{course_id}", status_code=200, response_model=dict)
def read_course(course_id: str):
    try:
        p=Course.objects.get(id=course_id)
        return course_to_json(p)
    except Course.DoesNotExist:
        raise HTTPException(status_code=404, detail="Error")

@app.put("/courses/{course_id}", status_code=200,response_model=dict)
def update_course(course_id: str, course: CourseData):
    Course.objects.get(id=course_id).update(**course.dict())
    return {"message": "Course successfully updated"}

@app.delete("/courses/{course_id}", status_code=200)
def delete_course(course_id: str):
    Course.objects(id=course_id).delete()
    return {"message": "Course successfully deleted"}

@app.post("/students", status_code=201,response_model=dict)
def create_student(student_data: StudentData):
    add_student = Student(**student_data.dict()).save()
    return {"message":"Studentsuccessfully created", "id": str(add_student.id)} 

@app.get("/students/{student_id}", status_code=200,response_model=dict)
def read_student(student_id: str):
    try:
        read_students = Student.objects.get(id=student_id)
        return student_to_json(read_students)
    except Student.DoesNotExist:
        raise HTTPException(status_code=404, detail="Error")

@app.put("/students/{student_id}", status_code=200)
def update_student(student_id: str, student: StudentData):
    Student.objects.get(id=student_id).update(**student.dict())
    return {"message": "Student successfully updated"}

@app.delete("/students/{student_id}", status_code=200)
def delete_student(student_id: str):
    Student.objects(id=student_id).delete()
    return {"message": "Student successfully deleted"}