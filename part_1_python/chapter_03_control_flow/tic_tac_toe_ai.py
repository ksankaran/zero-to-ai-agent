# From: Zero to AI Agent, Chapter 3, Section 3.7
# tic_tac_toe_ai.py
# Tic-Tac-Toe vs AI (without functions)

print("=" * 40)
print("TIC-TAC-TOE vs AI")
print("=" * 40)
print("You are X, AI is O")
print("Positions are numbered 1-9:")
print("")
print(" 1 | 2 | 3 ")
print("-----------")
print(" 4 | 5 | 6 ")
print("-----------")
print(" 7 | 8 | 9 ")
print("")

# Initialize the board (using individual variables)
pos1 = " "
pos2 = " "
pos3 = " "
pos4 = " "
pos5 = " "
pos6 = " "
pos7 = " "
pos8 = " "
pos9 = " "

game_over = False
winner = None

while not game_over:
    # Display current board
    print("")
    print(f" {pos1} | {pos2} | {pos3} ")
    print("-----------")
    print(f" {pos4} | {pos5} | {pos6} ")
    print("-----------")
    print(f" {pos7} | {pos8} | {pos9} ")

    # Player move
    valid_move = False
    while not valid_move:
        move = int(input("\nYour move (1-9): "))

        # Check each position
        if move == 1 and pos1 == " ":
            pos1 = "X"
            valid_move = True
        elif move == 2 and pos2 == " ":
            pos2 = "X"
            valid_move = True
        elif move == 3 and pos3 == " ":
            pos3 = "X"
            valid_move = True
        elif move == 4 and pos4 == " ":
            pos4 = "X"
            valid_move = True
        elif move == 5 and pos5 == " ":
            pos5 = "X"
            valid_move = True
        elif move == 6 and pos6 == " ":
            pos6 = "X"
            valid_move = True
        elif move == 7 and pos7 == " ":
            pos7 = "X"
            valid_move = True
        elif move == 8 and pos8 == " ":
            pos8 = "X"
            valid_move = True
        elif move == 9 and pos9 == " ":
            pos9 = "X"
            valid_move = True
        else:
            print("Invalid move! Try again.")

    # Check for winner after player move
    winner = None
    # Check rows
    if pos1 == pos2 == pos3 != " ":
        winner = pos1
    elif pos4 == pos5 == pos6 != " ":
        winner = pos4
    elif pos7 == pos8 == pos9 != " ":
        winner = pos7
    # Check columns
    elif pos1 == pos4 == pos7 != " ":
        winner = pos1
    elif pos2 == pos5 == pos8 != " ":
        winner = pos2
    elif pos3 == pos6 == pos9 != " ":
        winner = pos3
    # Check diagonals
    elif pos1 == pos5 == pos9 != " ":
        winner = pos1
    elif pos3 == pos5 == pos7 != " ":
        winner = pos3

    if winner == "X":
        # Display final board
        print("")
        print(f" {pos1} | {pos2} | {pos3} ")
        print("-----------")
        print(f" {pos4} | {pos5} | {pos6} ")
        print("-----------")
        print(f" {pos7} | {pos8} | {pos9} ")
        print("")
        print("You win! Great job!")
        game_over = True
    else:
        # Check if board is full (tie)
        board_full = (pos1 != " " and pos2 != " " and pos3 != " " and
                      pos4 != " " and pos5 != " " and pos6 != " " and
                      pos7 != " " and pos8 != " " and pos9 != " ")

        if board_full:
            # Display final board
            print("")
            print(f" {pos1} | {pos2} | {pos3} ")
            print("-----------")
            print(f" {pos4} | {pos5} | {pos6} ")
            print("-----------")
            print(f" {pos7} | {pos8} | {pos9} ")
            print("")
            print("It's a tie!")
            game_over = True
        else:
            # AI move
            print("")
            print("AI is thinking...")

            # AI strategy: try center first, then corners, then edges
            if pos5 == " ":
                pos5 = "O"
            elif pos1 == " ":
                pos1 = "O"
            elif pos3 == " ":
                pos3 = "O"
            elif pos7 == " ":
                pos7 = "O"
            elif pos9 == " ":
                pos9 = "O"
            elif pos2 == " ":
                pos2 = "O"
            elif pos4 == " ":
                pos4 = "O"
            elif pos6 == " ":
                pos6 = "O"
            elif pos8 == " ":
                pos8 = "O"

            # Check if AI won
            winner = None
            # Check rows
            if pos1 == pos2 == pos3 != " ":
                winner = pos1
            elif pos4 == pos5 == pos6 != " ":
                winner = pos4
            elif pos7 == pos8 == pos9 != " ":
                winner = pos7
            # Check columns
            elif pos1 == pos4 == pos7 != " ":
                winner = pos1
            elif pos2 == pos5 == pos8 != " ":
                winner = pos2
            elif pos3 == pos6 == pos9 != " ":
                winner = pos3
            # Check diagonals
            elif pos1 == pos5 == pos9 != " ":
                winner = pos1
            elif pos3 == pos5 == pos7 != " ":
                winner = pos3

            if winner == "O":
                # Display final board
                print("")
                print(f" {pos1} | {pos2} | {pos3} ")
                print("-----------")
                print(f" {pos4} | {pos5} | {pos6} ")
                print("-----------")
                print(f" {pos7} | {pos8} | {pos9} ")
                print("")
                print("AI wins! Better luck next time!")
                game_over = True

print("")
print("Thanks for playing!")
print("=" * 40)
