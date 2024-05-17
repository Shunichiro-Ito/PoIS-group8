from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from schemas import users,posts,nodes
import crud, models
from database import SessionLocal, engine
from typing import Union

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/users/", response_model=users.UserInDB)
def create_user(user: users.UserInDB, db: Session = Depends(get_db)):
    db_user = crud.get_users(db,username=user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="username already registered")
    return crud.create_user(db=db, user=user)

@app.get("/users/by_order", response_model=list[users.UserInDB])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users

@app.get("/users/by_id", response_model=users.UserInDB)
def read_users(user_id: int, db: Session = Depends(get_db)):
    user = crud.get_users(db, user_id=user_id)
    return user

@app.get("/users/by_username", response_model=users.UserInDB)
def read_user(username: str, db: Session = Depends(get_db)):
    db_user = crud.get_users(db, username=username)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@app.get("/users/by_ids", response_model=list[users.UserInDB])
def read_users(user_ids:list[int], db: Session = Depends(get_db)):
    users = crud.get_users(db, user_ids=user_ids)
    return users

@app.get("/admin",response_model=bool)
def verify_admin(user_id:int,db:Session=Depends(get_db)):
    return crud.get_admin(db,user_id=user_id)

@app.post("/admin",response_model=bool)
def set_admin(user_id:int,db:Session=Depends(get_db)):
    return crud.create_admin(db,admin_id=user_id)

@app.post("/admin",response_model=bool)
def delete_admin(user_id:int,db:Session=Depends(get_db)):
    return crud.delete_admin(db,admin_id=user_id)

@app.get("/tags",response_model=users.UserInDBtag)
def show_tags(user_id:Union[int,str],db:Session=Depends(get_db)):
    userTag=users.UserInDBtag(**crud.get_tags(db,user_id=user_id))
    return userTag

@app.post("/tags",response_model=users.UserInDBtag)
def update_interest_tag(user:users.UserInDBtag,db:Session=Depends(get_db)):
    return crud.update_user(db,user)

