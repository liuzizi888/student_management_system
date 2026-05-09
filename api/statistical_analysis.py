from fastapi import APIRouter, Depends, HTTPException

from dao.statistical_analysis import student_salary, employ_times, employ_avg_time
from db.database import get_db, Session
from dao import statistical_analysis
from schemas.employment import CommonResponse, StudentSalaryItem
from utils.log import logger

analysis_router = APIRouter()



# 查询所有超过30岁的学生
@analysis_router.get("/age/over30",summary = '查询所有超过30岁的学生')
def get_students_over_30(db=Depends(get_db)):
    result1 = statistical_analysis.get_detail_over_30(db)
    return {
        "message": "查询成功",
        "status_code": 200,
        "data":result1
    }

# 统计每个班级的⼈数以及男⽣⼥⽣的⼈数
@analysis_router.get("/count",summary = '统计每个班级的⼈数以及男⽣⼥⽣的⼈数')
def count_students(db=Depends(get_db)):
    count1= statistical_analysis.count_students1(db)
    return {
        "message": "查询成功",
        "status_code": 200,
        "data": count1
    }

# 查询每次考试成绩都在80分以上的学生
@analysis_router.get('/score/excellent',summary='查询80+的学生')
def get_student(db = Depends(get_db)):
    try:
        result=statistical_analysis.get_excellent_student(db)
        if result:
            return {"message": "查询成功",'status_code':200,'data':result}
    except Exception as e:
            logger.error(e)
            raise HTTPException(status_code=500, detail=str(e))
    return {'message': '查询失败！,无符合要求的数据', 'status_code': 501}

# 查询有两次以上不及格的学⽣的姓名，班级和不及格成绩
@analysis_router.get('/score/excellent_1',summary='查询有两次以上不及格的学⽣的姓名，班级和不及格成绩')
def get_1_student(db = Depends(get_db)):
    try:
        result=statistical_analysis.get_excellent_1_student(db)
        if result:
            return {"message": "查询成功",'status_code':200,'data':result}
    except Exception as e:
            logger.error(e)
            raise HTTPException(status_code=500, detail=str(e))
    return {'message': '查询失败！,无符合要求的数据', 'status_code': 501}

# 统计每次考试每个班级的平均分，按照从⾼到低排序
@analysis_router.get('/score/excellent_2',summary='统计每次考试每个班级的平均分，按照从⾼到低排序')
def get_2_student(db = Depends(get_db)):
    try:
        result=statistical_analysis.get_excellent_2_student(db)
        if result:
            return {"message": "查询成功",'status_code':200,'data':result}
    except Exception as e:
            logger.error(e)
            raise HTTPException(status_code=500, detail=str(e))
    return {'message': '查询失败！,无符合要求的数据', 'status_code': 501}

@analysis_router.get("/top_salary", response_model=CommonResponse,summary='统计就业薪资最⾼的前五名学⽣的姓名，班级和就业时间，就业公司')
def get_top_salary(limit: int = 5, db: Session = Depends(get_db)):
    try:
        raw_data = student_salary(db)
        formatted_data = []
        for item in raw_data:
            formatted_data.append(StudentSalaryItem(
                student_id=item[0],
                student_name=item[1],
                class_id=item[2],
                open_time=item[3],
                company=item[4]
            ))
        return CommonResponse(message="查询成功", data=formatted_data)
    except Exception as e:
        db.rollback()
        logger.error(f"查询薪资失败: {e}")
        raise HTTPException(status_code=500, detail="内部服务器错误")


@analysis_router.get("/employ_time",summary='统计每个学⽣的就业时⻓（offer下发时间-就业开放时间）')
def employ_student_time(db: Session = Depends(get_db)):
    try:
        raw_data = employ_times(db)
        return raw_data
    except Exception as e:
        db.rollback()
        logger.error(f"查询时长失败: {e}")
        raise HTTPException(status_code=500, detail="内部服务器错误")


@analysis_router.get("/avg_time",summary='统计每个班级的平均就业时⻓（只统计进⼊就业阶段的学⽣，也就是有就业开放时间）')
def employ_avg_times(db: Session = Depends(get_db)):
    try:
        raw_data = employ_avg_time(db)
        return raw_data
    except Exception as e:
        db.rollback()
        logger.error(f"查询平均时长失败: {e}")
        raise HTTPException(status_code=500, detail="内部服务器错误")