import math
import queue

def _get_movements_4n():
    """
    Get all possible 4-connectivity movements.
    :return: list of movements with cost [(dx, dy, movement_cost)]
    """
    return [(1, 0, 1.0),
            (0, 1, 1.0),
            (-1, 0, 1.0),
            (0, -1, 1.0)]

def _get_movements_8n():
    """
    Get all possible 8-connectivity movements. Equivalent to get_movements_in_radius(1).
    :return: list of movements with cost [(dx, dy, movement_cost)]
    """
    s2 = math.sqrt(2)
    return [(1, 0, 1.0),
            (0, 1, 1.0),
            (-1, 0, 1.0),
            (0, -1, 1.0),
            (1, 1, s2),
            (-1, 1, s2),
            (-1, -1, s2),
            (1, -1, s2)]

def dijkstra(start_m, goal_m, gmap, movement='8N', occupancy_cost_factor=3):
    # totalNodes = gmap.dim_cells[0] * gmap.dim_cells[1]
    path_record = {}
    candidates = queue.PriorityQueue()

    # get array indices of start and goal
    start = gmap.get_index_from_coordinates(start_m[0], start_m[1])
    goal = gmap.get_index_from_coordinates(goal_m[0], goal_m[1])

    # check if start and goal nodes correspond to free spaces
    if gmap.is_occupied_idx(start):
        raise Exception('Start node is not traversable')
    if gmap.is_occupied_idx(goal):
        raise Exception('Goal node is not traversable')

    # get possible movements
    if movement == '4N':
        movements = _get_movements_4n()
    elif movement == '8N':
        movements = _get_movements_8n()
    else:
        raise ValueError('Unknown movement')

    candidates.put((0, None, start))   # store (distance, previous-node, current-node)
    while candidates:
        dis, prev_node, curr_node = candidates.get()
        # print(curr_node, "\t", goal)
        if curr_node == goal:
            # print(True)
            path_record[curr_node] = prev_node
            break
        if curr_node in path_record:
            continue
        path_record[curr_node] = prev_node

        # check all neighbors
        for dx, dy, deltacost in movements:
            # determine new position
            new_x = curr_node[0] + dx
            new_y = curr_node[1] + dy
            new_node = (new_x, new_y)

            # check whether new position is inside the map or is an obstacle
            # if not, skip node
            if not gmap.is_inside_idx(new_node) or gmap.is_occupied_idx(new_node):
                continue
            if new_node not in path_record:
                candidates.put((dis+deltacost, curr_node, new_node))
    # reconstruct path backwards (only if we reached the goal)
    path = []
    path_idx = []
    # print(len(path_record))
    # print(path_record)
    if goal in path_record:
        node = goal
        while node:
            path_idx.append(node)
            # transform array indices to meters
            node_m_x, node_m_y = gmap.get_coordinates_from_index(node[0], node[1])
            path.append((node_m_x, node_m_y))
            node = path_record[node]
        # reverse so that path is from start to goal.
        path.reverse()
        path_idx.reverse()

    # print("path_idx len: ", len(path_idx))
    # print("path_idx:\n", path_idx)
    return path, path_idx


