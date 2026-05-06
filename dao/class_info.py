from sqlalchemy.orm import Session
from models.class_info import ClassInfo
from datetime import datetime

def query_all(db:Session)->list:
    '''
    查询所有数据
    :param db: Session
    :return: list
    '''
    class_info =db.query(ClassInfo).filter(ClassInfo.del_flag != 'Y').all()
    return class_info

def query_limit(db:Session,skip:int=0,limit:int=10)->list:
    '''
    查询分页数据
    :param db: Session
    :param skip: int
    :param limit: int
    :return: list
    '''
    class_info = db.query(ClassInfo).order_by(ClassInfo.class_id).offset(skip).limit(limit).all()
    return class_info

def query_one(db:Session,class_id:int)->object:
    '''
    查询单个数据
    :param db: Session
    :param class_id: int
    :return:object
    '''
    class_info = db.query(ClassInfo).filter(ClassInfo.class_id == class_id,ClassInfo.del_flag != 'Y').first()
    return class_info

def put_class_info(db:Session,class_id:int, put_data_dict:dict) -> bool:
    '''
    修改数据
    :param db: Session
    :param class_id: int
    :param put_data_dict: dict
    :return:bool
    '''
    data_class=db.query(ClassInfo).filter(ClassInfo.class_id == class_id).first()
    if data_class:
        data_class.course_start_date = put_data_dict['course_start_date']
        data_class.is_homeroom_teacher = put_data_dict['is_homeroom_teacher']
        data_class.class_teacher = put_data_dict['class_teacher']
        data_class.update_time = datetime.now()
        db.commit()
        return True
    return False
def delete_class_info(db:Session,class_id:int) -> bool:
    '''
    删除数据
    :param db:Session
    :param class_id:int
    :return:bool
    '''
    data_class = db.query(ClassInfo).filter(ClassInfo.class_id == class_id,ClassInfo.del_flag != 'Y').first()
    if data_class:
        data_class.del_flag ='Y'
        db.commit()
        return True
    return False
def add_class_info(db:Session,add_data_dict:dict) -> bool:
    '''
    增加数据
    :param db: Session
    :param add_data_dict: dict
    :return: bool
    '''
    if add_data_dict:
        db.add(ClassInfo(class_id=add_data_dict['class_id']
                         ,course_start_date=add_data_dict['course_start_date']
                         ,is_homeroom_teacher=add_data_dict['is_homeroom_teacher']
                         ,class_teacher=add_data_dict['class_teacher']
                         ,create_time=datetime.now()
                         ,update_time=datetime.now()))
        db.commit()
        return True
    return False




