def gameplay(gameboard, p1_move, p2_move, endgame):
    print("Starting Game: ")
    End=False
    raw_in=input("Who goes first, player 1 or player 2? ")
    first_player=1 if (raw_in=="1" or raw_in=="p1" or raw_in=="player 1") else 2
    while(not End):
        gameboard=p1_move(gameboard)
        End=endgame(gameboard)
        if(not End):
            gameboard=p2_move(gameboard)
            End=endgame(gameboard)
    return None
