# the whole process: 
from collections import Counter
import numpy as np
import datetime

from sql_run import crud
import dependencies

def cal_jaccard_sim(set1, set2):
    intersection = set1.intersection(set2)
    union = set1.union(set2)
    jaccard_similarity = len(intersection) / len(union)
    return jaccard_similarity

# input: one user clicks homepage
# output: candidate_text(dict)
# tips:     
# show key(title)
# show value(sim) in 0-1
def main(current_user):
    # tag of age: 
    # 0: 15-18; 1: 18-22; 2: 22-25; 3: 25-30; 4: 30-50; 5: 50-59
    # all tags:
    # 0: age area; 1: gender; 2: occupation(main); 3: occupation(other)
    age_list = [15, 18, 22, 25, 30, 50]

    u1 = {0: '2', 1: 'f', 2: '新卒入社', 3: '人事', 4: '編集', 5: 'マーケティング'}
    u2 = {0: '3', 1: 'm', 2: '会社員', 3: '公務員', 4: 'クラブ会員'} 
    u3 = {0: '1', 1: 'm', 2: '大学生'}  # 慶應義塾/早稲田
    u4 = {0: '5', 1: 'm', 2: ''} # ?
    u5 = {0: '2', 1: 'f', 2: '新卒入社', 3: '制作'} 
    u6 = {0: '4', 1: 'm', 2: '中途入社', 3: '総務', 4: '管理', 5: 'f'}
    u7 = {0: '0', 1: 'm', 2: '大学生', 3: '高校生', 4: '受験', 5: 'f'}
    u8 = {0: '5', 1: 'f', 2: '専業主婦'} 
    u9 = {0: '', 1: 'f', 2: ''}  # ?
    u10 = {0: '3', 1: 'm', 2: '会社員', 3:'中途入社', 4: 'f'} 
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

    current_user     
    # data = crud.get_users(Session(), all=True)
    # first_key, first_value = list(urrent_user.items())[j]
    # key, value = next(iter(first_value.items())) # gender, occupation, birth, interested_tag
    
    # calculate user's age area
    birth_date = current_user['birth']
    current_date = date.today()
    age = current_date.year - birth_date.year
    flag = True
    age_range = 0
    for i in range(5):
        if age < age_list[i] and age >= age_list[i + 1]:
            flag = False
            age_range = i
            continue
    if flag == True: age_range = 5

    # get user's other information
    gender = current_user['gender']
    if gender == "男性":
        gender = 'm'
    else:
        gender = 'f'

    occupation = current_user['occupation']
    # 大分类(temporary):  新卒入社， 会社員， 大学生， 専業主婦， 中途入社
    
    interested_tags = dependencies.show_tags(Session(), current_user['user_id'])
    if len(interested_tags) < 5:
        popular_tag = ['就活', '仕事', '恋愛', '引越し', 'お花見、春'] #
        for i in range(5 - len(interested_tags)):
            interested_tags.append(popular_tag[i])

    current_user_profile = {0: age_range, 1: gender, 2: occupation, 3: interested_tags}
    set2 = set(current_user_profile.values())

    # 先filter tag（若个数不够，则展示常用的tag）
    # db: 收集user感兴趣的tag，若不足5个，则补足-> interested_tag=list[0~4]
    # 计算new user和10个分类的相似度
      #db：获取new user的profile
    # 按照相似度高低选取想要的tag
    sorted_sim = {}
    for i in range(len(List)):
        set1 = set(List[i].values())
        sim = cal_jaccard_sim(set1, set2)
        sorted_sim.update({'i': sim})
    # sorted_sim为dict, key为kmeans类别，value为计算的相似度
    sorted_sim = dict(sorted(sorted_sim.items(), key=lambda item: item[1], reverse = True))
    
    final_recommend_text_list = []
    for i in interested_tag:
        for j in range(10):
            key, value = list(sorted_sim.items())[j]
            for k in range(all text as dict):
                candidate_text = {}
                if k[tag] == i and k[kmeans] == key:
                    candidate_text.update({'k[title]': key})
                # 暂时无随机
                # if candidate_text != []:
                #     random_candidate_text = random.choice(candidate_text.items())
                # final_recommend_text_list.update(random_candidate_text.keys, )
                if len(candidate_text) == 5:
                    continue
    
    # for i in range(5):
    #     key, value = list(candidate_text.items())[i]
    # print(candidate_text)

    return candidate_text
    


#if __name__ == "__main__":
#    main()