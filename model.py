from sqlalchemy import Column, Integer, String,Text
from database import base

#blog table
class Blog(base):
    __tablename__="blogs"
    id=Column(Integer,primary_key=True,index=True)
    title=Column(String,nullable=False)
    content=Column(Text)
