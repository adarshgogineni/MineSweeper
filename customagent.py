import numpy as np
import graphics
import random
import opennegb
import custompred

"""
class box:
    def __init__(self,state,neg_mine):
        self.state = state
        self.neg_mine = neg_mine
        self.neg_Notmine = 8 - neg_mine
        self.disc_mine = []
        self.disc_safe = []
    def discbox_mine(self, i , j):
        if(len(self.disc_mine) != 8):
            self.disc_mine.append((i,j))
    def discbox_safe(self, i , j):
        if(len( self.disc_safe) !=):
            self.disc_safe.append((i,j))



def up(ival, jval,n):
    if(ival ==0):
        return None
    return [ival-1, jval]
def down(ival, jval,n):
    if(ival <n-1):
        return [iva+1, jval]
    return None
def left(ival,jval,n):
        if(jval >0):
            return [ival , jval -1]
        return
        None
def right(ival, jval, n ):
    if(jval<n-1):
        return[ival, jval+1]
    return None
def upleft(ival, jval , n):
    if( up(ival,jval,n) != None and left(ival,jval,n) != None):
        return[ival-1, jval-1]
    return None
def upright(ival, jval , n):
    if( up(ival,jval,n) != None and right(ival,jval,n) != None):
        return[ival-1, jval+1]
    return None
def downleft(ival, jval, n):
    if( down(ival,jval,n) != None and left(ival,jval,n) != None):
        return[ival+1, jval-1]
    return None
def downright(ival, jval, n):
    if( down(ival,jval,n) != None and right(ival,jval,n) != None):
        return[ival+1, jval+1]
    return None
"""

#In this algorithm we are keeping track of the boxed already discovered to find the borderline boxes.
def get_smallest(bbox_rank):
    s = -1
    index = -1
    for box in bbox_rank:
        if( s == -1):
            s = box[1]
            index = box[0]
            continue
        if(box[1] < s):
            s = box[1]
            index = box[0]
    return index
def update_org( index , org_arr ,n):
    x = opennegb.getneg(index[0], index[1],n)
    for neg in x:
        if( org_arr[neg[0]][neg[1]] != -2 and org_arr[neg[0]][neg[1]] != 0 and org_arr[neg[0]][neg[1]] != -1 ):
            org_arr[neg[0]][neg[1]] -=1



def mark_allsafe(ival,jval,agent_mtx, n,pairs ,  disc_box ,arr , org_arr):
    x = opennegb.getneg(ival, jval,n)
    for index in x:
        i = index[0]
        j = index[1]
        if( check_inpairs(index, pairs) == False):
            continue
        org_arr[i][j] = arr[i][j]
        #pairs.remove(index)
        if( index not in disc_box):
            disc_box.append(index)
        agent_mtx[i][j] = 1
    return x
def sm_idf(ival, jval , agent_mtx ,n):
    x = opennegb.getneg(ival, jval,n)
    safe = []
    mine = []
    unidf = []
    for index in x:
        if( agent_mtx[index[0], index[1]] == 1):
            safe.append(index)
        if( agent_mtx[index[0], index[1]] == -1):
            mine.append(index)
        if( agent_mtx[index[0], index[1]] == 0):
            unidf.append(index)
    return safe , mine , unidf

def set_allmines(unidf, agent_mtx , pairs,disc_box, org_arr,n):
    for index in unidf:
        if (check_inpairs(index, pairs) == False):
            continue
        org_arr[index[0]][index[1]] = -1
        #update_org( index , org_arr,n)
        agent_mtx[index[0]][index[1]] = -1
        pairs.remove(index)  #removing the identified box
        if( index not in disc_box):
            disc_box.append(index)
def check_inpairs(index, pairs):
    if( len(pairs) ==0):
        return False
    for p in pairs:
        if( index[0] == p[0] and index[1] == p[1]):
            return True

    return False


def mark_safe(unidf, agent_mtx , pairs ,disc_box , org_arr , arr):
    for index in unidf:
        if ( check_inpairs(index, pairs) == False ):
            continue
        pairs.remove(index)
        if(index not in disc_box):
            disc_box.append(index)
        agent_mtx[index[0]][index[1]] = 1
        org_arr[index[0]][index[1]] = arr[index[0]][index[1]]


