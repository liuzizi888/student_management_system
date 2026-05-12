from pydantic import BaseModel, Field, validator
from datetime import date, datetime


class ClassInfo(BaseModel):
    # '班级编号':int,必填
    class_id: int = Field(..., description="班级编号")
    #'课程开始时间':data,必填
    course_start_date: date = Field(..., description="课程开始时间")
    #'班主任': str,字符串长度小于等于20,必填
    is_homeroom_teacher: str = Field(..., min_length=1, max_length=20, description="班主任")
    #'授课老师': str,字符串长度小于等于20,必填
    class_teacher: str = Field(..., min_length=1, max_length=20, description="授课老师")


    # ==================== 自定义校验：课程开始时间不能超过当前日期 ====================
    @validator('course_start_date')
    def course_start_date_validator(cls, value):
        if value <= date.today():
            return value
        raise ValueError('课程开始时间不能晚于今天')
