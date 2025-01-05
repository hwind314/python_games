import functions2 as f
import random

# transfer tile set from functions.py
nums = f.nums
winds = f.winds
joker = f.joker
dragons = f.dragons
flowers = f.flowers
full_set = f.full_set

# setup game
my_hand = []
my_stack = []
discards = []

# opponents
while True:
    n_players = input("How many players in this game? ")
    try:
        n_players = int(n_players)  # Attempt to convert to integer
        if n_players == 3 or n_players == 4:
            break  # Exit the loop if successful
    except ValueError:
        print("Value invalid. Please try again.")

players = ["player"]
players_hands = {}
players_stacks = {}

for n in list(range(int(n_players) - 1)):
    player_name = "opponent_" + str(n)
    players.append(player_name)
    players_hands[player_name] = []
    players_stacks[player_name] = []
    f.draw(players_hands[player_name], players_stacks[player_name], 13)

# order of game
random.shuffle(players)
print("Order of game: " + str(players))

# initiate game
input("Press 'Enter' to start game.")

# set up player hand
f.draw(my_hand, my_stack, 13)
f.show(my_hand, my_stack)

# START GAME
round_counter = 1
current_player_index = 0

while True:
    print("ROUND " + str(round_counter))

    player = players[current_player_index]
    print(f"{player}'s move.")

    # check if set still has tiles
    if len(full_set) == 0:
        print("No more tiles. No winner.")
        break

    # player move
    if player == "player":
        f.show(my_hand, my_stack)
        old_hand = my_hand.copy()

        # draw tile
        f.draw(my_hand, my_stack, 1)
        new_hand = my_hand.copy()

        # check if win
        if f.check_win(my_hand):
            print("Congratulations! You've won!")
            break

        # Find the new tile
        new_tile = None
        if len(new_hand) > len(old_hand):
            new_tile_set = set(new_hand) - set(old_hand)
            if new_tile_set:
                new_tile = new_tile_set.pop()  # Extract the new tile from the set
            else:
                # Handle case where there are duplicates in `old_hand` or `new_hand`
                for tile in new_hand:
                    if new_hand.count(tile) > old_hand.count(tile):
                        new_tile = tile
                        break

        if new_tile:
            print("Tile drawn: " + new_tile)
        else:
            print("No new tile detected.")

        # discard
        f.discard(my_hand, discards)

        # show
        f.show(my_hand, my_stack)

    else:
        # opponent move
        # draw tile
        f.draw(players_hands[player], players_stacks[player], 1)

        # check if opponent can win
        if f.check_win(players_hands[player]):
            print(player + " has won. You've lost.")
            break

        # discard random tile
        f.opponent_discard(players_hands[player], discards)

        # check if player can pong / kong
        opponent_discard = discards[-1]
        print(opponent_discard)

        result = f.possible_move(opponent_discard, my_hand)

        if result is None or result[0] == "none":
            print("No possible move")
        else:
            claim, moves = result

            # Ensure unique moves
            if claim == "pong":
                print("Pong options:")
            else:
                print("Kong options:")

            # Display all possible options
            for i, move in enumerate(moves, start=1):
                print(f"{i}: {move}")

            # Ask the player if they want to make a move
            while True:
                make_move = input(f"Would you like to {claim}? (y/n): ").lower()
                if make_move in ("y", "n"):
                    break
                print("Invalid input. Please type 'y' or 'n'.")

            if make_move == "y":
                # Handle selection if there are multiple options
                if len(moves) > 1:
                    while True:
                        try:
                            selected_option = int(input(f"Select an option (1-{len(moves)}): ")) - 1
                            if 0 <= selected_option < len(moves):
                                break
                            else:
                                print(f"Invalid option. Please choose a number between 1 and {len(moves)}.")
                        except ValueError:
                            print("Invalid input. Please enter a number.")
                else:
                    selected_option = 0  # Only one option

                # Get the selected move
                move = moves[selected_option]
                print(f"You chose: {move}")

                # Remove tile from discards (assuming the last discard is being removed)
                discards.pop()

                # Remove tiles from hand and add to stack
                for tile in move:
                    if tile not in my_hand:
                        my_stack.append(tile)
                    else:
                        my_hand.remove(tile)
                        my_stack.append(tile)

                # redraw to 13 and show
                f.draw(my_hand, my_stack, 13 - len(my_hand))
                my_stack.sort()
                flattened_stack = [item for sublist in my_stack for item in
                                   (sublist if isinstance(sublist, list) else [sublist])]
                flattened_stack.sort()  # Sort stack
                my_stack = flattened_stack

                f.show(my_hand, my_stack)


    print(f"End of ROUND {round_counter}")
    current_player_index += 1
    round_counter += 1

    # start next round
    if current_player_index >= len(players):
        current_player_index = 0

    input("Press 'Enter' for next player")

# allow other players to pong/kong

# fix line 130: when player can pong/kong
