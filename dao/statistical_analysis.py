from fastapi import Depends
from sqlalchemy import func
from sqlalchemy.sql.functions import count,min

from database import Session, get_db
from models.employment import Employment
from models.score import Score
from models.student import Student


def get_detail_over_30(db: Session):
    '''
    查询年龄大于30岁的学生信息
    :param db: Session
    :return: 查询结果
    '''
    result = db.query(Student).filter(Student.del_flag != 'Y', Student.age > 30).all()
    return result


def count_students1(db: Session):
    '''
    统计每个班级的⼈数以及男⽣⼥⽣的⼈数
    :param db:Session
    :return:统计结果
    '''
    class_count = db.query(Student.class_id, func.count(Student.student_id)).group_by(Student.class_id).all()
    gender_count = db.query(Student.gender, func.count(Student.student_id)).group_by(Student.gender).all()
    class_count1 = [{"班级编号": k, "班级人数": v} for k, v in class_count]
    gender_count1 = [{"性别": k, "人数": v} for k, v in gender_count]
    return {'班级人数统计': class_count1,
            '男女生人数统计': gender_count1
            }

# 成绩统计
# 5.查询每次考试成绩都在80分以上的学⽣的编号，姓名和成绩
def get_excellent_student(db: Session, result_list=None):
    excellent_student_ids = (db.query(Score.student_id).filter(Score.del_flag != 'Y').
                             group_by(Score.student_id).having(func.min(Score.score) >= 80).all())
    excellent_student_id = [x[0] for x in excellent_student_ids]
    print(f'{excellent_student_ids}')
    if not excellent_student_ids:
        return []
    results = (
        db.query(
            Student.student_id,
            Student.name,
            Score.score,
            Score.kaohe_rank
        ).join(Score, Student.student_id == Score.student_id).filter(
            Student.del_flag != "Y",
            Score.del_flag != "Y",
            Student.student_id.in_(excellent_student_id)).all())
    result = [{"student_id": lst[0], "name": lst[1], "score": lst[2],
               "kaohe_rank": lst[3]}
              for lst in results]
    return result

# 查询有两次以上不及格的学⽣的姓名，班级和不及格成绩
def get_excellent_1_student(db: Session):
    student_ids = (db.query(Score.student_id).filter(Score.del_flag != 'Y',Score.score < 60).
                   group_by(Score.student_id).having(func.count(Score.score)==2).all())
    student_id = [x[0] for x in student_ids]
    print(f'{student_ids}')
    if not student_ids:
        return []
    results = (db.query(Student.name,Student.class_id,Score.score).
              join(Score,Student.student_id == Score.student_id).filter(Student.del_flag != "Y",Score.del_flag != "Y",Student.student_id.in_(student_id),Score.score < 60))
    result = [{"name": lst[0], "class_id": lst[1], "score": lst[2]} for lst in results]
    return result
# 统计每次考试每个班级的平均分，按照从⾼到低排序
def get_excellent_2_student(db: Session):
    results = db.query(Student.class_id,func.avg(Score.score)).join(Score).group_by(Student.class_id).order_by(func.avg(Score.score).desc()).all()
    result = [{"class_id": lst[0], "avg(Score.score)": lst[1]} for lst in results]
    return result


# 统计就业薪资最⾼的前五名学⽣的姓名，班级和就业时间，就业公司
def student_salary(db: Session = Depends(get_db)):
    stu_salary = db.query(
        Employment.student_id,
        Employment.student_name,
        Employment.class_id,
        Employment.open_time,
        Employment.company
    ).filter(Employment.salary.isnot(None)).order_by(Employment.salary.desc()).limit(5).all()
    return stu_salary


# 统计每个学⽣的就业时⻓（offer下发时间-就业开放时间）
def employ_times(db: Session = Depends(get_db)):
    query = db.query(
        Employment,
        (Employment.offer_time - Employment.open_time)
    ).all()

    emp_list = []
    for row in query:
        employment_obj = row[0]
        dateDay = row[1]
        obj = {'employment': employment_obj, 'dateDay': dateDay}
        emp_list.append(obj)
    return emp_list


# 统计每个班级的平均就业时⻓（只统计进⼊就业阶段的学⽣，也就是有就业开放时间）
def employ_avg_time(db: Session = Depends(get_db)):
    query = db.query(
        Employment.class_id,
        func.avg(Employment.offer_time - Employment.open_time)
    ).filter(
        Employment.open_time.isnot(None)
    ).group_by(
        Employment.class_id
    ).all()

    emp_list = []
    for row in query:
        class_id = row[0]
        avg_data = row[1]
        obj = {'class_id': class_id, 'avg_data': avg_data}
        emp_list.append(obj)
    return emp_list

