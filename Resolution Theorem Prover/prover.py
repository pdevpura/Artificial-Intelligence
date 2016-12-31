import time
import sys
import getopt
import os
import math
import operator
import copy
import argparse
from sets import Set
import itertools
import random
import time
from heapq import heappush, heappop
#get the variables in a literal and append it with the result
def get_all_vars(A,res):

    for i,var in enumerate(A):
        if(i==0):
            continue
        if not isinstance(A[i],list):
            res.append(A[i])
        else:
            get_all_vars(var,res)
    return 1

#check if the clauses have any common variable. If so change the variable
def get_common_vars(list1,list2,dict):
    res1=[]
    res2=[]
    res =[]
    found=0
    get_all_vars(list1,res1)
    get_all_vars(list2,res2)
    for ele1 in res1:
        for ele2 in res2:
            if ele1==ele2:
                found =1
                num=random.sample(xrange(1,10000),1)    # random get a number and change the variable
                var1 = ele1+str(num[0])
                dict[ele1]=var1
    if found:
        return 1
    return 0

# apply function does the substitution in the dictionary
# if the new key is already present in terms of a value. then we will substitute the value of the key.
def apply(term_dict, changed_term):
	if len(term_dict)>0:
		for i in range(len(changed_term)):
			if isinstance(changed_term[i], str):
				while changed_term[i] in term_dict.keys():
					for key in term_dict:
						if changed_term[i] == key:
							changed_term[i] = term_dict[key]
	 		else:
	 			apply(term_dict, changed_term[i])

#Perform substitution in the clause list based  on the keys in the dict
def substitute(dict_list, rest_term):

    if len(dict_list)>0 and len(rest_term):
        for i in range(len(rest_term)):
            if isinstance(rest_term[i],str): #If its a variable then do a substitution else recursive call this function
                while rest_term[i] in dict_list.keys():
                    for key in dict_list:
                        if rest_term[i]==key:
                            rest_term[i]=dict_list[key]
            else:
                substitute(dict_list,rest_term[i])

# helper function that calls unify and performs the unification
def unify_helper(E2,E1,dict_list):
    if(len(E1)==0 and len(E2)==0):  # check if E1 and E2 are empty
        return []
    elif (E1[0]!=E2[0]) or (len(E1)!=len(E2)):  # check if length unequal return 'FAIL' for a literal
        return 'FAIL'
    else:
        z1=unify(E1[1:],E2[1:],dict_list)   # calls the main unification function
        return z1

# helper function for updating the dictionary which is called by update dict
def update_dict_helper(dict_key,dict_val,sing_key,sing_val):
    if len(dict_val)>1 and isinstance(dict_val,list):
       dict_val[1] =  update_dict_helper(dict_key,dict_val[1],sing_key,sing_val)
       return dict_val
    #elif len(dict_val)==1 and (dict_val is sing_key):
    elif len(dict_val)==1 and (dict_val is sing_key):
        return sing_val
    else:
        return dict_val
#update_dict calls update_dict_helper function to update the dictionary
def update_dict(dict_list, sing_key, sing_val):
    if len(dict_list)>0:
        for key in dict_list.keys():
            if len(dict_list[key]) >= 1:
                dict_list[key]=update_dict_helper(key,dict_list[key],sing_key,sing_val)


# checks for the duplicate list A and B
def is_duplicate(list_A,B):
    tempB1 = B[1]
    tempB2 = B[2]
    tempB1.sort()
    tempB2.sort()
    for A in list_A:
        tempA1 = A[1]
        tempA2 = A[2]
        tempA1.sort()
        tempA2.sort()
        if(tempA1==tempB1)  and (tempA2==tempB2):   # if duplicate return 1
            return 1
    return 0



# check if the clause is empty. If so return 1
def is_found(new_list_out):
    if(new_list_out==[[],[]]):
        return 1
    else:
        return 0
# used for question answering. Check if we have got the answer. If so return 1
def is_answer(new_list_out):
    if len(new_list_out[0])==1 and len(new_list_out[1])==0 and new_list_out[0][0][0]=='answer':
        print 'The answer is ',new_list_out[0][0][1]
        return 1
    return 0

