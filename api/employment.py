from fastapi import APIRouter, Depends, HTTPException
from schemas.employment import Employment
from db.database import get_db
from dao import employment as crud_employment
from utils.log import logger

employment_router = APIRouter()
from typing import Literal, Union  #限制参数传值


@employment_router.post('add', summary='增加就业信息接口')
def add_employment(employment: Employment, db=Depends(get_db)):
    '''
    :param employment:
    :param db:
    :return:
    '''
    try:
        employment_dump = employment.model_dump()
        if crud_employment.add(db, employment_dump):
            return {'message': '增加成功！', 'status_code': 200}
    except Exception as e:
        db.rollback()
        logger.error(e)
        raise HTTPException(status_code=500, detail=str(e))
    return {'message': '增加失败！', 'status_code': 501}


#查询学生就业信息 只能传 3 种固定值学生编号、就业公司、工资，有数据 → 返回成功 JSON 没数据 → 返回 404 错误
# @employment_router.get('query_by_type', summary='查询就业信息接口')
# def get_employment_by_id(key: Literal["学生编号", "就业公司", "工资"], value: Union[str, int],db=Depends(get_db)):
#     result = crud_employment.get_employment(db, key,value)
#     if result:
#         return {"message": '查询成功', 'status_code': 200, "data": result}
#     raise HTTPException(status_code=404, detail='查无此人')
#
#
# 修改学生就业信息 通过 employment_id 找到要修改的记录 传入新的信息覆盖旧信息 返回更新成功 / 失败
@employment_router.put('/{employment_id}', summary='修改就业信息接口')
def put_employment(employment_id: int, employment: Employment, db=Depends(get_db)):
    try:
        employment_dump = employment.model_dump()
        if crud_employment.put_employment(db, employment_id, employment_dump):
            return {"message": "更新成功", 'status_code': 200}
    except Exception as e:
        db.rollback()
        logger.error(e)
        raise HTTPException(status_code=500, detail=str(e))
    return {'message': '更新失败！', 'status_code': 501}


# 删除学生就业信息
@employment_router.delete('/{employment_id}', summary='删除就业信息接口')
def delete_employment(employment_id: int, db=Depends(get_db)):
    # 删除
    if crud_employment.delete_employment(db, employment_id):
        return {"message": '删除成功', 'status_code': 200}
    else:
        db.rollback()
        return {'message': '删除失败', 'status_code': 501}


@employment_router.get('/page', summary='分页查询就业信息接口')
async def page_show_offer(key: Literal["全部", "学生编号", "就业公司", "工资"], value: Union[str, int, None] = None,
                          page: int = 1, size: int = 5, db=Depends(get_db)):
    lists = crud_employment.page_display_offer_info(db, key, value, page, size)
    return {"message": '查询成功', 'status_code': 200, "data": lists if lists else []}
