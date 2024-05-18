from typing import List,Union,Optional
from sqlalchemy.orm import Session

import models
from sql.schemas import posts, users,nodes
from typing import overload
from fastapi import HTTPException
import fakedb,fakedb_search

@overload
def get_feedback(db: Session, post_id: int, user_id: int):
    return [fakedb.fake_feedback_db[i] 
            for i in fakedb.fake_feedback_db 
            if i['post_id']==post_id and i['user_id']==user_id
    ][0]
    return db.query(models.Feedback).filter(
        models.Feedback.post_id == post_id,
        models.Feedback.user_id == user_id
    ).first()

@overload
def get_feedback(db: Session, post_id: int):
    return [fakedb.fake_feedback_db[i] 
            for i in fakedb.fake_feedback_db 
            if i['post_id']==post_id
    ]
    return db.query(models.Feedback).filter(models.Feedback.post_id == post_id).all()

@overload
def get_feedback(db: Session, user_id: int):
    return [fakedb.fake_feedback_db[i] 
            for i in fakedb.fake_feedback_db 
            if i['user_id']==user_id
    ]
    return db.query(models.Feedback).filter(models.Feedback.user_id == user_id).all()

@overload
def get_users(db: Session, user_id: int):
    return [fakedb.fake_users_db[i] for i in fakedb.fake_users_db if i['user_id']==user_id][0]
    return db.query(models.User).filter(models.User.user_id == user_id).first()

@overload
def get_users(db: Session, username: str):
    return fakedb.fake_users_db.get(username)
    return db.query(models.User).filter(models.User.username == username).first()

@overload
def get_users(db: Session, user_ids: List[int]):
    return [fakedb.fake_users_db[i] for i in fakedb.fake_users_db if i['user_id'] in user_ids]
    return db.query(models.User).filter(models.User.user_id.in_(user_ids)).all()

@overload
def get_users(db: Session, skip: int = 0, limit: int = 100):
    return [fakedb.fake_users_db[i] for i in fakedb.fake_users_db][skip:skip+limit]
    return db.query(models.User).offset(skip).limit(limit).all()

@overload
def get_users(db: Session, all=True):
    return fakedb.fake_users_db
    return db.query(models.User).all()
def get_users(
        db: Session, 
        user_id: Union[int, List[int], None] = None,
        username: Optional[str] = None,
        skip: int = 0,
        limit: int = 100
):

    # If 'username' is provided, return the user matching that username
    if username:
        return fakedb.fake_users_db.get(username)
        return db.query(models.User).filter(models.User.username == username).first()
        
    # If 'user_id' is provided and it's a list, return users matching those IDs
    if isinstance(user_id, list):
        return [fakedb.fake_users_db[i] for i in fakedb.fake_users_db if i['user_id'] in user_id] if db is None else db.query(models.User).filter(models.User.user_id.in_(user_id)).all()

    # If 'user_id' is provided and it's a single ID, return the user matching that ID
    if isinstance(user_id, int):
        return [fakedb.fake_users_db[i] for i in fakedb.fake_users_db if i['user_id'] == user_id][0] if db is None else db.query(models.User).filter(models.User.user_id == user_id).first()


    # Default case: return users with pagination
    return [fakedb.fake_users_db[i] for i in fakedb.fake_users_db][skip:skip+limit] if db is None else db.query(models.User).offset(skip).limit(limit).all()

def get_admin(db: Session, admin_id: int):
    admin=get_users(db,admin_id)
    return fakedb.fake_users_db.get(admin['username'])
    return db.query(models.Admin).filter(models.Admin.user_id == admin_id).first()

@overload
def get_tags(db: Session, user_id: int):
    return [fakedb.fake_interest_tag_db[i] for i in fakedb.fake_interest_tag_db if i['user_id']==user_id]
    return db.query(models.interest_tag).filter(models.interest_tag.user_id == user_id).all()

@overload
def get_tags(db: Session, username: str):
    return [fakedb.fake_interest_tag_db[i] for i in fakedb.fake_interest_tag_db if i['user_id']==get_users(db,username=username)['user_id']]
    return db.query(models.interest_tag).filter(models.User.user_name == username).all()

