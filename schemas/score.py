from pydantic import BaseModel,Field

# # 成绩创建/录入
class Score_add(BaseModel):
    student_id: int=Field(...)
    kaohe_rank: int = Field(..., gt=0,le=100,description='必填，正整数')
    score: int=Field(...,ge=0,description='必填，正整数')
# 外键关联学生   #成绩修改
class Score_update(BaseModel):
    student_id: int=Field(...)
    kaohe_rank: int = Field(..., gt=0,le=100,description='必填，正整数')
    score: int=Field(...,ge=0,description='必填，正整数')
