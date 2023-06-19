import numpy as np
import random
import networkx as nx

# We want to create a dungeon floor plan
# N, S, W, E stand for directions, left top is lowest index being north west
# while bottom right is east south with the highest index
# First index stands for north to south
# Second stands for West to East

# We have 5 tile types:
# - N, S, W, E are all Ramp tiles, where the ramp connects to one height higher than
#   their own ground from their opposite direction to their facing direction
# - G stands for ground
# - H - stands for Hole
# - O stands for Obstacle
# - P stands for Powerup
# The second char of each tile represents the height level. Holes can only be on height level 0

# All tiles shall be connected, and tiles are connected if they follow the rules of being just pathable from
# one another, based on height. Ramps are only pathable from their two endpoints, where the facing endpoint is one up


def get_opposite_neighbours(node, mst):
    neighbours = list(mst.neighbors(node))
    if len(neighbours) != 2:
        return False

    node_x, node_y = node[0], node[1]
    n1_x, n1_y = neighbours[0][0], neighbours[0][1]
    n2_x, n2_y = neighbours[1][0], neighbours[1][1]

    # If the neighbours are on the same row (horizontal ramp)
    if n1_x == n2_x:
        return 'EW'
    # If the neighbours are on the same column (vertical ramp)
    elif n1_y == n2_y:
        return 'NS'

    return False


def dfs(node, prev_node, prev_dir, mst, floor_plan, max_height, size, ramp_prob):
    possible_ramp = get_opposite_neighbours(node, mst)

    prev_height = int(floor_plan[prev_node[0], prev_node[1]][1])
    if prev_dir == floor_plan[prev_node[0], prev_node[1]][0] and prev_dir != 'G':
        prev_height = prev_height + 1

    # If this node has exactly two opposite neighbours, there's a chance it becomes a ramp
    if possible_ramp and random.random() < ramp_prob:
        # Check the direction of the ramp
        direction = random.choice(list(possible_ramp))
        if prev_height == max_height:
            ramp_up = False
        elif prev_height == 0:
            ramp_up = True
        else:
            ramp_up = (direction == prev_dir)

        if ramp_up:
            # Ramp goes up, keep same height
            floor_plan[node[0], node[1]] = f'{direction}{str(prev_height)}'
        else:
            # Ramp goes down, lower height
            floor_plan[node[0], node[1]] = f'{direction}{str(prev_height - 1)}'
    else:
        floor_plan[node[0], node[1]] = f'G{str(prev_height)}'

    # Mirror to the other side!
    created_tile = floor_plan[node[0], node[1]]
    mirrored_tile = f'{mirrored_direction(created_tile[0])}{created_tile[1]}'
    floor_plan[node[1], node[0]] = mirrored_tile

    # Convert MST neighbors to a list and shuffle it
    neighbors = list(mst.neighbors(node))
    random.shuffle(neighbors)

    # Iterate over each neighbour exactly once, in random order
    for neighbour in neighbors:
        # Get the direction of the neighbour relative to the current node
        neighbour_dir = 'S' if neighbour[0] > node[0] else 'N' if neighbour[0] < node[0] else \
            'W' if neighbour[1] < node[1] else 'E'
        # If the neighbour hasn't been visited yet, do further processing with dfs
        if floor_plan[neighbour[0], neighbour[1]] == '##':
            dfs(neighbour, node, neighbour_dir, mst, floor_plan, max_height, size, ramp_prob)


def opposite_direction(direction):
    match direction:
        case 'G':
            return 'G'
        case 'N':
            return 'S'
        case 'S':
            return 'N'
        case 'E':
            return 'W'
        case 'W':
            return 'E'


def mirrored_direction(direction):
    match direction:
        case 'G':
            return 'G'
        case 'N':
            return 'W'
        case 'S':
            return 'E'
        case 'E':
            return 'S'
        case 'W':
            return 'N'


