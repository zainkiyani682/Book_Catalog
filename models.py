
#-------Creating Model Tables
from sqlalchemy import Column,Integer,String
from db import Base

class Book_Catalog(Base):
    __tablename__ = "book_catalog"

    id = Column(Integer,primary_key=True,index=True)
    title = Column(String(50),unique=True,nullable=True,index=True)
    author = Column(String(20))
    published_year = Column(Integer, nullable=False)
    summary = Column(String, nullable=True)