import nn
from enum import Enum
net=nn.searchengine('sql.db')

class searchRange(Enum):
    all = 'all'
    post = 'post'
    user = 'user'

class searcher():
    def __init__(self,dbname):
        self.con=mysql.connect(dbname)

    def __del__(self):
        self.con.close()

    def normalizescores(self,scores,smallIsBetter=0):
        vsmall=0.00001
        if smallIsBetter:
            minscore=min(scores.values())
            return dict([(u,float(minscore)/max(vsmall,l)) for (u,l) in scores.items()])
        else:
            maxscore=max(scores.values())
            if maxscore==0:
                maxscore=vsmall
            return dict([(u,float(c)/maxscore) for (u,c) in scores.items()])

    def nnscore(self,wordids,searchRange=all):
        # Get unique URL IDs as an ordered list
        if searchRange=='all':
            rows=self.con.query('select rowid from urllist') #not ready
        elif searchRange=='post':
            rows=self.con.query('select rowid from urllist where type="post"')
        elif searchRange=='user':
            rows=self.con.query('select rowid from urllist where type="user"')
        urlids=[urlid for urlid in set([row[0] for row in rows])]
        nnres=net.getresult(wordids,urlids)
        scores=dict([urlids[i],nnres[i]] for i in range(len(urlids)))
        return self.normalizescores(scores)
    
    def query(self,wordids,searchRange=all):
        score=self.nnscore(wordids,searchRange)
        postDetails=self.con.query('select * from postlist in(%s)' % ','.join([str(urlid) for urlid in score.keys()]))
        return postDetails