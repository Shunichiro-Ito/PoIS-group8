from typing import List,Union
from sqlalchemy.orm import Session

import models
from schemas import posts, users,nodes
from typing import overload
from fastapi import HTTPException

@overload
def get_users(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.user_id == user_id).first()

@overload
def get_users(db: Session, username: str):
    return db.query(models.User).filter(models.User.user_name == username).first()

@overload
def get_users(db: Session, user_ids: List[int]):
    return db.query(models.User).filter(models.User.user_id.in_(user_ids)).all()

@overload
def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()

def get_admin(db: Session, admin_id: int):
    return db.query(models.Admin).filter(models.Admin.user_id == admin_id).first()

@overload
def get_tags(db: Session, user_id: int):
    return db.query(models.interest_tag).filter(models.interest_tag.user_id == user_id).all()

@overload
def get_tags(db: Session, username: str):
    return db.query(models.interest_tag).filter(models.User.user_name == username).all()

@overload
def get_posts(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Post).offset(skip).limit(limit).all()

@overload
def get_posts(db: Session, post_ids: List[int]):
    return db.query(models.Post).filter(models.Post.post_id.in_(post_ids)).all()

@overload
def get_categories(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Category).offset(skip).limit(limit).all()

@overload
def get_categories(db: Session, category_ids: List[int]):
    return db.query(models.Category).filter(models.Category.category_id.in_(category_ids)).all()

def get_tfidf(db: Session, post_id: int):
    return db.query(models.Post_v_tfiddf).filter(models.Post_v_tfiddf.post_id == post_id).first()

def get_post_writers_initial(db: Session, user_id: int, post_id: int):
    return db.query(models.url).filter(
        models.url.user_id == user_id, 
        models.url.post_id == post_id
    ).first()

def get_post_writers_dynamic(db: Session, user_id: int, post_id: int):
    return db.query(models.Post_v_Writers_initialdata).filter(
        models.Post_v_Writers_initialdata.user_id == user_id, 
        models.Post_v_Writers_initialdata.post_id == post_id
    ).first()

def get_post_reader(db: Session, user_id: int, post_id: int):
    return db.query(models.Post_v_Readers).filter(
        models.Post_v_Readers.user_id == user_id, 
        models.Post_v_Readers.post_id == post_id
    ).first()

def get_hiddennode(db: Session, create_key: str,layer: int):
    return db.query(models.hiddennode).filter(
        models.hiddennode.create_key == create_key,
        models.hiddennode.layer == layer
        ).first()

@overload
def get_wordhidden(db: Session, fromid: int):
    return db.query(models.wordhidden).filter(models.wordhidden.fromid == fromid).all()

@overload
def get_wordhidden(db: Session, fromid: int, toid: int):
    return db.query(models.wordhidden).filter(
        models.wordhidden.fromid == fromid,
        models.wordhidden.toid == toid
    ).first()

@overload
def get_hiddenhidden(db: Session, fromid: int):
    return db.query(models.hiddenhidden).filter(
        models.hiddenhidden.fromid == fromid
        ).all()

@overload
def get_hiddenhidden(db: Session, toid: int):
    return db.query(models.hiddenhidden).filter(
        models.hiddenhidden.toid == toid
    ).all()

@overload
def get_hiddenhidden(db: Session, fromid: int, toid: int):
    return db.query(models.hiddenhidden).filter(
        models.hiddenhidden.fromid == fromid,
        models.hiddenhidden.toid == toid
    ).first()

@overload
def get_hiddenurl(db: Session, fromid: int):
    return db.query(models.hiddenurl).filter(
        models.hiddenurl.fromid == fromid
        ).all()

def get_hiddenurl(db: Session, toid: int):
    return db.query(models.hiddenurl).filter(
        models.hiddenurl.toid == toid
        ).all()

@overload
def get_hiddenurl(db: Session, fromid: int, toid: int):
    return db.query(models.hiddenurl).filter(
        models.hiddenurl.fromid == fromid,
        models.hiddenurl.toid == toid
    ).first()

def get_userresponsecache(db: Session):
    return db.query(models.userResponseCache).all()

@overload
def get_urls(db: Session, url_ids: List[int]):
    return db.query(models.url).filter(models.url.url_id.in_(url_ids)).all()