@overload
def get_posts(db: Session, skip: int = 0, limit: int = 100,anonymousIncluded: bool=False):
    return [fakedb.fake_posts_db[i] for i in fakedb.fake_posts_db if fakedb.fake_posts_db[i]['anonymous']==anonymousIncluded][skip:skip+limit]
    return db.query(models.Post).offset(skip).limit(limit).filter(
            models.Post.anonymous==anonymousIncluded
        ).all()

@overload
def get_posts(db: Session, post_ids: List[int],anonymousIncluded: bool=False):
    return [fakedb.fake_posts_db[i] for i in fakedb.fake_posts_db if i['post_id'] in post_ids]
    return db.query(models.Post).filter(
            models.Post.post_id.in_(post_ids),models.Post.anonymous==anonymousIncluded
        ).all()

@overload
def get_posts(db: Session, post_ids: List[int], username: str):
    user_id=get_users(db,username=username)['user_id']
    return [fakedb.fake_posts_db[i] 
            for i in fakedb.fake_posts_db 
            if i['post_id'] in post_ids and (
                fakedb.fake_posts_db[i]['anonymous']==False or 
                fakedb.fake_post_user_db[i]['user_id']==user_id
            )
    ]
    
    return db.query(models.Post).filter(
            models.Post.post_id.in_(post_ids),
            or_(models.Post.user_id == user_id, models.Post.anonymous==False)
        ).all()

@overload
def get_posts(db: Session, user_id: int,anonymousIncluded: bool=False):
    allposts= [fakedb.fake_posts_db[fakedb.fake_post_user_db[i]['post_id']] 
            for i in fakedb.fake_post_user_db 
            if fakedb.fake_post_user_db[i]['user_id']==user_id]
    if anonymousIncluded:
        return allposts
    else:
        return [i for i in allposts if i['anonymous']==False]
    if anonymousIncluded:
        db.query(models.Post).filter(models.Post.user_id == user_id).all()
    else:
        return db.query(models.Post).filter(
            models.Post.user_id == user_id,models.Post.anonymous==False
        ).all()

@overload
def get_categories(db: Session, skip: int = 0, limit: int = 100):
    return [fakedb.fake_category_db[i] for i in fakedb.fake_category_db][skip:skip+limit]
    return db.query(models.Category).offset(skip).limit(limit).all()

@overload
def get_categories(db: Session, category_ids: List[int]):
    return [fakedb.fake_category_db[i] for i in fakedb.fake_category_db if i['tag_id'] in category_ids]
    return db.query(models.Category).filter(models.Category.category_id.in_(category_ids)).all()

def get_tfidf(db: Session, post_id: int):
    return fakedb.posts_v_tfidf.get(post_id)
    return db.query(models.Post_v_tfiddf).filter(models.Post_v_tfiddf.post_id == post_id).first()

def get_post_writers_initial(db: Session, user_id: int, post_id: int):
    return [
        fakedb.fake_post_writer_init_db[i] 
        for i in fakedb.fake_post_writer_init_db 
        if i['user_id']==user_id and i['post_id']==post_id
    ][0]
    return db.query(models.url).filter(
        models.url.user_id == user_id, 
        models.url.post_id == post_id
    ).first()

def get_post_writers_dynamic(db: Session, user_id: int, post_id: int):
    return [
        fakedb.fake_post_writer_dynamic_db[i] 
        for i in fakedb.fake_post_writer_dynamic_db 
        if i['user_id']==user_id and i['post_id']==post_id
    ][0]
    return db.query(models.Post_v_Writers_initialdata).filter(
        models.Post_v_Writers_initialdata.user_id == user_id, 
        models.Post_v_Writers_initialdata.post_id == post_id
    ).first()

def get_post_reader(db: Session, user_id: int, post_id: int):
    return [
        fakedb.fake_post_reader_db[i]
        for i in fakedb.fake_post_reader_db
        if i['user_id']==user_id and i['post_id']==post_id
    ][0]
    return db.query(models.Post_v_Readers).filter(
        models.Post_v_Readers.user_id == user_id, 
        models.Post_v_Readers.post_id == post_id
    ).first()

