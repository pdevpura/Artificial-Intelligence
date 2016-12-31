import time
import sys
import getopt
import os
import math
import operator
import copy
import argparse
from sets import Set
'''
Node Class which has information about its val, parent for backtracking, dir=the way we reached this node
depth information, heuristics information and f value.
It also contains some methods to update f and h value
'''
class Node:
    def __init__(self,val,parent,dir,h=0, depth=0,f=0):
        self.val = val
        self.parent = parent
        self.dir =dir
        self.h =h
        self.depth = depth
        self.f = f

    def updateH(self,h_val):
        self.h = h_val

    def updatedepth(self,depth):
        self.depth = depth

    def updateF(self):
        self.f = self.h + self.depth
'''
It checks for the goal state whether we have reached it or not and returns true or false
'''

def isGoal(state):
    goal_state = [1,2,3],[8,0,4],[7,6,5]
    #print "GOAL", goal_state, state
    return goal_state == state
'''
This function finds the position of zero in the node and return the coordinates
'''

def findZero (cur_state):
    for y,row in enumerate(cur_state):
        for x,col in enumerate(row):
            if ( cur_state[y][x] == 0 ):
                return [y,x]
'''
This function finds the position of the element and return its coordinates
'''
def findEle (cur_state,ele):
    for y,row in enumerate(cur_state):
        for x,col in enumerate(row):
            #if cur_state[y][x] == 0:
            #    return [1,1]
            if ( cur_state[y][x] == ele ):
                return [y,x]

'''
This function checks if its a visited state or not and return true or false
'''
def checkState(each_state, all_states):
    for vis_state in all_states:
        if(vis_state.val==each_state.val):
            return True
    return False

#'''
'''
This function generates the list of next state based on the cur_state and position of zero.
The next state can be up, down, left and right and return the list of new states
'''


def findNextStates(cur_state,z_pos):
    res_state =[]
    #print z_pos
    y = z_pos[0]
    x = z_pos[1]
    #print y,x,len(cur_state)
    #up,left down ,right



    if(y-1>=0 ):    #move up
        new_state = copy.deepcopy(cur_state.val)
        new_state[y][x],new_state[y-1][x] = new_state[y-1][x], new_state[y][x]
        newNode = Node(copy.deepcopy(new_state),cur_state,"UP",0,cur_state.depth+1)
        res_state.append(newNode)

    if (x-1>=0):            #left

        new_state = copy.deepcopy(cur_state.val)
        new_state[y][x], new_state[y][x-1] = new_state[y][x-1], new_state[y][x]
        newNode = Node(copy.deepcopy(new_state), cur_state, "LEFT",0,cur_state.depth+1)
        res_state.append(newNode)


    if (y+1 <= len(cur_state.val)-1):   #down

        new_state = copy.deepcopy(cur_state.val)
        new_state[y][x], new_state[y + 1][x] = new_state[y + 1][x], new_state[y][x]
        newNode = Node(copy.deepcopy(new_state), cur_state, "DOWN",0,cur_state.depth+1)
        res_state.append(newNode)
    if (x+1<=len(cur_state.val[0])-1):    #right
        new_state = copy.deepcopy(cur_state.val)
        new_state[y][x], new_state[y][x + 1] = new_state[y][x + 1], new_state[y][x]
        newNode = Node(copy.deepcopy(new_state), cur_state, "RIGHT",0,cur_state.depth+1)
        res_state.append(newNode)





    #print len(res_state)
    return res_state
'''

def findNextStates(cur_state,z_pos):
    res_state =[]
    #print z_pos
    y = z_pos[0]
    x = z_pos[1]
    #print y,x,len(cur_state)
    #up,left down ,right



    if(y-1>=0 ):    #move up
        new_state = copy.deepcopy(cur_state.val)
        new_state[y][x],new_state[y-1][x] = new_state[y-1][x], new_state[y][x]
        newNode = Node(copy.deepcopy(new_state),cur_state,"UP",0,cur_state.depth+1)
        res_state.append(newNode)

    if (y+1 <= len(cur_state.val)-1):   #down

        new_state = copy.deepcopy(cur_state.val)
        new_state[y][x], new_state[y + 1][x] = new_state[y + 1][x], new_state[y][x]
        newNode = Node(copy.deepcopy(new_state), cur_state, "DOWN",0,cur_state.depth+1)
        res_state.append(newNode)

    if (x-1>=0):            #left

        new_state = copy.deepcopy(cur_state.val)
        new_state[y][x], new_state[y][x-1] = new_state[y][x-1], new_state[y][x]
        newNode = Node(copy.deepcopy(new_state), cur_state, "LEFT",0,cur_state.depth+1)
        res_state.append(newNode)

    if (x+1<=len(cur_state.val[0])-1):    #right
        new_state = copy.deepcopy(cur_state.val)
        new_state[y][x], new_state[y][x + 1] = new_state[y][x + 1], new_state[y][x]
        newNode = Node(copy.deepcopy(new_state), cur_state, "RIGHT",0,cur_state.depth+1)
        res_state.append(newNode)





    #print len(res_state)
    return res_state
'''
'''
This function generates the full path when we reach the goal state.
Basically it generates the list of direction of how we reached from a particular state to goal state.
'''

