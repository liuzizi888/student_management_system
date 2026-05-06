import logging
import os
from dotenv import load_dotenv

load_dotenv()

# 从环境变量读取配置
LOG_DIR = os.getenv('LOG_DIR', 'log')
LOG_PATH = os.getenv('LOG_PATH', 'log/student_management_system.log')
LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')

# 将 LOG_LEVEL 字符串转换为 logging 常量
LOG_LEVEL_MAP = {
    'DEBUG': logging.DEBUG,
    'INFO': logging.INFO,
    'WARNING': logging.WARNING,
    'ERROR': logging.ERROR,
    'CRITICAL': logging.CRITICAL
}
log_level = LOG_LEVEL_MAP.get(LOG_LEVEL, logging.INFO)

# 先创建 log 文件夹（不存在就自动创建）
if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)

logger = logging.getLogger("student_management_system_logger")
logger.setLevel(log_level)

# 创建文件处理器
file_handler = logging.FileHandler(LOG_PATH)
file_handler.setLevel(log_level)

# 创建控制台处理器
console_handler = logging.StreamHandler()
console_handler.setLevel(log_level)

# 设置日志格式
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
file_handler.setFormatter(formatter)
console_handler.setFormatter(formatter)

# 将处理器添加到日志记录器
logger.addHandler(file_handler)
logger.addHandler(console_handler)