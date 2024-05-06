from datetime import date

fake_users_db = {
    "johndoe": dict(
        username="johndoe",
        displayed_name="johndoe",
        full_name="John Doe",
        email="johndoe@example.com",
        hashed_password="$2a$12$aCCjSgmDLA2swqpLU3ORtuE71DmWaDoU82C.5H2tMXU65rh561kvK", #toEncode
        birth=date(2004,1,1),
        gender="m",
        occupation="student",
        mbti="ESTP",
        interested_tag=["就活","勉強"]
    ),
    "alice": dict(
        username="alice",
        displayed_name="alice",
        full_name="Alice Wonderson",
        email="alice@example.com",
        hashed_password="fakehashedsecret2",
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
        content="Failed!!!",
        age=20,
        post_date=date(2024,5,4),
        tag_id=["職場"],
        anonymous=True,
        good=10,
        impossible=2,
        early=0
    )
}

fake_post_user_db={
    1:dict(
        post_id=1,
        user_id="johndoe",
        feature_vector=[0,1,0.9,0.2,0.5]
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
}