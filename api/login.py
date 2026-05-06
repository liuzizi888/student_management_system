from fastapi import APIRouter, Request, Response, Form, Depends
from starlette.responses import HTMLResponse
from database import get_db
from utils.decorator import get_token, auth, aes_decrypt
from dao import sysuser
from utils.log import logger
from dotenv import load_dotenv
from datetime import datetime
import os

load_dotenv()

# 从环境变量读取配置
COOKIE_EXPIRE = int(os.getenv('COOKIE_EXPIRE', '2592000'))

login_router = APIRouter()


# 登录接口：校验账号密码后下发cookie token
@login_router.post("/login")
async def login(res: Response, username: str = Form(...), password: str = Form(...), db=Depends(get_db)):
    # 1. 根据账号查询用户
    user = sysuser.queryUserById(db, username)
    if not user:
        logger.warning(f'{username}账号不存在')
        return {"code": 400, "msg": "账号不存在"}
    # 2. 判断密码是否正确
    if user.password != password:
        logger.warning(f'{username}密码错误')
        return {"code": 400, "msg": "密码错误"}
    # # 3. 获取用户角色
    role = user.role.role_name
    # 4. 生成token
    token = get_token(user.id, role)
    # 设置浏览器cookie
    res.set_cookie(
        key="token",
        value=token,
        max_age=COOKIE_EXPIRE,
        httponly=True
    )
    res.headers["Role"] = role          # 角色
    res.headers["Username"] = username  # 账号
    logger.info(f'{username}登录成功')
    return {"code": 200, "msg": "登录成功"}


# 登录页面
@login_router.get("/home", response_class=HTMLResponse)
def admin_page():
    with open("html/manager.html", "r", encoding="utf-8") as f:
        return f.read()

# 登出接口：清除cookie
@login_router.get("/logout")
async def logout(res: Response):
    res.delete_cookie("token")
    return {"msg": "退出登录成功"}


# 获取当前登录用户信息
@login_router.get("/userinfo")
async def get_userinfo(request: Request, db=Depends(get_db)):
    token = request.cookies.get("token")
    if not token:
        return {"code": 401, "msg": "请先登录"}
    try:
        info = aes_decrypt(token)
        now = int(datetime.now().timestamp())
        if now > info["exp"]:
            return {"code": 401, "msg": "登录已过期，请重新登录"}
        # 查询用户
        user = sysuser.queryUserByPK(db, info["uid"])
        if not user:
            return {"code": 404, "msg": "用户不存在"}
        return {
            "code": 200,
            "data": {
                "uid": info["uid"],
                "username": user.username,
                "role": info["role"],
                "role_name": user.role.role_name
            }
        }
    except Exception as e:
        logger.error(f"获取用户信息失败: {e}")
        return {"code": 401, "msg": "Token无效或已过期"}


@login_router.get("/manager", response_class=HTMLResponse)
def admin_page():
    with open("html/manager.html", "r", encoding="utf-8") as f:
        return f.read()