@overload
def get_urls(db: Session):
    return db.query(models.url).all()

@overload
def get_urls(db: Session, type: str):
    return db.query(models.url).filter(models.url.type == type).all()

def create_user(
        db: Session, 
        user: users.UserInDB,
        url: users.url
):
    db_user=models.User(**user.model_dump())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return {
        "user":db_user,
        "url":create_url(db,url,db_user.user_id,'user')
    }

def create_admin(db: Session, admin_id: int):
    db_admin=models.Admin(id=admin_id)
    db.add(db_admin)
    db.commit()
    db.refresh(db_admin)
    return db_admin

def create_post(
        db: Session, 
        post: posts.PostInDB,
        tfidf: posts.Post_v_tfidf,
        writers_dynamic: posts.Post_v_Writers_dinamicdata,
        readers: posts.Post_v_Readers,
        url: posts.url
):
    db_post=models.Post(**post.model_dump())
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return {
        "post":db_post,
        "tfidf":create_tfidf(db,tfidf,db_post.post_id),
        "writers_dynamic":create_writers_dynamic(db,writers_dynamic,db_post.post_id),
        "readers":create_readers(db,readers,db_post.post_id),
        "url":create_url(db,url,db_post.post_id)
    }

def create_tfidf(db: Session, tfidf: posts.Post_v_tfidf, post_id: int):
    db_tfidf=models.Post_v_tfiddf(**tfidf.model_dump())
    db.add(db_tfidf)
    db.commit()
    db.refresh(db_tfidf)
    return db_tfidf

def create_writers_initial(db: Session, writers_initial: posts.Post_v_Writers_initialdata):
    db_writers_initial=models.Post_v_Writers_initialdata(**writers_initial.model_dump())
    db.add(db_writers_initial)
    db.commit()
    db.refresh(db_writers_initial)
    return db_writers_initial

def create_writers_dynamic(db: Session, writers_dynamic: posts.Post_v_Writers_dinamicdata,):
    db_writers_dynamic=models.Post_v_Writers_dinamicdata(**writers_dynamic.model_dump())
    db.add(db_writers_dynamic)
    db.commit()
    db.refresh(db_writers_dynamic)
    return db_writers_dynamic

def create_readers(db: Session, readers: posts.Post_v_Readers):
    db_readers=models.Post_v_Readers(**readers.model_dump())
    db.add(db_readers)
    db.commit()
    db.refresh(db_readers)
    return db_readers

def create_url(
        db: Session, 
        url: Union[posts.url,users.url], 
        id: int, 
        type: str
):
    
    db_url=models.url(**url.model_dump())
    db.add(db_url)
    db.commit()
    db.refresh(db_url)
    return db_url

def create_category(
        db: Session, 
        category: posts.Category
):
    db_category=models.Category(**category.model_dump())
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category

def create_interest_tag(
        db: Session, 
        interest_tag: users.interest_tag
):
    db_interest_tag=models.interest_tag(**interest_tag.model_dump())
    db.add(db_interest_tag)
    db.commit()
    db.refresh(db_interest_tag)
    return db_interest_tag

def create_hiddennode(
        db: Session, 
        hiddennode: nodes.hiddennode,
):
    db_hiddennode=models.hiddennode(**hiddennode.model_dump())
    db.add(db_hiddennode)
    db.commit()
    db.refresh(db_hiddennode)
    return db_hiddennode

def create_wordhidden(
        db: Session, 
        wordhidden: nodes.wordhidden
):
    db_wordhidden=models.wordhidden(**wordhidden.model_dump())
    db.add(db_wordhidden)
    db.commit()
    db.refresh(db_wordhidden)
    return db_wordhidden

def create_hiddenhidden(
        db: Session, 
        hiddenhidden: nodes.hiddenhidden
):
    db_hiddenhidden=models.hiddenhidden(**hiddenhidden.model_dump())
    db.add(db_hiddenhidden)
    db.commit()
    db.refresh(db_hiddenhidden)
    return db_hiddenhidden

def create_hiddenurl(
        db: Session, 
        hiddenurl: nodes.hiddenurl
):
    db_hiddenurl=models.hiddenurl(**hiddenurl.model_dump())
    db.add(db_hiddenurl)
    db.commit()
    db.refresh(db_hiddenurl)
    return db_hiddenurl