@app.get("/posts/by_order", response_model=list[posts.PostInDB])
def read_posts(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    posts = crud.get_posts(db, skip=skip, limit=limit)
    return posts

@app.get("/posts/by_ids", response_model=list[posts.PostInDB])
def read_posts(post_ids:list[int], db: Session = Depends(get_db)):
    posts = crud.get_users(db, post_ids=post_ids)
    return posts

@app.get("/categories/by_order", response_model=list[posts.Category])
def read_categories(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    categories = crud.get_categories(db, skip=skip, limit=limit)
    return categories

@app.get("/categories/by_ids", response_model=list[posts.Category])
def read_posts(post_ids:list[int], db: Session = Depends(get_db)):
    categories = crud.get_categories(db, post_ids=post_ids)
    return categories

@app.get("/tfidf/",response_model=posts.Post_v_tfiddf)
def get_tfidf(post_id:int,db:Session=Depends(get_db)):
    return crud.get_tfidf(db,post_id=post_id)

@app.get("/post_writers_initial",response_model=posts.Post_v_Writers_initialdata)
def get_postwriterinitial(user_id,post_id:int,db:Session=Depends(get_db)):
    return crud.get_post_writers_initial(db,user_id=user_id,post_id=post_id)

@app.get("/post_writers_dynamic",response_model=posts.Post_v_Writers_dinamicdata)
def get_postwriterdynamic(user_id,post_id:int,db:Session=Depends(get_db)):
    return crud.get_post_writers_dynamic(db,user_id=user_id,post_id=post_id)

@app.post_reader("/post_readers",response_model=posts.Post_v_Readers)
def get_postreader(user_id,post_id:int,db:Session=Depends(get_db)):
    return crud.get_post_reader(db,user_id=user_id,post_id=post_id)

@app.get("/wordhidden", response_model=nodes.wordhidden)
def get_wordhidden(fromid:int,toid:int,db:Session=Depends(get_db)):
    return crud.get_wordhidden(db,fromid=fromid,toid=toid)

@app.get("/hiddenhidden", response_model=nodes.hiddenhidden)
def get_hiddenhidden(fromid:int,toid:int,db:Session=Depends(get_db)):
    return crud.get_hiddenhidden(db,fromid=fromid,toid=toid)

@app.get("/hiddenurl", response_model=nodes.hiddenurl)
def get_hiddenurl(fromid:int,toid:int,db:Session=Depends(get_db)):
    return crud.get_hiddenurl(db,fromid=fromid,toid=toid)

@app.get("/wordhidden/all", response_model=list[nodes.wordhidden])
def get_wordhidden(fromid:int,db:Session=Depends(get_db)):
    return crud.get_wordhidden(db,fromid=fromid)

@app.get("/hiddenhidden/all", response_model=list[nodes.hiddenhidden])
def get_hiddenhidden(fromid:int,db:Session=Depends(get_db)):
    return crud.get_hiddenhidden(db,fromid=fromid)

@app.get("/hiddenurl/all", response_model=list[nodes.hiddenurl])
def get_hiddenurl(fromid:int,db:Session=Depends(get_db)):
    return crud.get_hiddenurl(db,fromid=fromid)

@app.get("/userResponseCache", response_model=nodes.userResponseCache)
def get_userResponseCache(id:int,db:Session=Depends(get_db)):
    return crud.get_userresponsecache(db)

@app.get("/urls",response_model=Union[posts.url,users.url])
def get_url(url_ids:list[int],db:Session=Depends(get_db)):
    return crud.get_urls(db,url_ids=url_ids)

@app.post("/posts", response_model=posts.PostInDB)
def create_post(post: posts.PostInDB, db: Session = Depends(get_db)):
    tfidfSchema=posts.Post_v_tfiddf(**post.model_dump())
    writer_dynamic=posts.Post_v_Writers_dinamicdata(**post.model_dump())
    readers=posts.Post_v_Readers(**post.model_dump())
    url=posts.url(**post.model_dump())
    return crud.create_post(db=db, post=post,tfidf=tfidfSchema,writer_dynamic=writer_dynamic,readers=readers,url=url)

@app.post("/writers_initial",response_model=posts.Post_v_Writers_initialdata)
def create_writer_initial(post: posts.Post_v_Writers_initialdata, db: Session = Depends(get_db)):
    writers_initial=posts.Post_v_Writers_initialdata(**post.model_dump())
    return crud.create_writer_initial(db=db, writer_initial=writers_initial)

@app.post("/category",response_model=posts.Category)
def create_category(category: posts.Category, db: Session = Depends(get_db)):
    category=posts.Category(**category.model_dump())
    return crud.create_category(db=db, category=category)

@app.post("/hiddennode",response_model=nodes.hiddennode)
def create_hiddennode(hiddennode: nodes.hiddennode, db: Session = Depends(get_db)):
    hiddennode=nodes.hiddennode(**hiddennode.model_dump())
    return crud.create_hiddennode(db=db, hiddennode=hiddennode)

@app.post("/wordhidden",response_model=nodes.wordhidden)
def create_wordhidden(wordhidden: nodes.wordhidden, db: Session = Depends(get_db)):
    wordhidden=nodes.wordhidden(**wordhidden.model_dump())
    return crud.create_wordhidden(db=db, wordhidden=wordhidden)

@app.post("/hiddenhidden",response_model=nodes.hiddenhidden)
def create_hiddenhidden(hiddenhidden: nodes.hiddenhidden, db: Session = Depends(get_db)):
    hiddenhidden=nodes.hiddenhidden(**hiddenhidden.model_dump())
    return crud.create_hiddenhidden(db=db, hiddenhidden=hiddenhidden)

@app.post("/hiddenurl",response_model=nodes.hiddenurl)
def create_hiddenurl(hiddenurl: nodes.hiddenurl, db: Session = Depends(get_db)):
    hiddenurl=nodes.hiddenurl(**hiddenurl.model_dump())
    return crud.create_hiddenurl(db=db, hiddenurl=hiddenurl)

@app.post("/userResponseCache",response_model=nodes.userResponseCache)
def create_userResponseCache(userResponseCache: nodes.userResponseCache, db: Session = Depends(get_db)):
    userResponseCache=nodes.userResponseCache(**userResponseCache.model_dump())
    return crud.create_userResponseCache(db=db, userResponseCache=userResponseCache)

@app.post("/users/updatepw",response_model=users.UserInDB)
def update_password(user:users.UserInDBpw,db:Session=Depends(get_db)):
    return crud.update_user(db,user)

@app.post("/users/updatepi",response_model=users.UserInDB)
def update_personal_info(user:users.UserInDBchar,db:Session=Depends(get_db)):
    return crud.update_user(db,user)

@app.post("/users/certified",response_model=users.UserInDB)
def certified_user(user:users.UserCert,db:Session=Depends(get_db)):
    return crud.certified_user(db,user)

@app.post("/post/feedback")
def feedback_post(post:posts.PostInDBfeedback,db:Session=Depends(get_db)):
    return crud.update_post(db,post)

@app.post("/tfidf",response_model=posts.Post_v_tfiddf)
def update_tfidf(post:posts.Post_v_tfiddf,db:Session=Depends(get_db)):
    return crud.update_tfidf(db,post)

@app.post("/post_reader",response_model=posts.Post_v_Readers)
def update_postreader(post:posts.Post_v_Readers,db:Session=Depends(get_db)):
    return crud.update_post_reader(db,post)

@app.post("/wordhidden/update",response_model=nodes.wordhidden)
def update_wordhidden(wordhidden:nodes.wordhidden,db:Session=Depends(get_db)):
    return crud.update_wordhidden(db,wordhidden)

@app.post("/hiddenhidden/update",response_model=nodes.hiddenhidden)
def update_hiddenhidden(hiddenhidden:nodes.hiddenhidden,db:Session=Depends(get_db)):
    return crud.update_hiddenhidden(db,hiddenhidden)

@app.post("/hiddenurl/update",response_model=nodes.hiddenurl)
def update_hiddenurl(hiddenurl:nodes.hiddenurl,db:Session=Depends(get_db)):
    return crud.update_hiddenurl(db,hiddenurl)

@app.post("/userResponseCache/clear",response_model=bool)
def clear_userResponseCache(db:Session=Depends(get_db)):
    return crud.clear_userresponsecache(db)