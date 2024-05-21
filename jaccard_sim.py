# recommender - first phase
# user (group) similarity

from collections import Counter
import numpy as np
from datetime import date,datetime
import pandas as pd
from models.posts import DisplayPost

from sql import crud
import dependencies
from dependencies import db
def cal_jaccard_sim(set1, set2):
    intersection = set1.intersection(set2)
    union = set1.union(set2)
    jaccard_similarity = len(intersection) / len(union)
    return jaccard_similarity

def read_original_data():
    # df = pd.read_csv('D:\\final_intergrated_text_for_DB.csv')  
    df = pd.read_csv('final_intergrated_text_for_DB2.csv')
    return df

# input: one user clicks homepage
# output: candidate_text(dict)
# tips:     
# show key(title)
# show value(sim) in 0-1
def main(current_user):
    df = read_original_data()
    df['tag_id'] = df['tag_id'].astype(float)
    
    # tag of age: 
    # 0: 15-18; 1: 18-22; 2: 22-25; 3: 25-30; 4: 30-50; 5: 50-59
    # all tags:
    # 0: age area; 1: gender; 2: occupation(main); 3: occupation(other)
    u1 = {0: '5', 1: 'f', 2: '専業主婦'}
    u2 = {0: '0', 1: 'm', 2: '大学生', 3: '高校生', 4: '1', 5: 'f'} 
    u3 = {0: '2', 1: 'm', 2: '会社員', 3: '3', 4: 'f', 5: '中途入社', 6: '新卒入社', 7: '会社員', 8: '人事', 9: '事務', 10: '製造業', 11: '営業'}  
    u4 = {0: '2', 1: 'f', 2: '3', 3: '新卒入社', 4: 'マーケティング', 5: '編集', 6: '営業', 7: '会社員'} 
    u5 = {0: '2', 1: 'f', 2: '新卒入社', 3: '制作', 4: '3'} 
    u6 = {0: '5', 1: 'm'}
    u7 = {0: '2', 1: '3', 2: '4', 3: 'm', 4: 'f', 5: '会社員'}
    u8 = {0: '2', 1: '3', 2: '4', 3: 'f', 4: 'm', 5: '広告', 6: '管理', 7: 'ITエンジニア', 8: 'クリエイティブ', 9: 'サービス', 10: '医療・福祉', 11: '販売', 12: '会社員'} 
    u9 = {0: '0', 1: '1', 2: 'm', 3: 'f'}  
    u10 = {0: '4', 1: 'm', 2: 'f', 3: 'm', 4: '両親'}

    List = []
    List.append(u1)
    List.append(u2)
    List.append(u3)
    List.append(u4)
    List.append(u5)
    List.append(u6)
    List.append(u7)
    List.append(u8)
    List.append(u9)
    List.append(u10)
     
    # data = crud.get_users(Session(), all=True)
    # first_key, first_value = list(urrent_user.items())[j]
    # key, value = next(iter(first_value.items())) # gender, occupation, birth, interested_tag
    
    # user - age area
    birth_date = current_user.birth
    current_date = date.today()
    age = current_date.year - birth_date.year
    # i 5个取值（年龄段的开头），6个年龄段
    flag = True
    age_range = 0
    age_list = [15, 18, 22, 25, 30, 50]
    for i in range(5):
        if age < age_list[i + 1] and age >= age_list[i]:
            flag = False
            age_range = i
            continue
    if flag == True:
        age_range = 5

    # user - gender
    gender = current_user.gender
    if gender == "男性":
        gender = 'm'
    else:
        gender = 'f'
    
    # user - occupation
    occupation = current_user.occupation

    # user - 大分类(temporary):  新卒入社， 会社員， 大学生， 専業主婦， 中途入社,  両親 
    # if age_list == 1:
    #     general_occupation == "高校生"
    # if age_list == 1:
    #     general_occupation == "大学生"
    # if age_list == 2:
    #     general_occupation == "新卒入社"
    # if age_list == 3 or age_list == 4:
    #     general_occupation == "会社員/中途入社"
    # if age_list == 5  and gender == 'f':
    #     general_occupation == "専業主婦"
    # general_occupation = current_user['general_occupation']
    
    # user - interesd tags
    # db: 收集user感兴趣的tag，若不足5个，则补足热门tag-> interested_tag=list[0~4]
    interested_tags = []
    interested_tags_original = dependencies.show_tags(db=db, user = current_user)
    for i in range(len(interested_tags_original)):
        key, value = list(interested_tags_original.items())[i]
        if value['tag_id'] == 4:
            value['tag_id'] = '就活'
        if value['tag_id'] == 5:
            value['tag_id'] = '仕事'
        interested_tags.append(value['tag_id'])
            
    popular_tag=crud.get_categories(db=db)
    #popular_tag = ['就活', '仕事', '恋愛', '引越し', 'お花見、春', 'キャンプ', '大学生活']
    i = 0
    if len(interested_tags) < 5:
        res = 5 - len(interested_tags)
        for j in range(len(popular_tag)):
            if popular_tag[j] not in interested_tags:
                interested_tags.append(popular_tag[j])
                i += 1
            if i == res:
                break
        
    current_user_profile = {0: age_range, 1: gender, 2: occupation}
    set2 = set(current_user_profile.values())

    # 计算new user和10个分类的相似度
    sorted_sim = {}
    for i in range(len(List)):
        set1 = set(List[i].values())
        sim = cal_jaccard_sim(set1, set2)
        sorted_sim.update({i: sim})
    # sorted_sim为dict, key为kmeans类别，value为计算的相似度
    sorted_sim = dict(sorted(sorted_sim.items(), key = lambda item: item[1], reverse = True))
    
    # 提取属于相似度最高的kmeans（若为空则顺延至下一个）组且tag符合兴趣的text
    final_recommend_text_dict = {}
    output_list = []
    for i in interested_tags:
        for j in range(10):
            key, value = list(sorted_sim.items())[j]
            max_len = 0
            current_max_text = {}
            
            for k in range(len(df['title'])):
                # 随机 -> 选文章长度最长
                if df.loc[k, 'tag'] == i and df.loc[k, 'kmeans'] == key:
                    max_len = max(max_len, len(df.loc[k, 'content']))
                    if len(df.loc[k, 'content']) == max_len:
                        current_max_text = {df.loc[k, 'title']: value}
                        #output=DisplayPost(**dict(df.loc[k]),
                        #                    **{"score":value})
                                           
            if max_len != 0:
                final_recommend_text_dict.update(current_max_text)
                merge_dict = final_recommend_text_dict.copy()
                for index, row in df.iterrows():
                    if row['title'] in merge_dict.keys():
                        
                        row['post_date']=datetime.strptime(row['post_date'],'%d/%m/%Y').date()
                        row['tag_id']=[row['tag']]
                        out=DisplayPost(**dict(row),
                                        **{"score":merge_dict[row['title']]})
                        print(out)
                        output_list.append(out)
                        
                output_list
                break

        

                
    
    # for i in range(5):
    #     key, value = list(candidate_text.items())[i]
    # print(candidate_text)
    return output_list