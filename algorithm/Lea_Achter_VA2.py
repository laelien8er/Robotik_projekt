open_list = []  # tuple with (node, h*(x), g(x))
close_list = []
final_field = [1, 2, 3, 8, 0, 4, 7, 6, 5]
path = []


def estimation(node):
    """get manhattan distance from node to final position, sum of all pos"""
    cur_field = node
    dist = 0
    for num in cur_field:
        cur_pos = cur_field.index(num)
        fin_pos = final_field.index(num)
        row = abs((cur_pos // 3) - (fin_pos // 3))
        col = abs((cur_pos % 3) - (fin_pos % 3))
        dist += (row + col)
    return dist


def find_neighbors(node):
    """find new positions"""
    swap = {-1: 'Left', 1: 'Right', 3: 'Down', -3: 'Up'}
    neighbors = []
    act_field = node[0]
    pos_zero = act_field.index(0)
    for s, d in swap.items():
        if 0 <= pos_zero + s <= 8:
            new_field = act_field.copy()
            new_field[pos_zero + s], new_field[pos_zero] = new_field[pos_zero], new_field[pos_zero + s]
            if new_field not in close_list:
                neighbors.append(new_field)
                path.append((node[0], new_field, d))
    return neighbors


def get_best_node():
    """get node with shortest f(x) and remove from open"""
    min_node = open_list[0]
    for t in open_list:
        if t[1] + t[2] < min_node[1] + min_node[2]:
            min_node = t
    open_list.remove(min_node)
    return min_node


def get_path():
    best_path = []
    node_bef = final_field
    while True:
        for p in path:
            if node_bef == start:
                return best_path[::-1]
            if p[1] == node_bef:
                best_path.append(p[2])
                node_bef = p[0]
                break


def a_star(start_node):
    open_list.append(start_node)
    while True:
        best_node = get_best_node()
        if best_node[0] == final_field:
            return get_path()
        for neighbor in find_neighbors(best_node):
            open_list.append((neighbor, estimation(neighbor), best_node[2] + 1))
        close_list.append(best_node[0])
        if len(open_list) == 0:
            break
    return 'no path could be found'


inp = input('Geben Sie bitte die Startposition mit Komma getrennt ein:')
start = [int(n) for n in inp.split(',')]
start_pos = (start, 0, 0)
print('Der gefundene Weg ist:', a_star(start_pos))
