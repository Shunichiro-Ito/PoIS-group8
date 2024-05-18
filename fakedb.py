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

fake_interest_tag_db={
    1:dict(
        user_id=1,
        tag_id=1
    ),
    2:dict(
        user_id=1,
        tag_id=2
    ),
    3:dict(
        user_id=1,
        tag_id=6
    ),
    4:dict(
        user_id=1,
        tag_id=7
    ),
    5:dict(
        user_id=2,
        tag_id=5
    ),
    6:dict(
        user_id=2,
        tag_id=4
    ),
    7:dict(
        user_id=3,
        tag_id=1
    ),
    8:dict(
        user_id=3,
        tag_id=2
    ),
    9:dict(
        user_id=3,
        tag_id=3
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
    ),
    2:dict(
        post_id=2,
        user_id=3,
    )
}

fake_admin_db={
    1:dict(
        username="admin"
    )
}

fake_category_db={
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

posts_v_tfidf={
    1:dict(
        post_id=1,
        tfidf_0=0.5,
        tfidf_1=0.2,
        tfidf_2=0.9,
        tfidf_3=0.1,
        tfidf_4=0.3,
        tfidf_5=0.4,
        tfidf_6=0.5,
        tfidf_7=0.6,
        tfidf_8=0.7,
        tfidf_9=0.8,
        tfidf_10=0.9,
        tfidf_11=0.1,
        tfidf_12=0.2,
        tfidf_13=0.3,
        tfidf_14=0.4,
        tfidf_15=0.5,
        tfidf_16=0.6,
        tfidf_17=0.7,
        tfidf_18=0.8,
        tfidf_19=0.9,
    ),
    2:dict(
        post_id=2,
        tfidf_0=0.5,
        tfidf_1=0.2,
        tfidf_2=0.9,
        tfidf_3=0.1,
        tfidf_4=0.3,
        tfidf_5=0.4,
        tfidf_6=0.5,
        tfidf_7=0.6,
        tfidf_8=0.7,
        tfidf_9=0.8,
        tfidf_10=0.9,
        tfidf_11=0.1,
        tfidf_12=0.2,
        tfidf_13=0.3,
        tfidf_14=0.4,
        tfidf_15=0.5,
        tfidf_16=0.6,
        tfidf_17=0.7,
        tfidf_18=0.8,
        tfidf_19=0.9,
    )
}

fake_post_writer_init_db={
    1:dict(
        user_id=0,
        post_id=1,
        category_id=1,
        age=20,
        gender="m",
        occupation="admin"
    ),
    2:dict(
        user_id=3,
        post_id=2,
        category_id=1,
        age=20,
        gender="f",
        occupation="clerk"
    )
}

fake_post_writer_dynamic_db={
    1:dict(
        user_id=0,
        post_id=1,
        category_id=1,
        age=20,
        gender="m",
        occupation="admin",
        mbti="INTP"
    ),
    2:dict(
        user_id=3,
        post_id=2,
        category_id=1,
        age=20,
        gender="f",
        occupation="clerk",
        mbti="ISFP"
    )
}

fake_post_reader_db={
    1:dict(
        user_id=2,
        post_id=1,
        feedback="good"
    ),
    2:dict(
        user_id=2,
        post_id=2,
        feedback="impossible"
    ),
    3:dict(
        user_id=3,
        post_id=2,
        feedback="good"
    ),
    4:dict(
        user_id=1,
        post_id=2,
        feedback="early"
    ),
}
