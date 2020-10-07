from heapq import heappush, heappop
import quadtreemap

def _get_movements_4n(qtm, tile):
    neighborList = []
    neighborList.append(qtm.quadtree.tileIntersect(quadtreemap.BoundingBox(tile.boundary.x0-1, tile.boundary.y0,
                                                                    tile.boundary.width+2, tile.boundary.height)))
    neighborList.append(qtm.quadtree.tileIntersect(quadtreemap.BoundingBox(tile.boundary.x0, tile.boundary.y0-1,
                                                                    tile.boundary.width, tile.boundary.height+2)))
    movements = [(til, quadtreemap.Point.disOf2Points(tile.getCenter(), til.getCenter())) for til in neighborList]
    return movements

def _get_movements_8n(qtm: quadtreemap.QuadTreeMap , tile: quadtreemap.Tile):
    neighborList = qtm.quadtree.tileIntersect(quadtreemap.BoundingBox(tile.boundary.x0-1, tile.boundary.y0-1,
                                            tile.boundary.width+2, tile.boundary.height+2))
    movements = [(til, quadtreemap.Point.disOf2Points(tile.getCenter(), til.getCenter())) for til in neighborList]
    return movements

def a_star_quadtree(start_m, goal_m, qtm, movement='8N', occupancy_cost_factor=3):
    # get array indices of start and goal
    start = qtm.quadtree.searchTileByIdx(quadtreemap.Point(start_m[0], start_m[1]))
    goal = qtm.quadtree.searchTileByIdx(quadtreemap.Point(goal_m[0], goal_m[1]))
    # check if start and goal nodes correspond to free spaces
    if not start or start.tile_points:
        raise Exception('Start node is not traversable')
    if not goal or goal.tile_points:
        raise Exception('Goal node is not traversable')

    # add start node to front
    # front is a list of (total estimated cost to goal, total cost from start to node, node, previous node)
    start_node_cost = 0
    start_node_estimated_cost_to_goal = quadtreemap.Point.disOf2Points(start.getCenter(), goal.getCenter()) + start_node_cost
    front = [(start_node_estimated_cost_to_goal, start_node_cost, start, None)]

    # use a dictionary to remember where we came from in order to reconstruct the path later on
    came_from = {}
    visited = set()

    # while there are elements to investigate in our front.
    while front:
        # get smallest item and remove from front.
        element = heappop(front)

        # if this has been visited already, skip it
        total_cost, cost, pos, previous = element
        if pos in visited:
                continue
        # now it has been visited, mark with cost
        visited.add(pos)

        # set its previous node
        came_from[pos] = previous

        # if the goal has been reached, we are done!
        if pos == goal:
            break

        # get possible movements
        if movement == '4N':
            movements = _get_movements_4n(qtm, pos)
        elif movement == '8N':
            movements = _get_movements_8n(qtm, pos)
        else:
            raise ValueError('Unknown movement')
        # check all neighbors
        for til, deltacost in movements:
            new_pos = til

            # add node to front if it was not visited before and is not an obstacle
            if (not new_pos in visited) and (not new_pos.tile_points):
                # potential_function_cost = gmap.get_data_idx(new_pos)*occupancy_cost_factor
                potential_function_cost = 0
                new_cost = cost + deltacost + potential_function_cost
                # new_total_cost_to_goal = new_cost + dist2d(new_pos, goal) + potential_function_cost
                new_total_cost_to_goal = new_cost + quadtreemap.Point.disOf2Points(new_pos.getCenter(), goal.getCenter()) + potential_function_cost

                heappush(front, (new_total_cost_to_goal, new_cost, new_pos, pos))

    # reconstruct path backwards (only if we reached the goal)
    path = []
    path_idx = []
    if pos == goal:
        while pos:
            path_idx.append(pos)
            # transform array indices to meters
            # pos_m_x, pos_m_y = gmap.get_coordinates_from_index(pos[0], pos[1])
            # path.append((pos_m_x, pos_m_y))
            pos = came_from[pos]

        # reverse so that path is from start to goal.
        path.reverse()
        path_idx.reverse()

    return path, path_idx
