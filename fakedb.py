from datetime import date


fake_users_db = {
    "johndoe": dict(
        username="johndoe",
        displayed_name="johndoe",
        full_name="John Doe",
        email="johndoe@example.com",
        hashed_password="fakehashedsecret",
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
    "E2BGPDF4t4":dict(
        post_id="E2BGPDF4t4",
        content="Failed!!!",
        age=20,
        tag_id=["職場"],
        anonymous=True,
        good=10,
        impossible=2,
        early=0
    )
}