from sqlalchemy import Column, Integer, String, Date, DateTime, Float, ForeignKey
from sqlalchemy.orm import relationship

from database import Base, engine

#就业信息表
class Employment(Base):
    __tablename__ = "t_employment_info"
    employment_id = Column(Integer, primary_key=True,autoincrement=True, comment="学生就业信息编号")
    # student_id = Column(Integer, nullable=False, comment="学生编号")
    student_id = Column(Integer, ForeignKey("t_student.student_id"),nullable=False, comment="学生编号")
    student_name = Column(String(20), comment="学生姓名")
    class_id = Column(Integer,ForeignKey("t_class_info.class_id"),nullable=False, comment="班级编号")
    # class_id = Column(Integer, , nullable=False, comment="班级编号")
    class_code = Column(Integer, comment="学生班级编号")
    open_time = Column(Date, comment="就业开放时间")
    offer_time = Column(Date, comment="offer下发时间")
    company = Column(String(50), comment="就业公司")
    salary = Column(Float, comment="就业薪资")
    del_flag = Column(String(20), nullable=False, default=None, comment="软删除 ''-正常 Y-删除")
    creat_time= Column(DateTime, nullable=False,comment ="创建时间")
    update_time = Column(DateTime, nullable=False,comment="更新时间")
    # 学生（一）对应就业信息（多）
    t_student = relationship("Student", back_populates="t_employment_info")
    # 就业信息（多）对应 班级（一）
    t_class_info = relationship("ClassInfo", back_populates="t_employment_info")

    def __repr__(self):
        return f"Employment:{self.employment_id},{self.student_id},{self.student_name},{self.class_id}"

