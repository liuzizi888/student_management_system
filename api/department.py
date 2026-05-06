from fastapi import APIRouter, Depends, HTTPException, Query, Path, Request
from schemas.department import Department
from database import get_db
from dao import department
from utils.log import logger
from utils.decorator import auth

department_router = APIRouter()


@department_router.post("/add", summary='增加部门信息')
@auth(allow_role=["admin"])
async def add_department(request: Request, dep: Department, db=Depends(get_db)):
    try:
        dep_obj = dep.dict()
        ret = department.add_department(db, dep_obj)
        if ret:
            return {'message': '增加成功！', 'status_code': 200}
    except Exception as e:
        logger.error(e)
        db.rollback()
        raise HTTPException(status_code=500, detail='增加失败' + str(e))
    return {'message': '增加失败,请检查parent_id字段是否存在!', 'status_code': 501}


@department_router.put("/update", summary='修改部门信息')
@auth(allow_role=["admin"])
async def update_department(request: Request, dep: Department, department_id: int = Query(..., description="部门ID"),
                            db=Depends(get_db)):
    try:
        dep_obj = dep.dict()
        ret_count = department.update_department(db, department_id, dep_obj)
        if ret_count > 0:
            return {'message': '修改成功！', 'status_code': 200}
    except Exception as e:
        logger.error(e)
        db.rollback()
        raise HTTPException(status_code=500, detail='修改失败' + str(e))
    return {'message': '修改失败，请检查parent_id字段是否存在!', 'status_code': 501}


@department_router.delete("/{department_id}", summary='删除部门信息')
@auth(allow_role=["admin"])
async def delete_department(request: Request, department_id: int = Path(..., description='部门ID'), db=Depends(get_db)):
    try:
        ret = department.delete_department(db, department_id)
        if ret:
            return {'message': '删除成功！', 'status_code': 200}
    except Exception as e:
        logger.error(e)
        db.rollback()
        raise HTTPException(status_code=500, detail='删除失败' + str(e))
    return {'message': '删除失败，请检查此数据是否还存在！', 'status_code': 501}


@department_router.get("/page/{page_size}/{page_num}", summary='查询部门信息（分页）')
@auth(allow_role=["admin", "employee"])
async def query_department_page(request: Request, dept_name: str | None = Query(None, description="部门名称（可选）"),
                                page_size: int = Path(..., description='显示的条数'),
                                page_num: int = Path(..., description='页数'), db=Depends(get_db)):
    try:
        dep_list = department.query_all_dept(db, dept_name, page_size, page_num)
        return {'message': '查询成功！', 'status_code': 200, 'data': dep_list}
    except Exception as e:
        logger.error(e)
        raise HTTPException(status_code=500, detail='查询失败' + str(e))
    return {'message': '查询失败！', 'status_code': 501}


@department_router.get('/query_parent', summary='查询父部门')
@auth(allow_role=["admin", "employee"])
async def query_parent(request: Request, parent_id: int = Query(0, description="父节点，不传默认查顶级 0"),
                       db=Depends(get_db)):
    try:
        dep_dict = department.query_parent_dept(db, parent_id)
        return {'message': '查询成功！', 'status_code': 200, 'data': dep_dict}
    except Exception as e:
        logger.error(e)
        raise HTTPException(status_code=500, detail='查询失败' + str(e))
    return {'message': '查询失败！', 'status_code': 501}
