from sqlmodel import create_engine

# postgresql 远程连接配置
# db_host = "pgm-uf6ym103x0oknpgdao.pg.rds.aliyuncs.com"
# engine = create_engine(f"postgresql://postgres:SHenjiale0911!@{db_host}:5432/test")


# 使用项目目录下的 SQLite 文件（相对路径 ./database.db）
DATABASE_URL = "sqlite:///./database.db"
engine = create_engine(
    DATABASE_URL,
    echo=True,  # 可选：打印 SQL 日志，调试时有用
)