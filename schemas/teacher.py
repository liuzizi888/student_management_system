from datetime import datetime, date
from pydantic import BaseModel, Field, field_validator
from typing import Literal


class TeacherInfo(BaseModel):
    # 老师编号，整数类型
    # teacher_id: int = Field(ge=0, description='老师编号')

    # 老师名字，必填
    name: str = Field(..., min_length=2, max_length=20, description='老师名字')

    # 老师性别，男/女
    sex: Literal["男", "女"] = "男"

    # 老师生日，日期类型年月日
    birth: date = Field(..., description='老师生日')

    # 老师任教科目，java,Python,前端，大数据，人工智能，云计算，测试，运维，产品，UI
    subject: Literal['java', 'Python', '前端', '大数据', '人工智能', '云计算', '测试', '运维', '产品', 'UI'] = "java"

    # # 数据创建时间，年月日时分秒
    # create_time: datetime = Field(..., description='创建时间')
    #
    # # 数据更新时间，年月日时分秒
    # update_time: datetime = Field(..., description='更新时间')


# # 校验姓名格式是否正确
# @field_validator('name')
# def check_name(cls, v):
#     if len(v) < 2 or len(v) > 20:
#         raise ValueError('输入的值长度不符合规范，请输入长度在2~20的值')
#     return v

#
# # 校验任教科目，仅允许指定科目
# @field_validator('subject')
# def check_subject(cls, v):
#     if v not in ['java', 'Python', '前端', '大数据', '人工智能', '云计算', '测试', '运维', '产品', 'UI']:
#         raise ValueError('输入的值有误，请重新输入')
#     return v

#
# if __name__ == '__main__':
#     # 测试合法数据
#     valid_data = {
#         'teacher_id': 1001,
#         'name': '林晓楠',
#         'sex': '女',
#         'birth': date(1985, 3, 12),
#         'subject': '8989',
#         'create_time': datetime(2024, 1, 15, 9, 30, 0),
#         'update_time': datetime(2024, 1, 15, 9, 30, 0),
#         'del_fail': None
#     }
#     try:
#         teacher = TeacherInfo(**valid_data)
#         print('数据校验通过：', teacher.model_dump())  # Pydantic V2 里 .dict() 过期了，必须换成 .model_dump()
#     except ValueError as e:
#         print('数据校验失败：', e)
