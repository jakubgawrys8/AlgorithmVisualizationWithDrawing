import globals as gv
import random

def calculate_neighbors(current_node):

    neighbors = []

    # policzyc 8x Neighbour
    process_neighbor(neighbors, gv.Position.TOP_LEFT, current_node)
    process_neighbor(neighbors, gv.Position.TOP, current_node)
    process_neighbor(neighbors, gv.Position.TOP_RIGHT, current_node)
    process_neighbor(neighbors, gv.Position.RIGHT, current_node)
    process_neighbor(neighbors, gv.Position.BOTTOM_RIGHT, current_node)
    process_neighbor(neighbors, gv.Position.BOTTOM, current_node)
    process_neighbor(neighbors, gv.Position.BOTTOM_LEFT, current_node)
    process_neighbor(neighbors, gv.Position.LEFT, current_node)

    return neighbors


def process_neighbor(neighbors, position, current_node):

    x,y = 0,0

    match position:
        case gv.Position.TOP_LEFT:
            x = current_node.x - 1
            y = current_node.y - 1
        case gv.Position.TOP:
            x = current_node.x
            y = current_node.y - 1
        case gv.Position.TOP_RIGHT:
            x = current_node.x + 1
            y = current_node.y - 1
        case gv.Position.RIGHT:
            x = current_node.x + 1
            y = current_node.y
        case gv.Position.BOTTOM_RIGHT:
            x = current_node.x + 1
            y = current_node.y + 1
        case gv.Position.BOTTOM:
            x = current_node.x
            y = current_node.y + 1
        case gv.Position.BOTTOM_LEFT:
            x = current_node.x - 1
            y = current_node.y + 1
        case gv.Position.LEFT:
            x = current_node.x - 1
            y = current_node.y

    neighbor_node = gv.Node(x, y)
    neighbors.append(neighbor_node)



def calculate_neighbor_distances(q, neighbor, ending_node):

    distances_updated = False

    for o_n in gv.openList:
        if(o_n.equals(neighbor)):
            neighbor.g = o_n.g
            neighbor.h = o_n.h
            neighbor.f = o_n.f
            break

    gx = abs(neighbor.x - q.x)
    gy = abs(neighbor.y - q.y)
    g = 10 * (gx + gy) + (14 - 2 * 10) * min(gx, gy)

    g = g + q.g

    hx = abs(neighbor.x - ending_node.x)
    hy = abs(neighbor.y - ending_node.y)
    h = 10 * (hx + hy) + (14 - 2 * 10) * min(hx, hy)

    if(g == 1):
        neighbor.g = g
        neighbor.h = h
        neighbor.f = g + h
        distances_updated = False
    else:
        if(g < neighbor.g):
            neighbor.g = g
            neighbor.h = h
            neighbor.f = g + h
            distances_updated = True
        else:
            neighbor.g = g
            neighbor.h = h
            neighbor.f = g + h
            distances_updated = False

    return distances_updated


def find_open_node_with_least_distance():

    q = gv.openList[0]

    nodes_with_less_f = []

    for o_n in gv.openList:
        if(o_n.f <= q.f):
            q = o_n
            nodes_with_less_f.append(o_n)

    for o_n in nodes_with_less_f:
        if(o_n.h < q.h):
            q = o_n

    return q


def check_if_neighbor_exists(neighbor):
    if(gv.neighborsList):
        for s in gv.neighborsList:
            if(neighbor.equals(s)):
                return True
            else:
                return False
    else:
        return False


def process_open_list(ending_node):

    if(gv.openList):

        q = find_open_node_with_least_distance()

        # End
        if(q.equals(ending_node)):
            find_final_path()
            gv.game_end = True
            return

        if(q in gv.openList):
            gv.openList.remove(q)

        gv.closedList.append(q)

        neighbors = calculate_neighbors(q)
        for neighbor in neighbors:
            skip_neighbor = False

            if(neighbor.x < 0 or neighbor.y < 0 or neighbor.x > gv.number_of_x_blocks - 1 or neighbor.y > gv.number_of_y_blocks - 1):
                skip_neighbor = True

            if(gv.terrainList):
                for t_n in gv.terrainList:
                    if(t_n.equals(neighbor)):
                        skip_neighbor = True
                        break

            for c_n in gv.closedList:
                if(c_n.equals(neighbor)):
                    skip_neighbor = True
                    break

            if(skip_neighbor):
                continue   


            distances_updated = calculate_neighbor_distances(q, neighbor, ending_node)
            neighbor_found = False

            o_n_neighbor = None
            for o_n in gv.openList:
                if(o_n.equals(neighbor)):
                    o_n_neighbor = o_n
                    neighbor_found = True
                    break
           
            if(distances_updated and neighbor_found):
                o_n_neighbor.g = neighbor.g
                o_n_neighbor.h = neighbor.h
                o_n_neighbor.f = neighbor.f
                o_n_neighbor.parent = q
                # gv.openList.append(neighbor)
                continue

            if(not neighbor_found):
                neighbor.parent = q
                gv.openList.append(neighbor)


def find_final_path():

    gv.finalList = []

    if(gv.closedList):
        last_node = gv.closedList[-1]

        gv.finalList.insert(0, last_node)
        parent = last_node.parent

        while(parent):
            # node = parent
            gv.finalList.insert(0, parent)
            parent = parent.parent