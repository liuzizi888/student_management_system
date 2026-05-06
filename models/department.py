# -*- coding: utf-8 -*-
from database import Base
from sqlalchemy import Column, Integer, String, DateTime, func
from sqlalchemy.orm import relationship


class Department(Base):
    __tablename__ = 't_department'
    department_id = Column(Integer, primary_key=True, autoincrement=True, nullable=False, comment="部门ID")
    dept_name = Column(String(50), nullable=False, comment="部门名称")
    parent_id = Column(Integer, comment="上级部门ID，0为顶级")
    leader = Column(String(20), comment="部门负责人")
    phone = Column(String(20), comment="联系电话")
    remark = Column(String(255), comment="备注")
    create_time = Column(DateTime, nullable=False, server_default=func.now(), comment="创建时间")
    update_time = Column(DateTime, nullable=False, server_default=func.now(), comment="更新时间")
    del_flag = Column(String(20), default="0",  comment="软删除：Y为删除")
    consultants = relationship('Consultant', back_populates='department')


