#test tic tac toe
import os
import time
from board_game_engine import gameplay
from random import randint

def total_nodes(n):
    return (n*(1+total_nodes(n-1))) if (n>1 and n<995) else 1

def board_conversion(board):
    solution=[]
    visual=[part[:] for part in board]
    for y in range(len(board)):
        for x in range(len(board[y])):
            numpad=(7-(3*y))+x
            if (board[y][x]=="*"):
                visual[y][x]=str(numpad)
                solution.append(numpad)
    return (visual, solution)


def toarray(string):
    return [a for a in string]

def atos(picture):
    final_string=""
    for row in picture:
        final_string+="".join(row)
    return final_string

def stoa(string, leny):
    lenx=(len(string))/leny
    if(int(lenx)!=lenx):
        return Nonestar
    final_array=[]
    for y in range(leny):
        current_row=[]
        for x in range(lenx):
            current_row.append(string[x+(y*lenx)])
        final_array.append(current_row)
    return final_array


def moves(board):
    spots=[]
    for y in range(len(board)):
        for x in range(len(board[y])):
            if(board[y][x]=="*"):
                spots.append([y, x])
    return spots

def sums(board):
    intboard=[thing[:] for thing in board]
    for a in range(len(intboard)):
        for b in range(len(intboard[a])):
            if(intboard[a][b]=="O"):
                intboard[a][b]=1
            elif(intboard[a][b]=="X"):
                intboard[a][b]=-1
            else:
                intboard[a][b]=0
    #you're not going to like this next part
    _sums=[] # r1, r2, r3, c1, c2, c3, d1, d2
    _sums.append(sum(intboard[0]))
    _sums.append(sum(intboard[1]))
    _sums.append(sum(intboard[2]))
    for a in range(len(board)):
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
        for a in range(len(board)):
            print("".join(board[a]))
        return True
    elif(comp_best==-3):
        winning_pos=scores.index(-3)
        print("\nThe Computer Wins!")
        for a in range(len(board)):
            print("".join(board[a]))
        return True
    else:
        if(len(moves(board))<1):
            print("\nTie!")
            for a in range(len(board)):
                print("".join(board[a]))
            return True
    return False

def human_move(board):
    print("\n\n\n---------------YOUR TURN-----------------")
    gamestate=board_conversion(board)
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
            board[y][x]="O" if (gamestate[0][y][x]==str(choice)) else board[y][x]
    for row in board:
        print("".join(row))
    return board

def computer_move(board):
    print("\nComputer is thinking.  Please be patient")
    avaliable=moves(board)
    evaluated=[]
    print("Crunching ", total_nodes(len(avaliable)), " nodes in tree")
    for possibility in avaliable:
        next_board=[thing[:] for thing in board]
        next_board[possibility[0]][possibility[1]]="X"
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
        out=evaluated.pop(evaluated.index(1))
        evaluated.append(out)
        evaluated.reverse()
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
        try:
            choice=max_list[randint(0, len(max_list))][0]
        except IndexError:
            choice=evaluated[0][0]        
    else:
        choice=evaluated[0][0]
    board[choice[0]][choice[1]]="X"
    #print("\n\n\n")
    #for row in board:
        #print("".join(row))
    #input("\nPress enter to continue")
    return board

def branch_eval(branch, player, lower_sum=0):
    avaliable=moves(branch)
    children=[]
    for pair in avaliable:
        newboard=[thing[:] for thing in branch]
        newboard[pair[0]][pair[1]]=player
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
        children.append([[thing[:] for thing in newboard], score])
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

    

#print(str(branch_eval(grid, "O")))
gameplay(grid, computer_move, human_move, game_over)
