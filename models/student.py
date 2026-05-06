from sqlalchemy import Column, Integer, String, Date, DateTime, Float, ForeignKey,func
from sqlalchemy.orm import relationship

from database import Base, engine
#学生表
class Student(Base):
    __tablename__ = 't_student'
    student_id = Column(Integer, primary_key=True, autoincrement=True, comment="学生编号")
    class_id = Column(Integer, ForeignKey("t_class_info.class_id"),comment="班级编号")
    name = Column(String(20), nullable=False, comment="学生姓名")
    origin = Column(String(50), comment="籍贯")
    school = Column(String(50), comment="毕业学校")
    major = Column(String(30), comment="专业")
    entry_time = Column(Date, comment="入学时间")
    graduate_time = Column(Date, comment="毕业时间")
    degree = Column(String(10), comment="学历")
    consultant_id = Column(Integer, comment="顾问编号")
    age = Column(Integer, nullable=False, comment="年龄")
    gender = Column(String(10), nullable=False, comment="性别")
    create_time = Column(DateTime,server_default=func.now(),  comment="创建时间")
    update_time = Column(DateTime,server_default=func.now(),  comment="修改时间")
    del_flag = Column(String(10),default="0", comment="软删除")
    # 班级（一）对应学生（多）
    t_class_info = relationship("ClassInfo", back_populates="t_student")
    # 学生（一）对应分数（多）
    t_student_score = relationship("Score", back_populates="t_student")
    # 学生（一）对应就业信息（一）
    t_employment_info = relationship("Employment", back_populates="t_student")