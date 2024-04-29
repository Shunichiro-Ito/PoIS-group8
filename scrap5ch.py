import requests
from bs4 import BeautifulSoup
import csv
import re
import os

def extractLinks(soup):
    for element in soup.body.find_all('a'):
        category=element.find_previous_sibling('b')
        if category:
            link=element.get('href')
            name=element.get_text()
            yield {'category':category.get_text(),'name':name,'link':link}

def createBoardmap(filename='boardmap.csv',base_url='https://www2.5ch.net/5ch.html'):
    res = requests.get(base_url)
    soup = BeautifulSoup(res.text, 'html.parser')

    with open(filename, 'w', newline='') as csvfile:
        fieldnames =['category',
                    'name',
                    'link'
                    ]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()

        # iterate over links
        for i in extractLinks(soup):
            writer.writerow(i)

def extractPosts(url,post_limit,screen):
    url=url+'subback.html'
    res = requests.get(url)
    soup = BeautifulSoup(res.text, 'html.parser')
    
    posts=soup.find(id='trad')
    if posts:
        posts=posts.find_all('a')
    else:
        posts=[]

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
            postUrl=post.get('href')
            if postUrl.endswith('/l50'):
                postUrl=postUrl[:-4]

            yield {'link':postUrl,
                'title':title,
                'article_no':article_no}
    
def extractArticle(postUrl,article_limit):

    res = requests.get(postUrl)
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
        
def extractDataToTxt(filename='boardmap.csv',row_limit=1000,post_limit=9999,article_limit=9999,screenOut=10):
    with open(filename,'r') as bdmap:
        reader=csv.DictReader(bdmap)
        rows=list(reader)

    for r in range(len(rows)):
        row=rows[0]
        postsUrl=row['link']
        Posts=extractPosts(postsUrl,post_limit,screenOut)
        directory=f'5ch/{"-".join([row['category'],row['name']])}/'

        if not os.path.isdir(directory):
            os.mkdir(directory)

        for post in Posts:
            print(f"{post['title']} {post['link']}\n")
            articles=extractArticle('/'.join([postsUrl,post['link']]),
                        article_limit)
            postfilename=f"{directory}{post['link']}.txt"
            if not os.path.isfile(postfilename):
                with open(postfilename,'w') as postfile:
                    postfile.write(post['title'])
                    postfile.write(f"Article No: {post['article_no']}")
                    for article in articles:
                        postfile.write(f"{article['username']}\n{article['content']}")

        del(rows[0])
        with open(filename,'w') as bdmap:
            fieldnames =['category',
                        'name',
                        'link'
                        ]
            writer = csv.DictWriter(bdmap, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(rows)

        row_limit-=1
        if row_limit==0:
            break