def mark_mine(def_mine, agent_mtx , disc_box , pairs , org_arr, arr):

    for mine in def_mine:
        if(  check_inpairs(mine, pairs) == False):
            continue
        if( arr[mine[0]][mine[1]] == -1):
            print("<-----found mine using smart pick--------->")
            print(mine)
        else:
            print("<-----False alarm--------->")
            continue
        #print(mine)
        agent_mtx[mine[0]][mine[1]] = -1
        org_arr[mine[0]][mine[1]]= -1
        if( mine not in disc_box):
            disc_box.append(mine)
        pairs.remove(mine)


def agent_moves(ij_pairs, pairs, agent_mtx, arr,n, disc_box , org_arr):
    #print(ij_pairs)
    if(check_inpairs(ij_pairs, pairs) == True):
        pairs.remove(ij_pairs)
    ival = ij_pairs[0]
    jval = ij_pairs[1]
    if( arr[ival][jval] == -1): #the box is a mine
        if (agent_mtx[ival][jval] != -1):
            print("<------Steped on a mine------>")
            agent_mtx[ival][jval] = -1
            org_arr[ival][jval] = -1
            #update_org(ij_pairs, org_arr, n)
            return
        return
    if(arr[ival][jval] == 0): #the box has no neightbors that are mines
        agent_mtx[ival][jval] = 1
        org_arr[ival][jval] = arr[ival][jval]
        x = mark_allsafe(ival,jval,agent_mtx,n , pairs , disc_box, arr , org_arr)
        for index in x: #keep exploring
            if( check_inpairs(index, pairs) == False):
                continue
            else:
                agent_moves(index, pairs, agent_mtx, arr,n, disc_box, org_arr)
        return


    safe ,mines , unidf = sm_idf(ival , jval, agent_mtx, n)  # if you are here then it means you are not in a mine or a box with all safe neighbors but now you have to make a decision
    #now we have number of identidied safe and mines round the box
    if( arr[ival][jval] - len(mines) == len(unidf)):  # in this we are saying that if the total number of mines - the known mines = hidden then all hidden are mines
        agent_mtx[ival][jval] = 1
        org_arr[ival][jval] = arr[ival][jval]
        if( len(unidf) > 0):
            print("<-------found mines------>")
            print(unidf)
        set_allmines(unidf, agent_mtx , pairs,disc_box, org_arr,n)
        return  # return because no where to go now
    totalsafe = 8-arr[ival][jval]
    if( totalsafe - len(safe) == len(unidf)):
        agent_mtx[ival][jval]=1
        org_arr[ival][jval] = arr[ival][jval]
        mark_safe(unidf, agent_mtx , pairs , disc_box, org_arr , arr)
        random.shuffle(unidf)  # shuffles it to meake it more random
        for index in unidf:
            if( check_inpairs(index, pairs) == False):
                continue
            else:
                pairs.remove(index)
                if(index not in disc_box):
                    disc_box.append(index)
                agent_moves(index, pairs, agent_mtx, arr,n,disc_box)  # recorsive meathods that explores the once that are safe
    agent_mtx[ival][jval] = 1
    org_arr[ival][jval] = arr[ival][jval]


def start_agent(n, arr):
    pairs = []
    disc_box = []
    org_arr = np.zeros(shape=(n,n))
    for i in range(0,n):
        for j in range(0,n):
            org_arr[i][j] = -2
            pairs.append((i,j))
    #return_box =[]
    agent_mtx = np.zeros((n,n))
    ival = random.randint(0,len(pairs))-1
    while(len(pairs) >0):
        ij_pairs = pairs[ival]
        pairs.remove(ij_pairs)
        disc_box.append(ij_pairs)
        agent_moves(ij_pairs, pairs, agent_mtx, arr,n, disc_box, org_arr)
        org_arr = org_arr
        for box in disc_box:
            agent_moves(box, pairs, agent_mtx, arr, n, disc_box, org_arr)
        safe_picks , def_mine , bbox_rank = custompred.smartpick(disc_box, arr, org_arr,n  , agent_mtx) #this returns safe pick and def mine
        #print("safe_pics")
        #print(safe_picks)
        #print("agent arr is")
        #print(agent_mtx)
        #print("our arr is")
        #print(org_arr)
        #input("")

        mark_mine(def_mine,  agent_mtx , disc_box , pairs , org_arr ,arr)

        if(len(safe_picks) == 0):
        #    ij_pairs = get_smallest(bbox_rank)
            ival = random.randint(0,len(pairs))-1#pairs.index(ij_pairs)
            continue

        ival  = pairs.index(safe_picks[0]) #we can optimize this by treversing over all the safe picks but we are onlt picking one in the safe picks


        #if(pairs == None): #you don't need this
            #break

    return agent_mtx
