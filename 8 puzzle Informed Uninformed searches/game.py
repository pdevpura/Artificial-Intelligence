import time
import sys
import getopt
import os
import math
import operator
import copy

'''
class node_attr that keep tracks of node_list
'''
class node_attr:
    def __init__(self,val, id):
        self.id = []
        self.id.extend(id)
        self.val = val
    def gen_reverse(self):
        self.id.reverse()

'''
algorithm for min_max
'''

def min_max(cur_state):
    max_val = float('-inf')

    for i,state in enumerate(cur_state):
        #call the min_play
        temp_node = min_play(state)
        val = temp_node.val
        #change the value if value got is higher than max_val right now
        if val > max_val:
            max_val = val
            max_move = i+1
            node_id = temp_node.id
    temp_id=copy.deepcopy(node_id)
    temp_id.append(max_move)

    new_node = node_attr(max_val,temp_id)
    return new_node
'''
min_play function that max_play and return the min value at this level
'''
def min_play(cur_state):
    min_val = float('inf')
    node_id =[]
    max_move =[]
    #if reached the terminal node. If so return
    if not isinstance(cur_state,tuple):
        new_node = node_attr(copy.deepcopy(cur_state),[])
        return new_node
    for i,state in enumerate(cur_state):
        temp_node = max_play(state)
        val = temp_node.val
        # check the value got is lower than min_val. If so, update the min_val
        if val < min_val:
            min_val = val
            max_move =[i+1]
            node_id = temp_node.id
    temp_id = copy.deepcopy(node_id)
    temp_id.extend(max_move)
    new_node = node_attr(min_val, temp_id)
    return new_node
'''
max_play function that calls the min_play and returns the max_val
'''

def max_play(cur_state):
    max_val = float('-inf')
    #check if it is the terminal node or not. If so return
    if not isinstance(cur_state,tuple):
        new_node = node_attr(copy.deepcopy(cur_state), [])
        return new_node
        #print "NOT instance", cur_state
        #return cur_state
    for i,state in enumerate(cur_state):
        temp_node = min_play(state)
        val = temp_node.val
        if val > max_val:
            max_val = val
            max_move = i+1
            node_id = temp_node.id
    temp_id = copy.deepcopy(node_id)
    temp_id.append(max_move)
    new_node = node_attr(max_val, temp_id)
    return new_node

'''
COde for alpha beta pruning
calls the min_play2 function.
'''

def alpha_beta(cur_state,alpha,beta):
    max_val = float('-inf')
    new_alpha =copy.deepcopy(alpha)
    new_beta = copy.deepcopy(beta)
    for i,state in enumerate(cur_state):
        temp_node = min_play2(state,new_alpha,new_beta)
        val = temp_node.val
        #print "check ",val
        new_alpha = max(new_alpha, val)
        #print "MINIMAX",new_alpha,new_beta
        if(new_alpha>beta):
            print "MINIMAX CUT after ",state,"in subtree",cur_state

            node_id = temp_node.id
            temp_id = copy.deepcopy(node_id)
            temp_id.append(val)
            new_node = node_attr(val, temp_id)
            return new_node
        # update the val is greater than max val
        if val > max_val:
            max_val = val
            max_move = i+1
            node_id = temp_node.id

    temp_id=copy.deepcopy(node_id)
    temp_id.append(max_move)

    new_node = node_attr(max_val,temp_id)
    return new_node
'''
min_play2 function calls the max_play and return the min node at this level
'''
def min_play2(cur_state,alpha,beta):
    min_val = float('inf')
    node_id =[]
    max_move =[]
    # check if it is the terminal node or not
    if not isinstance(cur_state,tuple):
        new_node = node_attr(copy.deepcopy(cur_state),[])
        return new_node
    new_alpha = copy.copy(alpha)
    new_beta = copy.copy(beta)
    for i,state in enumerate(cur_state):
        temp_node = max_play2(state,new_alpha,new_beta)
        val = temp_node.val
        new_beta = min(new_beta,val)
        #print "MIN",alpha,new_beta
        # if we achieve this condition then we have got the min_cut
        if(alpha>new_beta):
            print "MIN CUT after ", state, "in subtree", cur_state
            node_id = temp_node.id
            temp_id = copy.deepcopy(node_id)
            temp_id.append(val)
            new_node = node_attr(val, temp_id)
            return new_node
        #update the min_val if calue lesser than min_val
        if val < min_val:
            min_val = val
            max_move =[i+1]
            node_id = temp_node.id
    temp_id = copy.deepcopy(node_id)
    temp_id.extend(max_move)
    new_node = node_attr(min_val, temp_id)
    return new_node

