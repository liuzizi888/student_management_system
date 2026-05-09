"""
认证中间件：统一处理用户认证和权限验证
"""
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse
from fastapi import HTTPException
from datetime import datetime
import json
import base64
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from dotenv import load_dotenv
import os

load_dotenv()

# 从环境变量读取配置
AES_KEY = os.getenv('AES_KEY', '1234567890123456').encode()
AES_IV = os.getenv('AES_IV', '1234567890123456').encode()

# 不需要认证的路径
EXCLUDE_PATHS = [
    "/",                        # 根路径（登录页）
    "/login",                   # 登录接口
    "/operate/login",           # 登录接口（带前缀）
    "/operate/logout",          # 登出接口
    "/userinfo",                # 用户信息接口（可能需要调整）
    "/frontend/",               # 前端静态资源
    "/log/",                    # 日志静态资源
    "/docs",                    # Swagger文档
    "/redoc",                   # ReDoc文档
    "/openapi.json",            # OpenAPI Schema
]


def aes_decrypt(token: str):
    """AES解密"""
    try:
        byte = base64.b64decode(token)
        cipher = Cipher(algorithms.AES(AES_KEY), modes.CBC(AES_IV))
        decrypt = cipher.decryptor()
        data = decrypt.update(byte) + decrypt.finalize()

        unpad = padding.PKCS7(128).unpadder()
        plain = unpad.update(data) + unpad.finalize()
        return json.loads(plain.decode())
    except:
        return None


class AuthMiddleware(BaseHTTPMiddleware):
    """认证中间件"""

    async def dispatch(self, request: Request, call_next):
        path = request.url.path

        # 检查是否需要跳过认证
        if self._should_skip(path):
            return await call_next(request)

        # 获取token
        token = request.cookies.get("token")
        if not token:
            return JSONResponse(
                status_code=401,
                content={"code": 401, "msg": "请先登录"}
            )

        # 验证token
        info = aes_decrypt(token)
        if not info:
            return JSONResponse(
                status_code=401,
                content={"code": 401, "msg": "Token无效或已过期"}
            )

        # 检查token是否过期
        now = int(datetime.now().timestamp())
        if now > info["exp"]:
            return JSONResponse(
                status_code=401,
                content={"code": 401, "msg": "登录已过期，请重新登录"}
            )

        # 将用户信息注入到request state中，供后续路由使用
        request.state.user = {
            "uid": info["uid"],
            "role": info["role"]
        }

        return await call_next(request)

    def _should_skip(self, path: str) -> bool:
        """检查路径是否需要跳过认证"""
        # 精确匹配
        if path in EXCLUDE_PATHS:
            return True

        # 前缀匹配
        for exclude_path in EXCLUDE_PATHS:
            if path.startswith(exclude_path):
                return True

        return False


def require_role(allowed_roles: list):
    """
    角色权限验证依赖（用于路由层面）
    
    使用方式：
    @app.get("/xxx")
    async def xxx(request: Request, role=Depends(require_role(["admin", "teacher"]))):
        ...
    """
    def check_role(request: Request):
        if not hasattr(request.state, "user"):
            raise HTTPException(status_code=401, detail="请先登录")
        
        user_role = request.state.user.get("role")
        
        # admin拥有所有权限
        if user_role == "admin":
            return user_role
        
        # 检查是否在允许的角色列表中
        if user_role not in allowed_roles:
            raise HTTPException(status_code=403, detail="无权访问该接口")
        
        return user_role
    
    return check_role


def get_current_user(request: Request):
    """
    获取当前登录用户信息的依赖
    
    使用方式：
    @app.get("/xxx")
    async def xxx(request: Request, user=Depends(get_current_user)):
        uid = user["uid"]
        role = user["role"]
        ...
    """
    if not hasattr(request.state, "user"):
        raise HTTPException(status_code=401, detail="请先登录")
    return request.state.user
