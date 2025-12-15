from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# MySQL connection URL
MYSQL_URL = "mysql+pymysql://root:jerome@localhost:3306/gen_brand"

engine = create_engine(
    MYSQL_URL,
    echo=True
)

# Database session
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)

# Base model class
Base = declarative_base()
