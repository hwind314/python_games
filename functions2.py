import random

# TILE SET
num = range(1, 10)

circle_n = []
bamboo_n = []
character_n = []

for n in num:
    circle_n.append("c." + str(n))
    bamboo_n.append("b." + str(n))
    character_n.append("n." + str(n))

nums = circle_n + bamboo_n + character_n

winds = ["wind.n", "wind.s", "wind.e", "wind.w"]

joker = ["joker"]

dragons = ["dragon.red", "dragon.green", "dragon.white"]

flowers = ["flower.1", "flower.2", "flower.3", "flower.4"]

set1 = nums + winds + joker + dragons + flowers


def repeat_list_flat(input_list, number_to_repeat):
    return input_list * number_to_repeat


full_set = repeat_list_flat(set1, 4)


# FUNCTIONS
def check_flower(player_hand, player_stack):
    changes = 0
    to_remove = []
    to_add = []
    flower_add = []

    for x_tile in player_hand:
        if x_tile in flowers:
            player_stack.append(x_tile)
            to_remove.append(x_tile)
            draw(to_add, flower_add, 1)
            changes += 1

    for x_tile in to_remove:
        player_hand.remove(x_tile)

    for x_tile in to_add:
        player_hand.append(x_tile)

    for x_tile in flower_add:
        player_stack.append(x_tile)

    if changes != 0:
        check_flower(player_hand, player_stack)

    player_hand.sort()


def draw(player_hand, player_stack, n_to_draw):
    for _ in list(range(n_to_draw)):
        r_tile = random.choice(full_set)
        player_hand.append(r_tile)
        full_set.remove(r_tile)

        # check flowers
        check_flower(player_hand, player_stack)


def show(player_hand, stack):
    print("Your Hand: ")
    print(player_hand)
    print("Your Stack: ")
    print(stack)


def discard(player_hand, discards):
    discard_tile = input("Which tile to discard? ")

    while discard_tile not in player_hand:
        discard_tile = input("Tile Invalid. please try again: ")

    player_hand.remove(discard_tile)
    discards.append(discard_tile)


def opponent_discard(player_hand, discards):
    pairs = []

    used = []
    unused = []

    for tile in player_hand:
        if tile in used:
            continue
        else:
            # check picture tiles
            if tile not in nums:
                # check if can be paired
                if player_hand.count(tile) == 1:
                    unused.append(tile)
                elif player_hand.count(tile) == 3:
                    for _ in list(range(3)):
                        used.append(tile)
                else:
                    pairs.append([tile, tile])
                    for _ in list(range(2)):
                        used.append(tile)
            # check number tiles:
            else:
                # check for same tiles
                if player_hand.count(tile) == 2:
                    pairs.append([tile, tile])
                    for _ in list(range(2)):
                        used.append(tile)
                elif player_hand.count(tile) == 3:
                    for _ in list(range(3)):
                        used.append(tile)
                else:
                    # check ordered pairing
                    opponent_result = check_num_in_row(tile, player_hand)

                    if opponent_result is None or opponent_result[0] == "none":
                        unused.append(tile)

    joker_tile = "joker"

    while True:
        if len(unused) > 0:
            discard_tile = random.choice(unused)
        elif len(pairs) > 0:
            discard_pair = random.choice(pairs)
            discard_tile = random.choice(discard_pair)
        else:
            discard_tile = random.choice(player_hand)

        if discard_tile != joker_tile:
            break

    player_hand.remove(discard_tile)
    discards.append(discard_tile)


def check_num_in_row(check_tile, player_hand):
    if check_tile not in nums:
        return ["none", None]

    tile_letter = check_tile[0:2]  # Extract the letter part
    tile_num = int(check_tile[-1])  # Extract the number part
    num_joker = player_hand.count("joker")

    # Generate potential tiles for sequences
    check_a = tile_letter + str(tile_num - 2)
    check_b = tile_letter + str(tile_num - 1)
    check_c = tile_letter + str(tile_num + 1)
    check_d = tile_letter + str(tile_num + 2)

    # Store potential matches
    results = []

    # Check sequences without jokers
    if check_a in player_hand and check_b in player_hand:
        results.append([check_a, check_b, check_tile])
    if check_b in player_hand and check_c in player_hand:
        results.append([check_b, check_tile, check_c])
    if check_c in player_hand and check_d in player_hand:
        results.append([check_tile, check_c, check_d])

    # Check sequences with jokers
    if num_joker > 0:
        for candidate in [[check_a, check_tile, "joker"], [check_b, check_tile, "joker"],
                          [check_tile, check_c, "joker"], [check_d, check_tile, "joker"]]:
            if all(tile in player_hand or tile == "joker" for tile in candidate):
                results.append(candidate)

    # Return results
    if results:
        return ["pong", results]
    return ["none", None]


