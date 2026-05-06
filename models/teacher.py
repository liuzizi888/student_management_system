from sqlalchemy import Column, Integer, String, Date, DateTime, Float, ForeignKey,Table
from sqlalchemy.orm import relationship
from database import Base, engine
ClassToTeacher = Table(
    't_class_to_teacher',
    Base.metadata,
      # <--- 加上这一行！告诉 SQLAlchemy：如果表已存在，就复用，不要报错
    Column('class_id', Integer, ForeignKey("t_class_info.class_id"), comment="班级编号"),
    Column('teacher_id', Integer, ForeignKey("t_teacher_info.teacher_id"), comment="老师编号"),
    Column('create_time', DateTime, comment="创建时间"),
    Column('update_time', DateTime, comment="修改时间"),
    Column('del_flag', String(10), default="0", comment="软删除"),
    extend_existing=True
)
class TeacherInfo(Base):
    __tablename__ = 't_teacher_info'
    teacher_id = Column(Integer, primary_key=True, autoincrement=True, comment="老师编号")
    name = Column(String(20), nullable=False, comment="老师姓名")
    sex = Column(String(20), nullable=False, comment="性别")
    birth = Column(Date, nullable=False, comment="老师生日")
    subject = Column(String(20), nullable=False, comment="任教科目")
    create_time = Column(DateTime, nullable=False, comment="创建时间")
    update_time = Column(DateTime, nullable=False, comment="更新时间")
    del_flag = Column(String(20), default=None)
    # 班级（多）对应老师（多）
    t_class_info = relationship("ClassInfo",secondary=ClassToTeacher,back_populates="t_teacher_info")


