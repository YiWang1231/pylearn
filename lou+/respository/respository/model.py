from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Integer, DateTime


engine = create_engine('mysql+pymysql://root:wangyi@localhost:3306/shiyanlougithub?charset=utf8')
Base = declarative_base()


class Respository(Base):
    __tablename__ = 'repositories'
    id = Column(Integer, primary_key=True)
    name = Column(String(64))
    update_time = Column(DateTime)


if __name__ == '__main__':
    Base.metadata.create_all(engine)