# recommender - second phase
# content-based (cosine similarity)

# as new post is added, immediately cal its Tf-idf

import numpy as np
import pandas as pd

from routers import posts
import preprocessing
import dependencies
from sql_run import crud

def process_new_text():
    # ? 数据库中PostIn无id?
    # output: list
    data_content = routers.posts.submit_post.new_post[content]
    data_id = routers.posts.submit_post.new_post[post_id]
    X = np.concatenate([data_id, data_content], axis=1)
    df = pd.DataFrame(X, columns=['id','text'])
    df_processed = preprocessing.Tfidf_Vectorization(df)
    df_processed = df_processed.values.tolist()
    return df_processed

def get_feedback():
    #class Feedback(Enum):
    # good="good"
    # early="early"
    # impossible="impossible"

    # ? 获取某个用户的所有feedback，对应post(id, title, content, tf-idf)
    user_feedback = routers.posts.feedback.[feedback]
    if user_feedback == 'good':
        user_feedback = 1
    if user_feedback == 'early':
        user_feedback = 0
    if user_feedback == 'impossible':
        user_feedback = -1


def cosine_similarity(vector1, vector2):
    dot_product = np.dot(vector1, vector2)
    norm_vector1 = np.linalg.norm(vector1)
    norm_vector2 = np.linalg.norm(vector2)
    cosine_sim = dot_product / (norm_vector1 * norm_vector2) 
    return cosine_sim

def get_recommend_text():
    # 遍历找到post的feedback是1的-》顺延到是0
    # 遍历tf-idf
    get_feedback() #???
    user_preference_vector = np.mean(useful_articles_tfidf, axis=0)

    interested_tags = dependencies.show_tags(Session(), current_user['user_id'])
    if len(interested_tags) < 5:
        # (modified) based on the db contents
        popular_tag = ['就活', '仕事', '恋愛', '引越し', 'お花見、春']
        for i in range(5 - len(interested_tags)):
            interested_tags.append(popular_tag[i])

    candidate_dict = {}
    final_recommend_text = {}
    for i in range(len(interested_tag)):
        # get all?
        all_posts = crud.get_posts(Session(),skip=0,limit=1000, anonymousIncluded=True)
        for j in range(len(all_posts)):
            if all_posts['tag_id'] == interested_tag[i]:            
                candidate_vector = crud.get_tfidf(Session(), post_id)
                cos_sim = cosine_similarity(candidate_vector, user_preference_vector)
                candidate_dict.update({'i': all_posts['post_id'], all_posts['post_title'], all_posts['post_content'], cos_sim})
    
        sorted_candidate_turple = sorted(candidate_dict.items(), key=lambda item: item[1]['cos_sim'], reverse=True)
        max_key, max_value = sorted_candidate_turple[0]
        final_recommend_text.update({'i': max_value[1], max_value[3]})
    return final_recommend_text



