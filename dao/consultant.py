from sqlalchemy.orm import Session
from models.consultant import Consultant
from models.department import Department
from datetime import datetime


def add_consultant(db: Session, add_data: dict) -> bool:
    '''
    增加顾问
    :param add_data:
    :param db: Session
    :param department: dict
    :return: bool
    '''
    #部门存在才可增加
    if add_data['dept_id'] == 0:
        return False
    if add_data['dept_id']:
        print(db.query(Department).filter(Department.department_id == add_data['dept_id'],
                                          Department.del_flag != 'Y'))
        dep_obj = db.query(Department).filter(Department.department_id == add_data['dept_id'],
                                              Department.del_flag != 'Y').first()
        print(dep_obj)
        if dep_obj is None:
            return False

    add_data['create_time'] = datetime.now()
    consultant = Consultant(**add_data)
    db.add(consultant)
    db.commit()
    db.refresh(consultant)
    return True


def update_consultant(db: Session, consultant_id: int, update_data: dict) -> int:
    '''
    修改顾问
    :param consultant_id: int
    :param db: Session
    :param department_id:  int
    :param update_data: dict
    :return: int 返回修改的条数
    '''
    # 所传的部门存在才可修改
    if update_data['dept_id'] == 0:
        return False
    if update_data['dept_id']:
        dep_obj = db.query(Department).filter(Department.department_id == update_data['dept_id'],
                                              Department.del_flag != 'Y').first()
        if dep_obj is None:
            return False

    update_data['update_time'] = datetime.now()
    update_count = db.query(Consultant).filter(Consultant.consultant_id == consultant_id).update(update_data)
    db.commit()
    return update_count


def delete_consultant(db: Session, consultant_id: int) -> bool:
    '''
    根据顾问ID删除顾问信息
    :param db:
    :param consultant_id:
    :return:
    '''
    consultant = db.query(Consultant).filter(Consultant.consultant_id == consultant_id).first()
    if consultant:
        consultant.update_time = datetime.now()
        consultant.del_flag = 'Y'
        db.commit()
        return True
    return False


def query_all(db: Session, page_size: int = 10, page_num: int = 1) -> dict:
    '''
    查询所有顾问信息（分页处理,总条数）
    :param db:Session
    :param page_size:10
    :param page_num:1
    :return:dict
    '''
    obj = db.query(Consultant).filter(Consultant.del_flag != 'Y').order_by(
        Consultant.update_time.desc())
    total = obj.count()
    consultants = obj.limit(
        page_size).offset((page_num - 1) * page_size).all()
    return {'total': total, 'data': consultants}