def check_match_tiles(check_tile, player_hand):
    num_joker = player_hand.count("joker")
    matching_tiles = [tile for tile in player_hand if tile == check_tile]

    results = []

    if len(matching_tiles) == 2:  # 2 in hand + 1 discarded = Pong
        results.append(["pong", [matching_tiles + [check_tile]]])

    if len(matching_tiles) == 3:  # 3 in hand + 1 discarded = Kong
        results.append(["kong", [matching_tiles + [check_tile]]])

    if len(matching_tiles) == 1 and num_joker > 0:
        results.append(["pong", [matching_tiles + [check_tile] + ["joker"]]])

    if len(matching_tiles) == 0 and num_joker > 1:
        results.append(["pong", [matching_tiles + [check_tile] + ["joker", "joker"]]])

    # Return results
    if results:
        return ["pong", results]
    return ["none", None]


def possible_move(discard_tile, player_hand):
    candidates = []
    move = "pong"

    num_result = check_num_in_row(discard_tile, player_hand)
    match_result = check_match_tiles(discard_tile, player_hand)

    # Check if both results are invalid
    if not num_result or num_result[0] == "none":
        if not match_result or match_result[0] == "none":
            return ["none", []]  # Return "none" with an empty list if no valid moves

    # Process valid num_result
    if num_result and num_result[0] != "none":
        _, num_moves = num_result
        if num_moves:  # Only add if num_moves is valid
            candidates.extend(num_moves)
        if len(num_moves) == 4:
            move = "kong"

    # Process valid match_result
    if match_result and match_result[0] != "none":
        _, match_moves = match_result
        if match_moves:  # Only add if match_moves is valid
            candidates.extend(match_moves)
        if len(match_moves) == 4:
            move = "kong"

    return [move, candidates]


def check_win(tiles):
    jokers = tiles.count("joker")
    triples = []
    pair = []

    used = []

    for t_tile in tiles:
        # Check if the hand cannot win
        if len(pair) > 1:
            return False

        # Skip already used tiles
        if t_tile in used:
            continue

        # Handle picture tiles (winds, dragons)
        if t_tile not in nums:
            count = tiles.count(t_tile)

            if count == 1:  # Single tile, invalid
                return False
            elif count == 3:  # Triplet
                triples.append([t_tile, t_tile, t_tile])
                used.extend([t_tile] * 3)
            elif count == 2:  # Pair
                if len(pair) == 0:
                    pair.append([t_tile, t_tile])
                    used.extend([t_tile] * 2)
                elif jokers > 0:  # Use a joker for triplet
                    triples.append([t_tile, t_tile, "joker"])
                    used.extend([t_tile] * 2 + ["joker"])
                    jokers -= 1
                else:
                    return False

        # Handle number tiles
        else:
            count = tiles.count(t_tile)

            if count == 2:  # Pair
                if len(pair) == 0:
                    pair.append([t_tile, t_tile])
                    used.extend([t_tile] * 2)
                else:
                    return False
            elif count == 3:  # Triplet
                triples.append([t_tile, t_tile, t_tile])
                used.extend([t_tile] * 3)
            else:
                # Check for sequences
                num_result = check_num_in_row(t_tile, tiles)

                if num_result[0] == "none":
                    return False
                else:
                    sequence = num_result[1][0]
                    triples.append(sequence)
                    used.extend(sequence)

    # Ensure all tiles are used
    if sorted(used) != sorted(tiles):
        return False

    # Validate structure (4 triples and 1 pair)
    if len(triples) != 4 or len(pair) != 1:
        return False

    return True
