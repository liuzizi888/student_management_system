from pydantic import BaseModel, Field, field_validator
from typing import Literal
from datetime import datetime, date


class Cosulant(BaseModel):
    name: str = Field(..., min_length=1, max_length=20, description='顾问姓名')
    gender: Literal['男', '女'] = '男'
    dept_id: int = Field(..., description='所属部门ID')
    position: str = Field(..., min_length=1, max_length=50, description='职位')
    phone: str = Field(default=None, pattern=r"^1[3-9]\d{9}$", description='联系电话')
    entry_date: datetime = Field(..., description='入职日期')
    status: Literal[1, 0] = 1  #'状态 1在职 0离职'
    remark: str = Field(..., min_length=1, max_length=255, description='备注')

    @field_validator('entry_date')
    def entry_date_before_tomorrow(cls, value: datetime):
        from datetime import timedelta
        tomorrow = date.today() + timedelta(days=1)

        if value.date() >= tomorrow:
            raise ValueError("入职日期必须少于明天")
        return value