def get_hiddennode(db: Session, create_key: str,layer: int):
    return [i['create_key'] for i in fakedb_search.fake_hiddennode_db
            if i['create_key']==create_key and i['layer']==layer][0]
    return db.query(models.hiddennode).filter(
        models.hiddennode.create_key == create_key,
        models.hiddennode.layer == layer
        ).first()

@overload
def get_wordhidden(db: Session, fromid: int):
    return [fakedb_search.fake_wordhidden_db[i] 
            for i in fakedb_search.fake_wordhidden_db 
            if i['fromid']==fromid
    ]
    return db.query(models.wordhidden).filter(models.wordhidden.fromid == fromid).all()

@overload
def get_wordhidden(db: Session, fromid: int, toid: int):
    return [fakedb_search.fake_wordhidden_db[i] 
            for i in fakedb_search.fake_wordhidden_db 
            if i['fromid']==fromid and i['toid']==toid
    ][0]
    return db.query(models.wordhidden).filter(
        models.wordhidden.fromid == fromid,
        models.wordhidden.toid == toid
    ).first()

@overload
def get_hiddenhidden(db: Session, fromid: int):
    return [fakedb_search.fake_hiddenhidden_db[i]
            for i in fakedb_search.fake_hiddenhidden_db
            if i['fromid']==fromid
    ]
    return db.query(models.hiddenhidden).filter(
        models.hiddenhidden.fromid == fromid
        ).all()

@overload
def get_hiddenhidden(db: Session, toid: int):
    return [fakedb_search.fake_hiddenhidden_db[i]
            for i in fakedb_search.fake_hiddenhidden_db
            if i['toid']==toid
    ]
    return db.query(models.hiddenhidden).filter(
        models.hiddenhidden.toid == toid
    ).all()

@overload
def get_hiddenhidden(db: Session, fromid: int, toid: int):
    return [fakedb_search.fake_hiddenhidden_db[i]
            for i in fakedb_search.fake_hiddenhidden_db
            if i['fromid']==fromid and i['toid']==toid
    ][0]
    return db.query(models.hiddenhidden).filter(
        models.hiddenhidden.fromid == fromid,
        models.hiddenhidden.toid == toid
    ).first()

@overload
def get_hiddenurl(db: Session, fromid: int):
    return [fakedb_search.fake_hiddenurl_db[i]
            for i in fakedb_search.fake_hiddenurl_db
            if i['fromid']==fromid
    ]
    return db.query(models.hiddenurl).filter(
        models.hiddenurl.fromid == fromid
        ).all()

@overload
def get_hiddenurl(db: Session, toid: int):
    return [fakedb_search.fake_hiddenurl_db[i]
            for i in fakedb_search.fake_hiddenurl_db
            if i['toid']==toid
    ]
    return db.query(models.hiddenurl).filter(
        models.hiddenurl.toid == toid
        ).all()

@overload
def get_hiddenurl(db: Session, fromid: int, toid: int):
    return [fakedb_search.fake_hiddenurl_db[i]
            for i in fakedb_search.fake_hiddenurl_db
            if i['fromid']==fromid and i['toid']==toid
    ][0]
    return db.query(models.hiddenurl).filter(
        models.hiddenurl.fromid == fromid,
        models.hiddenurl.toid == toid
    ).first()

def get_userresponsecache(db: Session):
    return db.query(models.userResponseCache).all()

@overload
def get_urls(db: Session, url_ids: List[int]):
    return [fakedb_search.fake_url_db[i] 
            for i in fakedb_search.fake_url_db 
            if i['url_id'] in url_ids
    ]
    return db.query(models.url).filter(models.url.url_id.in_(url_ids)).all()

@overload
def get_urls(db: Session):
    return fakedb_search.fake_url_db
    return db.query(models.url).all()

@overload
def get_urls(db: Session, type: str):
    return [fakedb_search.fake_url_db[i] 
            for i in fakedb_search.fake_url_db 
            if i['type']==type
    ]
    return db.query(models.url).filter(models.url.type == type).all()

