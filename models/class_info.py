from sqlalchemy import Column, Integer, String, Date, DateTime, Float, ForeignKey, Table, func
from sqlalchemy.orm import relationship
from database import Base, engine
#中间表
ClassToTeacher = Table(
    't_class_to_teacher',
    Base.metadata,
      # <--- 加上这一行！告诉 SQLAlchemy：如果表已存在，就复用，不要报错
    Column('class_id', Integer, ForeignKey("t_class_info.class_id"), comment="班级编号"),
    Column('teacher_id', Integer, ForeignKey("t_teacher_info.teacher_id"), comment="老师编号"),
    Column('create_time', DateTime, server_default=func.now(), comment="创建时间"),
    Column('update_time', DateTime, server_default=func.now(), comment="修改时间"),
    Column('del_flag', String(10), default='0', comment="软删除"),
    extend_existing=True
)



#班级信息表
class ClassInfo(Base):
    __tablename__ = 't_class_info'
    class_id = Column(Integer, primary_key=True, comment='班级编号')
    course_start_date = Column(Date, nullable=False, comment='课程开始时间')
    is_homeroom_teacher = Column(String(20), nullable=False, comment='班主任')
    class_teacher = Column(String(20), nullable=False, comment='授课老师')
    create_time = Column(DateTime, nullable=False, comment='创建时间')
    update_time = Column(DateTime, nullable=False, comment='更新时间')
    del_flag = Column(String(20), default='0', comment='软删除')
    #班级（一）对应学生（多）
    t_student = relationship("Student",back_populates="t_class_info")
    #班级（多）对应老师（多）
    t_teacher_info = relationship("TeacherInfo",secondary=ClassToTeacher,back_populates="t_class_info")
    # 就业信息（多）对应 班级（一）
    t_employment_info = relationship("Employment", back_populates="t_class_info")




