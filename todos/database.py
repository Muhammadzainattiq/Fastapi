#setting the database

from sqlalchemy import create_engine,Column ,Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

db_url = "postgresql://piaic_owner:Q93uTWrvoNbK@ep-silent-mouse-a15lvoa8.ap-southeast-1.aws.neon.tech/todos?sslmode=require"

engine = create_engine(db_url)
SessionLocal = sessionmaker(autoflush=False, autocommit= False, bind= engine)

Base = declarative_base()

class Todo(Base):
    __tablename__ = "todos"

    id = Column(Integer, primary_key=True, index= True)
    title = Column(String, index = True)
    description = Column(String, index = True)