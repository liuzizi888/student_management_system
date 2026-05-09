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
    # 确保 dept_id 是整数
    dept_id = int(add_data.get('dept_id', 0))
    
    #部门存在才可增加
    if dept_id == 0:
        return False
    
    dep_obj = db.query(Department).filter(
        Department.department_id == dept_id,
        Department.del_flag != 'Y'
    ).first()
    
    if dep_obj is None:
        return False

    # 只保留模型需要的字段
    consultant_data = {
        'name': add_data.get('name'),
        'gender': add_data.get('gender', '男'),
        'dept_id': dept_id,
        'position': add_data.get('position'),
        'phone': add_data.get('phone'),
        'entry_date': add_data.get('entry_date'),
        'status': int(add_data.get('status', 1)),
        'remark': add_data.get('remark'),
        'create_time': datetime.now(),
        'del_flag': '0'
    }
    
    consultant = Consultant(**consultant_data)
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
    # 确保 dept_id 是整数
    dept_id = int(update_data.get('dept_id', 0))
    
    # 所传的部门存在才可修改
    if dept_id == 0:
        return False
    
    dep_obj = db.query(Department).filter(
        Department.department_id == dept_id,
        Department.del_flag != 'Y'
    ).first()
    
    if dep_obj is None:
        return False

    # 只保留需要更新的字段
    update_fields = {
        'name': update_data.get('name'),
        'gender': update_data.get('gender'),
        'dept_id': dept_id,
        'position': update_data.get('position'),
        'phone': update_data.get('phone'),
        'entry_date': update_data.get('entry_date'),
        'status': int(update_data.get('status', 1)),
        'remark': update_data.get('remark'),
        'update_time': datetime.now()
    }
    
    update_count = db.query(Consultant).filter(
        Consultant.consultant_id == consultant_id
    ).update(update_fields)
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


def query_all(db: Session, consultant_name: str | None, page_size: int = 10, page_num: int = 1) -> dict:
    '''
    查询所有顾问信息（分页处理,总条数）
    :param db:Session
    :param consultant_name: 顾问姓名（模糊查询，可为None）
    :param page_size:10
    :param page_num:1
    :return:dict
    '''
    query = db.query(Consultant).filter(Consultant.del_flag != 'Y')
    
    if consultant_name:
        query = query.filter(Consultant.name.like('%' + consultant_name + '%'))
    
    obj = query.order_by(Consultant.update_time.desc())
    total = obj.count()
    consultants = obj.limit(page_size).offset((page_num - 1) * page_size).all()
    
    # 转换为字典列表，避免序列化 SQLAlchemy 关系对象时出错
    consultant_list = []
    for c in consultants:
        consultant_dict = {
            'consultant_id': c.consultant_id,
            'name': c.name,
            'gender': c.gender,
            'dept_id': c.dept_id,
            'position': c.position,
            'phone': c.phone,
            'entry_date': c.entry_date,
            'status': c.status,
            'remark': c.remark
        }
        consultant_list.append(consultant_dict)
    
    return {'total': total, 'data': consultant_list}
