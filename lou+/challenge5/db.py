from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Table
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy import Column, String, Integer, Text
engine = create_engine("mysql+pymysql://root:wangyi@localhost:3306/blog")
#({flavor}://{user}:{password}@{host}/database)
Base = declarative_base()
# meta = MetaData


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String(64), nullable=False, index=True)
    password = Column(String(64), nullable=False)
    email = Column(String(64), nullable=False, index=True)
    articles = relationship("Article", backref='author')
    userinfo = relationship("UserInfo", backref="user", uselist=False)#不是必须的

    def __repr__(self):
        return "%s(%r)" % (self.__class__.__name__, self.username)


Base.metadata.create_all(engine)


class Article(Base):

    __tablename__ = "articles"
    id = Column(Integer, primary_key=True)
    title = Column(String(255), nullable=False, index=True)
    content = Column(Text)
    user_id = Column(Integer, ForeignKey("users.id"))
    # author = relationship("Users") backref就不用在这设置

    def __repr__(self):
        return "%s(%r)" % (self.__class__.__name__, self.title)


class UserInfo(Base):

    __tablename__ = "userinfos"
    id = Column(Integer, primary_key=True)
    name = Column(String(64))
    qq = Column(String(11))
    phone = Column(String(11))
    link = Column(String(64))
    user_id = Column(Integer, ForeignKey("users.id"))


article_tag = Table(
    #第一个参数为表的名字，第二个参数是metadata,两个是必须的
    "article_tag", Base.metadata,
    #对于辅助表，一般要储存关联两个表的 id， 并设为外键
    Column("article_id", Integer, ForeignKey("articles.id")),
    Column("tag_id", Integer, ForeignKey("tags.id"))

)


class Tag(Base):
    __tablename__ = "tags"
    id = Column(Integer, primary_key=True)
    name = Column(String(64), nullable=False, index=True)

    def __repr__(self):
        return "%s(%r)" % (self.__class__.__name__, self.name)


if __name__ == "__main__":
    Base.metadata.create_all(engine)