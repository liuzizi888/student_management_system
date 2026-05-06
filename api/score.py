from fastapi import APIRouter, Depends, HTTPException,Path,Query
# from scripts.regsetup import description

from database import get_db
from dao import score
from utils.log import logger
from sqlalchemy.orm import Session

from schemas.score import Score_add,Score_update

score_router = APIRouter()

# 1. 按考核序次录入成绩
@score_router.post('/score', summary='按考核序次录入成绩信息接口')
def create_score(score_obj: Score_add,db: Session = Depends(get_db)):
    try:
        score_dict = score_obj.model_dump()
        result=score.add_score(db=db,score=score_dict)
        if result:
            return {'message': '增加成功！','status_code':200,'data':result}
    except Exception as e:
        db.rollback()
        logger.error(e)
        raise HTTPException(status_code=500, detail=str(e))
    return {'message': '增加失败！','status_code':501}


#2.获取某个学生所有成绩
@score_router.get('/score/{student_id}', summary='获取某个学生所有成绩信息接口')
def get_score(student_id:int = Path(...,description='学生ID'),db: Session = Depends(get_db)):
    try:
        result=score.get_score(db,student_id)
        if result:
            return {'message': '查询成功','status_code':200,'data':result}
    except Exception as e:
        db.rollback()
        logger.error(e)
        raise HTTPException(status_code=500, detail=str(e))
    return {'message': '查询无数据','status_code':501}


# 3. 修改指定学生的某次成绩（按 学生编号 + 考核序次）
@score_router.put('/score/update', summary='修改指定学生的某次成绩（按 学生编号 + 考核序次）')
def put_score(score1:Score_update,student_id:int= Query(...,description='学生id'),kaohe_rank:int=Query(...,description='考核序次')
              ,db: Session = Depends(get_db)):
    try:
        score_dict = score1.model_dump()
        result=score.update_score(db, student_id,kaohe_rank, score_dict)
        if result:
            return {"message": "更新成功",'status_code':200,'data':result}
    except Exception as e:
            db.rollback()
            logger.error(e)
            raise HTTPException(status_code=500, detail=str(e))
    return {'message': '修改失败！', 'status_code': 501}
# 4. 删除指定学生的某次成绩（按 学生编号 + 考核序次）
@score_router.delete("/score/delete", summary='删除指定学生的某次成绩（按 学生编号 + 考核序次）')
def delete_scores(student_id:int= Query(...,description='学生id'),kaohe_rank=Query(...,description='考核序次'),
                  db: Session = Depends(get_db)):
    try:
        if score.delete_score(db, student_id,kaohe_rank):
            return {"message": '删除成功','status_code':200}
    except Exception as e:
        db.rollback()
        logger.error(e)
        raise HTTPException(status_code=500, detail=str(e))
    return {'message': '删除失败！','status_code':501}