def can_move_to(tile1, tile2, direction):
    tile1_height = int(tile1[1])
    tile2_height = int(tile2[1])

    # If both tiles are ground tiles of the same height
    if tile1_height == tile2_height and 'G' in tile1 and 'G' in tile2:
        return True

    # If one of the tiles is a hole, it shouldn't be reached
    if 'H' in tile1 or 'H' in tile2:
        return False

    # Check if one of the tiles is a ground tile:
    ground_tile = None
    ramp_tile = None
    if 'G' in tile1:
        ground_tile = tile1
        ramp_tile = tile2
    elif 'G' in tile2:
        ground_tile = tile2
        ramp_tile = tile1
        direction = opposite_direction(direction)

    # If one of the tiles is a ramp and the other is a ground tile
    if ramp_tile and ground_tile:
        ramp_height = int(ramp_tile[1])
        ground_height = int(ground_tile[1])

        # If the ramp is facing the direction of the move
        if ramp_tile[0] == direction:
            return ground_height == ramp_height

        # If the ramp is facing the opposite direction of the move
        elif ramp_tile[0] == opposite_direction(direction):
            return ground_height == ramp_height + 1

        # the ramp is sideways and unreachable
        else:
            return False

    # If only case left: both tiles are ramps!
    if 'N' in tile1 or 'S' in tile1 or 'W' in tile1 or 'E' in tile1 and 'N' in tile2 or 'S' in tile2 or 'W' in tile2 or 'E' in tile2:
        ramp1_height = int(tile1[1])
        ramp2_height = int(tile2[1])

        # both ramps are in the direction the tiles are from one another
        if tile1[0] == direction or tile2[0] == direction:

            # If both ramps are facing each other
            if tile1[0] == opposite_direction(tile2[0]):
                # They are reachable if their base heights match
                return ramp1_height == ramp2_height

            # If both ramps are facing the same direction
            elif tile1[0] == tile2[0] == direction:
                return ramp1_height == ramp2_height + 1
            elif tile1[0] == tile2[0] == opposite_direction(direction):
                return ramp1_height == ramp2_height - 1

        # only way sideways ramps can be pathable from one to the next is, if they are identical
        elif tile1 == tile2:
            return True

    # If none of the above conditions are met, we can't reach the tile
    return False


def build_adjacency_matrix(floor_plan):
    size = floor_plan.shape[1]
    # Create a list to map non-hole tiles to indices in the adjacency matrix
    tile_to_index = []
    # Create a list to keep track of whether each tile is a hole
    is_hole = np.array([['H' in tile for tile in row] for row in floor_plan])
    for x in range(size):
        for y in range(size):
            if not is_hole[x, y]:
                tile_to_index.append((x, y))

    # Create the adjacency matrix with the appropriate size
    n_tiles = len(tile_to_index)
    adj_matrix = np.zeros((n_tiles, n_tiles), dtype=bool)

    # Create a reverse mapping from tiles to indices
    index_to_tile = {tile: index for index, tile in enumerate(tile_to_index)}

    # For each non-hole tile
    for index, (x, y) in enumerate(tile_to_index):
        # For each neighboring tile
        for direction in ['N', 'S', 'E', 'W']:
            if direction == 'N':
                dx, dy = -1, 0
            elif direction == 'S':
                dx, dy = 1, 0
            elif direction == 'E':
                dx, dy = 0, 1
            else:  # 'W'
                dx, dy = 0, -1
            nx, ny = x + dx, y + dy
            if 0 <= nx < size and 0 <= ny < size and not is_hole[nx, ny]:
                tile1 = floor_plan[x, y]
                tile2 = floor_plan[nx, ny]
                # If tile1 can move to tile2, set the corresponding cell in the adjacency matrix to True
                if can_move_to(tile1, tile2, direction):
                    adj_matrix[index, index_to_tile[(nx, ny)]] = True

    return adj_matrix


def mirror_mst(mst):
    mirrored_mst = nx.Graph()

    for u, v in mst.edges():
        x1, y1 = u
        x2, y2 = v
        mirrored_u = (y1, x1)
        mirrored_v = (y2, x2)
        # Add original edge and its mirrored version
        mirrored_mst.add_edge(u, v, weight=mst[u][v]['weight'])
        mirrored_mst.add_edge(mirrored_u, mirrored_v, weight=mst[u][v]['weight'])

    return mirrored_mst


