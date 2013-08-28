#test tic tac toe
import os
import time
from board_game_engine import gameplay
from random import randint
from switches import case
from switches import switch
##from switch import case



class BOARD:
    def __init__(self, parent, override=False):
        picture=parent.send() if (not override) else parent
        self.pic=[part[:] for part in picture]
        self.stasis=[part[:] for part in self.pic]

    def rebuild(self):
        self.pic=[part[:] for part in self.stasis]

    def mark(self, thing, location):
        self.pic[location[0]][location[1]]=thing

    def view(self, spacer=""):
        for row in self.pic:
            print(spacer.join(row))

    def send(self):
        return [part[:] for part in self.pic]
        
        
def total_nodes(n):
    return (n*(1+total_nodes(n-1))) if (n>1 and n<995) else 1

def board_conversion(board): #takes image only
    solution=[]
    visual=[part[:] for part in board]
    for y in range(len(board)):
        for x in range(len(board[y])):
            numpad=(7-(3*y))+x
            if (board[y][x]=="*"):
                visual[y][x]=str(numpad)
                solution.append(numpad)
    return (visual, solution)




def moves(board): #takes image only
    spots=[]
    for y in range(len(board)):
        for x in range(len(board[y])):
            if(board[y][x]=="*"):
                spots.append([y, x])
    return spots

def sums(board):
    intboard=board.send()
    for a in range(len(intboard)):
        for b in range(len(intboard[a])):
##            if(intboard[a][b]=="O"):
##                intboard[a][b]=1
##            elif(intboard[a][b]=="X"):
##                intboard[a][b]=-1
##            else:
##                intboard[a][b]=0
            intboard[a][b]=switch(intboard[a][b], case("O", lambda x=0: 1), case("X", lambda x=0:-1), default=(lambda x=0: x))
    #you're not going to like this next part
    _sums=[] # r1, r2, r3, c1, c2, c3, d1, d2
    _sums.append(sum(intboard[0]))
    _sums.append(sum(intboard[1]))
    _sums.append(sum(intboard[2]))
    for a in range(len(board.pic)):
        if(len(_sums)>=4):
            _sums[3]+=intboard[a][0]
        else:
            _sums.append(intboard[a][0])
        if(len(_sums)>=5):
            _sums[4]+=intboard[a][1]
        else:
            _sums.append(intboard[a][1])
        if(len(_sums)>=6):
            _sums[5]+=intboard[a][2]
        else:
            _sums.append(intboard[a][2])
    _sums.append(intboard[0][0])
    _sums[6]+=intboard[1][1]
    _sums[6]+=intboard[2][2]
    _sums.append(intboard[0][2])
    _sums[7]+=intboard[1][1]
    _sums[7]+=intboard[2][0]
    #print(_sums)
    return _sums
        
def game_over(board):
    scores=sums(board)
    human_best=max(scores)
    comp_best=min(scores)
    if(human_best==3):
        winning_pos=scores.index(3)
        print("\nThe Player Wins!")
        board.view()
        return True
    elif(comp_best==-3):
        winning_pos=scores.index(-3)
        print("\nThe Computer Wins!")
        board.view()
        return True
    else:
        if(len(moves(board.send()))<1):
            print("\nTie!")
            board.view()
            return True
    return False

def human_move(board):
    print("\n\n\n---------------YOUR TURN-----------------")
    gamestate=board_conversion(board.send())
    for row in gamestate[0]:
        print(" ".join(row))
    valid=False
    while(not valid):
        choice=input("\nWhich move will you make: ")
        for option in gamestate[1]:
            valid=True if (int(choice)==option) else valid
    print("\n\nYour Choice:")
    for y in range(len(gamestate[0])):
        for x in range(len(gamestate[0][y])):
            if(gamestate[0][y][x]==str(choice)):
                board.mark("O", [y,x])
    board.view()
    return board

def computer_move(board):
    print("\nComputer is thinking.  Please be patient")
    avaliable=moves(board.send())
    evaluated=[]
    print("Crunching ", total_nodes(len(avaliable)), " nodes in tree")
    next_board=BOARD(board)
    for possibility in avaliable:
        next_board.rebuild()
        next_board.mark("X", possibility)
        if(min(sums(next_board))==-3):
            evaluated=[[possibility, 999]]
            break
        evaluated.append([possibility, branch_eval(next_board, "O")])
        if(evaluated[len(evaluated)-1][1]==1):
            evaluated[len(evaluated)-1][1]=-1000000
        else:
            evaluated[len(evaluated)-1][1]=abs(evaluated[len(evaluated)-1][1])
        #print(evaluated[len(evaluated)-1][1])
        #for row in next_board:
            #print("".join(row))
        #print("\n\n")
    evaluated.sort(key=lambda x : x[1])
    evaluated.reverse()
    try:
        evaluated.insert(0,(evaluated.pop(evaluated.index(1)))) # :)
    except ValueError:
        pass            
    #computer seems to make valid defensive moves, but tends to pick awkward offensive moves
    if(len(evaluated)==1):
        choice=evaluated[0][0]
    elif(evaluated[0][1]==evaluated[1][1]):
        seek=evaluated[0][1]
        max_list=[]
        for pairing in evaluated:
            if(pairing[1]==seek):
                max_list.append(pairing)
        #im only treating the symptoms of a problem here.  until i can identify the problem
        #in a small unidentified case, it encounters an IndexError when attempting this
        try:
            choice=max_list[randint(0, len(max_list))][0]
        except IndexError:
            choice=evaluated[0][0]
            print("Encountered Odd Index Error!\n", max_list)
    else:
        choice=evaluated[0][0]
    board.mark("X", choice)
    #print("\n\n\n")
    #for row in board:
        #print("".join(row))
    #input("\nPress enter to continue")
    return board

def branch_eval(branch, player, lower_sum=0):
    avaliable=moves(branch.send())
    children=[]
    newboard=BOARD(branch)
    for pair in avaliable:
        newboard.rebuild()
        newboard.mark(player, pair)
        _max=max(sums(newboard))
        _min=min(sums(newboard))
        if(_max==3 and _min!=-3):
            score=1
            if(player=="O"):
                return 1
        elif(_min==-3 and _max!=3):
            score=-1
            if(player=="X"):
                return -1
        else:
            score=0
        children.append([BOARD(newboard), score])
    next_player="O" if (player=="X") else "X"
    branch_score=0
    for child in children:
        if(child[1]==0):
            child[1]=branch_eval(child[0], next_player)
        branch_score+=child[1]
    return branch_score
            
                      
grid=[]
grid.append(["*","*","*"])
grid.append(["*","*","*"])
grid.append(["*","*","*"])
grid=BOARD(grid, True)

#print(str(branch_eval(grid, "O")))



gameplay(grid, computer_move, human_move, game_over)