#out_pos is a pos clause
#in_neg is a neg clause
#in_list is a input pos,neg clause i.e complete llist
#out_list is a output pos,neg clause i.e. complete list
def find_new_clause(out_pos,in_neg,in_list,out_list,A):
    #print "find_new_clause",out_pos,in_neg
    if len(out_pos)>0 and len(in_neg)>0:
        for i, lit in enumerate(out_pos):   #iterate over all the literals
            for j, lit2 in enumerate(in_neg):   #iterate over the neg literals
                dict_list = {}
                c = unify_helper(lit, lit2, dict_list) # call the unify helper function to unify it
                if c is not 'FAIL': # if unification exists call substitute and update
                    new_list_in = copy.deepcopy(in_list)
                    new_list_out = copy.deepcopy(out_list)
                    substitute(dict_list, new_list_in[1:])
                    substitute(dict_list, new_list_out[1:])
                    if (new_list_in[1][j] == new_list_out[2][i]):
                        new_list_in[1].pop(j)
                        new_list_out[2].pop(i)
                        new_list_out[1].extend(new_list_in[1])
                        new_list_out[2].extend(new_list_in[2])
                        index_in = new_list_in[0]
                        index_out = new_list_out[0]

                        new_list_out[0]=len(A)+1
                        if is_answer(new_list_out[1:]): #check if the new clause has resulted in an answer. If so return 1
                            temp='FINAL RES: '+str(index_in)+','+str(index_out)
                            f.write(temp)
                            file2.write(temp)
                            return 1

                        if is_found(new_list_out[1:]):
                            temp='FINAL RES: '+str(index_in)+','+str(index_out)
                            f.write(temp)
                            file2.write(temp)
                            return 1
                        #A.append(new_list_out)
                        new_list_out[1].sort()
                        new_list_out[2].sort()
                        list_c = copy.deepcopy(new_list_out)
                        new_list_out[1] = list(new_list_out[1] for new_list_out[1], _ in itertools.groupby(new_list_out[1]))
                        new_list_out[2] = list(new_list_out[2] for new_list_out[2], _ in itertools.groupby(new_list_out[2]))
                        if not is_duplicate(A,new_list_out):

                            A.append(new_list_out)
                            resf=''
                            resf = parser(new_list_out,resf)
                            #if(list_c!=new_list_out):
                                #print list_c, new_list_out
                            helper_print(index_in, index_out, dict_list, resf)
                            f_res2=str(new_list_out)+'\t\t using '+str(dict_list)+' '+str(index_in)+','+str(index_out)+'\n'
                            file2.write(f_res2)

                        else:
                            pass

    else:
        return 'FAIL'

#check if we can do resolution on the clauses
def is_reso(list1,list2,list3,list4):
    ct=0
    for ele1 in list1:
        for ele2 in list2:
            if ele1==ele2:
                 ct+=1
            if(ct>1):
                return 0
    for ele1 in list3:
        for ele2 in list4:
            if ele1==ele2:
                 ct+=1
            if(ct>1):   # Cant resolve as two negative and two pos exists
                #print "NO RES"
                return 0
    return 1

# two pointer function that performs the resolution.
#out_ct takes the count
def resolution(out_ct, A):
    temp=[]
    while out_ct<len(A):
        in_ct=0
        #in_ct takes starts from 0 reaches till the out_ct
        #print out_pos,out_neg
        while in_ct<out_ct:
            out_list = copy.deepcopy(A[out_ct])
            out_pos = out_list[1]
            out_neg = out_list[2]
            in_list=copy.deepcopy(A[in_ct])
            in_pos = in_list[1]
            in_neg = in_list[2]
            if is_reso(in_neg,out_pos,out_neg,in_pos):#check if we can resolve them
                new_list1 =in_list[1]+in_list[2]
                new_list2 = out_list[1]+out_list[2]
                dict ={}
                if (get_common_vars(new_list1,new_list2,dict)):# if common vars then change them
                    
                    apply(dict,out_pos)
                    apply(dict,out_neg)
                    #substitute(dict,in_list[2])
                    #print out_pos,out_neg
                z1 = find_new_clause(in_neg,out_pos,out_list,in_list,A)             #this appends in A
                #check if z1 is 1. If so we have reached the solution
                if z1 is 1:
                    print "YES WE HAVE A SOLUTION"
                    te = 'NUMBER OF STEPS:',len(A)
                    print te
                    file2.write(str(te))
                    return
                # check if z2 is 1. If so we have reached the solution
                z2 = find_new_clause(out_neg,in_pos,in_list,out_list,A)
                if z2 is 1:
                    print "YES WE HAVE A SOLUTION"
                    te = 'NUMBER OF STEPS:',len(A)
                    print te
                    file2.write(str(te))
                    return
            in_ct += 1

        out_ct += 1

