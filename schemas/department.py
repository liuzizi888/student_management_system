from pydantic import BaseModel, Field

class Department(BaseModel):
    '''
    Department Model 部门类
    '''
    dept_name: str = Field(..., min_length=1, max_length=50, description='部门名称')
    parent_id: int = Field(default=0, description='上级部门ID，0为顶级')
    leader: str = Field(default=None, min_length=1, max_length=20, description='部门负责人')
    phone: str = Field(default=None, pattern=r"^1[3-9]\d{9}$", description='联系电话')
    remark: str = Field(default=None, description='备注')
