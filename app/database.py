import os, time
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.pool import StaticPool, OperationalError
from sqlalchemy.orm import sessionmaker

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./app.db")
SQL_ECHO = os.getenv("SQL_ECHO", "false").lower() == "true"
RETRIES = int(os.getenv("DB_RETRIES", "10"))
DELAY = float(os.getenv("DB_RETRY_DELAY", "1.5"))

connect_args = {"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}

for _ in range(RETRIES):
    try:
        engine = create_engine(DATABASEURL, pool_pre_ping=True, echo=SQL_ECHO, connect_args=connect_args)
        with engine.connect():
            pass
        break
    except OperationalError:
        time.sleep(DELAY)

SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False, expire_on_commit=False)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()