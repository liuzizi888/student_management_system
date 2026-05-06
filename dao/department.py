from sqlalchemy.orm import Session
from models.department import Department
from datetime import datetime


def add_department(db: Session, add_data: dict) -> bool:
    '''
    增加部门
    :param add_data:
    :param db: Session
    :param department: dict
    :return: bool
    '''
    #父部门不存在，不让增加
    if add_data['parent_id'] != 0:
        dep_obj = db.query(Department).filter(Department.department_id == add_data['parent_id'],
                                              Department.del_flag != 'Y').first()
        if dep_obj is None:
            return False

    add_data['create_time'] = datetime.now()
    department = Department(**add_data)
    db.add(department)
    db.commit()
    db.refresh(department)
    return True


def update_department(db: Session, department_id: int, update_data: dict) -> int:
    '''
    修改部门信息
    :param db: Session
    :param department_id:  int
    :param update_data: dict
    :return: int 返回修改的条数
    '''
    # 父部门不存在，不让增加
    if update_data['parent_id'] != 0:
        dep_obj = db.query(Department).filter(Department.department_id == update_data['parent_id'],
                                              Department.del_flag != 'Y').first()
        if dep_obj is None:
            return False

    update_data['update_time'] = datetime.now()
    update_count = db.query(Department).filter(Department.department_id == department_id).update(update_data)
    db.commit()
    return update_count


def delete_department(db: Session, department_id: int) -> bool:
    '''
    根据部门ID删除部门信息
    :param db: Session
    :param department_id: 部门ID
    :return: bool
    '''
    department = db.query(Department).filter(Department.department_id == department_id).first()
    if department:
        department.update_time = datetime.now()
        department.del_flag = 'Y'
        db.commit()
        return True
    return False


def query_all_dept(db: Session, dept_name: str, page_size: int = 10, page_num: int = 1) -> dict:
    '''
    查询所有部门信息（分页处理+总条数）
    :param db:Session
    :param page_size:10
    :param page_num:1
    :return:dict
    '''
    obj = db.query(Department).filter(Department.del_flag != 'Y').order_by(Department.update_time.desc())
    print(obj)
    if dept_name and dept_name.strip():
        obj = db.query(Department).filter(Department.del_flag != 'Y', Department.dept_name.like(f'%{dept_name}%')).order_by(Department.update_time.desc())

    total = obj.count()
    departments = obj.limit(
        page_size).offset((page_num - 1) * page_size).all()
    return {'total': total, 'data': departments}


def query_parent_dept(db: Session, parent_id: int) -> list:
    '''
    根据parent_id查询父节点部门
    :param parent_id: int
    :param db:Session
    :return:list
    '''
    departments = db.query(Department).filter(Department.del_flag != 'Y', Department.parent_id == parent_id).all()
    print(departments)
    return departments
