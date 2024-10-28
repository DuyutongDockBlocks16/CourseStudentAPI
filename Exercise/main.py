from fastapi import FastAPI
from course_student_api import CourseStudentAPI


# 创建 FastAPI 实例
app = FastAPI()

# 创建 API 类实例
api = CourseStudentAPI()

# 注册路由
app.include_router(api.router)


# 注册数据库启动和关闭事件
@app.on_event("startup")
def on_startup():
    api.start_db()


@app.on_event("shutdown")
def on_shutdown():
    api.shutdown_db()
