import numpy as np

def up(ival, jval,n):
    if(ival ==0):
        return None
    return [ival-1, jval]
def down(ival, jval,n):
    if(ival <n-1):
        return [ival+1, jval]
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
L =[up, down , left , right , upleft , upright , downleft , downright]
def getneg(ival, jval , n):
    neg =[]
    for ele in L:
        temp =  ele(ival , jval, n)
        if( temp != None):
            neg.append((temp[0], temp[1]))

    return neg