def getFullPath(cur_state):
    node_list=[]

    while cur_state.parent:
        # print "YESSS",cur_state.parent
        #print cur_state.dir
        node_list.insert(0, cur_state.dir)
        cur_state = cur_state.parent
    return node_list


'''
Perform sorting based on the attribute of a class.
'''
def sortBased(fringe,op):
    fringe.sort(key = operator.attrgetter(op))

'''
This function find the value of the H1 heuristics
'''
def findH1(each_state,goal_state):
    ct = 0
    for y,row in enumerate(each_state.val):
        for x,col in enumerate(row):
            #if each_state.val[y][x]==0:
            #   continue
            if(each_state.val[y][x] != goal_state[y][x]):
                ct += 1
    return ct
'''
This function finds the value for the H2 heuristics
'''
def findH2(each_state,goal_state):
    ct = 0
    for i in range(9):
        pos1 = findEle(each_state.val, i)
        pos2 = findEle(goal_state, i)
        ct += abs(pos1[0]-pos2[0]) + abs(pos1[1]-pos2[1])

    return ct

'''
GREEDY Search Algorithm
'''
def greedy(state,goal_state,heu):
    visited = []                                    #keep track of visited nodes
    newNode = Node(copy.deepcopy(state), [], "NONE")        #initialize node
    fringe = []
    fringe.append(newNode)                          #storage element for nodes
    max_fringe_len = 0
    nodes_inserted = 1
    while len(fringe) > 0:
        sortBased(fringe,'h')                       # sort based on heuristics value
        max_fringe_len = max(max_fringe_len,len(fringe))        # to maximum fringe length
        cur_state = fringe.pop(0)
        visited.append(cur_state)
        #check if we have reached the goal oor not
        if (isGoal(cur_state.val)):
            res_path = getFullPath(cur_state)
            print res_path
            print "Max visited Nodes Length:", len(visited)
            print "Max Fringe Len:", max_fringe_len
            print "Nodes Inserted:", nodes_inserted
            #print "VISITED LEN", len(visited),"MAX FRINGE LEN",max_fringe_len,"Depth",cur_state.depth
            return
        z_pos = findZero(cur_state.val)     # find the position of the zero
        # get the next states from the current state
        new_states = findNextStates(cur_state, z_pos)
        new_states.reverse()
        #insert the new_states in the fringe if not visited
        for each_state in new_states:
            # if(checkState(each_state,visited) or checkState(each_state,fringe)):
            if (checkState(each_state, visited)):
                # print "FOUND"
                pass
            else:
                # print each_state.val
                #h1_val = findH1(each_state, goal_state)
                #each_state.updateH1(h1_val)
                if heu =='h1':
                    h_val = findH1(each_state, goal_state)
                elif heu == 'h2':
                    h_val = findH2(each_state, goal_state)
                else:
                    print "Wrong heuristics"
                each_state.updateH(h_val)
                fringe.insert(0, each_state)
                nodes_inserted += 1

'''
 A-STAR Search
'''
def a_star (state,goal_state,heu):

    visited = []
    newNode = Node(copy.deepcopy(state), [], "NONE")
    fringe = []             # storage element for the nodes
    fringe.append(newNode)
    max_fringe_size = 0
    visited_dict ={}        # keep track of visited nodes
    nodes_inserted = 1
    while len(fringe) > 0:
        max_fringe_size = max(max_fringe_size,len(fringe))
        sortBased(fringe,'f')       #sorting based on the f value
        cur_state = fringe.pop(0)
        visited.append(cur_state)   # append the visited node
        visited_dict[get_tuple(cur_state.val)] = 1
        # check if we have reached the goal or not
        if (isGoal(cur_state.val)):
            res_path = getFullPath(cur_state)
            print res_path
            print "Nodes Inserted:", nodes_inserted
            print "Max Fringe Len:", max_fringe_size
            print "Max visited Nodes Length:", len(visited)

            #print "A_star VISITED LEN", len(visited),"FRINGE LEN",len(fringe),"depth=",cur_state.depth,"max_fringe_size=",max_fringe_size
            return
        # get the position of zero and find the new states
        z_pos = findZero(cur_state.val)
        new_states = findNextStates(cur_state, z_pos)
        new_states.reverse()
        for each_state in new_states:
            # if(checkState(each_state,visited) or checkState(each_state,fringe)):
            #if (checkState(each_state, visited)):
            #check if the state is visited or not
            if get_tuple(each_state.val) in visited_dict:

                pass
            else:
                #Apply heuristics
                if heu == 'h1':
                    h_val = findH1(each_state, goal_state)
                elif heu == 'h2':
                    h_val = findH2(each_state, goal_state)
                else:
                    print "Wrong heuristics"
                each_state.updateH(h_val)
                each_state.updateF()
                fringe.insert(0, each_state)
                nodes_inserted += 1