def create_userresponsecache(     
        db: Session, 
        userresponsecache: nodes.userResponseCache
):
    db_userresponsecache=models.userResponseCache(**userresponsecache.model_dump())
    db.add(db_userresponsecache)
    db.commit()
    db.refresh(db_userresponsecache)
    return db_userresponsecache

@overload
def update_user(
        db: Session, 
        user: users.UserInDBpw,
):
    if user.username==None:
        userDB=get_users(db,user.user_id)
    else:
        userDB=get_users(db,user.username)
    userDB.hashed_password=user.hashed_password
    db.commit()
    return {
        "user":userDB,
    }

@overload
def update_user(
        db: Session, 
        user: users.UserInDBchar,
):
    if user.username==None:
        userDB=get_users(db,user.user_id)
    else:
        userDB=get_users(db,user.username)
    userDB.birth=user.birth
    userDB.gender=user.gender
    userDB.occupation=user.occupation
    userDB.mbti=user.mbti
    db.commit()
    return {
        "user":userDB,
    }

@overload
def update_user(
        db: Session, 
        user: users.UserInDBtag,
):
    db.execute(f"DELETE FROM interest_tag WHERE user_id={user.user_id}")
    for tag in user.interested_tag:
        db.add(models.interest_tag(user_id=user.user_id,tag_id=tag))
    db.commit()
    userDB=get_users(db,user.user_id)
    return {
        "user":users.UserInDBtag(**vars(userDB)),
    }

@overload
def update_user(
        db: Session,
        user: users.UserCert,
):
    if user.username==None:
        userDB=get_users(db,user.user_id)
    else:
        userDB=get_users(db,user.username)
    userDB.certified=user.certified
    db.commit()
    return {
        "user":userDB,
    }

def update_post(
        db: Session, 
        post: posts.PostInDBfeedback
):
    postDB=get_posts(db,post.post_id)
    
    postDB.good=post.good
    postDB.impossible=post.impossible
    postDB.tell_me_earlier=post.early
    db.commit()
    return {
        "post":postDB,
    }

def update_tfidf(
        db: Session, 
        tfidf: posts.Post_v_tfidf
):
    tfidfDB=get_tfidf(db,tfidf.post_id)
    tfidfDB.tfidf=tfidf.tfidf
    db.commit()
    return {
        "tfidf":tfidfDB,
    }

def update_post_reader(
        db: Session, 
        reader: posts.Post_v_Readers
):
    readerDB=get_post_reader(db,reader.user_id,reader.post_id)
    readerDB.Feedback=reader.Feedback
    db.commit()
    return {
        "reader":readerDB,
    }

def update_wordhidden(
        db: Session, 
        wordhidden: nodes.wordhidden
):
    wordhiddenDB=get_wordhidden(db,wordhidden.fromid,wordhidden.toid)
    if wordhiddenDB==None:
        wordhiddenDB=create_wordhidden(db,wordhidden)
    wordhiddenDB.strength=wordhidden.strength
    db.commit()
    return {
        "wordhidden":wordhiddenDB,
    }

def update_hiddenhidden(
        db: Session, 
        hiddenhidden: nodes.hiddenhidden
):
    hiddenhiddenDB=get_hiddenhidden(db,hiddenhidden.fromid,hiddenhidden.toid)
    hiddenhiddenDB.strength=hiddenhidden.strength
    db.commit()
    return {
        "hiddenhidden":hiddenhiddenDB,
    }

def update_hiddenurl(
        db: Session, 
        hiddenurl: nodes.hiddenurl
):
    hiddenurlDB=get_hiddenurl(db,hiddenurl.fromid,hiddenurl.toid)
    hiddenurlDB.strength=hiddenurl.strength
    db.commit()
    return {
        "hiddenurl":hiddenurlDB,
    }

def clear_userresponsecache(db: Session):
    try:
        db.execute(f"DELETE FROM userResponseCache")
        db.commit()
        return True
    except:
        raise HTTPException(status_code=404, detail="userResponseCache not found")
    
def delete_admin(db: Session, admin_id: int):
    try:
        db.execute(f"DELETE FROM Admin WHERE id={admin_id}")
        db.commit()
        return True
    except:
        raise HTTPException(status_code=404, detail="Admin not found")