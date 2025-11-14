from sqlmodel import create_engine

# 使用项目目录下的 SQLite 文件（相对路径 ./app/db/database.db）
# 之前项目根目录有一个 `database.db`，但实际数据位于 `app/db/database.db`。
# 使用相对路径指向 `app/db/database.db`，以保证应用和本仓库中 db 文件一致。
DATABASE_URL = "sqlite:///./app/db/database.db"
engine = create_engine(
    DATABASE_URL,
    echo=True,  # 可选：打印 SQL 日志，调试时有用
)