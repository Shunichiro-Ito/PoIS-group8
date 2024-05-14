from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import numpy as np
import pandas as pd
import os
import re
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.pipeline import make_pipeline, make_union
from sklearn.decomposition import TruncatedSVD
from tqdm._tqdm_notebook import tqdm_notebook as tqdm
tqdm.pandas()
from IPython.core.interactiveshell import InteractiveShell
InteractiveShell.ast_node_interactivity = "all"
import warnings
warnings.filterwarnings('ignore')


def pre_preprocess(x):
    return str(x).lower()

def rm_spaces(text):
    spaces = ['\u200b', '\u200e', '\u202a', '\u2009', '\u2028', '\u202c', '\ufeff', '\uf0d8', '\u2061', '\u3000', '\x10', '\x7f', '\x9d', '\xad',
              '\x97', '\x9c', '\x8b', '\x81', '\x80', '\x8c', '\x85', '\x92', '\x88', '\x8d', '\x80', '\x8e', '\x9a', '\x94', '\xa0',
              '\x8f', '\x82', '\x8a', '\x93', '\x90', '\x83', '\x96', '\x9b', '\x9e', '\x99', '\x87', '\x84', '\x9f',
             ]
    for space in spaces:
            text = text.replace(space, ' ')
    return text

def remove_urls(x):
    x = re.sub(r'(https?://[a-zA-Z0-9.-]*)', r'', x)

    # original
    x = re.sub(r'(quote=\w+\s?\w+;?\w+)', r'', x)
    return x

def clean_html_tags(x, stop_words=[]):
    for r in html_tags:
        x = x.replace(r, '')
    for r in empty_expressions:
        x = x.replace(r, ' ')
    for r in stop_words:
        x = x.replace(r, '')
    return x

def replace_num(text):
    text = re.sub('[0-9]{5,}', '', text)
    text = re.sub('[0-9]{4}', '', text)
    text = re.sub('[0-9]{3}', '', text)
    text = re.sub('[0-9]{2}', '', text)
    return text

def get_url_num(x):
    pattern = "https?://[\w/:%#\$&\?\(\)~\.=\+\-]+"
    urls = re.findall(pattern, x)
    return len(urls)


def clean_puncts(x):
    for punct in puncts:
        x = x.replace(punct, f' {punct} ')
    return x

#zenkaku = '０,１,２,３,４,５,６,７,８,９,（,）,＊,「,」,［,］,【,】,＜,＞,？,・,＃,＠,＄,％,＝'.split(',')
#hankaku = '0,1,2,3,4,5,6,7,8,9,q,a,z,w,s,x,c,d,e,r,f,v,b,g,t,y,h,n,m,j,u,i,k,l,o,p'.split(',')

def clean_text_jp(x):
    x = x.replace('。', '')
    x = x.replace('、', '')
    x = x.replace('\n', '') # 改行削除
    x = x.replace('\t', '') # タブ削除
    x = x.replace('\r', '')
    x = re.sub(re.compile(r'[!-\/:-@[-`{-~]'), ' ', x)
    x = re.sub(r'\[math\]', ' LaTex math ', x) # LaTex削除
    x = re.sub(r'\[\/math\]', ' LaTex math ', x) # LaTex削除
    x = re.sub(r'\\', ' LaTex ', x) # LaTex削除
    #for r in zenkaku+hankaku:
    #    x = x.replace(str(r), '')
    x = re.sub(' +', ' ', x)
    return x

def preprocess(data):
    data = pre_preprocess(data)
    data = rm_spaces(data)
    data = remove_urls(data)
    data = clean_puncts(data)
    data = replace_num(data)
    data = clean_html_tags(data, stop_words=other)
    data = clean_text_jp(data)
    return data

def get_sentence_features(train, col):
    train[col + '_num_chars'] = train[col].apply(len)
    train[col + '_num_words'] = train[col].apply(lambda x: len(x.split()))
    train[col + '_num_unique_words'] = train[col].apply(lambda comment: len(set(w for w in comment.split())))
    return train

