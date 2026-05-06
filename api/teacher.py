from fastapi import APIRouter, Depends, HTTPException, Query, Path
from database import get_db, Session
from schemas.teacher import TeacherInfo
from utils.log import logger
from dao.teacher import check_teachers, add_teacher, del_teacher, up_teacher

teacher_router = APIRouter()


# 查询老师信息
@teacher_router.get("/check_teacher",summary='查询老师信息接口')
def check_teacher(page_num: int = 1, page_size: int = 10, db: Session = Depends(get_db)):
    try:
        teacher = check_teachers(db=db, page_num=page_num, page_size=page_size)
        return {'message': '查询成功！', 'status_code': 200, 'data': teacher}
    except Exception as e:
        db.rollback()
        logger.error(e)
        raise HTTPException(status_code=500, detail=str(e))
    return {'message': '查询失败！', 'status_code': 501}


# 添加老师信息
@teacher_router.post("/add_teacher",summary='添加老师信息接口')
def post_teacher(data: TeacherInfo, db: Session = Depends(get_db)):
    data_dict = data.model_dump()
    try:
        teacher = add_teacher(db, data_dict)
        return teacher
    except Exception as e:
        db.rollback()
        logger.error(e)
        raise HTTPException(status_code=500, detail=str(e))


# 修改老师信息
@teacher_router.put("/update_teacher/{teacher_id}",summary='修改老师信息接口')
def update_teacher(data: TeacherInfo, teacher_id: int = Path(..., description='老师ID'), db: Session = Depends(get_db)):
    data_dict = data.model_dump()
    try:
        teacher = up_teacher(db, teacher_id, data_dict)
        return teacher
    except Exception as e:
        db.rollback()
        logger.error(e)
        raise HTTPException(status_code=500, detail=str(e))


# 删除老师信息
@teacher_router.delete("/delete_teacher/{teacher_id}",summary='删除老师信息接口')
def delete_teacher(teacher_id: int, db: Session = Depends(get_db)):
    try:
        teacher = del_teacher(db, teacher_id)
        return teacher
    except Exception as e:
        db.rollback()
        logger.error(e)
        raise HTTPException(status_code=500, detail=str(e))
