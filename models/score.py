from sqlalchemy import Column, Integer, String, Date, DateTime, Float, ForeignKey,func
from sqlalchemy.orm import relationship

from database import Base, engine


#分数表
class Score(Base):
    __tablename__ = 't_student_score'
    score_id=Column(Integer,primary_key=True,autoincrement=True,comment="成绩id")
    student_id = Column(Integer,ForeignKey("t_student.student_id"),nullable=False, comment="学生编号")
    kaohe_rank = Column(Integer,comment='考核序次')
    score = Column(Integer,comment='成绩')
    create_time = Column(DateTime, comment='创建时间')
    update_time = Column(DateTime, comment= '更新时间')
    del_flag=Column(String(10),default=0,comment='软删除')
    # 学生（一）对应分数（一）
    t_student = relationship("Student", back_populates="t_student_score")



