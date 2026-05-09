from fastapi import FastAPI, HTTPException, Request
import uvicorn
from utils.log import logger
from fastapi.responses import HTMLResponse
from api.statistical_analysis import analysis_router
from fastapi.staticfiles import StaticFiles
from api import class_info, student, teacher, employment, score, login, consultant, department
from utils.auth_middleware import AuthMiddleware
from datetime import datetime
from dotenv import load_dotenv
import os

load_dotenv()

# 从环境变量读取配置
HOST = os.getenv('HOST', 'localhost')
PORT = int(os.getenv('PORT', '8937'))
FRONTEND_DIR = os.getenv('FRONTEND_DIR', 'frontend')
LOG_DIR = os.getenv('LOG_DIR', 'log')

app = FastAPI(title="学生管理系统",
              description="基于 FastAPI + SQLAlchemy 实现的前后端分离学生信息管理系统",
              version="1.0.0"
              )

# 注册认证中间件
app.add_middleware(AuthMiddleware)

app.include_router(student.student_router, prefix='/student', tags=['学生基本信息'])
app.include_router(score.score_router, prefix="/score", tags=["成绩板块"])
app.include_router(employment.employment_router, prefix='/employment', tags=["就业信息系统"])
app.include_router(class_info.class_router, prefix='/class_info', tags=["班级管理系统"])
app.include_router(teacher.teacher_router, prefix="/teacher", tags=["教师信息管理系统"])
app.include_router(analysis_router, prefix='/student', tags=['统计分析接口'])
app.include_router(department.department_router, prefix='/department', tags=['部门信息'])
app.include_router(consultant.consultant_router, prefix='/consultant', tags=['顾问信息'])
app.include_router(login.login_router, prefix='/operate', tags=['账号操作'])

#用来查看日志
app.mount("/log", StaticFiles(directory=LOG_DIR))

#挂载 frontend 文件夹
app.mount("/frontend", StaticFiles(directory=FRONTEND_DIR, html=True), name="frontend")

# 根路径重定向到登录页面

# 登录页面
@app.get("/", response_class=HTMLResponse, tags=['登录页面'])
def root(request: Request):
    # 中间件已处理认证，未登录用户会被重定向到登录页
    with open("frontend/index.html", "r", encoding="utf-8") as f:
        return f.read()

if __name__ == '__main__':
    logger.info(f'启动项目，监听地址：http://{HOST}:{PORT}')
    uvicorn.run('main:app', host=HOST, port=PORT)
