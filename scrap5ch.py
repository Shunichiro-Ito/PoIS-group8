import requests
from bs4 import BeautifulSoup
import csv
import re
import os
import time
import random
import sys
csv.field_size_limit(sys.maxsize)

def make_request_with_retry(url, max_retries=3, timeout=5):
    retries = 0
    while retries < max_retries:
        try:
            interval=random.uniform(0,1)
            time.sleep(interval)
            response = requests.get(url, timeout=timeout)
            if response.status_code == 200:
                return response
        except requests.Timeout:
            print(f"Request timed out. Retrying ({retries + 1}/{max_retries})...")
        except requests.RequestException as e:
            print(f"Request failed: {e}")
        
        retries += 1  # Wait for a short duration before retrying
    
    print(f"Failed to get response from {url} after {max_retries} retries.")
    with open('failUrl.csv','w') as fail:
        writer=csv.writer(fail)
        writer.writerow(url)
    return None

def extractLinks(soup):
    for element in soup.body.find_all('a'):
        category=element.find_previous_sibling('b')
        if category:
            link=element.get('href')
            name=element.get_text()
            yield {'category':category.get_text(),'name':name,'link':link}

def createBoardmap(filename='boardmap.csv',base_url='https://www2.5ch.net/5ch.html'):
    res = make_request_with_retry(base_url)
    soup = BeautifulSoup(res.text, 'html.parser')

    with open(filename, 'w', newline='',encoding='utf-8') as csvfile:
        fieldnames =['category',
                    'name',
                    'link'
                    ]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()

        # iterate over links
        for i in extractLinks(soup):
            writer.writerow(i)

def updateBoardmap(rows,bdmapfilename):
    del(rows[0])
    with open(bdmapfilename,'w',encoding='utf-8') as bdmap:
        fieldnames =['category',
                    'name',
                    'link'
                    ]
        writer = csv.DictWriter(bdmap, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

def updateTagFile(filename,newRow):
    with open(filename,'r',encoding='utf-8') as tagfile:
        reader = csv.DictReader(tagfile)
        rows=list(reader)

    rows.append(newRow)

    with open(filename,'w',encoding='utf-8') as tagfile:
        fieldnames =['category',
                     'tag',
                     'category link',
                     'post_link',
                     'post_title',
                     'article_no',
                     'post_no',
                     'content'
                     ]
        writer = csv.DictWriter(tagfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

def extractPosts(url,post_limit,screen):
    Subbackurl=url+'subback.html'
    res = make_request_with_retry(Subbackurl)
    if res:
        soup = BeautifulSoup(res.text, 'html.parser')
        posts=soup.find(id='trad')
        base=soup.find('base')
    else:
        posts=[]
        base=None

    if posts:
        posts=posts.find_all('a')

    if base:
        base=base.get('href')[1:-1]
        
        base=''.join([url.split('.net')[0],
                       '.net',
                       '/',
                       base])

    post_limit=min(post_limit,len(posts))
    for i in range(post_limit):
        post=posts[i]

        compiler=re.compile(r'\d+: (.*) \((\d+)\)')
        values=compiler.match(post.get_text())
        if values:
            title,article_no=values.groups()
        else:
            title,article_no=None,0
            
        if screen<int(article_no):
            post_no=post.get('href')
            if post_no.endswith('/l50'):
                post_no=post_no[:-4]

            if base:
                postUrl='/'.join([base,post_no])

            yield {'post_link':postUrl,
                'post_title':title,
                'article_no':article_no,
                'post_no':post_no
                }
    
def extractArticle(postUrl,article_limit):

    res = make_request_with_retry(postUrl)
    if res:
        soup = BeautifulSoup(res.text, 'html.parser')
        
        articles=soup.find_all('article')
        article_limit=min(article_limit,len(articles))
        for i in range(article_limit):
            article=articles[i]
        
            username=article.find('span','postusername')
            if username:
                username=username.get_text()
            
            content=article.find('section','post-content')
            if content:
                content=content.get_text()
            
            yield {'username':username,
                'content':content}
    else:
        yield {'username':'',
            'content':''}
        
def extractDataToTxt(filename='boardmap.csv',row_limit=1000,post_limit=9999,article_limit=9999,screenOut=10):

    with open(filename,'r',encoding='utf-8') as bdmap:
        reader=csv.DictReader(bdmap)
        rows=list(reader)

    print(rows)

    for r in range(len(rows)):
        
        row=rows[0]
        postsUrl=row['link']
        Posts=extractPosts(postsUrl,post_limit,screenOut)
        tagFile=f'5ch/{"-".join([row["category"],row["name"]])}.csv'

        categoryInfo={'category':row["category"],
                      'tag':row["name"],
                      'category link':postsUrl}

        print(f"{r}: {categoryInfo}\n")

        if not os.path.isfile(tagFile):
            with open(tagFile, 'w', newline='',encoding='utf-8') as tagcsvfile:
                postFieldnames =['category',
                            'tag',
                            'category link',
                            'post_link',
                            'post_title',
                            'article_no',
                            'post_no',
                            'content'
                            ]
                writer = csv.DictWriter(tagcsvfile, fieldnames=postFieldnames)

                writer.writeheader()

        for post in Posts:
            tagFileRow=categoryInfo.copy()
            articles=extractArticle(post['post_link'],
                        article_limit)
            
            tagFileRow.update(post)
            content=[]
            
            for article in articles:
                counter+=1
                content.append(article)

            tagFileRow.update({'content':str(content)})
            updateTagFile(tagFile,tagFileRow)

        updateBoardmap(rows,filename)

        row_limit-=1
        if row_limit==0:
            break
