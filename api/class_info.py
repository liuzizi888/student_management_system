from fastapi import APIRouter, Depends, HTTPException, Path, Query
from schemas.class_info import ClassInfo
from database import get_db
from utils.log import logger
from schemas import class_info
from dao import class_info

class_router = APIRouter()


@class_router.get('/get_class_all', summary='查询所有班级信息接口')
def get_class_all(db=Depends(get_db)):
    result = class_info.query_all(db)
    try:
        if result:
            return {"message": '查询成功', 'status_code': 200, "data": result}
    except Exception as e:
        logger.error(e)
        raise HTTPException(status_code=500, detail='未查询到信息')
    return {"message": '查询失败', "status_code": 501}


@class_router.get('/get_class_limit', summary='分页查询班级信息接口')
def get_class_limit(db=Depends(get_db), skip=Query(default=0,description='查询起始条数'), limiit=Query(default=10,description='查询条数')):
    result = class_info.query_limit(db, skip, limiit)
    try:
        if result:
            return {"message": '查询成功', 'status_code': 200, "data": result}
    except Exception as e:
        logger.error(e)
        raise HTTPException(status_code=500, detail='未查询到信息')
    return {"message": '查询失败', "status_code": 501}


@class_router.get('/{class_id}', summary='查询单个班级信息接口')
def get_class(class_id: int = Path(..., description='班级ID'), db=Depends(get_db)):
    result = class_info.query_one(db, class_id)
    try:
        if result:
            return {"message": '查询成功', 'status_code': 200, "data": result}
    except Exception as e:
        logger.error(e)
        raise HTTPException(status_code=500, detail='未查询到信息')
    return {"message": '查询失败', "status_code": 501}


@class_router.put('/{class_id}', summary='修改班级信息接口')
def put_class(put_data: ClassInfo, class_id: int = Path(..., description='班级ID'), db=Depends(get_db)):
    put_data_dict = put_data.model_dump()
    try:
        if class_info.put_class_info(db, class_id, put_data_dict):
            return {"message": '修改成功'}
    except Exception as e:
        db.rollback()
        logger.error(e)
        raise HTTPException(status_code=404, detail='未找到数据，删除失败')


@class_router.delete('/{class_id}', summary='删除班级信息接口')
def delete_class(class_id: int = Path(..., description='班级ID'), db=Depends(get_db)):
    try:
        if class_info.delete_class_info(db, class_id):
            return {"message": '删除成功'}
        else:
            return {"message": '未找到数据，删除失败'}
    except Exception as e:
        db.rollback()
        logger.error(e)
        raise HTTPException(status_code=404, detail='未找到数据，删除失败')


@class_router.post('/', summary='增加班级信息接口')
def add_class(add_data: ClassInfo, db=Depends(get_db)):
    add_data_dict = add_data.model_dump()
    try:
        if class_info.add_class_info(db, add_data_dict):
            return {"message": '增加成功'}
    except Exception as e:
        db.rollback()
        logger.error(e)
        raise HTTPException(status_code=404, detail='增加失败')
