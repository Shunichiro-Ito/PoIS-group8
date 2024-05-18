from math import tanh
from enum import Enum
from sql import crud
#from sql.database import SessionLocal
from sql.schemas import nodes

import fakedb_search


# Sigmoid function
def dtanh(y):
    return 1.0 - y*y

class action(Enum):
    click = 'click'
    good = 'good'
    early = 'early'
    impossible = 'impossible'

# Neural network class
class searchnet:
    """
    Class for neural network
    wordids: list of word ids
    hiddenids of hidden layer 1: list of hidden node ids 
    hiddenids of hidden layer 2: list of hidden node ids
    urls: list of url ids
    
    
    """
    def __init__(self):
        self.db = 
        #SessionLocal()

    def __del__(self):
        #self.db.close()
        pass



#    def maketables(self):
#        self.con.query('create table hiddennode(create_key)')
#        self.con.query('create table wordhidden(fromid, toid, strength)') relational table
#        self.con.query('create table hiddenhidden(fromid, toid, strength)')
#        self.con.query('create table hiddenurl(fromid, toid, strength)')
#        self.con.commit()
    
    def getstrength(self,fromid, toid, layer):
        if layer == 0: res=crud.get_wordhidden(self.db,fromid=fromid,toid=toid)
        elif layer == 1: res=crud.get_hiddenhidden(self.db,fromid=fromid,toid=toid)
        else: res=crud.get_hiddenurl(self.db,fromid=fromid,toid=toid)
        
        #res = self.con.query('select strength from %s where fromid=%d and toid=%d' % (table, fromid, toid)).fetchone()
        if res == None:
            if layer == 0: return -0.2
            if layer == 1: return 0
            if layer == 2: return 0.1
        return res[0]
    
    def setstrength(self, fromid, toid, layer, strength):
        if layer == 0: 
            wordhidden=nodes.wordhidden(fromid=fromid,toid=toid,strength=strength)
            res=crud.update_wordhidden(self.db,wordhidden=wordhidden)
        elif layer == 1: 
            hiddenhidden=nodes.hiddenhidden(fromid=fromid,toid=toid,strength=strength)
            res=crud.update_hiddenhidden(self.db,hiddenhidden=hiddenhidden)
        else: 
            hiddenurl=nodes.hiddenurl(fromid=fromid,toid=toid,strength=strength)
            res=crud.update_hiddenurl(self.db,hiddenurl=hiddenurl)
        

    def generatehiddennode(self, wordids, urls):
        if len(wordids) > 3: return None
        createkey = '_'.join(sorted([str(wi) for wi in wordids]))
        res = crud.get_hiddennode(self.db,create_key=createkey,layer=0)

        if res == None:
            hiddennode1=nodes.hiddennode(create_key=createkey,layer=0)
            hiddennode2=nodes.hiddennode(create_key=hiddennode1.id,layer=1)
            cur = crud.create_hiddennode(self.db,hiddennode=hiddennode1)
            hiddenid1 = cur.id
            cur = crud.create_hiddennode(self.db,hiddennode=hiddennode2)
            hiddenid2=cur.id
            for wordid in wordids:
                self.setstrength(wordid, hiddenid1, 0, 1.0/len(wordids))
            
            self.setstrength(hiddenid1, hiddenid2, 1, 0.1)
            for urlid in urls:
                self.setstrength(hiddenid2, urlid, 2, 0.1)
            self.con.commit()

    def getallhiddenids(self, wordids, urlids):
        l1 = {}
        l2 = {}
        for wordid in wordids:
            cur=crud.get_wordhidden(self.db,fromid=wordid)
            for row in cur: l1[row['toid']] = 1
        for l1id in l1.keys():
            cur = crud.get_hiddenhidden(self.db,fromid=l1id)
            for row in cur: l2[row['toid']] = 1
        for urlid in urlids:
            cur = crud.get_hiddenurl(self.db,toid=urlid)
            for row in cur: l2[row['fromid']] = 1
        for l2id in l2.keys():
            cur = crud.get_hiddenhidden(self.db,toid=l2id)
            for row in cur: l1[row['fromid']] = 1
        return l1.keys(),l2.keys()
    
    def setupnetwork(self, wordids, urlids):
        # nodes of neural network
        self.wordids = wordids
        self.hiddenids1, self.hiddenids2 = self.getallhiddenids(wordids, urlids)
        self.urlids = urlids

        self.ai = [1.0]*len(self.wordids)
        self.ah1 = [1.0]*len(self.hiddenids1)
        self.ah2 = [1.0]*len(self.hiddenids2)
        self.ao = [1.0]*len(self.urlids)

        # matrix of weights between word and url
        self.wi = [[self.getstrength(wordid, hiddenid1, 0) 
                    for hiddenid1 in self.hiddenids1] 
                    for wordid in self.wordids]
        self.wh= [[self.getstrength(hiddenid1, hiddenid2, 1) 
                    for hiddenid2 in self.hiddenids2] 
                    for hiddenid1 in self.hiddenids1]
        self.wo = [[self.getstrength(hiddenid2, urlid, 2) 
                    for urlid in self.urlids] 
                    for hiddenid2 in self.hiddenids2]
        
    def feedforward(self):
        # input layer
        for i in range(len(self.wordids)):
            self.ai[i] = 1.0

        # hidden layer 1
        for j in range(len(self.hiddenids1)):
            sum = 0.0
            for i in range(len(self.wordids)):
                sum += self.ai[i] * self.wi[i][j]
            self.ah1[j] = tanh(sum)

        # hidden layer 2
        for j in range(len(self.hiddenids2)):
            sum = 0.0
            for i in range(len(self.hiddenids1)):
                sum += self.ah1[i] * self.wh[i][j]
            self.ah2[j] = tanh(sum)

        # output layer
        for k in range(len(self.urlids)):
            sum = 0.0
            for j in range(len(self.hiddenids2)):
                sum += self.ah2[j] * self.wo[j][k]
            self.ao[k] = tanh(sum)
        return self.ao[:]

    def getresult(self, wordids, urlids):
        self.setupnetwork(wordids, urlids)
        return self.feedforward()

    def backPropagate(self, targets, N=0.4):
        # calculate errors for output
        output_deltas = [0.0]*len(self.urlids)
        for k in range(len(self.urlids)):
            error = targets[k] - self.ao[k]
            output_deltas[k] = dtanh(self.ao[k]) * error

        # calculate errors for hidden layer 2
        hidden_deltas2 = [0.0]*len(self.hiddenids2)
        for j in range(len(self.hiddenids2)):
            error = 0.0
            for k in range(len(self.urlids)):
                error += output_deltas[k] * self.wo[j][k]
            hidden_deltas2[j] = dtanh(self.ah2[j]) * error

        # calculate errors for hidden layer 1
        hidden_deltas1 = [0.0]*len(self.hiddenids1)
        for j in range(len(self.hiddenids1)):
            error = 0.0
            for k in range(len(self.hiddenids2)):
                error += hidden_deltas2[k] * self.wh[j][k]
            hidden_deltas1[j] = dtanh(self.ah1[j]) * error

        # update output weights
        for j in range(len(self.hiddenids2)):
            for k in range(len(self.urlids)):
                change = output_deltas[k] * self.ah2[j]
                self.wo[j][k] += N * change

        # update hidden layer 2 weights
        for j in range(len(self.hiddenids1)):
            for k in range(len(self.hiddenids2)):
                change = hidden_deltas2[k] * self.ah1[j]
                self.wh[j][k] += N * change

        # update hidden layer 1 weights
        for i in range(len(self.wordids)):
            for j in range(len(self.hiddenids1)):
                change = hidden_deltas1[j] * self.ai[i]
                self.wi[i][j] += N * change

    def trainquery(self, wordids, urlids, selectedurl, action:action='click'):
        # generate a hidden node if necessary
        self.generatehiddennode(wordids, urlids)
        self.setupnetwork(wordids, urlids)
        self.feedforward()
        targets = [0.0]*len(urlids)
        targets[urlids.index(selectedurl)] = 1.0
        if action == 'click':
            error = self.backPropagate(targets,0.3)
        elif action == 'good':
            error = self.backPropagate(targets,0.4)
        elif action == 'early':
            error = self.backPropagate(targets,0.5)
        elif action == 'impossible':
            error = self.backPropagate(targets,-0.2)
        self.updatedatabase()

    def updatedatabase(self):
        # set them to database
        for i in range(len(self.wordids)):
            for j in range(len(self.hiddenids1)):
                self.setstrength(self.wordids[i], self.hiddenids1[j], 0, self.wi[i][j])
        for j in range(len(self.hiddenids1)):
            for k in range(len(self.hiddenids2)):
                self.setstrength(self.hiddenids1[j], self.hiddenids2[k], 1, self.wh[j][k])
        for j in range(len(self.hiddenids2)):
            for k in range(len(self.urlids)):
                self.setstrength(self.hiddenids2[j], self.urlids[k], 2, self.wo[j][k])
        self.con.commit()