def main():
    tagger = MeCab.Tagger('-r/dev/null -d/home/hoge/mydic')

    puncts = [',', '.', '"', ':', ')', '(', '-', '!', '?', '|', ';', "'", '$', '&', '/', '[', ']', '>', '%', '=', '#',
              '*', '+', '\\', '•', '~', '@', '£',
              '·', '_', '{', '}', '©', '^', '®', '`', '<', '→', '°', '€', '™', '›', '♥', '←', '×', '§', '″', '′', 'Â',
              '█', '½', 'à', '…', '\n', '\xa0', '\t',
              '“', '★', '”', '–', '●', 'â', '►', '−', '¢', '²', '¬', '░', '¶', '↑', '±', '¿', '▾', '═', '¦', '║', '―',
              '¥', '▓', '—', '‹', '─', '\u3000', '\u202f',
              '▒', '：', '¼', '⊕', '▼', '▪', '†', '■', '’', '▀', '¨', '▄', '♫', '☆', 'é', '¯', '♦', '¤', '▲', 'è', '¸',
              '¾', 'Ã', '⋅', '‘', '∞', '«',
              '∙', '）', '↓', '、', '│', '（', '»', '，', '♪', '╩', '╚', '³', '・', '╦', '╣', '╔', '╗', '▬', '❤', 'ï', 'Ø',
              '¹', '≤', '‡', '√', ]

    html_tags = ['<p>', '</p>', '<table>', '</table>', '<tr>', '</tr>', '<ul>', '<ol>', '<dl>', '</ul>', '</ol>',
                 '</dl>', '<li>', '<dd>', '<dt>', '</li>', '</dd>', '</dt>', '<h1>', '</h1>',
                 '<br>', '<br/>', '<strong>', '</strong>', '<span>', '</span>', '<blockquote>', '</blockquote>',
                 '<pre>', '</pre>', '<div>', '</div>', '<h2>', '</h2>', '<h3>', '</h3>', '<h4>', '</h4>', '<h5>',
                 '</h5>',
                 '<h6>', '</h6>', '<blck>', '<pr>', '<code>', '<th>', '</th>', '<td>', '</td>', '<em>', '</em>']

    empty_expressions = ['&lt;', '&gt;', '&amp;', '&nbsp;',
                         '&emsp;', '&ndash;', '&mdash;', '&ensp;'
                                                         '&quot;', '&#39;']

    other = ['span', 'style', 'href', 'input']

    # read text_data
    content_set = []
    num = 0

    current_path = '.../text_data/'
    for filename in os.listdir(current_path):
        if filename.endswith('.txt'):
            file_path = os.path.join(current_path, filename)
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()
                content_set.append(content)
                num += 1

    df = pd.DataFrame(columns=['text'])
    df.text = pd.DataFrame(content_set)

    for i in range(80):
        df['text'].iloc[i] = preprocess(df['text'].iloc[i])

    df['wakati_text'] = df['text'].progress_apply(lambda x: ' '.join(tok.mecab_tokenizer(x)))

    df = get_sentence_features(df, 'wakati_text')

    # Tfidf-Vectorization
    n_components = 20
    col_num = n_components * 2
    SEED = 1129

    word_vectorizer = make_pipeline(
        TfidfVectorizer(sublinear_tf=True,
                        strip_accents='unicode',
                        analyzer='word',
                        token_pattern=r'\w{1,}',
                        stop_words='english',
                        ngram_range=(1, 2),
                        max_features=20000),
        TruncatedSVD(n_components=n_components, random_state=SEED)
    )

    char_vectorizer = make_pipeline(
        TfidfVectorizer(sublinear_tf=True,
                        strip_accents='unicode',
                        analyzer='char',
                        stop_words='english',
                        ngram_range=(1, 4),
                        max_features=50000),
        TruncatedSVD(n_components=n_components, random_state=SEED)
    )

    wakati_text_wd = word_vectorizer.fit_transform(df['wakati_text']).astype(np.float32)
    wakati_text_ch = char_vectorizer.fit_transform(df['wakati_text']).astype(np.float32)

    X = np.concatenate([wakati_text_wd, wakati_text_ch], axis=1)
    X = pd.DataFrame(X, columns=['text_wd_tfidf_svd_{}'.format(i) for i in range(col_num)])

    df = pd.concat([df, X], axis=1)

    df.to_csv('/text_data/df.csv', index=False)

if __name__ == "__main__":
    main()

