from fastapi import APIRouter, Depends, HTTPException, Query, Path, Request
from schemas.consultant import Cosulant
from database import get_db
from dao import consultant as consultant_dao
from utils.log import logger
from utils.decorator import auth

consultant_router = APIRouter()


@consultant_router.post("/add")
@auth(allow_role=["admin"])
async def add_consultant(request: Request, consultant: Cosulant, db=Depends(get_db), summary='增加顾问信息'):
    try:
        consultant_obj = consultant.dict()
        ret = consultant_dao.add_consultant(db, consultant_obj)
        if ret:
            return {'message': '增加成功！', 'status_code': 200}
    except Exception as e:
        logger.error(e)
        db.rollback()
        raise HTTPException(status_code=500, detail='增加失败' + str(e))
    return {'message': '增加失败，请检查dept_id的值是否存在!', 'status_code': 501}


@consultant_router.put("/update", summary='修改顾问信息')
@auth(allow_role=["admin"])
async def update_consultant(request: Request, consultant: Cosulant, consultant_id: int = Query(..., description="顾问ID"), db=Depends(get_db)):
    try:
        consultant_obj = consultant.dict()
        ret_count = consultant_dao.update_consultant(db, consultant_id, consultant_obj)
        if ret_count > 0:
            return {'message': '修改成功！', 'status_code': 200}
    except Exception as e:
        logger.error(e)
        db.rollback()
        raise HTTPException(status_code=500, detail='修改失败' + str(e))
    return {'message': '修改失败，请检查dept_id的值是否存在!', 'status_code': 501}


@consultant_router.delete("/{consultant_id}", summary='删除顾问信息')
@auth(allow_role=["admin"])
async def delete_consultant(request: Request, consultant_id: int = Path(..., description='顾问ID'), db=Depends(get_db)):
    try:
        ret = consultant_dao.delete_consultant(db, consultant_id)
        if ret:
            return {'message': '删除成功！', 'status_code': 200}
    except Exception as e:
        logger.error(e)
        db.rollback()
        raise HTTPException(status_code=500, detail='删除失败' + str(e))
    return {'message': '删除失败,请检查此数据是否还存在！', 'status_code': 501}


@consultant_router.get("/page/{page_size}/{page_num}", summary='查询顾问信息（分页）')
@auth(allow_role=["admin", "employee"])
async def query_department_page(request: Request, db=Depends(get_db), page_size: int = Path(..., description='显示的条数'),
                          page_num: int = Path(..., description='页数')):
    try:
        dep_list = consultant_dao.query_all(db, page_size, page_num)
        return {'message': '查询成功！', 'status_code': 200, 'data': dep_list}
    except Exception as e:
        logger.error(e)
        raise HTTPException(status_code=500, detail='查询失败' + str(e))
    return {'message': '查询失败！', 'status_code': 501}


