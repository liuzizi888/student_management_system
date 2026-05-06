from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from database import Base


# 角色表
class SysRole(Base):
    __tablename__ = "t_sys_role"
    id = Column(Integer, primary_key=True)
    role_name = Column(String(30))
    role_desc = Column(String(100))

    # 关联用户
    users = relationship("SysUser", back_populates="role")


# 用户表
class SysUser(Base):
    __tablename__ = "t_sys_user"
    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True)
    password = Column(String(255))
    role_id = Column(Integer, ForeignKey("t_sys_role.id"))
    create_time = Column(DateTime)

    # 关联角色
    role = relationship("SysRole", back_populates="users")


