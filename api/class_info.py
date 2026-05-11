"""
班级信息管理接口模块

本模块提供班级信息的增删改查API接口，包括：
- 查询班级信息（支持全部、单条、分页）
- 修改班级信息
- 删除班级信息
- 新增班级信息
"""

from fastapi import APIRouter, Depends, HTTPException, Path, Query
from schemas.class_info import ClassInfo
from db.database import get_db
from utils.log import logger
from schemas import class_info
from dao import class_info

# 创建班级信息路由实例
class_router = APIRouter()


@class_router.get('/', summary='查询班级信息接口')
def get_class(
    db=Depends(get_db),
    class_id: int = Query(default=None, description='班级ID，不传则查询全部或分页'),
    skip: int = Query(default=None, description='查询起始条数'),
    limit: int = Query(default=None, description='查询条数')
):
    """
    查询班级信息
    
    支持三种查询模式：
    - 仅传 class_id：查询指定班级
    - 仅传 skip/limit：分页查询
    - 不传任何参数：查询所有班级
    
    参数:
        db: 数据库会话依赖注入
        class_id: 班级ID（可选），用于查询单个班级
        skip: 查询起始条数（可选），用于分页
        limit: 查询条数（可选），用于分页
    
    返回:
        包含查询结果的响应数据
    """
    try:
        # 查询单个班级
        if class_id is not None:
            result = class_info.query_one(db, class_id)
            if result:
                return {"message": '查询成功', 'status_code': 200, "data": result}
            return {"message": '未找到数据', "status_code": 404}
        
        # 分页查询
        if skip is not None and limit is not None:
            result = class_info.query_limit(db, skip, limit)
            if result:
                return {"message": '查询成功', 'status_code': 200, "data": result}
            return {"message": '查询失败', "status_code": 501}
        
        # 查询所有
        result = class_info.query_all(db)
        if result:
            return {"message": '查询成功', 'status_code': 200, "data": result}
        return {"message": '查询失败', "status_code": 501}
    except Exception as e:
        logger.error(e)
        raise HTTPException(status_code=500, detail='查询异常')


@class_router.put('/{class_id}', summary='修改班级信息接口')
def put_class(put_data: ClassInfo, class_id: int = Path(..., description='班级ID'), db=Depends(get_db)):
    """
    根据班级ID修改班级信息
    
    参数:
        put_data: 待修改的班级信息，包含班级名称、描述等字段
        class_id: 班级ID，通过路径参数传递
        db: 数据库会话依赖注入
    
    返回:
        修改操作结果消息
    """
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
    """
    根据班级ID删除班级信息
    
    参数:
        class_id: 班级ID，通过路径参数传递
        db: 数据库会话依赖注入
    
    返回:
        删除操作结果消息
    """
    try:
        if class_info.delete_class_info(db, class_id):
            return {"message": '删除成功'}
        else:
            return {"message": '未找到数据，删除失败'}
    except Exception as e:
        db.rollback()
        logger.error(e)
        raise HTTPException(status_code=404, detail='未找到数据，删除失败')


@class_router.post('/', summary='新增班级信息接口')
def add_class(add_data: ClassInfo, db=Depends(get_db)):
    """
    新增班级信息
    
    参数:
        add_data: 待新增的班级信息，包含班级名称、描述等必填字段
        db: 数据库会话依赖注入
    
    返回:
        新增操作结果消息
    """
    add_data_dict = add_data.model_dump()
    try:
        if class_info.add_class_info(db, add_data_dict):
            return {"message": '增加成功'}
    except Exception as e:
        db.rollback()
        logger.error(e)
        raise HTTPException(status_code=404, detail='增加失败')