#sort function used to sort the list based on min_length
def sort_unit(a,b):
    return len(a[1])+len(a[2])-len(b[1])-len(b[2])

#unit pref based resolution
def unit_pref(out_ct,A):
    temp=[]
    vis=Set([])
    A.sort(sort_unit)
    out_ct =1
    h=[]
    in_ct =0
    #maintaining a heap h and picking up the min_length to resolve
    while(out_ct<len(A)):
        #h = []
        #in_ct = 0

        while in_ct <out_ct:
            out_list = copy.deepcopy(A[out_ct])
            out_pos = out_list[1]
            out_neg = out_list[2]
            in_list = copy.deepcopy(A[in_ct])
            in_pos = in_list[1]
            in_neg = in_list[2]
            ind = (out_list[0],in_list[0])
            if ind not in vis:
                heappush(h,(len(out_pos)+len(in_neg)+len(out_neg)+len(in_pos),[out_list,in_list]))
                #vis.add(ind)
            else:
                pass
                #print "FOUND",ind
            in_ct += 1

        len_A = len(A)
        #as long as we have clauses in heap we can try to resolve
        while len(h) > 0:
            #print "HEAP POP"
            p = heappop(h)
            in_list = p[1][1]
            out_list = p[1][0]
            out_pos = out_list[1]
            out_neg = out_list[2]
            in_pos = in_list[1]
            in_neg = in_list[2]
            ind =(out_list[0],in_list[0])
            vis.add(ind)
            if is_reso(in_neg, out_pos, out_neg, in_pos):
                new_list1 = in_list[1]+in_list[2]
                new_list2 = out_list[1]+out_list[2]
                dict ={}

                if (get_common_vars(new_list1, new_list2, dict)):
                    apply(dict, out_pos)
                    apply(dict, out_neg)
                    #print dict
                    #substitute(dict,in_list[2])
                    #substitute(dict,in_list[1])
                #    print out_pos, out_neg

                z1 = find_new_clause(in_neg, out_pos, out_list, in_list, A)  # this appends in A
                #if Z1 is 1 we have reached the solution
                if z1 is 1:
                    print "YES WE HAVE A SOLUTION"
                    te = 'NUMBER OF STEPS:',len(A)
                    print te
                    file2.write(str(te))
                    return
                #z2 is 1. we have reached the solution
                z2 = find_new_clause(out_neg, in_pos, in_list, out_list, A)
                if z2 is 1:
                    print "YES WE HAVE A SOLUTION"
                    te = 'NUMBER OF STEPS:',len(A)
                    print te
                    file2.write(str(te))
                    return

                if (len_A < len(A)):
                    break
        if (len_A < len(A)): # found a new clause then sort the list again
            out_ct = 1
            in_ct=0
            A.sort(sort_unit)
            h=[]
        else:
            out_ct += 1
            in_ct=0

