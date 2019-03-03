
from queue import PriorityQueue
from tabulate import tabulate
import copy

#Define the PuzzleNode class
class PuzzleNode:
    def __init__(self,state,fval,gval,parent=None):
        self.state = state
        self.fval = fval
        self.gval = gval
        #parent attribute to point to a parent node
        self.parent = parent
        self.pruned = False

    #comparison function based on f cost
    def __lt__(self,other):
        return self.fval < other.fval

    #print out a grid showing the board state
    def __str__(self):
        return tabulate(self.state, tablefmt="fancy_grid")

#the heuristic function for misplaced tiles
def h_misplaced(state):
    count = 0
    
    #Define the goal
    g = len(state[0])
    #create a simple list ordered 0 to g*g
    temp_goal = [i for i in range(g*g)]
    #then break the list into chunks of g using list comprehension
    goal = [temp_goal[i*g:(i+1)*g] for i in \
            range((len(temp_goal)+g-1)//g)]
    
    #for simplicity, take off the inner square brackets 
        #for the state and goal
    new_state = [j for i in state for j in i]
    new_goal = [j for i in goal for j in i]
    #through a loop, count how many elements are misplaced
    for i in range(0, g*g):
        if new_state[i] is not new_goal[i]:
            count += 1
    return count

#the heuristic function for manhattan distance
def h_manhattan(state):
    count = 0
    
    #Define the goal
    g = len(state[0])
    temp_goal = [i for i in range(g*g)]
    goal = [temp_goal[i*g:(i+1)*g] for i in \
            range((len(temp_goal)+g-1)//g)]
    
    #for every tile in the state
    for sublist in state:
        for i in sublist:
            #a denotes to the tile's x coordinate
            a = state.index(sublist)
            #b denotes to the tile's y coordinate
            b = sublist.index(i)
            #for every tile in the goal state
            for sublistt in goal:
                for k in sublistt:
                    if i in sublistt:
                        #c denotes to the goal tile's x coordinate
                        c = goal.index(sublistt)
                        #d denotes to the goal tile's y coordinate
                        d = sublistt.index(i)
                        #manhattan distance is the sum of the 
                            #difference in (a & c) + (b & d)
                        manh_for_i = (abs(a-c)+abs(b-d))
                        count += manh_for_i   
    #the above "for k in sublistt" triple counts each indices 
        #so divide count by g
    return(int(count/g))

heuristics = [h_misplaced, h_manhattan]

#finding the coordinates for the 0 tile
def find_zero(lst):
    for a, b in enumerate(lst):
        try:
            return (a, b.index(0))
        except ValueError:
            pass          

#move the 0 tile to either up, down, left, right
def swap(lst, directions):
    #create a new state to make changes to the original state
    new_lst = copy.deepcopy(lst) 
    q = find_zero(lst)
    if directions == "up":
        #if the zero would hit a wall doing this function,
            #just return(0)
        if q[0] == 0: return(0)
        else:
            a, b = q[0], q[0]-1
            #swap coordinate of "up" tile with the coordinate of 0
            new_lst[a][q[1]], new_lst[b][q[1]] = \
            new_lst[b][q[1]], new_lst[a][q[1]]
            return(new_lst)
        
    if directions == "down":
        if q[0] == len(lst[0])-1: return(0)
        else:
            a, b = q[0], q[0]+1
            new_lst[a][q[1]], new_lst[b][q[1]] = \
            new_lst[b][q[1]], new_lst[a][q[1]]
            return(new_lst)
        
    if directions == "left":
        if q[1] == 0: return(0)
        else:
            a, b = q[1], q[1]-1
            new_lst[q[0]][a], new_lst[q[0]][b] = \
            new_lst[q[0]][b], new_lst[q[0]][a]
            return(new_lst)
        
    if directions == "right":
        if q[1] == len(lst[0])-1: return(0)
        else:
            a, b = q[1], q[1]+1
            new_lst[q[0]][a], new_lst[q[0]][b] = \
            new_lst[q[0]][b], new_lst[q[0]][a]
            return(new_lst)

#Define the skeleton of a function solvePuzzle
#The design of this code has been influenced by 
    #R. Shekhar's A* search code in cs152 session 3.1
def solvePuzzle(n, state, heuristic, prnt=False):
    #Your implementation should first test whether or not the state 
        #provided is of the correct size and format, and contains 
        #every number from 0 to n^2 − 1 precisely once.
    if not all([any(i in l for l in state) for i in range(n)]):
        return 0, 0, -1
    if n < 2:
        return 0, 0, -1
    if len(state) is not n:
        return 0, 0, -1
    for e in range(n):
        if len(state[e]) is not n:
            return 0, 0, -1
    
    #Define the goal
    #create a simple list ordered 0 to n*n
    temp_goal = [i for i in range(n*n)]
    #then break the list into chunks of g using list comprehension
    goal = [temp_goal[i*n:(i+1)*n] for i in \
            range((len(temp_goal)+n-1)//n)]
    
    #define the start node
    start_node = PuzzleNode(state,heuristic(state),0) 
    
    #dictionary with cost to reach all visited nodes
    costs_db = {str(start):start_node}
    
    #define frontier through priority queue
    frontier = PriorityQueue()
    frontier.put(start_node)
    
    expansion_counter = 0
    
    while not frontier.empty():
    #take the next available node from the priority queue
        cur_node = frontier.get()
        
        #skip if this node has been marked for removal
        if cur_node.pruned:
            continue 

        #end function if we are at the goal
        if cur_node.state == goal: break
            
        #expand the node to up, down, left and right
        for d in ["up", "down", "left", "right"]:
            next_state = swap(cur_node.state, d)
            if next_state is not 0:
                #tentative cost value for child
                gval = cur_node.gval + 1 

                #if the child node has already been explored
                if str(next_state) in costs_db:
                    if costs_db[str(next_state)].gval > gval:
                        #mark it "pruned"
                        costs_db[str(next_state)].pruned = True 
                    else:
                        continue

                #heuristic cost from next node to goal
                hval = heuristic(next_state) 
                #create next child node
                next_node = PuzzleNode(next_state,gval+hval,\
                                       gval,cur_node) 
                frontier.put(next_node)
                #mark it "explored"
                costs_db[str(next_state)] = next_node
        expansion_counter = expansion_counter + 1
    
    if prnt:
        #reconstruct the optimal path
        optimal_path = [cur_node.state]
        while cur_node.parent:
            optimal_path.append((cur_node.parent).state)
            cur_node = cur_node.parent
        #the number of steps to optimally reach the goal state 
            #from the initial state
        print("A* search completed in %d steps\n"% \
              expansion_counter)
        print("Max frontier Size: %d\n"%frontier.qsize())
        print("Optimal Path to Goal:")
        for s in optimal_path[::-1]:
            print(s)
    return expansion_counter, frontier.qsize(), 0

scrambled_3 = [[[5,7,6],[2,4,3],[8,1,0]], 
               [[7,0,8],[4,6,1],[5,3,2]],
                 [[2,3,7],[1,8,0],[6,5,4]]]

results = []

#prints out the results from testing the boards on scrambled_3
for board in scrambled_3:
    for heuristic in heuristics:
        solve = solvePuzzle(len(board[0]), board, heuristic, \
                            prnt=False)
        results.append(list(solve))
        print(solve)

##reorganizing the results for tabulation preparation
results_steps_l = []
for i in results:
    results_steps_l.append(i[0])
#break the results_steps list into chunks of 2 using list comprehension
results_steps = [results_steps_l[i*2:(i+1)*2] for i in \
            range((len(results_steps_l)+1)//2)]
for j in results_steps:
    j.insert(0, (results_steps.index(j)+1))
    
results_front_l = []
for i in results:
    results_front_l.append(i[1])
results_front = [results_front_l[i*2:(i+1)*2] for i in \
            range((len(results_front_l)+1)//2)]
for j in results_front:
    j.insert(0, (results_front.index(j)+1))

##print results in table
print("\nTable 1: Performance of heuristics in terms of \
number of steps taken \n")
print(tabulate(results_steps, headers=["board","h_misplaced\
", "h_manhattan"],  tablefmt="fancy_grid"))
print("\n\nTable 2: Performance of heuristics in terms of \
maximum frontier size \n")
print(tabulate(results_front, headers=["board","h_misplaced\
", "h_manhattan"],  tablefmt="fancy_grid"))
