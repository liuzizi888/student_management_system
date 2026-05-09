from sqlalchemy.orm import Session
from models.student import Student
from sqlalchemy import func
from datetime import date, datetime


# 增加学生
def add_student(db: Session, student: dict) -> bool:
    '''
    添加学生
    :param db: Session
    :param student: dict
    :return: bool
    '''
    student['create_time'] = datetime.now()
    student['update_time'] = datetime.now()
    student = Student(**student)
    db.add(student)
    db.commit()
    return True


# 查询学生
# def get_detail(db: Session, key, value):
#     '''
#     多条件查询学生信息
#     :param db: Session
#     :param key: 查询类目
#     :param value: 查询类目下的值
#     :return:查询结果
#     '''
#     if key == '编号':
#         result = db.query(Student).filter(Student.student_id == value, Student.del_flag != 'Y').all()
#     elif key == '姓名':
#         result = db.query(Student).filter(Student.name == value, Student.del_flag != 'Y').all()
#     else:
#         result = db.query(Student).filter(Student.class_id == value, Student.del_flag != 'Y').all()
#     return result

def get_detail_by_id(db: Session, student_id):
    """根据编号查询单个学生"""
    return db.query(Student).filter(
        Student.student_id == student_id,
        Student.del_flag != 'Y'
    ).first()


def get_detail_with_pagination(db: Session, key, value, page=1, page_size=10):
    """分页查询学生信息"""
    base_query = db.query(Student).filter(Student.del_flag != 'Y')

    if key == '姓名':
        base_query = base_query.filter(Student.name == value)
    else:
        base_query = base_query.filter(Student.class_id == value)

    total = base_query.count()
    offset = (page - 1) * page_size
    result = base_query.offset(offset).limit(page_size).all()

    return result, total


# 修改学生信息
def put_student1(db: Session, id: int, student: dict):
    '''
    修改学生信息
    :param db: Session
    :param id: 学生编号
    :param student: 修改的学生信息
    :return: bool
    '''
    data_student = db.query(Student).filter(Student.student_id == id).first()
    if data_student:
        data_student.name = student.get("name")
        data_student.age = student.get("age")
        data_student.gender = student.get("gender")
        data_student.origin = student.get("origin")
        data_student.degree = student.get("degree")
        data_student.school = student.get("school")
        data_student.major = student.get("major")
        data_student.class_id = student.get("class_id")
        data_student.consultant_id = student.get("consultant_id")
        data_student.entry_time = student.get("entry_time")
        data_student.graduate_time = student.get("graduate_time")
        data_student.update_time = datetime.now()
        db.commit()
        return True
    return False


# 删除学生
def delete_student(db: Session, id: int):
    '''
    删除学生信息
    :param db: Session
    :param id:学生编号
    :return: bool
    '''
    student = db.query(Student).filter(Student.student_id == id, Student.del_flag != 'Y').first()
    if student:
        student.create_time = datetime.now()
        student.del_flag = 'Y'
        db.commit()
        return True
    return False