#Main unify function that get called from helper unify function
def unify(E2,E1,dict_list):
    #print "SDB",E2,E1
    res1=[]
    res2=[]
    var_list=[]
    var_list2=[]
    get_all_vars(E1, res1) # get all the vars in res1
    get_all_vars(E2, res2) # get all the vars in res2
    #IF both E1 and E2 are constants
    if E1==[] and E2 ==[]:
        return []
    if E1 != [] and E2 == []:
        print_debug('DEBUG FAIL I:: E1 is ' + str(E1) + ' E2 is ' + str(E2))
        return 'FAIL'
    elif E2 != [] and E1 == []:
        print_debug('DEBUG FAIL II:: E1 is ' + str(E1) + ' E2 is ' + str(E2))
        return 'FAIL'
    #print E1, E2
    if not isinstance(E1,list) or not isinstance(E2,list):
        if E1==E2:
            return []
        elif not isinstance(E1,list) and not isinstance(E2,list):
            if E1==E2:
                return []
            else:
                update_dict(dict_list,E1,E2)
                return dict_list.update({E1:E2})

        elif not isinstance(E1, list):
            res1 = []
            get_all_vars(E2,res1)

            if E1 in res1:
                print_debug('DEBUG FAIL 3:: E1 is ' + str(E1) + ' present in ' + str(E2)+': '+str(res1))
                return 'FAIL'
            else:
                update_dict(dict_list, E1, E2)
                return dict_list.update({E1:E2})
        #elif not isinstance(E2,list ) and get_all_vars(E2,var_list2)>0:
        elif not isinstance(E2, list):
            res1 = []
            get_all_vars(E2, res1)
            if E2 in res1:
                print_debug('DEBUG FAIL 4:: E2 is ' + str(E2) + ' present in ' + str(E1) + ': ' + str(res1))
                return 'FAIL'
            else:
                update_dict(dict_list, E2, E1)
                return dict_list.update({E2:E1})
        return 'FAIL'
    if (len(E1)>0 and len(E2)>0):
        first_E1 = E1[0]
        first_E2 = E2[0]
        rest_E1 = E1[1:]
        rest_E2 = E2[1:]
        if len(first_E1)==1 or len(first_E2)==1:
            z1 = unify(first_E1,first_E2,dict_list)
        else:
            z1 = unify_helper(first_E1,first_E2,dict_list)
        if z1=='FAIL':
            return 'FAIL'

        g1 = substitute(dict_list,rest_E1)  # perform substitution in rest_E1
        g2 = substitute(dict_list,rest_E2)  # perform substitution in rest_E2

        z2 = unify(rest_E1,rest_E2,dict_list)   # Now unify again rest_E1 and rest_E2

        if z2=='FAIL':
            return 'FAIL'

        return [z1,z2]
    return 'FAIL'




def print_debug(msg):
    if DEBUG:
        print msg
#parser for good print in file out.txt
def parser(data,resf):
    t1=[]

    data0=data[0]
    data1=data[1]
    data2=[2]
    res=''
    for pos_lit in data[1]:
        t1=[]
        parse_helper(pos_lit,t1)
        newt1 = ''.join(t1)
        if len(res)==0:
            res=newt1
        else:
            res+=' V '+newt1
    for neg_lit in data[2]:
        t1 = []
        parse_helper(neg_lit, t1)
        newt1 = ''.join(t1)
        if len(res) == 0:
            res = '~'+newt1
        else:
            res += ' V ~' + newt1

    resf=str(data[0])+'. '+res
    return resf

# hlper function to parse the file
def parse_helper(data,t1):
    if data ==[]:
        return;
    if not isinstance(data,list):
        t1+=data
        return
    len1 = len(data)
    if len1==1:
        t1+=data[0].upper()
    else:
        t1+=data[0]+'('
        data1=data[1:]
        for i,temp in enumerate(data1):
            if(i!=0):
                t1+=','
            if not isinstance(temp,list):
                # if(i==0):
                t1+=temp
                #else:
                    #t1+=','+temp
                    #print "never"
            else:
                parse_helper(temp,t1)
        t1+=')'
    return

def helper_print(index1,index2,dict, res ):
    f_res=res+'\t\t using '+str(dict)+' '+str(index1)+','+str(index2)+'\n'
    f.write(f_res)


