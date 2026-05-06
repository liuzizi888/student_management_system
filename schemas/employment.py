from typing import List

from pydantic import BaseModel, Field, model_validator
from datetime import date, datetime


class Employment(BaseModel):
    # 学号：必填,正整数
    student_id: int = Field(..., description="学生编号")
    # 班级编名：正整数
    class_id: int = Field(..., description='班级编号')
    # 学生姓名：长度20位
    student_name: str = Field(max_length=20, description='学生姓名')
    # 学生班级编号：正整数
    class_code: int = Field(default=None, description='学生班级编号')
    # 就业开放时间：
    open_time: date = Field(default=None, description='就业开放时间')
    # offer下发时间：长度50位
    offer_time: date = Field(default=None, description='offer下发时间')
    # 就业公司：长度50位
    company: str = Field(default=None, max_length=50, description='就业公司')
    # 就业薪资：长度50位
    salary: float = Field(default=None, description='就业薪资')



    # @model_validator(mode='after')
    # def check_time(self):
    #     # 如果两个时间都不为空，才校验
    #     if self.open_time and self.offer_time:
    #         if self.offer_time <= self.open_time:
    #             raise ValueError("offer下发时间必须大于就业开放时间")
    #     return self
class StudentSalaryItem(BaseModel):
    student_id: int
    student_name: str
    class_id: int
    open_time: date
    company: str


# 2. 定义统一的响应包装（包含 message 和 data）
class CommonResponse(BaseModel):
    message: str
    data: List[StudentSalaryItem]