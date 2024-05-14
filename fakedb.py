from datetime import date,datetime

fake_users_db = {
    "admin": dict(
        user_id=0,
        username="admin",
        displayed_name="admin",
        certified=True,
        hashed_password="$2a$12$aCCjSgmDLA2swqpLU3ORtuE71DmWaDoU82C.5H2tMXU65rh561kvK", #toEncode
        birth=date(1900,1,1),
        gender="m",
        occupation="admin",
        mbti="INTP",
        interested_tag=[]
    ),
    "jessica": dict(
        user_id=1,
        username="jessica",
        displayed_name="Jessica",
        certified=True,
        hashed_password="$2a$12$aCCjSgmDLA2swqpLU3ORtuE71DmWaDoU82C.5H2tMXU65rh561kvK", #toEncode
        birth=date(1970,1,1),
        gender="f",
        occupation="Housewife",
        mbti="ENFJ",
        interested_tag=["生活","育児","料理","家事"]
    ),
    "johndoe": dict(
        user_id=2,
        username="johndoe",
        displayed_name="John Doe",
        certified=False,
        hashed_password="$2a$12$aCCjSgmDLA2swqpLU3ORtuE71DmWaDoU82C.5H2tMXU65rh561kvK", #toEncode
        birth=date(2004,1,1),
        gender="m",
        occupation="student",
        mbti="ESTP",
        interested_tag=["就活","勉強"]
    ),
    "alice": dict(
        user_id=3,
        username="alice",
        displayed_name="Alice",
        certified=False,
        hashed_password="$2a$12$aCCjSgmDLA2swqpLU3ORtuE71DmWaDoU82C.5H2tMXU65rh561kvK",
        birth=date(2000,12,1),
        gender="f",
        occupation="clerk",
        mbti="ISFP",
        interested_tag=["生活","職場","化粧"]
    ),
}

fake_posts_db={
    1:dict(
        post_id=1,
        title="happy wife happy life",
        content="Failed!!!",
        age=20,
        post_date=datetime(2024,5,4,0,0,0),
        tag_id=["職場"],
        anonymous=True,
        good=10,
        impossible=2,
        early=0
    ),
    2:dict(
        post_id=2,
        title="coding is the best",
        content="Failed!!!",
        age=20,
        post_date=datetime(2024,5,4,0,0,0),
        tag_id=["職場"],
        anonymous=False,
        good=10,
        impossible=2,
        early=0
    ),
}

fake_post_user_db={
    1:dict(
        post_id=1,
        user_id=0,
        tfidf=[0,1,0.9,0.2,0.5]
    ),
    2:dict(
        post_id=2,
        user_id=3,
        tfidf=[0,1,0.9,0.2,0.5]
    )
}

fake_admin_db={
    1:dict(
        username="admin"
    )
}

fake_tag_db={
    1:dict(
        tag_id=1,
        tag_name="生活"
    ),
    2:dict(
        tag_id=2,
        tag_name="職場"
    ),
    3:dict(
        tag_id=3,
        tag_name="化粧"
    ),
    4:dict(
        tag_id=4,
        tag_name="勉強"
    ),
    5:dict(
        tag_id=5,
        tag_name="就活"
    ),
    6:dict(
        tag_id=6,
        tag_name="料理"
    ),
    7:dict(
        tag_id=7,
        tag_name="家事"
    ),
    8:dict(
        tag_id=8,
        tag_name="育児"
    ),
}

fake_feedback_db={
    1:dict(
        post_id=1,
        user_id=2,
        feedback="good"
    ),
    2:dict(
        post_id=2,
        user_id=2,
        feedback="impossible"
    ),
    3:dict(
        post_id=2,
        user_id=3,
        feedback="good"
    ),
    4:dict(
        post_id=2,
        user_id=1,
        feedback="early"
    ),
}