#########################################MAIN########################
def main():
    sys.setrecursionlimit(150000)
    random.seed(time.time())
    global DEBUG
    DEBUG = 0       #FLAG FOR DEBUG
    dict_list = {}
    res = []
    global f
    global file2
    f=open('out.txt','w')
    file2=open('out2.txt','w')
    #theo can be rr, custom,harmonia,howl,test
    #method can be qa, two_pointer,unit
    #type can be reso,unit
    if(len(sys.argv) == 4):
        theo = sys.argv[2]
        method = sys.argv[1]
        goal = int(sys.argv[3])
        if method != 'two_pointer':
            print 'INCORRECT METHOD'
            return
    elif(len(sys.argv)==3):
        theo = sys.argv[2]
        method = sys.argv[1]
        if method != 'unit':
            print 'INCORRECT METHOD'
            return
    else:
        print "INCORRECT ARGS"
        return

    #print theo,method,type

    ##THEOREMS FOR TESTING RESOLUTION
    a= [[1,[ ['rr',['a']]], [ ['coyote', 'y'] ]   ],
    [2,[ ['chase', 'z',['a']] ], [ ['coyote', 'z'] ]   ],
    [3,[ ['smart', 'x'] ],[ ['rr', 'x'], ['beep', 'x'] ]],
    [4,[], [ ['coyote', 'w'],['rr' ,'u'],['catch', 'w', 'u'],['smart', 'u'] ]],
    [5,[ ['frustrated', 's'], ['catch', 's', 't'] ], [ ['coyote', 's'], ['rr', 't'], ['chase', 's', 't'] ]],
    [6,[ ['beep', 'r'] ],  [ ['rr', 'r'] ]   ],
    [7,[ [ 'coyote', ['b']] ],[]   ],               #goal
    [8,[], [ ['frustrated',['b']] ]]]

    b= [[1, [['howl', 'z']], [['hound', 'z']]],
        [2, [], [['have', 'x', 'y'], ['cat', 'y'], ['have', 'x', 'z'], ['mouse', 'z']]],
        [3, [], [['ls', 'w'],['have', 'w', 'v'],['howl', 'v']]],
        [4, [['have',['john'],['a']]], []],
        [5, [['cat', ['a']],['hound', ['a']]], []],
        [6, [['mouse', ['b']]], []],
        [7, [['ls',['john']]], []],             #goal
        [8, [['have', ['john'], ['b']]], []]]

    c= [[1, [['v', 'x'], ['s', 'x', ['f', 'x']]], [['e', 'x']]],
        [2, [['v', 'y'], ['c', ['f', 'y']]], [['e', 'y']]],
        [3, [['e', ['a']]], []],
        [4,[['d',['a']]], []],
        [5, [['d', 'z']], [['s', ['a'], 'z']]],
        [6, [], [['d', 'w'], ['v', 'w']]],
        [7, [], [['d', 'r'], ['c', 'r']]]]   #goal

    d=[[1, [['grandparent', 'x', 'y']], [['parent', 'x', 'z'], ['parent', 'z', 'y']]],
         [2, [['parent', 'x', 'y']], [['mother', 'x', 'y']]],
         [3, [['parent', 'x', 'y']], [['father', 'x', 'y']]],
         [4, [['father', ['Zeus'], ['Ares']]], []],
         [5, [['mother', ['Hera'], ['Ares']]], []],
         [6, [['father', ['Ares'], ['Harmonia']]], []],
         [7, [['answer','x']], [['grandparent', 'x', ['Harmonia']]]]  # goal
         ]



    e= [[1,[['P','x',['BETA']],['Q','x'],['S','y','res']],[]],
        [2,[['R','x'],['T','x']],[['P','x','w']]],
        [3,[['R','x']],[['Q','x']]],
        [4,[['S','y',['ZETA']]],[['R','x']]],
        [5,[],[['S','y',['ZETA']]]],
        [6,[],[['T','x']]]
    ]





    #based on theorem set the prob and goal
    if(theo == 'howl'):
        prob=b
        #goal =6
    elif(theo == 'rr'):
        prob=a
        #goal = 6
    elif theo == 'custom':
        prob = c
        #goal = 6
    elif theo == 'harmonia':
        if method == 'qa':
            prob =f2
            #goal = 6
        else:
            prob=d
            #goal = 6
    elif theo == 'test':
        prob =e
        #goal = 4
    else:
        print 'INCORRECT NAME'
        return

    for k in prob:
        resf=''
        resf=parser(k,resf)+'\n'
        f.write(resf)
        new_str = str(k) +'\n'
        file2.write(new_str)
    #check for the method and call the function
    if(method == 'two_pointer'):
        resolution(goal,prob)   # two pointer
    elif(method == 'unit'):
        goal =6
        unit_pref(goal,prob)    #unit preference
    else:
        print "INCORRECT METHOD"


if __name__ == "__main__":
    main()
