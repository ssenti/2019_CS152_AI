#watched and referenced this tutorial to understand the basic concept and logic, and 
#implementation of MiniMaxAlgorithms: https://www.youtube.com/watch?v=gNhbZUOMl0M (Payne, 2014)

#referenced Russell & Novig's textbook to understand the basic concept and logic,
#implementation of MiniMaxAlgorithms and Alpha-Beta pruning

from sys import maxsize
from tabulate import tabulate
from copy import deepcopy
from itertools import groupby
import numpy

b = 3 #length of the board -- it should ideally be up to 15
n = 3 #number of straight lines

#test start_states (simulation below)
start_state = [[_] * b for i in range(b)]
start_state_2 = [[_, _, _], 
                 [_, 1, _], 
                 [-1, _, 1]]
    

class Node:
    def __init__(self, depth, player, row, col, state):
        self.depth = depth #225 to 0
        self.player = player #1 or -1
        self.state = state #starts with 225 empty spaces
        self.r = row #gives row of previous action made
        self.c = col #gives col of previous action made
        self.children = []
        #child nodes
        self.createChildren()
        #0 for draw / maxsize for player "1" win / -maxsize for player "-1" win
        self.utility = terminalTest(self)
    
    #creates the children nodes attached to this node
    def createChildren(self):
        if self.depth >= 0:
            for row in range(len(self.state)):
                for col in range(len(self.state)):
                    if self.state[row][col] == _:
                        new_state = deepcopy(self.state)
                        new_state[row][col] = self.player
                        self.children.append(Node(self.depth-1,
                                             -self.player, row, col,new_state))
    
    #string representation of a state
    def __str__(self):
        return tabulate(self.state, tablefmt="fancy_grid")
    
def MinMaxDecision(node):
    #find the best utility value out of all the child options
    best_Util = GetMaxValue(node, -maxsize, maxsize)
    #tracking the action (which is represented by the child node) that led to the best_util
    for child in node.children:
        if child.utility == best_Util:
            action = [child.r, child.c]
            return action
        
def GetMaxValue(node, alpha, beta):
    #if there was a win, return the maxsize value
    if terminalTest(node) is not 0:
        return terminalTest(node)
    else:
        #if there was no win, but all depth has been exhausted, then return 0
        if node.depth == 0:
            return 0
        #if there was no win, and the depth has not been exhausted, keep going
        else:
            #set default utility value
            v = maxsize *-node.player
            v_list = [v]
            for child in node.children:
                #call the GetMinValue algorithm
                if v <= GetMinValue(child, alpha, beta):
                    #if any of the child noe utility could "beat" the default value, replace it
                    v_list.append(child.utility)
                #prune away if optimal solution already found
                if beta <= max(v_list):
                    return max(v_list)
                a_list = deepcopy(v_list)
                a_list.append(alpha)
                alpha = max(a_list)
            return max(v_list)

        
def GetMinValue(node, alpha, beta):
    #if there was a win, return the maxsize value
    if terminalTest(node) is not 0:
        return terminalTest(node)
    else:
        #if there was no win, but all depth has been exhausted, then return 0
        if node.depth == 0:
            return 0
        else:
            #similar process to GetMaxValue algorithm
            v = maxsize *-node.player
            v_list = [v]
            for child in node.children:
                if v <= GetMaxValue(child, alpha, beta):
                    v_list.append(child.utility)
                if alpha >= min(v_list):
                    return min(v_list)
                b_list = deepcopy(v_list)
                b_list.append(beta)
                beta = min(b_list)
            return min(v_list)
    
def winCheck_row(node):
    for row in node.state:
        consec_row = [[k, sum(1 for i in g)] for k, g in groupby(row)]
        consec_row_len = []
        for i in consec_row:
            consec_row_len.append(i[1])
            if max(consec_row_len) >= n and i[0] is not _:
                return maxsize * int(i[0])
                break
    return 0

def winCheck_col(node):
    trans = numpy.transpose(node.state)
    for row in trans:
        consec_col = [[k, sum(1 for i in g)] for k, g in groupby(row)]
        consec_col_len = []
        for i in consec_col:
            consec_col_len.append(i[1])
            if max(consec_col_len) >= n and i[0] is not _:
                return maxsize * int(i[0])
                break
    return 0

def winCheck_diag(node):
    matrix = numpy.array(node.state)
    l = len(node.state)
    #referenced:Tolonen(2011)'s code (in reference section)
    diag = [matrix[::-1,:].diagonal(i) for i in range(-l,l)]
    diag.extend(matrix.diagonal(i) for i in range(l,-l,-1))
    diag = [n.tolist() for n in diag]
    #get diagonals
    for row in diag:
        consec_diag = [[k, sum(1 for i in g)] for k, g in groupby(row)]
        consec_diag_len = []
        for i in consec_diag:
            consec_diag_len.append(i[1])
            if max(consec_diag_len) >= n and i[0] is not _:
                return maxsize * int(i[0])
                break
            
#checking for terminal using the winCheck scearios above
def terminalTest(node):
    winCheck = [winCheck_row(node), winCheck_col(node), winCheck_diag(node)]
    if set(winCheck) != {0}:
        value = set(winCheck)
        if 0 in value:
            value.remove(0)
        return value.pop()
    else:
        return 0

#simple simulation for the next "optimal move" for two different states
    
j = Node(5, 1, 0, 0, start_state_2)

print(MinMaxDecision(j))

a = Node(9, 1, 0, 0, start_state)

print(MinMaxDecision(a))
