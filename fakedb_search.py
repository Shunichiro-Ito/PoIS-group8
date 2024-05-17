fake_hiddennode_db={
    1:dict(create_key="就活")
}

fake_wordhidden_db={
    1:dict(
        fromid="就活",
        toid="hidden1",strength=0.25),
    2:dict(
        fromid="就活",
        toid="hidden2",strength=0.25),
    3:dict(
        fromid="就活",
        toid="hidden3",strength=0.25),
    4:dict(
        fromid="就活",
        toid="hidden4",strength=0.25),
}


fake_hiddenhidden_db={
    1:dict(
        fromid="hidden1",
        toid="hidden5",strength=0.5),
    2:dict(
        fromid="hidden2",
        toid="hidden5",strength=0.5),
    3:dict(
        fromid="hidden3",
        toid="hidden5",strength=0.5),
    4:dict(
        fromid="hidden4",
        toid="hidden5",strength=0.5),
    5:dict(
        fromid="hidden1",
        toid="hidden6",strength=0.5),
    6:dict(
        fromid="hidden2",
        toid="hidden6",strength=0.5),
    7:dict(
        fromid="hidden3",
        toid="hidden6",strength=0.5),
    8:dict(
        fromid="hidden4",
        toid="hidden6",strength=0.25),
}

fake_hiddenurl_db={
    1:dict(
        fromid="hidden5",
        toid="url1",strength=0.3),
    2:dict(
        fromid="hidden5",
        toid="url2",strength=0.3),
    3:dict(
        fromid="hidden5",
        toid="url3",strength=0.4),
    4:dict(
        fromid="hidden6",
        toid="url1",strength=0.4),
    5:dict(
        fromid="hidden6",
        toid="url2",strength=0.3),
    6:dict(
        fromid="hidden6",
        toid="url3",strength=0.3),
}

fake_user_response_cache_db={
    1:dict(
        id="1",
        sessionvalue="1",
        querys="就活",
        selectedurl="url1",
        actions="search"),
    2:dict(
        id="2",
        sessionvalue="2",
        querys="進学",
        selectedurl="url2",
        actions="click"),
    3:dict(
        id="3",
        sessionvalue="3",
        querys="就活",
        selectedurl="url3",
        actions="good"),
    4:dict(
        id="4",
        sessionvalue="4",
        querys="生活",
        selectedurl="url1",
        actions="early"),
    5:dict(
        id="5",
        sessionvalue="5",
        querys="勉強",
        selectedurl="url2",
        actions="impossible"),
}

fake_url_db={
    1:dict(
        url_id="url1",
        url="https://www.google.com",
        category="post",
        user_id="None",
        post_id=1
    ),
    2:dict(
        url_id="url2",
        url="https://www.yahoo.com",
        category="user",
        user_id=2,
        post_id=None
    ),
    3:dict(
        url_id="url3",
        url="/posts/",
        category="post",
        user_id=None,
        post_id=2
    ),
}