'''
IDA-star search
'''

def ida_star(state,goal_state,heu):
    newNode = Node(copy.deepcopy(state), [], "NONE")
    fringe = []     # storage element for the nodes
    visited = []
    visited_dict = {}   # check if the node is visited or not
    fringe.append(newNode)
    cur_state =newNode
    if heu == 'h1':
        h_val = findH1(cur_state, goal_state)
    elif heu == 'h2':
        h_val = findH2(cur_state, goal_state)
    else:
        print "Wrong Heuristics"
    cur_state.updateH(h_val)
    cur_state.updateF()
    f_cut_off =cur_state.f
    f_val = 0
    iter = 0
    tot_visit_ct = 0
    #new_f_val = 0
    max_fringe_size = 0
    nodes_inserted = 1
    temp_list =[]
    while True:

        if (len(fringe)> 0):
            max_fringe_size = max(max_fringe_size,len(fringe))
            #sort based on f value
            sortBased(fringe, 'f')

            cur_state = fringe.pop(0)
            tot_visit_ct += 1
            visited_dict[get_tuple(cur_state.val)] = 1
            # check if we have reached the goal state or not
            if (isGoal(cur_state.val)):
                res_path = getFullPath(cur_state)
                print res_path
                print "Nodes Inserted:", nodes_inserted
                print "Max Fringe Len:", max_fringe_size
                print "Max visited Nodes Length:", tot_visit_ct
                print "Depth of recursion",cur_state.depth
                #print "IDA_STAR", "depth=",cur_state.depth,"tot_visit_ct=",tot_visit_ct,"MAx_FRINGE_SIZE=",max_fringe_size
                return
            z_pos = findZero(cur_state.val)
            # find the next states from current state
            new_states = findNextStates(cur_state, z_pos)
            new_states.reverse()
            for each_state in new_states:
                #push node only if the state is not visited
                if get_tuple(each_state.val) in visited_dict:
                    pass
                else:
                    if heu == 'h1':
                        h_val = findH1(cur_state, goal_state)
                    elif heu == 'h2':
                        h_val = findH2(cur_state, goal_state)
                    else:
                        print "Wrong Heuristics"
                    # update the heuristics value
                    each_state.updateH(h_val)
                    each_state.updateF()
                    # push into the temp list if node f value is higher than cut-off
                    if(each_state.f>f_cut_off):
                        temp_list.append(each_state.f)
                        temp_list = list(set(temp_list))
                    else:
                        #fringe.insert(0, each_state)
                        fringe.append(each_state)
                        nodes_inserted += 1
        else:
            # start next iteration when the length of the fringe is zero
            iter += 1
            f_cut_off = min(temp_list)
            temp_list.remove(f_cut_off)
            visited_dict = {}
            fringe = []
            fringe.append(Node(copy.deepcopy(state), [], "NONE"))



'''
IDS Search
'''

def ids(state,goal_state):
    iter = 0
    newNode = Node(copy.deepcopy(state), [], "NONE")
    fringe = []     # storing the nodes
    visited = []
    fringe.append(newNode)
    visited_dict ={}    # track for visited nodes
    tot_visited_ct = 0
    max_fringe_len = 0
    nodes_inserted = 1
    while True:
        max_fringe_len=max(max_fringe_len,len(fringe))
        if (len(fringe)>0):
            cur_state = fringe.pop(0)

            visited.append(cur_state)
            visited_dict[get_tuple(cur_state.val)] = 1
            tot_visited_ct += 1
            # check for those nodes whose cur_state == current depth
            if(cur_state.depth<iter):
                z_pos = findZero(cur_state.val)
                new_states = findNextStates(cur_state, z_pos)
                new_states.reverse()
                for each_state in new_states:
                    if get_tuple(each_state.val) in visited_dict:
                        # print "FOUND"
                        #check if we have reached the goal or not
                        if (isGoal(cur_state.val)):
                            res_path = getFullPath(cur_state)
                            print "Nodes Inserted:", nodes_inserted
                            print "Max Fringe Len:", max_fringe_len
                            print "Max visited Nodes Length:", tot_visited_ct
                           # print "Visied Nodes",tot_visited_ct,"Depth Reached",cur_state.depth,"Max fringe Len", max_fringe_len
                            print res_path
                            return

                    else:
                        # print each_state.val
                        fringe.insert(0, each_state)
                        nodes_inserted += 1
            elif(cur_state.depth == iter):
               pass
            else:
                continue


        else:

            iter += 1
            fringe = []
            visited =[]
            visited_dict = {}
            fringe.append(newNode)
            #print "DEPTH=", iter,"fringe len",len(fringe), len(visited)


