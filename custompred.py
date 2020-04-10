import numpy as np
import opennegb
import customagent
class disc_n:
    def __init__(self,index , ngb_box):
        self.box = index
        self.ngb_box = ngb_box
        self.val = 0

#class equ_box:
#    def __init__(self, boxes , parbox):

def get_rank( neg , org_arr):
    sum = 0
    for n in neg:
        if( org_arr[n[0]][n[1]] ==-2 or org_arr[n[0]][n[1]] == -1):
            continue
        sum += org_arr[n[0]][n[1]]
    return sum

def border_ornot(negh , nx , bbox_rank, org_arr , trv):
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

def get_box(disc_box,n , bbox_rank, org_arr):
    disc_boxes =[]
    trv = []
    for box in disc_box:
        negh = opennegb.getneg(box[0], box[1] , n) #return all neghbors of a box
        if( border_ornot( negh , n , bbox_rank , org_arr, trv)  == True ): #checks any of the neghbors are not discovered so that means if the box is a border
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
        self.ind = [box]
        self.par = [parent]
    #def min_max(min_val , max_val):
        self.min = 0
        self.max =  -1
        self.val = -1
    #def update_parval(org_arr):






def load_neg(ret,neg, parent):
    rettmp =[]
    for box in ret:
        if(box.ind[0] == neg):
            box.par.append(parent.box)
            return
        rettmp.append(box)
    ret.append(equ_help(neg,parent.box))
    return #rettmp


def group_allbox(bbox, org_arr, n):
    ret = []
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

def group_tog(group):
    retlist = []
    parents = []
    for box0 in group:
        if box0.par in parents:
            continue
        #temp =None
        for box1 in group:
            if(box0 == box1):
                continue
            if(box0.par == box1.par):
                #if(temp == None):
                for i in range(0,len(box1.ind)):
                    box0.ind.append(box1.ind[i])
                parents.append(box0.par)
                #else:
                    #temp[0].append(box1.ind)
        #if( temp == None):
            #temp = [[box0.ind], box0.par]


        retlist.append(box0)
    return retlist
def setmin_max(comp_box, org_arr0):
    for box in comp_box:
        #if( len(box) == 1):
        #    box.min = 1
        #    box.max = 1
        #    continue
        parents = box.par
        m =-1
        max = -1

        for parent in parents:
            if( m == -1):
                max = org_arr0[parent[0]][parent[1]]
                m = max
                continue
            if(org_arr0[parent[0]][parent[1]] < m ):
                m = org_arr0[parent[0]][parent[1]]
        box.min = 0 #the values that his box has to have
        print("<-----box length is----->")
        print(len(box.ind))
        print("<------min value is------>")
        print(m)
        #temp = len(box.ind)
        box.max = min(m,len(box.ind))
def check_sat(comp_box, org_arr0): #this basically checks if all the undiscovered neightbors have min values that can setisfy the question
    min = -1
    for box in comp_box:
        for parent in box.par:
            if(min = -1):
                min = org_arr0[parent[0]][parent[1]]
            elif(org_arr0[parent[0]][parent[1]]<min)
                min = org_arr0[parent[0]][parent[1]]
        if(box.max < min):
            return False
        min = -1
    return True

def prob_generator(comp_box, org_arr0 , com_set):


    i = 0
    val = 0
    val1 =0
    j =0
    org_temp = org_arr0.copy()
    while(i < len(comp_box) or comp_box[i].val <= comp_box[i].max):
        comp_box[i].val = val
        for parents in comp_box[i].par:
            org_arr0[parents[0]][parents[1]] -=val

        #now first update the max
        setmin_max(comp_box, org_arr0)

        if(check_sat(comp_box, org_arr0) == False):
            for parents in comp_box[i].par: #resetting if does not setisfy
                org_arr0[parents[0]][parents[1]] +=val #reset all the parents values
                if( comp_box[i].val == comp_box[i].max):
                    i+=1
                    val=0
                    continue
                val +=1
            continue

        val1 =0
        while(j <len(comp_box) or comp_box[j].val < comp_box[j].max):
            if (i==j):
                j+=1
                continue
            comp_box[j].val = val1

            for parents in comp_box[j].par:
                org_arr0[parents[0]][parents[1]] -=val1
            setmin_max(comp_box, org_arr0)
            if(check_sat(comp_box, org_arr0) == False):
                for parents in comp_box[j].par: #resetting if does not setisfy
                    org_arr0[parents[0]][parents[1]] +=val1 #reset all the parents values
                    if( comp_box[i].val == comp_box[i].max):
                        i+=1
                        val=0
                        continue
                    val +=1
                continue
            else:
                if(j == len(comp_box)-1): #we only check if it's the last box because we don't care about all possible testing
                    #combination solved
                    temp= []
                    for i in range(0, len(comp_box)):  #this part is used to save the solved configuration
                        temp.append(comp_box[i].val)
                    com_set.append(temp)

        i+=1
        org_arr0 = org_temp.copy()








def smartpick( disc_box , org_arr,n , agent_mtx): #org_arr is treated as a global discovered value by opening a box
    print("<------now doing smart pick---------->")
    print(org_arr)
    org_arr0 = org_arr.copy() #this is used to copy or als reset a matrix
    #print(type(org_arr0))
    bbox_rank = [] #this is another system that i implemented if we are at a position that we need to do it random. it's similar to probability but a lot less gurenteed
    bbox = get_box(disc_box,n , bbox_rank, org_arr)
    safe_picks =[]
    def_mine=[]
    checked = []
    for boxes in bbox:
        safe ,mines , unidf = customagent.sm_idf(boxes.box[0], boxes.box[1], agent_mtx, n)
        val = org_arr[boxes.box[0]][boxes.box[1]] - len(mines)
        boxes.val = val

    group = group_allbox(bbox,org_arr,n) #this makes a list a class of undiscovered box and the discovered neightbors

    comp_box = group_tog(group) #this makes a list of  class of boxes that have same discovered parents
    setmin_max(comp_box, org_arr0)#this sets min and max for all the groups
    #now this is where the fun stuff happens
    com_set = []
    prob_generator(comp_box, org_arr0, com_set)

    #so now that we have neighbors in a group we can think about setting up system of quation
    """
    for box in comp_box:
        print("<----the boxes are------->")
        print(box.ind)
        print("<----the parents are----->")
        print(box.par)
        print("<------min is------->")
        print(box.min)
        print("<------max is-------->")
        print(box.max)
        """
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
