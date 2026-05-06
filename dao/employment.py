from sqlalchemy.orm import Session
from models.employment import Employment
from datetime import datetime


# 定义一个名字叫 add 的函数
# db 是数据库连接对象（用来操作数据库） ：employment_ 是要添加的就业信息字典,,,
# 函数最后返回布尔值（成功 True / 失败 False）
def add(db: Session, employment_: dict) -> bool:
    employment_['creat_time'] = datetime.now()  # 往就业信息字典里加一个字段 creat_time（创建时间）
    employment_['update_time'] = datetime.now()  # datetime.now() = 获取当前系统时间
    employment = Employment(**employment_)
    db.add(employment)
    db.commit()
    return True


# 查询就业信息
# 定义函数：名字叫 get_employment 传入3个参数：db数据库连接、key查询类型、value查询值
def get_employment(db: Session, key, value):
    '''
    多条件查询学生就业信息
    :param db: Session
    :param key: 查询类目
    :param value: 查询类目下的值
    :return:查询结果
    '''
    if key == '学生编号':
        #去数据库里查 就业信息表（Employment）找到 学生 ID = 传入的 value并且 软删除标记 不等于 Y（即未删除）的 第一条数据
        result = db.query(Employment).filter(Employment.student_id == value, Employment.del_flag != 'Y').first()
    elif key == '就业公司':
        result = db.query(Employment).filter(Employment.company == value, Employment.del_flag != 'Y').all()
    else:  #工资范围
        result = db.query(Employment).filter(Employment.salary == value, Employment.del_flag != 'Y').all()
    return result


# 修改学生就业信息
def put_employment(db: Session, employment_id: int, employment: dict):
    '''
    修改学生信息
    :param db: Session
    :param employment_id: 编号
    :param student: 修改的学生信息
    :return: bool
    '''
    data_employment = db.query(Employment).filter(Employment.employment_id == employment_id).first()
    if data_employment:
        data_employment.student_id = employment.get("student_id")
        data_employment.class_id = employment.get("class_id")
        data_employment.student_name = employment.get("student_name")
        data_employment.class_code = employment.get("class_code")
        data_employment.open_time = employment.get("open_time")
        data_employment.offer_time = employment.get("offer_time")
        data_employment.company = employment.get("company")
        data_employment.salary = employment.get(" salary")
        data_employment.update_time = datetime.now()
        db.commit()
        return True
    return False


# 删除
def delete_employment(db: Session, employment_id: int):
    '''
    删除学生就业信息
    :param db: Session
    :param student_id:学生编号
    :return: bool
    '''
    employment = db.query(Employment).filter(Employment.employment_id == employment_id,
                                             Employment.del_flag != 'Y').first()
    if employment:
        employment.del_flag = 'Y'
        db.commit()
        return True
    return False


# 分页查询学生offer信息
def page_display_offer_info(db: Session, page: int, size: int):
    result = db.query(Employment).order_by(Employment.employment_id).offset((page - 1) * size).limit(size).all()
    return result
