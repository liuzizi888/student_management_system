from fastapi import APIRouter, Depends, HTTPException,Query
from schemas.student import Student
from db.database import get_db
from dao.student import add_student, get_detail_by_id,get_detail_with_pagination, delete_student,put_student1
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
# @student_router.get('/students',summary='查询学生信息')
# def get_student_by_type(key: Literal["编号", "姓名", "班级"], value: Union[str, int], db=Depends(get_db)):
#     result = get_detail(db, key,value)
#     if result:
#         return {"message": '查询成功', 'status_code': 200, "data": result}
#     raise HTTPException(status_code=404, detail='查无此人')

@student_router.get('/students', summary='查询学生信息')
def get_student_by_type(
        key: Literal["编号", "姓名", "班级"],
        value: Union[str, int],
        page: int = Query(1, ge=1, description="页码"),
        page_size: int = Query(10, ge=1, le=100, description="每页数量"),
        db=Depends(get_db)
):
    # 编号查询：返回单条，不分页
    if key == '编号':
        result = get_detail_by_id(db, value)
        if result:
            return {"message": '查询成功', 'status_code': 200, "data": result}
        raise HTTPException(status_code=404, detail='查无此人')

    # 姓名/班级查询：分页返回
    result, total = get_detail_with_pagination(db, key, value, page, page_size)
    if result:
        return {
            "message": '查询成功',
            'status_code': 200,
            "data": result,
            "pagination": {
                "page": page,
                "page_size": page_size,
                "total": total,
                "total_pages": (total + page_size - 1) // page_size
            }
        }
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
@student_router.delete('/students/{id}',summary= '删除学生信息')
def delete_student1(id: int, db=Depends(get_db)):
    # 删除
    if delete_student(db, id):
        return {"message": '删除成功', 'status_code': 200}
    else:
        db.rollback()
        return {'message': '删除失败'}