def create_user(
        db: Session, 
        user: users.UserInDB
):  
    fakedb.fake_users_db.update({user.username:user.model_dump()})
    urlDB=create_url(db,url='/'.join(['users',user.user_id]),id=user.user_id,type='user')
    return {
        "user":user,
        "url":urlDB
    }

    db_user=models.User(**user.model_dump())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return {
        "user":db_user,
        "url":create_url(db,url='/'.join(['users',user.user_id]),id=user.user_id,type='user')
    }

def create_admin(db: Session, admin_id: int):
    id=len(fakedb.fake_admin_db)
    fakedb.fake_admin_db.update({
        NotImplementedError:
        {
            "username":get_users(db,admin_id)['username'],
        }
    })
    return fakedb.fake_admin_db[id]
    db_admin=models.Admin(id=admin_id)
    db.add(db_admin)
    db.commit()
    db.refresh(db_admin)
    return db_admin

def create_post(
        db: Session, 
        post: posts.PostInDB,
        tfidf: posts.Post_v_tfidfnoId,
        writers_dynamic: posts.Post_v_Writers_dinamicdatanoId
):
    post.post_id=len(fakedb.fake_posts_db)+1
    fakedb.fake_posts_db.update({post.post_id:post.model_dump()})
    postout=fakedb.fake_posts_db[post.post_id]
    return {
        "post":postout,
        "tfidf":create_tfidf(db,tfidf,post.post_id),
        "writers_dynamic":create_writers_dynamic(db,writers_dynamic,post.post_id),
        "url":create_url(db,url="/".join(["post",post.post_id]),id=post.post_id,type='post')
    }
    db_post=models.Post(**post.model_dump())
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return {
        "post":db_post,
        "tfidf":create_tfidf(db,tfidf,db_post.post_id),
        "writers_dynamic":create_writers_dynamic(db,writers_dynamic,db_post.post_id),
        "url":create_url(db,url="/".join(["post",post.post_id]),id=post.post_id,type='post')
    }

def create_tfidf(db: Session, tfidf: posts.Post_v_tfidf, post_id: int):
    fakedb.posts_v_tfidf.update({post_id:tfidf.model_dump()})
    return fakedb.posts_v_tfidf[post_id]
    db_tfidf=models.Post_v_tfiddf(**tfidf.model_dump())
    db.add(db_tfidf)
    db.commit()
    db.refresh(db_tfidf)
    return db_tfidf

def create_writers_initial(db: Session, writers_initial: posts.Post_v_Writers_initialdata):
    fakedb.fake_post_writer_init_db.update({writers_initial.post_id:writers_initial.model_dump()})
    return fakedb.fake_post_writer_init_db[writers_initial.post_id]
    db_writers_initial=models.Post_v_Writers_initialdata(**writers_initial.model_dump())
    db.add(db_writers_initial)
    db.commit()
    db.refresh(db_writers_initial)
    return db_writers_initial

def create_writers_dynamic(db: Session, writers_dynamic: posts.Post_v_Writers_dinamicdata,):
    fakedb.fake_post_writer_dynamic_db.update({writers_dynamic.post_id:writers_dynamic.model_dump()})
    return fakedb.fake_post_writer_dynamic_db[writers_dynamic.post_id]
    db_writers_dynamic=models.Post_v_Writers_dinamicdata(**writers_dynamic.model_dump())
    db.add(db_writers_dynamic)
    db.commit()
    db.refresh(db_writers_dynamic)
    return db_writers_dynamic

def create_readers(db: Session, readers: posts.Post_v_Readers):
    fakedb.fake_post_reader_db.update({readers.post_id:readers.model_dump()})
    return fakedb.fake_post_reader_db[readers.post_id]
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
    fakedb_search.fake_url_db.update(
        {
            url.id:{
                "url_id":url.id,
                "url":url.url,
                "category":type,
                "user_id":id if type=='user' else None,
                "post_id":id if type=='post' else None
            }
        }
    )
    return fakedb_search.fake_url_db[url.id]
    db_url=models.url(**url.model_dump())
    db.add(db_url)
    db.commit()
    db.refresh(db_url)
    return db_url

def create_category(
        db: Session, 
        category: posts.Category
):
    fakedb.fake_category_db.update({category.tag_id:category.model_dump()})
    return fakedb.fake_category_db[category.tag_id]
    db_category=models.Category(**category.model_dump())
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category

