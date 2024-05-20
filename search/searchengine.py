from search import nn
from enum import Enum
import sql.crud as crud
net=nn.searchnet()

class searchRange(Enum):
    all = 'all'
    post = 'post'
    user = 'user'

class searcher():

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
            rows=crud.get_urls(net.db)
        elif searchRange=='post':
            rows=crud.get_urls(net.db,type='post')
        elif searchRange=='user':
            rows=crud.get_urls(net.db,type='user')
        urlids=[i['url_id'] for i in rows]
        nnres=net.getresult(wordids,urlids)
        scores=dict([urlids[i],nnres[i]] for i in range(len(urlids)))
        return self.normalizescores(scores)
    
    def query(self,wordids,searchRange=all):
        score=self.nnscore(wordids,searchRange)
        urls=crud.get_urls(net.db,url_ids=score.keys())
        return urls