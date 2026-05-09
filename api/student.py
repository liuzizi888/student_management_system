from fastapi import APIRouter, Depends, HTTPException
from schemas.student import Student
from db.database import get_db
from dao.student import add_student, get_detail, delete_student,put_student1
from utils.log import logger
from typing import Literal, Union

from schemas import student

student_router = APIRouter()


# 增加学生
@student_router.post('/students',summary='增加学生信息')
def add(student: Student, db=Depends(get_db)):
    try:
        student_obj = student.model_dump()
        add_student(db, student_obj)
        return {'message': '添加成功！', 'status_code': 200}
    except Exception as e:
        logger.error(e)
        db.rollback()
        raise HTTPException(status_code=500, detail='添加失败' + str(e))
    return {'message': '添加失败！', 'status_code': 501}


# 查询学生
@student_router.get('/students',summary='查询学生信息')
def get_student_by_type(key: Literal["编号", "姓名", "班级"], value: Union[str, int], db=Depends(get_db)):
    result = get_detail(db, key,value)
    if result:
        return {"message": '查询成功', 'status_code': 200, "data": result}
    raise HTTPException(status_code=404, detail='查无此人')


# 修改学生
@student_router.put('/students/{id}',summary='修改学生信息')
def put_student(id: int, student: student.Student_Request, db=Depends(get_db)):
    student_dict = student.model_dump()
    if put_student1(db, id, student_dict):
        return {"message": "更新成功", 'status_code': 200}
    else:
        db.rollback()
        logger.warning(id)
        return {"message": "更新失败"}


# 删除学生
@student_router.delete('/{student_id}',summary= '删除学生信息')
def delete_student1(student_id: int, db=Depends(get_db)):
    # 删除
    if delete_student(db, student_id):
        return {"message": '删除成功', 'status_code': 200}
    else:
        db.rollback()
        return {'message': '删除失败'}
