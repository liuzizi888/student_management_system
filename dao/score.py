from sqlalchemy.orm import Session
from sqlalchemy import func
from models.score import Score
from datetime import datetime


def add_score(db: Session, score:dict)->bool:
    ''''
    1.按考核序次录⼊考核成绩
    db: Session
    score: dict
    return: bool
    '''
    # 这里查询数据库中是否已存在该学生该次考核的成绩
    existing_score = db.query(Score).filter(
Score.student_id == score.get('student_id'),
    Score.kaohe_rank == score.get('kaohe_rank')).first()
    if existing_score:
        raise Exception(f"录入失败：学号 {score.get('student_id')} 在该考核序次中已存在成绩记录，请勿重复录入")
    score['create_time'] = datetime.now()
    score['update_time'] = datetime.now()
    score_obj = Score(**score)
    db.add(score_obj)
    db.commit()
    db.refresh(score_obj)
    return True
def get_score(db: Session, student_id:int):
    '''
    2.获取获取某个学生所有成绩
    :param db:
    :param student_id:
    :return: Score
    '''
    print(db.query(Score).filter(Score.student_id== student_id,Score.del_flag!='Y'))
    get_student_scores = db.query(Score).filter(Score.student_id== student_id,Score.del_flag!='Y').all()
    if len(get_student_scores)>0:
        return get_student_scores
    return None
def update_score (
        db: Session,
        student_id: int,
        kaohe_rank: int,
        score_dict: dict)->bool:
    '''
    3. 修改指定学生的某次成绩（按 学生编号 + 考核序次）
    :param db:
    :param student_id:
    :param kaohe_rank:
    :param score_dict:
    :return: bool
    '''
    score_update = db.query(Score).filter(
        Score.student_id == student_id,
        Score.kaohe_rank == kaohe_rank,
        Score.del_flag!='Y').first()
    if score_update:
        score_update.score = score_dict.get("score")
        db.commit()
        return True
    return False

def delete_score(db: Session, student_id: int, kaohe_rank: int)->bool:
    '''
    4. 删除指定学生的某次成绩（按 学生编号 + 考核序次）    :param db:
    :param student_id:
    :param kaohe_rank:
    :return: bool
    '''
    score_del = db.query(Score).filter(
        Score.student_id == student_id,Score.kaohe_rank == kaohe_rank).first()
    if score_del:
        score_del.del_flag = 'Y'
        db.commit()
        return True
    return False



