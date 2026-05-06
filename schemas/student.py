from pydantic import BaseModel,Field,validator
from datetime import date,datetime


class Student(BaseModel):
    # student_id:int = Field(...,description='学生编号')
    class_id: int = Field(description='班级编号')
    name: str = Field(max_length=50,description='学生名')
    origin: str = Field(description='籍贯')
    school: str = Field(description='毕业学校')
    major: str = Field(description='专业')
    entry_time: date=Field(description='入学日期')
    graduate_time: date=Field(description='毕业日期')
    degree: str = Field(description='学历')
    consultant_id: str= Field(description='顾问编号')
    age: int = Field(ge=0,le=100,description='年龄')
    gender: str = Field(description='性别')

class Student_Request(BaseModel):
    # student_id: int = Field(..., description='学生编号')
    class_id: int = Field(description='班级编号')
    name: str = Field(max_length=50, description='学生名')
    origin: str = Field(description='籍贯')
    school: str = Field(description='毕业学校')
    major: str = Field(description='专业')
    entry_time: date = Field(description='入学日期')
    graduate_time: date = Field(description='毕业日期')
    degree: str = Field(description='学历')
    consultant_id: str = Field(description='顾问编号')
    age: int = Field(ge=0, le=100, description='年龄')
    gender: str = Field(description='性别')

