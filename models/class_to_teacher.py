from sqlalchemy import Column, Integer, String, Date, DateTime, Float, ForeignKey,Table
from sqlalchemy.orm import relationship

from database import Base, engine
# class ClassToTeacher(Base):
#     __tablename__ = 't_class_to_teacher'
#     class_id = Column(Integer, ForeignKey("t_class_info.class_id"),comment="班级编号")
#     teacher_id = Column(Integer,  ForeignKey("t_teacher_info.teacher_id"),primary_key=True, comment="老师编号")
#     create_time = Column(DateTime, comment="创建时间")
#     update_time = Column(DateTime, comment="修改时间")
#     del_flag = Column(String(10), comment="软删除")

ClassToTeacher = Table(
    't_class_to_teacher',
    Base.metadata,
      # <--- 加上这一行！告诉 SQLAlchemy：如果表已存在，就复用，不要报错
    Column('class_id', Integer, ForeignKey("t_class_info.class_id"), comment="班级编号"),
    Column('teacher_id', Integer, ForeignKey("t_teacher_info.teacher_id"), comment="老师编号"),
    Column('create_time', DateTime, comment="创建时间"),
    Column('update_time', DateTime, comment="修改时间"),
    Column('del_flag', String(10), comment="软删除"),
    extend_existing=True
)