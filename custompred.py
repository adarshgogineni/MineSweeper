import numpy as np
import opennegb
import customagent
class disc_n:
    def __init__(self,index , ngb_box):
        self.box = index
        self.ngb_box = ngb_box
        self.val = 0

def get_rank( neg , org_arr):
    sum = 0
    for n in neg:
        if( org_arr[n[0]][n[1]] ==-2 or org_arr[n[0]][n[1]] == -1):
            continue
        sum += org_arr[n[0]][n[1]]
    return sum
def border_ornot(negh , nx , arr, bbox_rank, org_arr , trv):
    x =0
    for n1 in negh:
        if( org_arr[n1[0]][n1[1]] ==-2):
            x =1
            if( n1 in trv):
                continue
            trv.append(n1)
            neg = opennegb.getneg(n1[0], n1[1] , nx)
            n = get_rank(neg , org_arr)
            bbox_rank.append((n1,n))
            #return True
    if(x ==1 ):
        return True
    return False

def get_box(disc_box, arr,n , bbox_rank, org_arr):
    disc_boxes =[]
    trv = []
    for box in disc_box:
        negh = opennegb.getneg(box[0], box[1] , n) #return all neghbors of a box
        if( border_ornot( negh , n, arr , bbox_rank , org_arr, trv)  == True ): #checks any of the neghbors are not discovered so that means if the box is a border
            disc_boxes.append( disc_n( box ,negh ))
    return disc_boxes
def undesc_neg(bbox , org_arr):
    und_box =[]
    for b in bbox.ngb_box:
        if( org_arr[b[0]][b[1]] == -2):
            und_box.append((b[0], b[1]))
    return und_box

def remove_com( boxes_a ,boxes_b ):
    comm = []
    for box_a in boxes_a:
        for box_b in boxes_b:
            if( box_a[0] == box_b[0] and box_a[1] == box_b[1]):
                comm.append(box_a)
    for box in comm:
        boxes_a.remove(box)
        boxes_b.remove(box)
    return len(comm)

def check_ifcom( bboxi, bboxj, org_arr): #just like the name check the common and if two boxes have all in common except one for each box then it returns true and gives the two non common boex is a list
    if(bboxi.val == bboxj.val -1 or bboxi.val-1 == bboxj.val ):
        a = undesc_neg(bboxi, org_arr) #returns the undescovered neghbors of the box
        b = undesc_neg(bboxj, org_arr)
        n = remove_com( a ,b) #removes the common neghbors
        if( len(a) == len(b) and len(a ) == 1 and len(b) ==1 and n >0): #if only one left in each

            return True , [a[0] , b[0]] #reuturn the True and the neghbors
    return False , None
class equ_help:
    """docstring for ."""

    def __init__(self, box, parent):
        self.ind = box
        self.par = [parent]


def load_neg(ret,neg, parent):
    rettmp =[]
    for box in ret:
        if(box.ind == neg):
            box.par.append(parent.box)
            return
        rettmp.append(box)
    ret.append(equ_help(neg,parent.box))
    return #rettmp


def group_allbox(bbox, org_arr, n):
    ret = []
    #ret = ret.reshape((n,n))
    #for i in range(0,n):
    #    for j in range(0,n):
    #        ret[i][j] = []
    m =1
    #print(len(bbox))
    for box in bbox:
        if(org_arr[box.box[0]][box.box[1]] == -1):
            continue
        a = undesc_neg(box, org_arr)
        #print(a)
        if( len(a) ==0):
            continue

        for neg in a:
            #print(m)
            #print(neg)
            load_neg(ret, neg, box)
            #ret[neg[0]][neg[1]].append(box.box)
        #if(len(a) == 0):
        #    continue
        m +=1
    return ret
def smartpick( disc_box , arr , org_arr,n , agent_mtx):
    print("<------now doing smart pick---------->")
    bbox_rank = [] #this is another system that i implemented if we are at a position that we need to do it random. it's similar to probability but a lot less gurenteed
    bbox = get_box(disc_box, arr,n , bbox_rank, org_arr)
    safe_picks =[]
    def_mine=[]
    checked = []
    for boxes in bbox:
        safe ,mines , unidf = customagent.sm_idf(boxes.box[0], boxes.box[1], agent_mtx, n)
        val = org_arr[boxes.box[0]][boxes.box[1]] - len(mines)
        boxes.val = val

    group = group_allbox(bbox,org_arr,n)
    for b in group:
        print("<----the box is----->")
        print(b.ind)
        print("<---the parent is----->")
        print(b.par)
    #print(group)
    for i in range(0,len(bbox)):
        #print(bbox[i].ngb_box) #this prints out the each discovered box's neighbors
        for j in range(0,len(bbox)):
            if( i==j or bbox[i].val == -1 or bbox[j].val == -1 ):
                continue
            if( (bbox[i].box,bbox[j].box) in checked or (bbox[j].box,bbox[i].box) in checked ):
                continue

            com,get_neg = check_ifcom( bbox[i], bbox[j] , org_arr)
            checked.append((bbox[i].box,bbox[j].box))
            if( com == True):

                #print("<------found one------>")
                #print(get_neg)
                if(bbox[i].val == bbox[j].val):
                    safe_picks.append(get_neg[0])
                    safe_picks.append(get_neg[1])
                if( bbox[i].val > bbox[j].val):
                    safe_picks.append(get_neg[1])
                    def_mine.append(get_neg[0])
                if( bbox[j].val > bbox[i].val):
                    safe_picks.append(get_neg[0])
                    def_mine.append(get_neg[1])

    return safe_picks , def_mine , bbox_rank