def initialize_floor_plan(size, max_height, ramp_prob):
    # Create a 2D grid graph
    grid_graph = nx.grid_2d_graph(size, size)
    grid_graph_lowtriang = nx.Graph()

    # Assign weights to the lower-left triangle edges and mirror them to the upper-right triangle
    for u, v in grid_graph.edges():
        if u[0] >= u[1] and v[0] >= v[1]:  # this will consider the lower-left triangle including the diagonal
            grid_graph_lowtriang.add_edge(u, v)
            weight = np.random.uniform(1, 10)
            grid_graph_lowtriang[u][v]['weight'] = weight

    # Compute minimum spanning tree
    mst = nx.minimum_spanning_tree(grid_graph_lowtriang, algorithm='kruskal', weight='weight')
    mst = mirror_mst(mst)

    # Empty floor plan
    floor_plan = np.full((size, size), '##', dtype=object)

    x, y = np.random.randint(size, size=2)
    start_node = (x, y)  # start at a random node
    start_height = np.random.randint(0, max_height + 1)  # random starting height
    floor_plan[start_node[0], start_node[1]] = 'G' + str(start_height)  # initialize starting node
    floor_plan[start_node[1], start_node[0]] = 'G' + str(start_height)  # initialize mirrored node

    dfs(start_node, start_node, 'G', mst, floor_plan, max_height, size, ramp_prob)

    return floor_plan


def add_to_map(floor_plan, num_items, size, item_type):
    items_added = 0
    while items_added < num_items:
        if num_items - items_added == 1:  # Check if this is the last item to add
            x = np.random.randint(size)
            y = x  # Ensure it's on the diagonal
        else:
            x, y = np.random.randint(size, size=2)
        tile = floor_plan[x, y]
        if 'G' in tile:
            height = tile[1]
            floor_plan[x, y] = f'{item_type}{height}'
            if x != y:
                floor_plan[y, x] = f'{item_type}{height}'
                items_added += 1
            items_added += 1


def add_obstacles(floor_plan, num_obstacles, size):
    add_to_map(floor_plan, num_obstacles, size, 'O')


def add_power_ups(floor_plan, num_power_up, size):
    add_to_map(floor_plan, num_power_up, size, 'P')


def add_holes(floor_plan, num_holes, size):
    holes_added = 0
    adj_matrix = build_adjacency_matrix(floor_plan)

    graph = nx.from_numpy_array(adj_matrix)
    assert nx.is_connected(graph), "the graph was never connected to begin with! Get a life!"
    while holes_added < num_holes:
        if num_holes - holes_added == 1:  # Check if this is the last hole to add
            x = np.random.randint(size)
            y = x  # Ensure it's on the diagonal
        else:
            x, y = np.random.randint(size, size=2)
        tile = floor_plan[x, y]
        if 'G' in tile:
            floor_plan[x, y] = 'H0'
            if x != y:
                floor_plan[y, x] = 'H0'
                holes_added += 1  # count mirrored hole
            adj_matrix = build_adjacency_matrix(floor_plan)
            new_graph = nx.from_numpy_array(adj_matrix)
            if nx.is_connected(new_graph):  # if the new graph is still connected
                holes_added += 1
            else:  # if the new graph is not connected, revert the change
                floor_plan[x, y] = tile
                if x != y:
                    floor_plan[y, x] = tile
                    holes_added -= 1  # decrease mirrored hole count


def generate_floor_plan(size, max_height, num_holes, num_obstacles, num_power_up, ramp_prob):
    floor_plan = initialize_floor_plan(size, max_height, ramp_prob)

    add_holes(floor_plan, num_holes, size)
    add_obstacles(floor_plan, num_obstacles, size)
    add_power_ups(floor_plan, num_power_up, size)

    return floor_plan


def print_floor_plan(floor_plan):
    for row in floor_plan:
        for tile in row:
            print(tile, end=' ')
        print()


s = 5
max_h = 3
num_o = 3
num_h = 2
num_p = 1
ramp_p = 0.9

fp = generate_floor_plan(s, max_h, num_h, num_o, num_p, ramp_p)
print_floor_plan(fp)