def create_interest_tag(
        db: Session, 
        interest_tag: users.interest_tag
):
    fakedb.fake_interest_tag_db.update({interest_tag.user_id:interest_tag.model_dump()})
    return fakedb.fake_interest_tag_db[interest_tag.user_id]
    db_interest_tag=models.interest_tag(**interest_tag.model_dump())
    db.add(db_interest_tag)
    db.commit()
    db.refresh(db_interest_tag)
    return db_interest_tag

def create_hiddennode(
        db: Session, 
        hiddennode: nodes.hiddennode,
):
    fakedb_search.fake_hiddennode_db.update({hiddennode.create_key:hiddennode.model_dump()})
    return fakedb_search.fake_hiddennode_db[hiddennode.create_key]
    db_hiddennode=models.hiddennode(**hiddennode.model_dump())
    db.add(db_hiddennode)
    db.commit()
    db.refresh(db_hiddennode)
    return db_hiddennode

def create_wordhidden(
        db: Session, 
        wordhidden: nodes.wordhidden
):
    id=len(fakedb_search.fake_wordhidden_db)
    fakedb_search.fake_wordhidden_db.update({id:wordhidden.model_dump()})
    return fakedb_search.fake_wordhidden_db[id]
    db_wordhidden=models.wordhidden(**wordhidden.model_dump())
    db.add(db_wordhidden)
    db.commit()
    db.refresh(db_wordhidden)
    return db_wordhidden

def create_hiddenhidden(
        db: Session, 
        hiddenhidden: nodes.hiddenhidden
):
    id=len(fakedb_search.fake_hiddenhidden_db)
    fakedb_search.fake_hiddenhidden_db.update({id:hiddenhidden.model_dump()})
    return fakedb_search.fake_hiddenhidden_db[id]
    db_hiddenhidden=models.hiddenhidden(**hiddenhidden.model_dump())
    db.add(db_hiddenhidden)
    db.commit()
    db.refresh(db_hiddenhidden)
    return db_hiddenhidden

def create_hiddenurl(
        db: Session, 
        hiddenurl: nodes.hiddenurl
):
    id=len(fakedb_search.fake_hiddenurl_db)
    fakedb_search.fake_hiddenurl_db.update({id:hiddenurl.model_dump()})
    return fakedb_search.fake_hiddenurl_db[id]
    db_hiddenurl=models.hiddenurl(**hiddenurl.model_dump())
    db.add(db_hiddenurl)
    db.commit()
    db.refresh(db_hiddenurl)
    return db_hiddenurl

def create_userresponsecache(     
        db: Session, 
        userresponsecache: nodes.userResponseCache
):
    id=len(fakedb_search.fake_user_response_cache_db)
    fakedb_search.fake_user_response_cache_db.update({id:userresponsecache.model_dump()})
    return fakedb_search.fake_user_response_cache_db[id]
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
    #db.commit()
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
    #db.commit()
    return {
        "user":userDB,
    }

@overload
def update_user(
        db: Session, 
        user: users.UserInDBtag,
):
    current_tag=get_tags(db,user.user_id)
    for tag in current_tag:
        fakedb.fake_interest_tag_db.pop(current_tag['tag_id'])
    for tag in user.interested_tag:
        create_interest_tag(db,models.interest_tag(user_id=user.user_id,tag_id=tag))
    return {
        "user":get_users(db,user.user_id),
    }
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
    #db.commit()
    return {
        "user":userDB,
    }