'''
max_play2 that calls min_val and return max node at this level
'''

def max_play2(cur_state,alpha,beta):
    max_val = float('-inf')
    # check if it is a terminal node or not
    if not isinstance(cur_state,tuple):
        new_node = node_attr(copy.deepcopy(cur_state), [])
        return new_node
    new_alpha = copy.deepcopy(alpha)
    new_beta = copy.deepcopy(beta)
    for i,state in enumerate(cur_state):
        temp_node = min_play2(state,new_alpha,new_beta)
        val = temp_node.val
        new_alpha = max(val,new_alpha)
        #print "MAX",new_alpha,beta
        # if we meet this condition then we can cut the tree
        if new_alpha > beta:
            node_id = temp_node.id
            temp_id = copy.deepcopy(node_id)
            temp_id.append(val)
            new_node = node_attr(val, temp_id)
            print "MAX CUT after ", state, "in subtree", cur_state
            return new_node
        # update the max val if val is greater than max_val
        if val > max_val:
            max_val = val
            max_move = i+1
            node_id = temp_node.id
    temp_id = copy.deepcopy(node_id)
    temp_id.append(max_move)
    new_node = node_attr(max_val, temp_id)
    return new_node

'''
Main function starts here
'''

def main():
    #cur_state = (((1, (4, 7)), (3, ((5, 2), (2, 8, 9), 0, -2), 7, (5, 7, 1)), (8, 3)),(((8, (9, 3, 2), 5), 2, (9, (3, 2), 0)), ((3, 1, 9), 8, (3, 4))))
    #cur_state = ((4, (7, 9, 8), 8), (((3, 6, 4), 2, 6), ((9, 2, 9), 4, 7, (6, 4, 5))))          #1      2,1,3
    #cur_state = (((1, 4), (3, (5, 2, 8, 0), 7, (5, 7, 1)), (8, 3)), (((3, 6, 4), 2, (9, 3, 0)), ((8, 1, 9), 8, (3, 4))))   #2       1 1 2
    #cur_state = (5, (((4, 7, -2), 7), 6))                               #3      2,2
    #cur_state = ((8, (7, 9, 8), 4), (((3, 6, 4), 2, 1), ((6, 2, 9), 4, 7, (6, 4, 5))))     #4   1,3
    #cur_state = (((1, (4, 7)), (3, ((5, 2), (2, 8, 9), 0, -2), 7, (5, 7, 1)), (8, 3)), (((8, (9, 3 ,2), 5), 2,(9, (3, 2), 0)), ((3, 1, 9), 8, (3, 4 ))))       #5  2,1,1,3

    ##dictionary to store the current configuartion
    cur_state_dict={}
    cur_state_dict[1] = ((4, (7, 9, 8), 8), (((3, 6, 4), 2, 6), ((9, 2, 9), 4, 7, (6, 4, 5))))
    cur_state_dict[2] = (((1, 4), (3, (5, 2, 8, 0), 7, (5, 7, 1)), (8, 3)), (((3, 6, 4), 2, (9, 3, 0)), ((8, 1, 9), 8, (3, 4))))
    cur_state_dict[3] = (5, (((4, 7, -2), 7), 6))
    cur_state_dict[4] = ((8, (7, 9, 8), 4), (((3, 6, 4), 2, 1), ((6, 2, 9), 4, 7, (6, 4, 5))))
    cur_state_dict[5] = (((1, (4, 7)), (3, ((5, 2), (2, 8, 9), 0, -2), 7, (5, 7, 1)), (8, 3)), (((8, (9, 3 ,2), 5), 2,(9, (3, 2), 0)), ((3, 1, 9), 8, (3, 4 ))))
    #check for correct arguments
    if(len(sys.argv) == 3 ):
        cur_state = cur_state_dict[int(sys.argv[2])]

    else:
        print "Please give correct arguments game.py min_max 1"
        return
    #call min-max
    if(sys.argv[1]=='min-max'):
        node = min_max(cur_state)
        node.gen_reverse()
    #call alpha-beta
    elif (sys.argv[1]=='alpha-beta'):
        alpha = float('-inf')
        beta = float('inf')
        node = alpha_beta(cur_state, alpha, beta)
        node.gen_reverse()

    else:
        print "Incorrect game-play algorithm. Please give as input either min-max or alpha-beta"

    print "Node List:",node.id, "Max val:",node.val

if __name__ == "__main__":
    main()




