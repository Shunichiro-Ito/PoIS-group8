from sqlalchemy import Boolean, Column, ForeignKey, Integer, String,Date,Float,Double,Enum,DateTime
from sqlalchemy.orm import relationship

from database import Base


class User(Base):
    __tablename__ = "users"
    user_id = Column(Integer, primary_key=True)
    user_name = Column(String, unique=True, index=True)
    display_name = Column(String)
    hashed_password = Column(String)
    certified = Column(Boolean, default=False)
    age = Column(Integer)
    gender=Column(Enum("f","m"))
    occupation=Column(String)
    mbti=Column(String)

    interest_tags=relationship("interest_tag", back_populates="user")
    posts = relationship("Post", back_populates="owner")
    admin=relationship("Admin", back_populates="detail")
    url=relationship("url", back_populates="user")

class Admin(Base):
    __tablename__ = "admin"

    user_id = Column(Integer, ForeignKey("users.id"),primary_key=True)
    detail=relationship("User", back_populates="admin")

class Post(Base):
    __tablename__ = "posts"

    post_id = Column(Integer, primary_key=True)
    title = Column(String, index=True)
    content = Column(String, index=True)
    category_id = Column(Integer, ForeignKey("categories.id"))
    age_at_failure = Column(Integer)
    good=Column(Integer)
    impossible=Column(Integer)
    tell_me_earlier=Column(Integer)
    posting_date=Column(DateTime)
    anonimous=Column(Boolean)
    owner_id = Column(Integer, ForeignKey("users.id"))

    owner = relationship("User", back_populates="posts")
    category = relationship("Category", back_populates="posts")
    tfidf=relationship("Post_v_tfiddf", back_populates="post")
    url=relationship("url", back_populates="post")


class Category(Base):
    __tablename__ = "tags"

    category_id = Column(Integer, primary_key=True)
    key_words = Column(String, index=True)
    posts = relationship("Post", back_populates="category")

# Not finalised
class interest_tag(Base):
    __tablename__ = "interest_tag"

    user_id = Column(Integer,ForeignKey("users.id"), primary_key=True)
    tag_id = Column(Integer, ForeignKey("tags.category_id"), primary_key=True)

    user=relationship("User", back_populates="interest_tags")

class Post_v_tfiddf(Base):
    __tablename__ = "posts_v_tfiddf"

    post_id = Column(Integer, ForeignKey("posts.id"),primary_key=True)
    tfidf_0=Column(Double)
    tfidf_1=Column(Double)
    tfidf_2=Column(Double)
    tfidf_3=Column(Double)
    tfidf_4=Column(Double)
    tfidf_5=Column(Double)
    tfidf_6=Column(Double)
    tfidf_7=Column(Double)
    tfidf_8=Column(Double)
    tfidf_9=Column(Double)
    tfidf_10=Column(Double)
    tfidf_11=Column(Double)
    tfidf_12=Column(Double)
    tfidf_13=Column(Double)
    tfidf_14=Column(Double)
    tfidf_15=Column(Double)
    tfidf_16=Column(Double)
    tfidf_17=Column(Double)
    tfidf_18=Column(Double)
    tfidf_19=Column(Double)

    post=relationship("Post", back_populates="tfidf")

class Post_v_Writers_initialdata(Base):
    __tablename__ = "posts_v_Writers_initialdata"

    user_id = Column(Integer, ForeignKey("users.id"),primary_key=True)
    post_id = Column(Integer, ForeignKey("posts.id"),primary_key=True)
    category_id = Column(Integer, ForeignKey("tags.category_id"))
    age = Column(Integer)
    gender=Column(String)
    occupation=Column(String)

class Post_v_Writers_dinamicdata(Base):
    __tablename__ = "posts_v_Writers_dinamicdata"

    user_id = Column(Integer, ForeignKey("users.id"),primary_key=True)
    post_id = Column(Integer, ForeignKey("posts.id"),primary_key=True)
    category_id = Column(Integer, ForeignKey("tags.category_id"))
    age = Column(Integer)
    gender=Column(String)
    occupation=Column(String)
    mbti=Column(String)

class Post_v_Readers(Base):
    __tablename__ = "posts_v_Readers"

    user_id = Column(Integer, ForeignKey("users.id"),primary_key=True)
    post_id = Column(Integer, ForeignKey("posts.id"),primary_key=True)
    Feedback = Column(String)

class hiddennode(Base):
    __tablename__ = "hiddennode"

    create_key = Column(String, primary_key=True)

class wordhidden(Base):
    __tablename__ = "wordhidden"

    fromid = Column(Integer, ForeignKey("tags.category_id"),primary_key=True)
    toid = Column(Integer, ForeignKey("hiddennode.create_key"),primary_key=True)
    strength = Column(Float)

class hiddenhidden(Base):
    __tablename__ = "hiddenhidden"

    fromid = Column(Integer, ForeignKey("hiddennode.create_key"),primary_key=True)
    toid = Column(Integer, ForeignKey("hiddennode.create_key"),primary_key=True)
    strength = Column(Float)

class hiddenurl(Base):
    __tablename__ = "hiddenurl"

    fromid = Column(Integer, ForeignKey("hiddennode.create_key"),primary_key=True)
    toid = Column(Integer, ForeignKey("posts.id"),primary_key=True)
    strength = Column(Float)

class userResponseCache(Base):
    __tablename__ = "userResponseCache"

    id = Column(Integer, primary_key=True)
    sessionvalue=Column(String)
    querys=Column(String)
    selectedurl=Column(String)
    action=Column(String)

class url(Base):
    __tablename__ = "url"

    url_id = Column(Integer, primary_key=True)
    url=Column(String)
    Category=Column(Enum("post","user"))
    user_id=Column(Integer, ForeignKey("users.id"))
    post_id=Column(Integer, ForeignKey("posts.id"))

    post=relationship("Post", back_populates="url")
    user=relationship("User", back_populates="url")