@overload
def update_post(
        db: Session, 
        post_id: int,
        user_id: int, 
        feedback: Union[str,None]
):
    post=fakedb.fake_posts_db[post_id]
    current=[fakedb.fake_feedback_db[i] 
             for i in fakedb.fake_feedback_db 
             if i['post_id']==post_id 
             and i['user_id']==user_id
    ]
    if current:
        currentFeedback=fakedb.fake_feedback_db.pop(current[0])
        if feedback==None:
            post[currentFeedback['feedback']]-=1
        else:
            currentFeedback['feedback']=feedback
            fakedb.fake_feedback_db.update(currentFeedback)
            post[currentFeedback['feedback']]-=1
            post[feedback]+=1
        fb=currentFeedback
    else:
        fb=fakedb.fake_feedback_db.update({
            len(fakedb.fake_feedback_db):{
                "post_id":post_id,
                "user_id":user_id,
                "feedback":feedback
            }
        })
        post[feedback]+=1
    return {
        "post":post,
        "feedback":fb,
    }


    update_post_reader(db,posts.Post_v_Readers(user_id=user_id,post_id=post_id,Feedback=feedback))
    return output
    post=db.query(models.Post).filter(models.Post.post_id == post_id).first()
    oldfeedback=get_feedback(db,post_id,user_id)
    if oldfeedback:
        post.update({oldfeedback.feedback:post[oldfeedback.feedback]-1,
                    feedback:post[feedback]+1
                    })
        oldfeedback.feedback=feedback
        db.commit()
        db.refresh(post)
        db.refresh(oldfeedback)
        update_post_reader(db,posts.Post_v_Readers(user_id=user_id,post_id=post_id,Feedback=feedback))
        return {
            "post":post,
            "feedback":oldfeedback,
        }
    else:
        newFB=db.add(models.Feedback(post_id=post_id,user_id=user_id,feedback=feedback))
        post.update({feedback:post[feedback]+1})
        update_post_reader(db,posts.Post_v_Readers(user_id=user_id,post_id=post_id,Feedback=feedback))
        db.commit()
        db.refresh(post)
        return {
            "post":post,
            "feedback":newFB,
        }


@overload
def update_post(
        db: Session, 
        post: posts.PostInDBfeedback
):
    postDB=get_posts(db,post.post_id)
    
    postDB.good=post.good
    postDB.impossible=post.impossible
    postDB.tell_me_earlier=post.early
    #db.commit()
    return {
        "post":postDB,
    }

def update_tfidf(
        db: Session, 
        tfidf: posts.Post_v_tfidf
):
    tfidfDB=get_tfidf(db,tfidf.post_id)
    tfidfDB.tfidf=tfidf.tfidf
    #db.commit()
    return {
        "tfidf":tfidfDB,
    }

def update_post_reader(
        db: Session, 
        reader: posts.Post_v_Readers
):
    readerDB=get_post_reader(db,reader.user_id,reader.post_id)
    readerDB.Feedback=reader.Feedback
    #db.commit()
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
    #db.commit()
    return {
        "wordhidden":wordhiddenDB,
    }

def update_hiddenhidden(
        db: Session, 
        hiddenhidden: nodes.hiddenhidden
):
    hiddenhiddenDB=get_hiddenhidden(db,hiddenhidden.fromid,hiddenhidden.toid)
    hiddenhiddenDB.strength=hiddenhidden.strength
    #db.commit()
    return {
        "hiddenhidden":hiddenhiddenDB,
    }

def update_hiddenurl(
        db: Session, 
        hiddenurl: nodes.hiddenurl
):
    hiddenurlDB=get_hiddenurl(db,hiddenurl.fromid,hiddenurl.toid)
    hiddenurlDB.strength=hiddenurl.strength
    #db.commit()
    return {
        "hiddenurl":hiddenurlDB,
    }

def clear_userresponsecache(db: Session):
    try:
        fakedb_search.fake_user_response_cache_db.clear()
        return True
    except:
        raise HTTPException(status_code=404, detail="userResponseCache not found")
    try:
        db.execute(f"DELETE FROM userResponseCache")
        db.commit()
        return True
    except:
        raise HTTPException(status_code=404, detail="userResponseCache not found")
    
def delete_admin(db: Session, admin_id: int):
    try:
        username=get_users(db,admin_id)['username']
        admin_id=[i for i in fakedb.fake_admin_db if fakedb.fake_admin_db[i]['username']==username][0]
        fakedb.fake_admin_db.pop(admin_id)
        return True
    except:
        raise HTTPException(status_code=404, detail="Admin not found")
    try:
        db.execute(f"DELETE FROM Admin WHERE id={admin_id}")
        db.commit()
        return True
    except:
        raise HTTPException(status_code=404, detail="Admin not found")