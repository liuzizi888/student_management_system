from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker,declarative_base
from dotenv import load_dotenv
import os

load_dotenv()
DB_HOST = os.getenv('DB_HOST')
DB_PORT = os.getenv('DB_PORT', '3306')
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_NAME = os.getenv('DB_NAME')

# 连接池配置
DB_POOL_SIZE = int(os.getenv('DB_POOL_SIZE', '10'))
DB_MAX_OVERFLOW = int(os.getenv('DB_MAX_OVERFLOW', '20'))
DB_POOL_RECYCLE = int(os.getenv('DB_POOL_RECYCLE', '3600'))
DB_POOL_TIMEOUT = int(os.getenv('DB_POOL_TIMEOUT', '30'))

DATA_URL = f'mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'

engine = create_engine(DATA_URL,
                       # 连接池核心参数
                       pool_size=DB_POOL_SIZE,
                       max_overflow=DB_MAX_OVERFLOW,
                       pool_recycle=DB_POOL_RECYCLE,
                       pool_pre_ping=True,
                       pool_timeout=DB_POOL_TIMEOUT,
                       )

Base = declarative_base()

Session = sessionmaker(bind=engine)


def get_db() -> Session:
    try:
        db = Session()
        yield db
    finally:
        db.close()
