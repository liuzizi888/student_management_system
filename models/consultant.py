from sqlalchemy import Column, Integer, String, DateTime, Date, func, ForeignKey
from database import Base
from sqlalchemy.orm import relationship

class Consultant(Base):
    __tablename__ = 't_consultant'
    consultant_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(20), nullable=False, comment="顾问姓名")
    gender = Column(String(20), comment="性别 男 女")
    dept_id = Column(Integer, ForeignKey("t_department.department_id"), comment="所属部门ID")
    position = Column(String(50), comment="职位")
    phone = Column(String(20), comment="手机号")
    entry_date = Column(Date, comment="入职日期")
    status = Column(Integer, nullable=False, comment='状态 1在职 0离职')
    remark = Column(String(255), nullable=False, comment='备注')
    create_time = Column(DateTime, nullable=False, server_default=func.now(), comment="创建时间")
    update_time = Column(DateTime, nullable=False, server_default=func.now(), comment="更新时间")
    del_flag = Column(String(20), default="0", comment="软删除：Y为删除,0为正常")
    department = relationship('Department', back_populates='consultants')
