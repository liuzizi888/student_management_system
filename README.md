# 学生管理系统

基于 FastAPI + SQLAlchemy 实现的前后端分离学生信息管理系统

## 项目简介

这是一个功能完整的学生管理系统，包含学生、教师、班级、成绩、就业等多模块管理功能，支持统计分析。

## 技术栈

- **后端框架**：FastAPI ~= 0.129.0
- **ORM框架**：SQLAlchemy ~= 1.4.49
- **数据库**：MySQL
- **后端服务**：Uvicorn ~= 0.24.0
- **数据验证**：Pydantic ~= 2.13.2
- **加密库**：Cryptography ~= 46.0.7
- **环境管理**：python-dotenv ~= 1.2.2

## 项目结构

```
student_management_system/
├── api/                    # API接口路由
│   ├── student.py         # 学生管理接口
│   ├── teacher.py         # 教师管理接口
│   ├── class_info.py      # 班级管理接口
│   ├── score.py           # 成绩管理接口
│   ├── employment.py      # 就业管理接口
│   ├── consultant.py      # 顾问管理接口
│   ├── department.py      # 部门管理接口
│   ├── login.py           # 登录登出接口
│   └── statistical_analysis.py  # 统计分析接口
├── dao/                    # 数据访问层
├── models/                 # 数据库模型
├── schemas/                # 数据验证模式
├── utils/                  # 工具类
│   ├── decorator.py       # 权限装饰器、加密解密
│   └── log.py             # 日志配置
├── frontend/               # 前端页面
│   ├── login.html         # 登录页
│   ├── index.html         # 首页
│   ├── student.html       # 学生管理页
│   ├── teacher.html       # 教师管理页
│   ├── class.html         # 班级管理页
│   ├── score.html         # 成绩管理页
│   ├── employment.html    # 就业管理页
│   ├── analysis.html      # 统计分析页
│   ├── style.css          # 样式文件
│   └── utils.js           # 前端工具函数
├── log/                    # 日志文件目录
├── main.py                # 应用入口
├── database.py            # 数据库连接配置
├── requirements.txt       # 依赖包列表
├── .env                   # 环境变量配置
└── README.md              # 项目说明文档
```

## 功能模块

### 1. 用户认证
- 登录/登出
- Token认证（AES加密）
- 基于角色的权限控制

### 2. 学生管理
- 学生信息增删改查
- 按编号/姓名/班级搜索
- 软删除

### 3. 教师管理
- 教师信息增删改查
- 分页查询

### 4. 班级管理
- 班级信息增删改查

### 5. 成绩管理
- 成绩录入
- 学生成绩查询
- 成绩修改删除

### 6. 就业管理
- 就业信息增删改查
- 分页查询
- 多条件搜索

### 7. 统计分析
- 超过30岁学生统计
- 班级人数统计
- 成绩80分以上学生
- 两次不及格学生
- 班级平均分排名
- 薪资TOP5学生
- 就业时长统计
- 平均就业时长

## 快速开始

### 1. 环境准备

确保已安装Python 3.7+和MySQL数据库。

### 2. 安装依赖

```bash
pip install -r requirements.txt
```

### 3. 配置环境变量

复制 `.env` 文件并修改数据库连接信息：

```env
# 数据库配置
DB_HOST=localhost
DB_PORT=3306
DB_NAME=ai0313_deepseek
DB_USER=root
DB_PASSWORD=123456

# 服务配置
HOST=localhost
PORT=8937

# 安全配置
AES_KEY=1234567890123456
AES_IV=1234567890123456
TOKEN_EXPIRE=3600

# 日志配置
LOG_PATH=log/student_management_system.log
```

### 4. 数据库初始化

确保数据库已创建，表结构会在首次运行时自动创建（如果代码中有表创建逻辑）。

### 5. 启动服务

```bash
python main.py
```

服务将在 `http://localhost:8937` 启动。

### 6. 访问系统

- 首页/登录页：`http://localhost:8937/`
- API文档：`http://localhost:8937/docs`（Swagger UI）
- API文档：`http://localhost:8937/redoc`（ReDoc）

## API接口说明

### 认证接口
- `POST /operate/login` - 用户登录
- `GET /operate/logout` - 用户登出

### 学生管理
- `POST /student/students` - 添加学生
- `GET /student/students` - 查询学生
- `PUT /student/students/{id}` - 修改学生
- `DELETE /student/{student_id}` - 删除学生

### 教师管理
- `GET /teacher/check_teacher` - 查询教师
- `POST /teacher/add_teacher` - 添加教师
- `PUT /teacher/update_teacher/{teacher_id}` - 修改教师
- `DELETE /teacher/delete_teacher/{teacher_id}` - 删除教师

### 班级管理
- `GET /class_info/get_class_all` - 查询所有班级
- `GET /class_info/get_class_limit` - 分页查询班级
- `GET /class_info/{class_id}` - 查询单个班级
- `POST /class_info/` - 添加班级
- `PUT /class_info/{class_id}` - 修改班级
- `DELETE /class_info/{class_id}` - 删除班级

### 成绩管理
- `POST /score/score` - 录入成绩
- `GET /score/score/{student_id}` - 查询学生成绩
- `PUT /score/score/update` - 修改成绩
- `DELETE /score/score/delete` - 删除成绩

### 就业管理
- `POST /employment/add` - 添加就业信息
- `GET /employment/query_by_type` - 查询就业信息
- `PUT /employment/{employment_id}` - 修改就业信息
- `DELETE /employment/{employment_id}` - 删除就业信息
- `GET /employment/pageshow` - 分页查询就业信息

### 统计分析
- `GET /student/age/over30` - 查询30岁以上学生
- `GET /student/count` - 班级人数统计
- `GET /student/score/excellent` - 成绩80分以上学生
- `GET /student/score/excellent_1` - 两次不及格学生
- `GET /student/score/excellent_2` - 班级平均分排名
- `GET /student/top_salary` - 薪资TOP5学生
- `GET /student/employ_time` - 就业时长统计
- `GET /student/avg_time` - 平均就业时长

## 开发说明

### 前端开发

前端页面使用纯HTML、CSS、JavaScript开发，位于 `frontend/` 目录下。页面已通过FastAPI的 `StaticFiles` 挂载，可直接访问。

### 数据库连接

数据库连接配置在 `database.py` 中，使用 SQLAlchemy ORM 框架。

### 日志配置

日志配置在 `utils/log.py` 中，日志文件保存在 `log/` 目录下。

## 安全说明

- Token使用AES加密存储
- Cookie设置为httponly防止XSS攻击
- 支持基于角色的权限控制
- 数据库密码等敏感信息通过环境变量配置

## 许可证

MIT License
