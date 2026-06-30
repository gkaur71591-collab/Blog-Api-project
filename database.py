from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker,declarative_base
DATABASE_URL="postgresql://postgres:admin123@localhost:5433/blogdb"
engine=create_engine(DATABASE_URL)
#creating seesion for database
SessionLocal=sessionmaker(autocommit=False,autoflush=False,bind=engine)
base=declarative_base()