'''
DFS search
'''

def dfs(state,goal_state):
    visited = []
    newNode = Node(copy.deepcopy(state), [], "NONE")
    fringe = []     # storing the queueing elemnt
    fringe.append(newNode)
    max_fringe_len = 0
    visited_dict ={}
    nodes_inserted = 1
    while len(fringe) > 0:
        max_fringe_len = max(max_fringe_len,len(fringe))
        cur_state = fringe.pop(0)
        visited.append(cur_state)
        visited_dict[get_tuple(cur_state.val)] = 1
        # check if we have reached the goal
        if(isGoal(cur_state.val)):
            res_path = getFullPath(cur_state)
            print res_path
            print "Nodes Inserted:", nodes_inserted
            print "Max visited Nodes Length:", len(visited)
            print "Max Fringe Length:", max_fringe_len
            #print "Visited Nodes", len(visited),"Depth = ",cur_state.depth,"Max Fringe Len",max_fringe_len
            return
        z_pos = findZero(cur_state.val)
        new_states = findNextStates(cur_state, z_pos)
        new_states.reverse()
        for each_state in new_states:
            #check for the visited states
            if get_tuple(each_state.val) in visited_dict:
                #print "FOUND"
                pass
            else:
                fringe.insert(0,each_state)
                nodes_inserted += 1
'''
generate the tuple from the list of lists
'''

def get_tuple(cur_list):
    tup_list = tuple(tuple(x) for x in cur_list)
    return tup_list


'''
BFS search
'''
def bfs(state,goal_state):
    visited =[]
    visited_dict ={}
    newNode = Node(copy.deepcopy(state), [], "NONE")
    fringe = []     # storing nodes in the fringe
    fringe.append(newNode)
    fringe_dict={}
    fringe_dict[get_tuple(newNode.val)] = 1
    max_fringe_len = 0;
    nodes_inserted = 1

    while len(fringe) > 0:
        max_fringe_len = max(len(fringe), max_fringe_len)
        cur_state = fringe.pop(0)
        visited_dict[get_tuple(cur_state.val)] = 1      #keep track of the visited states
        if (isGoal(cur_state.val)):
            res_path = getFullPath(cur_state)
            print "Nodes Inserted:", nodes_inserted
            print "Max visited Nodes Length:",len(visited_dict)
            print "Max Fringe Len",max_fringe_len
            print res_path
            return
        z_pos = findZero(cur_state.val)

        new_states = findNextStates(cur_state, z_pos)
        for each_state in new_states:
            # if the state is a visited state or not
            if (get_tuple(each_state.val) in visited_dict):
                pass
            else:
                fringe.append(each_state)
                nodes_inserted += 1
'''
Main function
'''
def main():
    #state = [1,3,4],[8,6,2],[7,0,5]     #easy
    #state = [2,8,1],[0,4,3],[7,6,5]        #med
    #state = [5,6,7],[4,0,8],[3,2,1]     #hard
    #state = [2,8,1],[0,4,3],[7,6,5]
    #state = [5,6,7],[4,0,8],[3,2,1]
    #state = [1, 2, 3], [8, 4, 0], [7, 6, 5]
    goal_state = [1,2,3], [8,0,4], [7,6,5]
    parser = argparse.ArgumentParser()
    parser.add_argument("--search", help="Search algorithm")
    parser.add_argument("--level", help="easy")
    parser.add_argument("--heu", default=[])
    parser.add_argument("--val",default=[])
    args = parser.parse_args()
    arg_dict = vars(args)

    algo_opt1 = 'bfs','dfs','ids'
    algo_opt2 = 'greedy', 'a-star', 'ida-star'
    level_dict={}
    # dictionary to search the level and its corresponding state
    level_dict['easy'] = [1,3,4],[8,6,2],[7,0,5]
    level_dict['medium'] = [2,8,1],[0,4,3],[7,6,5]
    level_dict['hard'] = [5,6,7],[4,0,8],[3,2,1]
    #dictionary to select which search method
    algo_dict = {'bfs':bfs,'dfs':dfs, 'ids':ids, 'greedy':greedy, 'a-star':a_star, 'ida-star':ida_star }

    cur_state = level_dict[arg_dict['level']]

# check for which search method and heuristics if needed
    if arg_dict['search'] in algo_opt1:
        algo_dict[arg_dict['search']](cur_state,goal_state)
    elif arg_dict['search'] in algo_opt2:
        algo_dict[arg_dict['search']](cur_state, goal_state,arg_dict['heu'])
    else:
        print "Please give correct options"

if __name__ == "__main__":
    main()
